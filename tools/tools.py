import os

def get_version():
    return "v1.2.23-a"

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
