# Automatic collection assistance

```
Portions of this document may be machine translated.
```

## Introduction

Auto Gathering Assist can automatically get most of the materials in Teyvat world, such as collectables, loot, etc.

Examples: Automatic collection of sweet flowers and glass lilies, automatic brushing of slimes and fools (requires high level of practice).

This function integrates automatic combat assistance, automatic movement assistance, and pickup assistance. Make sure to read the configuration information about them before using them.

Note: For the time being, only some items in the Mond and Liyue area are supported. The scope will be gradually expanded in the future.

## Feature description

- Specify a collector, select the closest collector from the database to the location at startup to collect

- Resource/monster collection possible

- Automatic continuous harvesting

- Automatically go to Statues of The Seven to regain blood when a character dies

## Quick start

Set basic parameters in the GUI or in the settings/auto_collector.json file in the config folder.

Start automatic acquisition from the GUI interface.

## parameter settings

- Recommended to edit in GUI

| key | item |
|--------------|------------------|
| collection_name | The name of the item to be collected |
| collection_type | The type of collected items, divided into `COLLECTION` (general collection items) and `ENEMY` (combat drop items) |
| minimum_times_mask_col_id | When the blacklist is automatically generated, if the number of failed collection attempts exceeds this value, it will be entered into the blacklist and will not be collected again|

## Collect logs

The collection log (collection_log.json) is a log file generated by automatic collection assistance, including:

| key | item |
|--------------|------------------|
| time | collection time |
| id | The id of the type of drop |
| error_code | exit reason |
| picked item | All items picked during this collection |

Error Code Meaning

| err_code | item |
|----|----|
|`IN_PICKUP_COLLECTOR_TIMEOUT`|Pickup timeout|
|`CHARACTER_DIED`|A character died|
|`ALL_CHARACTER_DIED`|All characters died|
|`PICKUP_TIMEOUT_001`|No more items to pick up|
|`PICKUP_TIMEOUT_002`|The item has not been successfully picked up within the specified time|
|`PICKUP_END_001`| Pickup ends normally ~~ (almost impossible~~|

## Collected locations

The collected location (collected.json) holds the id of the collected item.

Auto Gathering Assist automatically ignores these locations. Delete it to recover.

You can select Auto Collector Log -> Generate Collected in the GUI Auto Collector Settings One-click generation will automatically determine whether the material has been refreshed based on the material refresh time.

## Blacklist settings

These collection items can be blocked by adding ids to the list of corresponding items.

If the collection of some ids often fails, you can add them to the blacklist, and they will be automatically skipped in the next collection.

This can be generated with one click in the GUI Auto Collector Settings by selecting Auto Collector Records - Generate Blacklist.