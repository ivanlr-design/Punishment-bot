Support1 = 928325966600761376
Support2 = 960193798460297246
Support3 = 960193866554822736
Support4 = 1024761069610213496

In_channel_1 = []
In_channel_2 = []
In_channel_3 = []
In_channel_4 = []

current_version = "v1.2.0"

v1patchnote = '''
```
V1.0.0 PATCH
    -Added a new form of security (Authorized users)
    -Added searchfortribeid <tribe id>
    -Added searchfortribename <tribe name>
    -Added .reload (not slash command)
    -Added punishment <Steam IDs> <Names> <Tribe Name> <Tribe ID> <Warning type> <Warnings> <Reason> <Punishment> <Proof>

V1.0.5 PATCH
    -Recoded punishment system
    -Added support for multiple warnings

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

```'''
