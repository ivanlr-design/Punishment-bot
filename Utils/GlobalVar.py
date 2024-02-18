Support1 = 928325966600761376
Support2 = 960193798460297246
Support3 = 960193866554822736
Support4 = 1024761069610213496

In_channel_1 = []
In_channel_2 = []
In_channel_3 = []
In_channel_4 = []

current_version = "v1.3.0"

v1patchnote = '''
```
V1.1.0 PATCH   
    -Added removepunishment <warning_uid> function!
    -Patched some bugs in punishment function
    -Added totalwarnings <Tribe Name> function!

V1.1.5 PATCH
    -Added wipeseasonalwarnings (wipes punishments related to seasonal warnings for wipes) function!
    -Added check <Id> function!

V1.2.0 PATCH
    -Mixed searchfortribename and searchfortribeid -> searchforpunishment <Tribe Name or Tribe id>
    -Added autoRoles in support channels

V1.2.5 PATCH
    -Made all functions none Keysensitive
    -Added earlypunishment (Gives the early punishment made) function
    -Fixed some bugs with totalwarnings

V1.3.0 PATCH
    -Made /tempban function, it will advice you about unban ppl when the time is over
    -Added debugging
    -Fixed some bugs
    -Added /getbans function (a little bit buggy)
```
'''

HelpList = '''```
Help List

/check <Id> (checks if a player is in punishment database)

/patchnotes (gave out the patch notes)

/punishment <Steam IDs> <Names> <Tribe Name> <Tribe ID> <Warning type> <Warnings> <Reason> <Punishment> <Proof> (Log a punishment)

/removepunishment <punishment uid> (delete a punishment from database)

/searchforpunishment <tribe name or tribe id> (Send tribe warnings)

/totalwarnings <tribe name> (Send how many warning does a tribe has)

/wipeseasonalwarnings (Deletes all seasonal warnings, usefull for wipes)

/earlypunishment (send the earlier punishment made)

/getbans (send all the banned users)

/tempban <Names> <IDs> <Tribe Name> <Warning type> <Warnings> <Reason> <Punishment> <Proof> <expire date exemple : 18/02/2024 22:52 
```'''
