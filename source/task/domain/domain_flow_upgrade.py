from source.util import *
from source.flow.utils.flow_template import FlowController, FlowTemplate, FlowConnector, EndFlowTemplate
import source.flow.utils.flow_code as FC
from source.combat import combat_controller
from source.common import timer_module
from source.funclib import generic_lib, movement
from source.funclib.err_code_lib import *
from source.manager import posi_manager as PosiM, asset
from source.interaction.interaction_core import itt
from source.api import yolov8_api
from source.flow.utils import flow_state as ST
from source.assets.domain import *
from source.common.timer_module import AdvanceTimer
from source.ui import page as UIPage
from source.ui.ui import ui_control


class DomainFlowConnector(FlowConnector):
    """
    各个类之间的变量中继器。
    """

    def __init__(self):
        super().__init__()
        self.checkup_stop_func = None
        self.combat_loop = combat_controller.CombatController()

        self.lockOnFlag = 0
        self.move_timer = timer_module.Timer()
        self.ahead_timer = timer_module.Timer()
        self.isLiYue = GIAconfig.Domain_IsObscuredDomain
        self.resin_mode = GIAconfig.Domain_Resin
        self.fast_mode = GIAconfig.Domain_FastMove

    def reset(self):
        self.lockOnFlag = 0
        self.move_timer = timer_module.Timer()
        self.ahead_timer = timer_module.Timer()
        self.isLiYue = GIAconfig.Domain_IsObscuredDomain
        self.resin_mode = GIAconfig.Domain_Resin
        self.fast_mode = GIAconfig.Domain_FastMove


class MoveToChallenge(FlowTemplate):
    """
    移动到开始挑战目标点。
    """

    def __init__(self, upper: DomainFlowConnector):
        super().__init__(upper, flow_id=ST.INIT_MOVETO_CHALLENGE, next_flow_id=ST.INIT_CHALLENGE)
        self.upper = upper

    def state_init(self):
        """
        检查并关闭可能的弹窗。
        """
        logger.info(t2t('正在开始挑战秘境'))
        movement.reset_view()
        if itt.get_text_existence(asset.LEY_LINE_DISORDER):
            self._next_rfc()
        if itt.get_img_existence(asset.IconUIInDomain):
            self._next_rfc()

        self.rfc = 1

    def state_before(self):
        """
        关闭弹窗，校准方向。
        Returns:

        """
        while 1:
            if itt.get_img_existence(asset.IconUIInDomain):
                break
            if itt.get_text_existence(asset.LEY_LINE_DISORDER):
                itt.move_and_click([PosiM.posi_domain['CLLD'][0], PosiM.posi_domain['CLLD'][1]], delay=1)
        time.sleep(0.5)
        movement.reset_view()
        time.sleep(2)
        movement.view_to_angle_domain(-90, self.upper.checkup_stop_func)
        self._next_rfc()
        if self.upper.fast_mode:
            itt.key_down('w')

    def state_in(self):
        """
        移动直到到达。
        Returns:

        """
        movement.view_to_angle_domain(-90, self.upper.checkup_stop_func)
        if self.upper.fast_mode:
            pass
        else:
            movement.move(movement.MOVE_AHEAD, 4)

        if generic_lib.f_recognition():
            itt.key_up('w')
            self._next_rfc()


class Challenge(FlowTemplate):
    def __init__(self, upper: DomainFlowConnector):
        super().__init__(upper, flow_id=ST.INIT_CHALLENGE, next_flow_id=ST.INIT_FINGING_TREE)
        self.upper = upper
        self.text_detect_timer = AdvanceTimer(4).start()

    def state_init(self):
        logger.info(t2t('正在开始战斗'))
        self.upper.combat_loop.continue_threading()  # 开始打架
        itt.key_press('f')
        time.sleep(0.1)

        self.upper.while_sleep = 1

        self._next_rfc()

    def state_in(self):
        """
        等打架打完。
        Returns:

        """
        if itt.get_img_existence(IconGeneralChallengeSuccess):
            self.rfc = FC.AFTER
            return
        if self.text_detect_timer.reached_and_reset():
            if itt.get_text_existence(asset.LEAVING_IN):
                self.rfc = FC.AFTER
                return
        self.rfc = FC.IN

    def state_after(self):

        self.upper.while_sleep = 0.1

        logger.info(t2t('正在停止战斗'))
        self.upper.combat_loop.pause_threading()
        # time.sleep(5)
        # logger.info(t2t('等待岩造物消失'))
        # time.sleep(5)
        self._next_rfc()


