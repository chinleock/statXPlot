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