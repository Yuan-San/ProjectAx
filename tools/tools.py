import os

def get_version():
    v="v1.2.16-a"
    return v

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
