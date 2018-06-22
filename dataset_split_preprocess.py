
# data segmentation code  # resize  origin code to match classifier model  and split the data set into training  and test set
import sys
import os
import shutil
import csv
import subprocess
import random
import time
import itertools
from PIL import Image

#UCM path
imagesPath = '/home/hpc-126/remote-host/UCM/UCMerced_LandUse'
converted_path ='/home/hpc-126/remote-host/UCM/train-128-20'

#NUPW Path
#imagesPath = '/home/hpc-126/remote-host/NUPW-45/NWPU-RESISC45'
#converted_path ='/home/hpc-126/remote-host/NUPW-45/train224x224'

train_path = ''
test_path =''
imageWidth =128
imageHeight =128
split_ratio =0.20 # ratio of train and test set size
datatype ='UCM'
labels = ''
if datatype == 'UCM':
    labels = {
      'golfcourse': 9,
      'overpass': 14,
      'freeway': 8,
      'denseresidential': 6,
      'mediumresidential': 12,
      'harbor': 10,
      'tenniscourt': 20,
      'mobilehomepark': 13,
      'parkinglot': 15,
      'agricultural': 0,
      'chaparral': 5,
      'airplane': 1,
      'river': 16,
      'baseballdiamond': 2,
      'intersection': 11,
      'beach': 3,
      'runway': 17,
      'forest': 7,
      'sparseresidential': 18,
      'buildings': 4,
      'storagetanks': 19
    }
elif datatype =='NUPW':
    labels = {
        'airplane': 0,
        'airport' : 1,
        'baseball_diamond': 2,
        'basketball_court': 3,
        'beach':4,
        'bridge':5,
        'chaparral':6,
        'church':7,
        'circular_farmland':8,
        'cloud':9,
        'commercial_area':10,
        'dense_residential':11,
        'desert':12,
        'forest':13,
        'freeway':14,
        'golf_course':15,
        'ground_track_field':16,
        'harbor':17,
        'industrial_area':18,
        'intersection':19,
        'island':20,
        'lake':21,
        'meadow':22,
        'medium_residential':23,
        'mobile_home_park':24,
        'mountain':25,
        'overpass':26,
        'palace':27,
        'parking_lot':28,
        'railway':29,
        'railway_station':30,
        'rectangular_farmland':31,
        'river':32,
        'roundabout':33,
        'runway':34,
        'sea_ice':35,
        'ship':36,
        'snowberg':37,
        'sparse_residential':38,
        'stadium':39,
        'storage_tank':40,
        'tennis_court':41,
        'terrace':42,
        'thermal_power_station':43,
        'wetland':44
}
else :
    print ('please specify the data type : UCM   NUPW')



def remove_dir(path):
    try:
      shutil.rmtree(path)
    except OSError, e:
      if e.errno == 2:
        pass
      else:
        raise


def convert_images(path):
  images = []
  train_path = os.path.join(converted_path, 'train')
  test_path = os.path.join(converted_path, 'test')
  os.mkdir(train_path)
  os.mkdir(test_path)
  for root, dirs, files in os.walk(path):
    if root == path:
      continue
    category = os.path.basename(root)
    label = labels[category]
    UCMjpgpath_train =(os.path.join(train_path, str(label)))
    UCMjpgpath_test = (os.path.join(test_path, str(label)))
    os.mkdir(UCMjpgpath_train)
    os.mkdir(UCMjpgpath_test)
    random.shuffle(files)
    count =0
    for name in files:
        im = Image.open(os.path.join(root, name))
        (width, height) = im.size
        if width != imageWidth or height != imageHeight:
            im = im.resize((imageWidth, imageHeight), Image.ANTIALIAS)
        if  name.find('.tif') ==-1:
            jpeg_name=name
        else:
            jpeg_name = name.replace(".tif", ".jpg")
        if count < int(len(files)*split_ratio):
            im.save(os.path.join(UCMjpgpath_train, jpeg_name))
        else:
            im.save(os.path.join(UCMjpgpath_test, jpeg_name))
        count+=1
  return images

def main (argv):
    if os.path.exists(converted_path):
        remove_dir(converted_path)
    os.mkdir(converted_path)
    convert_images(imagesPath)

if __name__== "__main__":
    main(sys.argv)
