# Genshin Impact Assistant 原神小助手
**|[Chinese](https://genshinimpactassistant.github.io/GIA-Document/#/)|[English](https://genshinimpactassistant.github.io/GIA-Document/#/en_US/)|**
<div align="center">

A multi-functional auto-assist based on image recognition and keystroke simulation, including auto combat, auto domain and auto claim materials in Teyvat world.  
基于图像识别和模拟按键的多功能原神自动辅助操作,包括自动战斗,自动刷秘境,自动刷大世界材料。  
The aim of GIA is: let the program play Genshin, and you just need to selected characters and raise them.  

[![GitHub Star](https://img.shields.io/github/stars/infstellar/genshin_impact_assistant?style=flat-square)](https://github.com/infstellar/genshin_impact_assistant/stargazers)
[![Release Download](https://img.shields.io/github/downloads/infstellar/genshin_impact_assistant/total?style=flat-square)](https://github.com/infstellar/genshin_impact_assistant/releases/download/v0.3.0/GIA.Launcher.v0.3.0.7z)
[![Release Version](https://img.shields.io/github/v/release/infstellar/genshin_impact_assistant?style=flat-square)](https://github.com/infstellar/genshin_impact_assistant/releases/latest)
[![Python Version](https://img.shields.io/badge/python-v3.7.6-blue?style=flat-square)](https://www.python.org/downloads/release/python-376/)
[![GitHub Repo Languages](https://img.shields.io/github/languages/top/infstellar/genshin_impact_assistant?style=flat-square)](https://github.com/infstellar/genshin_impact_assistant/search?l=Python)
![GitHub Repo size](https://img.shields.io/github/repo-size/infstellar/genshin_impact_assistant?style=flat-square&color=3cb371)
[![contributors](https://img.shields.io/github/contributors/infstellar/genshin_impact_assistant?style=flat-square)](https://github.com/infstellar/genshin_impact_assistant/graphs/contributors)

</div>

# 源码安装备注

- 文档中介绍的 `git submodule init` 之后如果有个别模块初始化失败，可以去仓库的assets下找到对应仓库直接下载源代码，如果使用 `git clone` 下载子目录，需要手动删除子目录下的 `.git` 目录，否则后续安装会复制 `.git` 文件夹导致报错
- 如果使用了conda虚拟环境，执行 `python setup install` 会报错 `win32gui` 相关报错，需要执行一下 `python.exe ${path_to_env}/Scripts/pywin32_postinstall.py -install`
- 如果未使用虚拟环境，需要执行一下 `python.exe Scripts/pywin32_postinstall.py -install`
- 部分逻辑执行有问题可以尝试自己在源代码中添加日志，然后修改对应代码逻辑。
- 需要使用管理员权限启动终端，执行 `python .\genshin_assistant.py` 启动脚本。退出脚本可以使用如下命令直接关闭：`Get-Process -Name "python" | Stop-Process -Force`


# General Introduction 基本介绍
A Genshin automatic operation assistance based on image recognition and simulated keyboard operation. Does not involve not-allowed operation.  
基于图像识别的原神自动操作辅助.使用图片识别与模拟键盘操作,不涉及违规操作.

To those who have not used GitHub: the blue text in the docs is a hyperlink that can be clicked.  
To没用过github的小伙伴: 描述文档中的蓝色文字是链接,可以打开的.

## Complete Documentation 详细信息

**[中文文档](https://genshinimpactassistant.github.io/GIA-Document/#/)** **如果喜欢，点个星星~** ⭐  
**[English Document](https://genshinimpactassistant.github.io/GIA-Document/#/en_US/)** **star~** ⭐  

## Demo Video 演示视频

<https://www.bilibili.com/video/BV1ps4y1T71A> v0.8.3 演示视频.  
<https://www.youtube.com/watch?v=ZieBDx6Go4A> v0.2.0 demo video, may be partially out of date.

## Main features 主要功能

Functions currently available  
目前可以使用的功能
### 1. Auto Combat Assist 战斗辅助
### 2. Auto Domain Assist 自动秘境
### 3. Auto Collect Assist 自动采集(基于Mission)
### 4. Auto Daily Commission Assist 每日委托(仅部分委托)
### 5. Claim Daily Reward 领取日常奖励
### 6. Auto Lay Line Outcrop Assist 自动地脉衍出辅助  
For more details, see **[English Document](https://genshinimpactassistant.github.io/GIA-Document/#/en_US/)**  
更多信息，查阅 **[中文文档](https://genshinimpactassistant.github.io/GIA-Document/#/)**  

## LICENSE 许可证
This project is licensed under the GNU General Public License v3.0.

## Announcement 声明
This software is open source, free of charge and for learning and exchange purposes only. The developer team has the final right to interpret this project. All problems arising from the use of this software are not related to this project and the developer team. If you encounter a merchant using this software to practice on your behalf and charging for it, it may be the cost of equipment and time, etc. The problems and consequences arising from this software have nothing to do with it.

本软件开源、免费，仅供学习交流使用。开发者团队拥有本项目的最终解释权。使用本软件产生的所有问题与本项目与开发者团队无关。若您遇到商家使用本软件进行代练并收费，可能是设备与时间等费用，产生的问题及后果与本软件无关。

## Acknowledgements 鸣谢 

Thanks to all the friends who participated in the development/testing (\*´▽ ')ノノ  
感谢所有参与到开发/测试中的朋友们 (\*´▽｀)ノノ

[![Contributors](https://contributors-img.web.app/image?repo=infstellar/genshin_impact_assistant)](https://github.com/infstellar/genshin_impact_assistant/graphs/contributors)