class FindingTree(FlowTemplate):
    def __init__(self, upper: DomainFlowConnector):
        super().__init__(upper, flow_id=ST.INIT_FINGING_TREE, next_flow_id=ST.INIT_MOVETO_TREE)
        self.direc_fb = True
        self.upper = upper
        self.move_num = 0
        self.keep_w_flag = False

    def get_tree_posi(self):
        """
        使用yolox获得石化古树在屏幕上的坐标
        Returns:

        """
        cap = itt.capture(jpgmode=0)
        # cv2.imshow('123',cap)
        # cv2.waitKey(0)
        results = yolov8_api.predictor.predict(cap)
        # logger.debug(addition_info)
        if results is not None and len(results) > 0:
            for result in results:
                if result.label == 'stone_tree':
                    return yolov8_api.predictor.get_center(result.box)
        return False

    # 校验目标角度并移动
    def check_and_move(self, result):
        x, y = yolov8_api.predictor.get_center(result.box)
        dx = int(x - SCREEN_CENTER_X)
        logger.debug(f"center x:{x}, y:{y} dx: {dx}")
        if abs(dx) <= 200:
            logger.debug(f"dx: {dx} 角度正确，向前移动")
            movement.move(movement.MOVE_AHEAD, 10)
        else:
            logger.debug(f"dx: {dx} 调整角度")
            if dx < 0:
                movement.cview(-5)
            else:
                movement.cview(5)
            movement.move(movement.MOVE_AHEAD, 5)

    def align_to_gate(self):
        logger.debug("准备找门")
        cap = itt.capture(jpgmode=0)
        # cv2.imshow('123',cap)
        # cv2.waitKey(0)
        results = yolov8_api.predictor.predict(cap)
        wall = None
        if len(results) > 0:
            for result in results:
                # 查找入口
                if result.label == 'entry_fire':
                    logger.debug(f"找到了入口火柱")
                    self.check_and_move(result)
                    area = yolov8_api.predictor.get_area(result.box)
                    if area > 82000:
                        logger.debug("面积够大，尝试查找树")
                        limit = 36
                        while not self.align_to_tree() and limit > 0:
                            logger.debug("未找到树，旋转视角")
                            movement.cview(10)
                            limit -= 1
                    if self.align_to_tree():
                        return True
                    self.align_to_gate()
                    return
                elif result.label == 'wall':
                    logger.debug(f'找到了石碑')
                    wall = result
        if wall is not None:
            logger.debug("未找到火炬，但是找到了墙壁石碑，向他移动")
            area = yolov8_api.predictor.get_area(wall.box)
            wall_width = wall.box[2] - wall.box[0]
            logger.debug(f"wall width: {wall_width}")
            logger.debug(f"石碑面积：{area}")
            if area > 100000 and wall_width > 300:
                logger.debug("石碑面积够大，旋转找入口")
                limit = 36
                while not self.find_entry_fire() and limit > 0:
                    logger.debug("未找到入口火炬，旋转视角")
                    movement.cview(10)
                    limit -= 1
                return
            self.check_and_move(wall)
        else:
            logger.debug("未找到入口火炬位置,旋转视角")
            movement.cview(15)
            self.align_to_gate()

    def find_entry_fire(self):
        cap = itt.capture(jpgmode=0)
        results = yolov8_api.predictor.predict(cap)
        for result in results:
            if result.label == 'entry_fire':
                logger.debug("旋转找到了入口火炬")
                return True
        return False

    def align_to_tree(self):
        """
        使视角对准-90°，同时根据当前位置与石化古树的差值设置移动距离。
        Returns: bool：石化古树是否存在。

        """
        logger.debug("准备对准树")
        # movement.view_to_angle_domain(-90, self.upper.checkup_stop_func)
        t_posi = self.get_tree_posi()
        if t_posi:
            movement.view_to_angle_domain(-90, self.upper.checkup_stop_func)
            t_posi = self.get_tree_posi()
            if not t_posi:
                return False
            dx = int(t_posi[0] - SCREEN_CENTER_X)
            logger.debug(f"tree distance centerX: {dx}")
            if dx >= 0:
                movement.move(movement.MOVE_RIGHT, self.move_num)
            else:
                movement.move(movement.MOVE_LEFT, self.move_num)
            if abs(dx) <= 20:
                self.upper.lockOnFlag += 1
                self.move_num = 1
            else:
                self.move_num = 2
            return True
        else:
            self.move_num = 4
            return False

    def state_init(self):
        logger.info(t2t('正在激活石化古树'))
        self.upper.lockOnFlag = 0
        self.keep_w_flag = False
        self._next_rfc()

    def state_in(self):
        logger.debug(f"state in: {self.upper.lockOnFlag}")
        if self.upper.lockOnFlag <= 5:

            is_tree = self.align_to_tree()
            self.upper.ahead_timer.reset()
            direc_lr = True
            self.direc_fb = True
            if not is_tree:
                if self.align_to_gate() is True:
                    logger.debug("找门成功，找到了树")
                    self._next_rfc()
                # movement.view_to_angle_domain(-90, self.upper.checkup_stop_func)
                # if self.upper.isLiYue:  # barrier treatment
                #     movement.jump_in_loop(jump_dt=10)
                #     if self.upper.move_timer.get_diff_time() >= 20:
                #         direc_lr = not direc_lr
                #         self.upper.move_timer.reset()
                #     if direc_lr:
                #         movement.move(movement.MOVE_LEFT, distance=10)
                #     else:
                #         movement.move(movement.MOVE_RIGHT, distance=10)
                #     if self.direc_fb:
                #         movement.move(movement.MOVE_AHEAD, distance=3)
                #     else:
                #         movement.move(movement.MOVE_AHEAD, distance=3)
                #     self.direc_fb = not self.direc_fb
                #
                # else:  # maybe can't look at tree
                #     logger.debug('can not find tree. moving back.')
                #     movement.move(movement.MOVE_BACK, distance=4)
        else:
            self._next_rfc()

        # 处理掉下虚空的情况

        if not ui_control.verify_page(UIPage.page_domain):
            time.sleep(0.2)
            if not ui_control.verify_page(UIPage.page_domain):
                logger.warning(f"Domain move fail")
                self.keep_w_flag = True
                self._next_rfc()


