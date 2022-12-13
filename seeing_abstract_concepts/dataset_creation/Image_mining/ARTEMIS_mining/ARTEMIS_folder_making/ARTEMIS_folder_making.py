import csv
import os
import cv2
import shutil
import json


### ________________________________________________________________
# get_list_of_files(): Function to get a list of all the paths for all images in the wikiart dataset (not just freshness ones)
### ________________________________________________________________def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath) 
    return allFiles

# ________________________________________________________________
### get_data(): get the JSON dict containing the list of pic IDs for each cluster
### ________________________________________________________________
def get_data():
  f = open('input/clusters_stats_n_pics_dict.json')
  data = json.load(f)
  return data


## ________________________________________________________________
### get_cluster_pic_list(): Function to get a list of all the paths for images tagged with a cluster
### ________________________________________________________________
def get_cluster_pic_list(cluster_name):
  data = get_data()
  counter = 0
  freshness_image_list = []
  for cluster, cluster_info in data.items():
    if cluster == cluster_name:
      pic_list = cluster_info['pic_ids']
  if len(pic_list) == 0:
    print("No images tagged with ", cluster_name, " in Artemis")
  else:
    print("There are ", len(pic_list), " images tagged with ", cluster_name, " in Artemis")
  return pic_list


### ________________________________________________________________
### check_cluster_pics(): Function to check that all the cluster pics are in the wikiart dataset
### ________________________________________________________________
def check_cluster_pics(cluster_name):
  cluster_wikiart_list = []
  cluster_missing_wikiart_list = []
  wikiart_imgs_list = getListOfFiles("wikiart-dataset")
  
  cluster_pics_list = get_cluster_pic_list(cluster_name)
  for pic in cluster_pics_list:
    pic = ("wikiart-dataset/" + pic).lower()
    if pic in wikiart_imgs_list:
      # print("Image " + pic + "for cluster " + cluster_name + " IS in wikiart dataset")
      cluster_wikiart_list.append(pic)
      continue
    else:
      # print("Image " + pic + "for cluster " + cluster_name + " IS NOT in wikiart dataset")
      cluster_missing_wikiart_list.append(pic)
  print(len(cluster_wikiart_list), "images PRESENT in wikiart artemis dataset")
  print(len(cluster_missing_wikiart_list),"Images NOT PRESENT in wikiart artemis dataset")
  return cluster_wikiart_list

### ________________________________________________________________
### createFreshnessArtemisDatasetFolder(): copies all images identified with freshness by locating their path 
### and copying them into a folder called freshness-dataset
### ________________________________________________________________
def createFreshnessArtemisDatasetFolder():
  freshness_wikiart_list = checkFreshnessPics()
  for f in freshness_wikiart_list:
    # if f == 'wikiart-dataset/pic_ID':
    #   print('nope')
    # else:
    shutil.copy(f, 'freshness-dataset')
  return

### ________________________________________________________________
### createNonFreshnessArtemisDatasetFolder(): copies all images NOT identified with freshness by locating their path 
### and copying them into a folder called freshness-dataset
### ________________________________________________________________
def createNonFreshnessArtemisDatasetFolder():
  wikiart_imgs_list = getListOfFiles("wikiart-dataset")
  freshness_pics_list = freshnessPicsList()
  for f in ad_imgs_list:
    if f in wikiart_imgs_list:
      continue
    else:
      shutil.copy(f, 'non-freshness-dataset')
  return



# ______________________________________________________FOR FRESH______________________________________________________

### ________________________________________________________________
# freshPicsList(): Function to get a list of all the paths for images tagged with fresh
### ________________________________________________________________
def freshPicsList(data):
  counter = 0
  fresh_image_list = []
  for pic_ID, pic_annotations in data.items():
    for annotation in pic_annotations:
      for item, item_value in annotation.items():
        if item == 'utterance':
          if type(item_value) is str:
            if 'fresh' in item_value.lower():
              if pic_ID not in fresh_image_list:
                counter += 1
                fresh_image_list.append(pic_ID)
  print("The number of pictures with utterances containing fresh are:", counter)
  if (counter == 0):
    print("No images tagged with fresh")
  return fresh_image_list

### ________________________________________________________________
# checkFreshPics(): Function to check that all the fresh pics are in the wikiart artemis dataset
### ________________________________________________________________

def checkFreshPics():
  fresh_wikiart_list = []
  fresh_missing_wikiart_list = []
  wikiart_imgs_list = getListOfFiles("wikiart-dataset")
  fresh_pics_list = freshPicsList(data)
  for fresh_pic in fresh_pics_list:
    fresh_pic = ("wikiart-dataset/" + fresh_pic).lower()
    if fresh_pic in wikiart_imgs_list:
      # print("Image " + freshness_pic + " IS in wikiart dataset")
      fresh_wikiart_list.append(fresh_pic)
      continue
    else:
      # print("Image " + freshness_pic + " IS NOT in wikiart dataset")
      fresh_missing_wikiart_list.append(fresh_pic)
  print(len(fresh_wikiart_list), "images PRESENT in wikiart artemis dataset")
  print(len(fresh_missing_wikiart_list),"Images NOT PRESENT in wikiart artemis dataset")
  return fresh_wikiart_list


### ________________________________________________________________
### createFreshArtemisDatasetFolder(): copies all images identified with fresh by locating their path 
### and copying them into a folder called fresh-dataset
### ________________________________________________________________
def createFreshArtemisDatasetFolder():
  fresh_wikiart_list = checkFreshPics()
  for f in fresh_wikiart_list:
    shutil.copy(f, 'fresh-dataset')
  return



### ________________________________________________________________
### createNonFreshArtemisDatasetFolder(): copies all images NOT identified with fresh by locating their path 
### and copying them into a folder called non-fresh-dataset
### ________________________________________________________________
def createNonFreshArtemisDatasetFolder():
  wikiart_imgs_list = getListOfFiles("wikiart-dataset")
  fresh_pics_list = freshPicsList(data)
  for f in wikiart_imgs_list:
    if f in fresh_pics_list:
      continue
    else:
      shutil.copy(f, 'non-freshness-dataset')
  return



AC_list = ['comfort', 'fun', 'violence', 'love', 'art', 'beauty', 'power', 'adventure', 'happiness', 'protection', 'death', 'safety', 'excitement', 'freedom', 'humor', 'hunger', 'desire', 'danger', 'fitness']

for ac in AC_list:
  check_cluster_pics(ac)


# print(len(freshnessPicsList(data)))
# print(len(getListOfFiles("wikiart-dataset")))
# print(getListOfFiles("wikiart-dataset")[10000])

# checkFreshnessPics()
# createFreshnessArtemisDatasetFolder()

# checkFreshPics()
# createFreshArtemisDatasetFolder()
# createNonFreshArtemisDatasetFolder()

