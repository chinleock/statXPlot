## For debug, print error

def is_samebins( bins1, bins2 ):
    if bins1 != bins2:
        print('[ERROR] bins size not same')
        return False
    return True

def is_inBins( bin, bins ):
    if bin < 0 or bin > bins:
        print('[ERROR] out of bin range')
        return False
    return True

def is_inEdges( val, edges):
    if not val in edges:
        print('[ERROR] %s not in edges'%str(val) )
        return False
    return True

def is_nameExist( name, names ):
    if name in names:
        print('[ERROR] %s already exist'%name)
        return True
    return False

def is_writeMode( action ):
    if action.lower() != 'w':
        print('[ERROR] read only')
        return False
    return True


     