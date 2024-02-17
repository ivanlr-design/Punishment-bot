from firebase_admin import db, credentials
def GetBans():
    alldata = db.reference("/Punishments")
    BanUids = []
    for uid in alldata:
        if 'ban' in alldata[uid]['Punishment']:
            BanUids.append(uid)
    
    return BanUids
