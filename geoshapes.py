# https://pythonhosted.org/Python%20Shapefile%20Library/
import shapefile
import sys

from PIL import Image, ImageDraw, ImageFont, ImageOps
from shapely.geometry import Polygon

def parse_shapefile(filename):
    """
    Open and parse shapefile filename
    Return objects (list of dicts)
    """
    sf = shapefile.Reader(filename)

    shapeRecs = sf.shapeRecords()

    objects = []
    for entry in shapeRecs:
        object_dict = {
            'name': entry.record[1],
            'key': int(entry.record[2]),
            'shape': Polygon(entry.shape.points),
            'bbox': tuple(entry.shape.bbox),
        }
        # if gemeinde_dict['shape'].bounds == str(entry.shape.bbox):
        #     gemeinden.append(gemeinde_dict)
        objects.append(object_dict)
    return objects

def get_zoomfactor(shapefile, im_width=1280, im_height=780, im_padding=15):
    """
    Extract bbox from shapefile
    Return zoomfactor to fit 
    """
    states = parse_shapefile(shapefile)
    bbox = states[0]['bbox']

    # calculate zoom factor of state bbox to fit in image
    horizontal = bbox[2] - bbox[0]
    vertical = bbox[3] - bbox[1]

    max_width = im_width - 2*im_padding
    max_height = im_height - 2*im_padding

    h_factor = max_width / horizontal
    v_factor = max_height / vertical

    if h_factor > v_factor:
        factor = v_factor
    else:
        factor = h_factor
    
    return factor, bbox

def draw_gemeinden(groups, factor, bbox, im, shapefile, width=1280, height=720, padding=15):
    """
    Generate map based on groups [(colorA, [ids]), (colorB, [ids]), ]
    Return image
    """

    draw = ImageDraw.Draw(im)
    
    gemeinden = parse_shapefile(shapefile)

    color1 = []
    color2 = []

    for item in groups[0][1]:
        color1.append(item)
    
    for item in groups[1][1]:
        color2.append(item)

    print(f'Generate map with highlighted communities: {color1} and {color2}.')

    for gemeinde in gemeinden:
        polygon = gemeinde['shape']
        #print(gemeinde['name'])

        zoomed_poly = []
        for coords in polygon.exterior.coords:
            zoomed2_cords = (coords[0] - bbox[0], coords[1] - bbox[1])
            zoomed2_cords = (round(zoomed2_cords[0] * factor) + padding, round(zoomed2_cords[1] * factor) + padding)
            # zooming will make many points obsolete - only add new points
            if not zoomed2_cords in zoomed_poly:
                zoomed_poly.append(zoomed2_cords)

        if gemeinde['key'] in color1:
            draw.polygon(zoomed_poly, fill=groups[0][0], outline='#ffffff')
        elif gemeinde['key'] in color2:
            draw.polygon(zoomed_poly, fill=groups[1][0], outline='#ffffff')        
        else:
            draw.polygon(zoomed_poly, fill='#aaaaaa', outline='#ffffff')

    im = ImageOps.flip(im)
    
    return im   
