def get_version():
    v="v1.2.6-a"
    return v 

def get_target(target, id):
    if target is None: target = id
    else:
        try: target = target.id
        except: pass
    return target