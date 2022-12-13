#second attempt
# ADVISE - Collecting data for which images have been tagged with specific symbols
# symbols have been clustered into 53 clusters
# Outputs: 
# - for each cluster, CSV file with details about each belonging pic 
# - a "small" dict in JSON (clusters_stats_dict.json) containing cluster stats (n of pics and symbol words)
# - a "big" dict in JSON (clusters_stats_n_pics_dict.json) containing cluster stats including a list of pic ids for each cluster


import json
import csv

def get_input_json():
  f = open('input/data.json', encoding='utf-8')
  pic_data = json.load(f)
  return pic_data

def get_clusters_json():
  f = open('input/selected_clustered_symbol_list.json', encoding='utf-8')
  cluster_data = json.load(f)
  return cluster_data


def get_mismatches():
  f = open('input/mismatches.json', encoding='utf-8')
  mismatches = json.load(f)
  return mismatches

def get_clusters():
  cluster_data = get_clusters_json()
  clusters = cluster_data["data"]
  return clusters

def get_matched_words_dict():
  # gather matched words for each of the symbol words to later use for cleaning
  # Inputs needed: selected_clustered_symbol_list.json and data.json
  data = get_input_json()
  clusters = get_clusters()
  matched_words_dict = {}
  for cluster in clusters:
    cluster_name = cluster["cluster_name"]
    cluster_words = cluster["symbols"]
    matched_words = []
    for key, value in data.items():
      for annotation in data[key]:
        for item in annotation:
          if isinstance(item, str):
            for cluster_word in cluster_words:
              for item in item.lower().replace('/',' ').split():
                if cluster_word in item:
                  if item not in matched_words:
                    matched_words.append(item)

  # update matched words dict
    matched_words_dict[cluster_name] = {}
    matched_words_dict[cluster_name]["cluster_words"] = cluster_words
    matched_words_dict[cluster_name]['matched_words'] = matched_words

  with open("output/matched_words_dict.json", "w") as outfile:
    json.dump(matched_words_dict, outfile)

  return matched_words_dict

def get_clusters_stats_n_pics(): # not clean (1st attempt)
  # gather data for images tagged with each cluster. 
  # Inputs needed: two original ADVISE JSON files: clustered_symbol_list.json and data.json
  # Outputs:
  # - for each cluster, CSV file with details about each belonging pic 
  # - a "small" dict in JSON (clusters_stats_dict.json) containing cluster stats (n of pics and symbol words)
  # - a "big" dict in JSON (clusters_stats_n_pics_dict.json) containing cluster stats including a list of pic ids for each cluster
  # Returns the "big" dict
  data = get_input_json()
  clusters = get_clusters()
  clusters_stats_dict = {}
  clusters_stats_n_pics_dict = {}
  for cluster in clusters:
    counter = 0
    cluster_id = cluster["cluster_id"]
    cluster_name = cluster["cluster_name"]
    cluster_words = cluster["symbols"]
    cluster_pic_ids = []
    rows = []
    for key, value in data.items():
      for annotation in data[key]:
        for item in annotation:
          if isinstance(item, str):
            for cluster_word in cluster_words:
              if cluster_word in item.lower():            
                if key not in cluster_pic_ids:
                  row = []
                  cluster_pic_ids.append(key)
                  counter = counter + 1
                  row.append(key)
                  row.append(cluster_word)
                  row.append(annotation)
                  other_words = []
                  for x in value:
                    other_words.append(x[4])
                  row.append(other_words)
                  rows.append(row)
    
    # print results of the looping for this cluster                  
    print("Total number of pics for cluster " + cluster_name + ': ' + str(counter))
    if (counter == 0):
      print("No images tagged for cluster", cluster_name)

    # update small dict containing cluster stats
    clusters_stats_dict[cluster_name] = {}
    clusters_stats_dict[cluster_name]["count"] = counter
    clusters_stats_dict[cluster_name]["cluster_words"] = cluster_words

    # update big dict containing all cluster stats w/ pic id's
    clusters_stats_n_pics_dict[cluster_name] = {}
    clusters_stats_n_pics_dict[cluster_name]["count"] = counter
    clusters_stats_n_pics_dict[cluster_name]["cluster_words"] = cluster_words
    clusters_stats_n_pics_dict[cluster_name]["pic_ids"] = cluster_pic_ids

    #for each cluster, output CSV file with details about each belonging pic 
    with open('output/individual_clusters/' + cluster_name +'.csv', 'w') as f:
      writer = csv.writer(f)
      writer.writerow(['pic_ID', 'symbol_word', 'symbol_coordinates', 'other_words'])
      writer.writerows(rows)
    
  # output small dict to json
  with open("output/clusters_stats.json", "w") as outfile:
    json.dump(clusters_stats_dict, outfile)

  # output big dict to json
  with open("output/clusters_stats_n_pics_dict.json", "w") as outfile:
    json.dump(clusters_stats_n_pics_dict, outfile)

  # returns the full big dict as object
  return clusters_stats_n_pics_dict