class MoveToTree(FlowTemplate):
    def __init__(self, upper: DomainFlowConnector):
        super().__init__(upper, flow_id=ST.INIT_MOVETO_TREE, next_flow_id=ST.INIT_ATTAIN_REAWARD)
        self.upper = upper

    def state_before(self):
        itt.key_down('w')
        self.upper.while_sleep = 0.1
        self._next_rfc()

    def state_in(self):
        # 跳跃前进
        if self.upper.ahead_timer.get_diff_time() >= 5:
            itt.key_press('spacebar')
            self.upper.ahead_timer.reset()

        movement.view_to_angle_domain(-90, self.upper.checkup_stop_func)
        if generic_lib.f_recognition():
            itt.key_up('w')
            self.upper.while_sleep = 0.2
            self._next_rfc()


class AttainReward(FlowTemplate):
    def __init__(self, upper: DomainFlowConnector):
        super().__init__(upper, flow_id=ST.INIT_ATTAIN_REAWARD, next_flow_id=ST.END_DOMAIN)
        self.upper = upper

    def state_before(self):
        itt.key_press('f')
        time.sleep(0.2)
        if not generic_lib.f_recognition():
            self._next_rfc()

    def state_in(self):
        if str(self.upper.resin_mode) == '40':
            itt.appear_then_click(asset.ButtonGeneralUseCondensedResin)
        elif str(self.upper.resin_mode) == '20':
            itt.appear_then_click(asset.ButtonGeneralUseOriginResin)

        if itt.get_text_existence(asset.domain_obtain):
            self._next_rfc()


class DomainFlowEnd(EndFlowTemplate):
    def __init__(self, upper: FlowConnector):
        super().__init__(upper, flow_id=ST.END_DOMAIN, err_code_id=ERR_PASS)


class DomainFlowController(FlowController):
    def __init__(self):
        super().__init__(flow_connector=DomainFlowConnector(),
                         current_flow_id=ST.INIT_MOVETO_CHALLENGE,
                         flow_name="DomainFlow")
        self.flow_connector = self.flow_connector  # type: DomainFlowConnector

        self._add_sub_threading(self.flow_connector.combat_loop)

        self.append_flow(MoveToChallenge(self.flow_connector))
        self.append_flow(Challenge(self.flow_connector))
        self.append_flow(FindingTree(self.flow_connector))
        self.append_flow(MoveToTree(self.flow_connector))
        self.append_flow(AttainReward(self.flow_connector))
        self.append_flow(DomainFlowEnd(self.flow_connector))

    def reset(self):
        self.flow_connector.reset()
        self.current_flow_id = ST.INIT_MOVETO_CHALLENGE
        self.reset_err_code()


if __name__ == '__main__':
    dfc = DomainFlowController()
    dfc.set_current_flow_id(ST.INIT_FINGING_TREE)
    dfc.start()
