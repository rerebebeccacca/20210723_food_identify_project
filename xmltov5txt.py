import xml.etree.ElementTree as ET
import os

image_set = 'train'
classes = ['fantuan','danbing','drinks','sliced_bread','teppanyaki_noodle','you_tiao']

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0]+box[1])/2.0 - 1
    y = (box[2]+box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x,y,w,h)

def convert_annotation(image_set, filename):
    in_file = open('%s/Annotations/%s.xml'%(image_set, filename))
    out_file = open('%s/txt/%s.txt'%(image_set, filename), 'w')

    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in classes == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


if __name__=='__main__':
    wd = os.getcwd()
    datasetfiledir = os.path.join(wd, image_set)
    txtfiledir = os.path.join(datasetfiledir, 'txt')
    if not os.path.exists(txtfiledir):
        os.makedirs(txtfiledir)

    JPEGImagesfiledir = os.path.join(datasetfiledir, 'JPEGImages')
    for filename in os.listdir(JPEGImagesfiledir):
        if not filename.startswith('.'):
            convert_annotation(image_set, filename[:-4])