def get_clean_clusters_stats_n_pics(mismatches):
  # gather data for images tagged with each cluster. 
  # Inputs needed: two original ADVISE JSON files: clustered_symbol_list.json and data.json
  # Outputs:
  # - for each cluster, CSV file with details about each belonging pic 
  # - a "small" dict in JSON (clusters_stats_dict.json) containing cluster stats (n of pics and symbol words)
  # - a "big" dict in JSON (clusters_stats_n_pics_dict.json) containing cluster stats including a list of pic ids for each cluster
  # Returns the "big" dict
  data = get_input_json()
  clusters = get_clusters()
  clusters_stats_dict = {}
  clusters_stats_n_pics_dict = {}
  for cluster in clusters:
    counter = 0
    cluster_id = cluster["cluster_id"]
    cluster_name = cluster["cluster_name"]
    cluster_words = cluster["symbols"]
    cluster_pic_ids = []
    rows = []
    for key, value in data.items(): #for each picture and its list of annotations
      for annotation in value: #for each annotation (itself a list of values) in the list of annotations
        for item in annotation: #for each item in the single annotation list
          if isinstance(item, str): #if the item is a string
            item = item.lower().replace('/',' ').split() # turn that item (a string) into a list of strings
            for cluster_word in cluster_words: # for each of the symbols in the cluster
              if cluster_word in item: # if the symbol is in the item list
                if item not in mismatches[cluster_name]: #make sure that it is not a mismatch
                  if key not in cluster_pic_ids: #make sure that it is not a duplicate
                    row = []
                    cluster_pic_ids.append(key)
                    counter = counter + 1
                    row.append(key)
                    row.append(cluster_word)
                    row.append(annotation)
                    other_words = []
                    for x in value:
                      other_words.append(x[4])
                    row.append(other_words)
                    rows.append(row)
                else: #if it is a mismatch, print it
                  print(item, " is a mismatch to ", cluster_word, "so pic ", key, "should not be added to", cluster_name) 
    
    # print results of the looping for this cluster                  
    print("Total number of pics for cluster " + cluster_name + ': ' + str(counter))
    if (counter == 0):
      print("No images tagged for cluster", cluster_name)

    # update small dict containing cluster stats
    clusters_stats_dict[cluster_name] = {}
    clusters_stats_dict[cluster_name]["count"] = counter
    clusters_stats_dict[cluster_name]["cluster_words"] = cluster_words

    # update big dict containing all cluster stats w/ pic id's
    clusters_stats_n_pics_dict[cluster_name] = {}
    clusters_stats_n_pics_dict[cluster_name]["count"] = counter
    clusters_stats_n_pics_dict[cluster_name]["cluster_words"] = cluster_words
    clusters_stats_n_pics_dict[cluster_name]["pic_ids"] = cluster_pic_ids

    #for each cluster, output CSV file with details about each belonging pic 
    with open('output/individual_clusters/' + cluster_name +'.csv', 'w') as f:
      writer = csv.writer(f)
      writer.writerow(['pic_ID', 'symbol_word', 'symbol_coordinates', 'other_words'])
      writer.writerows(rows)
    
  # output small dict to json
  with open("output/clusters_stats.json", "w") as outfile:
    json.dump(clusters_stats_dict, outfile)

  # output big dict to json
  with open("output/clusters_stats_n_pics_dict.json", "w") as outfile:
    json.dump(clusters_stats_n_pics_dict, outfile)

  # returns the full big dict as object
  return clusters_stats_n_pics_dict



mismatches = get_mismatches()
get_clean_clusters_stats_n_pics(mismatches)

