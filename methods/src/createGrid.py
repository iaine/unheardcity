'''

'''
from glob import glob


image_files = glob("./hhroad_imgs/*")

img_labels = ""
for img in image_files:
    img_labels += "<img class=\"grid\" src=\"{}\" width=\"250\" height=\"300\">\n".format(img)

print(img_labels)
