#
from PIL import Image, ImageDraw

from geoshapes import parse_shapefile, draw_gemeinden, get_zoomfactor
from analyze_data import group_items

SHAPEFILE = 'assets/gem/dvg2gem_nw.shp'
SHAPEFILE_STATE = 'assets/bld/dvg2bld_nw.shp'
IMAGE_WIDTH = 1280 # Only landscape mode is supported
IMAGE_HEIGHT = 720
IMAGE_PADDING = 15
IMAGE_BACKGROUND = (0, 0, 0, 0) # Any RGBA color
TARGET_FILENAME = 'output.png' # Filename for output
XLS_PATH = 'your_data.xlsx'

if __name__ == '__main__': 
    # Create list of gemeinden from shapefile 
    gemeinden = parse_shapefile(SHAPEFILE)

    # Sort gemeinden into groups
    groups = group_items(gemeinden, XLS_PATH)
    
    # Get zoom factor and bbox from state
    factor, bbox = get_zoomfactor(SHAPEFILE_STATE, IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_PADDING)
    
    # Set up image
    im_size = (IMAGE_WIDTH, IMAGE_HEIGHT)
    im = Image.new('RGBA', im_size, color=IMAGE_BACKGROUND)
    
    # Draw map
    im = draw_gemeinden(groups, factor, bbox, im, SHAPEFILE, IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_PADDING)
    
    # Save map image 
    im.save(TARGET_FILENAME) 
    print(f'Output saved to {TARGET_FILENAME}.') 