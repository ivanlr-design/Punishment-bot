from firebase_admin import db, credentials

def get_authorized_users():
    allowed_users = []
    ids = db.reference("/AuthorizedUsers").get()

    for id in ids:
        name = ids[id]['name']
        if name not in allowed_users:
            allowed_users.append(name)
    
    return allowed_users