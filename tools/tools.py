import os
import discord

def get_version():
    return "v1.4.6-a"

def get_target(target, id):
    if target is None: target = id
    else:
        try: target = target.id
        except: pass
    return target

def ismain():
    if os.getenv('ISMAIN') == "True":
        return True
    else:
        return False

def hierarchy_check(user, target):
    if target.top_role >= user.top_role:
        return 0
    else:
        return 1
