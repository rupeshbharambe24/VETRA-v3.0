import ast
import os.path
from xml.dom import minidom


#### ONLY ONE OBJECT PER IMAGE IS ASSUMED ####

out_dir = './udder-bottom-labels/'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

file = minidom.parse(r'D:\Projects\VETRA\Codes\VETRA v3.0\v3.0_Data\udder-bottom-labels.xml')

images = file.getElementsByTagName('image')

for image in images:

    width = int(image.getAttribute('width'))
    height = int(image.getAttribute('height'))
    name = image.getAttribute('name')
    elem = image.getElementsByTagName('points')
    
    # --- FIX STARTS HERE ---
    
    # 1. Get ALL bounding box elements for the current image
    bbox_list = image.getElementsByTagName('box')
    
    # 2. Check if a box exists. If not, skip this image and continue to the next one.
    if not bbox_list:
        print(f"Skipping image {name}: Bounding Box (<box>) not found.")
        continue # Skips the rest of the loop for this image
        
    # 3. If a box exists, proceed with the assumption of only one object
    bbox = bbox_list[0]

    width = int(image.getAttribute('width'))
    height = int(image.getAttribute('height'))
    name = image.getAttribute('name')
    elem = image.getElementsByTagName('points')
    bbox = image.getElementsByTagName('box')[0]
    xtl = int(float(bbox.getAttribute('xtl')))
    ytl = int(float(bbox.getAttribute('ytl')))
    xbr = int(float(bbox.getAttribute('xbr')))
    ybr = int(float(bbox.getAttribute('ybr')))
    w = xbr - xtl
    h = ybr - ytl
    label_file = open(os.path.join(out_dir, name[:-4] + '.txt'), 'w')

    for e in elem:

        label_file.write('0 {} {} {} {} '.format(str((xtl + (w / 2)) / width), str((ytl + (h / 2)) / height),
                                                 str(w / width), str(h / height)))

        points = e.attributes['points']
        points = points.value.split(';')
        points_ = []
        for p in points:
            p = p.split(',')
            p1, p2 = p
            points_.append([int(float(p1)), int(float(p2))])
        for p_, p in enumerate(points_):
            label_file.write('{} {}'.format(p[0] / width, p[1] / height))
            if p_ < len(points_) - 1:
                label_file.write(' ')
            else:
                label_file.write('\n')