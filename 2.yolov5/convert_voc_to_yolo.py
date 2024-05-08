import glob
import os
import pickle
import xml.etree.ElementTree as ET
from os import listdir, getcwd
from os.path import join
import tqdm


# 所有类别
classes = ['Ad', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', '10d', 'Jd', 'Qd', 'Kd', 'Ah', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', 'Jh', 'Qh', 'Kh', 'As', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', '10s', 'Js', 'Qs', 'Ks', 'Ac', '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', '10c', 'Jc', 'Qc', 'Kc']

# 获取文件列表
def getImagesInDir(dir_path):
    image_list = []
    for filename in glob.glob(dir_path + '/*.jpg'):
        image_list.append(filename)

    return image_list

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(dir_path, output_path, image_path):
    # dir_path：'########/images/train'
    # output_path '########/labels/train'
    # 文件名
    basename = os.path.basename(image_path)
    basename_no_ext = os.path.splitext(basename)[0]

    in_file = open(dir_path + '/' + basename_no_ext + '.xml')
    out_file = open(output_path + '/' + basename_no_ext + '.txt', 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


# 获取目录
cwd = getcwd()

# 所有要处理的文件夹
dirs = ['train', 'test']
# 遍历目录
for dir_path in dirs:
    # 构建目录 '########/images/train'
    full_dir_path = cwd + '/images/' + dir_path
    # 标注文件存储位置 '########/labels/train'
    output_path = cwd +'/labels/'+dir_path

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    # 获取所有图片（JPG格式）
    image_paths = getImagesInDir(full_dir_path)
    # 用于记录所有文件名
    list_file = open(output_path + '.txt', 'w')

    for image_path in tqdm.tqdm(image_paths,desc='processing'):
        # 写入文件名
        list_file.write(image_path + '\n')
        # 遍历文件，处理
        convert_annotation(full_dir_path, output_path, image_path)

    list_file.close()

    print("Finished processing: " + dir_path)