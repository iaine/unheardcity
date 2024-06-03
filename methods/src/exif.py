import subprocess
from glob import glob
import json

image_files = glob("./hhroad_imgs/*")

img_labels = {}
for img in image_files:

    command = "exiftool {}".format(img)
    data = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    img_data = data.stdout.decode('utf-8')
    labels = {}
    for d in img_data.split('\n'):
        _img = d.split(':')
        if len(_img) > 1: labels[_img[0].strip()] = _img[1].strip()
    img_labels[img] = labels

labels = []
for k, v in img_labels.items():
    if 'GPS Position' in img_labels[k]:
        _d = img_labels[k]['GPS Position'].replace('.','').replace(" deg ", '.').replace("' ", '').replace("\" N",'').replace("\" W",'')
        id = _d.split(',')
        labels.append({'lat': float(id[0]), 'lon': float(id[1].strip()), 'pic': k})
print(json.dumps(labels))
     