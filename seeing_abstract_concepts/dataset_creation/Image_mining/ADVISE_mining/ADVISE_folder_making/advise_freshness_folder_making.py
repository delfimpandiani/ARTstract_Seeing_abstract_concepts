import csv
import os
# import cv2
import shutil
import json

### ________________________________________________________________
# get_list_of_files(): Function to get a list of all the paths for all images in the wikiart dataset (not just freshness ones)
### ________________________________________________________________
def get_list_of_files(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + get_list_of_files(fullPath)
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

# ________________________________________________________________
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
  cluster_ads_list = []
  cluster_missing_ads_list = []
  ad_imgs_list = get_list_of_files("ads-dataset")
  cluster_pics_list = get_cluster_pic_list(cluster_name)
  for pic in cluster_pics_list:
    pic = "ads-dataset/" + str(pic)
    if pic in ad_imgs_list:
      # print("Image " + pic + "for cluster " + cluster_name + " IS in ads dataset")
      cluster_ads_list.append(pic)
      continue
    else:
      print("Image " + pic + "for cluster " + cluster_name + " IS NOT in ads dataset")
      cluster_missing_ads_list.append(pic)
  print(len(cluster_ads_list), "images PRESENT in ads dataset")
  print(len(cluster_missing_ads_list),"Images NOT PRESENT in ads dataset")
  return cluster_ads_list


### ________________________________________________________________
### create_cluster_pic_folder(): copies all images identified with the cluster_name by locating their path 
### and copying them into a folder called freshness-dataset
### ________________________________________________________________
def create_cluster_pic_folder(cluster_name):
  cluster_pics_list = get_cluster_pic_list(cluster_name)
  cluster_folder_name = str(cluster_name + '_dataset')
  for pic in cluster_pics_list:
    pic_path = "ads-dataset/" + str(pic)
    source = pic_path
    destination = "output/" + cluster_folder_name
    # print(source)
    try:
      shutil.copy(source, destination)
    except:
      print(source, " not found")
  return


# ________________________________________________________________
### (): 
### ________________________________________________________________



### ________________________________________________________________
### get_avg_contrast(): returns the average contrast value of an image
###### the algorithm is based on this: https://stackoverflow.com/questions/57256159/how-extract-contrast-level-of-a-photo-opencv
### ________________________________________________________________
# def get_avg_contrast(image_path):
#     img = cv2.imread(image_path) # read image
#     lab = cv2.cvtColor(img,cv2.COLOR_BGR2LAB) # convert to LAB color space
#     L,A,B=cv2.split(lab) # separate channels
#     kernel = np.ones((5,5),np.uint8) # compute minimum and maximum in 5x5 region using erode and dilate
#     min = cv2.erode(L,kernel,iterations = 1)
#     max = cv2.dilate(L,kernel,iterations = 1)
#     min = min.ae(np.float64) # convert min and max to floats
#     max = max.astype(np.float64) # convert min and max to floats
#     contrast = (max-min)/(max+min) # compute local contrast
#     average_contrast = 100*np.mean(contrast) # get average across whole image
#     print(image_path + " has an average contrast of " + str(average_contrast)+"%")
#     return average_contrast

# def freshnessContrast():
#   freshness_pics_list = freshnessPicsList()
#   for freshness_pic in freshness_pics_list:
#     get_avg_contrast(freshness_pic)
#     return

### ________________________________________________________________
### create_freshness_dataset_folder(): copies all images identified with freshness by locating their path 
### and copying them into a folder called freshness-dataset
### ________________________________________________________________
# def create_freshness_dataset_folder():
#   freshness_pics_list = freshnessPicsList()
#   for f in freshness_pics_list:
#     if f == 'ads-dataset/pic_ID':
#       print('nope')
#     else:
#       shutil.copy(f, 'freshness-dataset')
#   return


### ________________________________________________________________
### create_non_freshness_dataset_folder(): copies all images identified with freshness by locating their path 
### and copying them into a folder called freshness-dataset
### ________________________________________________________________
# def create_non_freshness_dataset_folder():
#   ad_imgs_list = getListOfFiles("ads-dataset")
#   freshness_pics_list = freshnessPicsList()
#   for f in ad_imgs_list:
#     if f in freshness_pics_list:
#       continue
#     else:
#       shutil.copy(f, 'non-freshness-dataset')
#   return

# print(freshnessPicsList()) ['ads-dataset/pic_ID', 'ads-dataset/4/119834.jpg', 'ads-dataset/10/171739.png', 'ads-dataset/10/175935.png', 'ads-dataset/1/150941.jpg', 'ads-dataset/0/98720.jpg', 'ads-dataset/0/98720.jpg' ...
# print(len(freshnessPicsList())) 182
# print(getListOfFiles("ads-dataset")[10])
# checkFreshnessPics()
# print(freshnessContrast())
# create_freshness_dataset_folder()
# create_non_freshness_dataset_folder()




AC_list = ['comfort', 'fun', 'violence', 'love', 'art', 'beauty', 'power', 'adventure', 'happiness', 'protection', 'death', 'safety', 'excitement', 'freedom', 'humor', 'hunger', 'desire', 'danger', 'fitness']

for ac in AC_list:
  # check_cluster_pics(ac)
  create_cluster_pic_folder(ac)
