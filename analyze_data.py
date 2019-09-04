# This file contains your code to assign gemeinden to groups and add colors to each group

def group_items(gemeinden, rawdata):
    """
    Sort communities in gemeinden into groups, based on rawdata
    Return gemeinden (List of tuples, consiting of color and keys of all communities in the group)
    """
    
    # define colors (currently only two colrs are supported)
    color1 = '#ff0000'
    color2 = 'blue'
    
    # define groups by key (has to be integer, not str)
    # This is just sample code, no real analysis happening here
    group1 = (
        color1,
        [
        gemeinden[12]['key'], 
        gemeinden[16]['key'], 
        gemeinden[2]['key'], 
        gemeinden[18]['key'], 
        gemeinden[51]['key'],
        ]
    )

    group2 = (
        color2,
        [
        gemeinden[5]['key'], 
        gemeinden[6]['key'], 
        gemeinden[19]['key'], 
        gemeinden[38]['key'], 
        gemeinden[31]['key'],
        ]
    )
    
    # combine colors and groups in tuples
    # groups = [(color1, [key1, key2, key3]), (color2, [key4, key5, key6])]
    groups = [group1, group2]
    
    return groups
