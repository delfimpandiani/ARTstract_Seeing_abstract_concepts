#second attempt


# ARTEMIS - Collecting data for which images have uttereances containing specific ACs
# only 19 ACs are searched:
# Outputs: 
# - for each cluster, CSV file with details about each belonging pic 
# - a "small" dict in JSON (clusters_stats_dict.json) containing cluster stats (n of pics and symbol words)
# - a "big" dict in JSON (clusters_stats_n_pics_dict.json) containing cluster stats including a list of pic ids for each cluster
# these data are cleaned by manually removing mismatched words

import json
import csv

def get_input_json():
  f = open('input/LEMMA_artemis_dict.json', encoding='utf-8')
  pic_data = json.load(f)
  return pic_data

def get_clusters_json():
  f = open('input/selected_clustered_symbol_list.json', encoding='utf-8')
  cluster_data = json.load(f)
  return cluster_data

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
      for annotation in value:
        for item, item_value in annotation.items():
          if item == 'utterance':
            print(item_value)
            # if isinstance(item_value, str):
            for cluster_word in cluster_words:
              for lemma in item_value:
                if cluster_word in lemma:
                  if lemma not in matched_words:
                    matched_words.append(lemma)
  # update matched words dict
    matched_words_dict[cluster_name] = {}
    matched_words_dict[cluster_name]["cluster_words"] = cluster_words
    matched_words_dict[cluster_name]['matched_words'] = matched_words

  with open("output/matched_words_dict.json", "w") as outfile:
    json.dump(matched_words_dict, outfile)

  return matched_words_dict

def get_cleaned_matched_words_dict():
  # this dict is manually made by manually cleaning the matched_words_dict created by the last function
  f = open('input/matches_and_mismatches.json', encoding='utf-8')
  clean_match_data = json.load(f)
  return clean_match_data

def get_clusters_stats_n_pics(): # not clean (1st attempt)
  # gather data for images containing tags for each cluster. 
  # Inputs needed: ARTEMIS dict JSON file (new_artemis_dict.json) and selected_clustered_symbol_list.json 
  # Outputs:
  # - for each cluster, CSV file with details about each belonging pic and utterance
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
      for annotation in value:
        for item, item_value in annotation.items():
          if item == 'utterance':
            if isinstance(item_value, str):
              for cluster_word in cluster_words:
                if cluster_word in item_value.lower():
                  if key not in cluster_pic_ids:
                    row = []
                    cluster_pic_ids.append(key)
                    counter = counter + 1
                    row.append(key)
                    row.append(cluster_word)
                    row.append(item_value)
                    rows.append(row)
                  else:
                    print(key, ' has more than one annotation mentioning ', cluster_word)

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
      writer.writerow(['pic_ID', 'symbol_word', 'utterance'])
      writer.writerows(rows)
    
  # output small dict to json
  with open("output/clusters_stats.json", "w") as outfile:
    json.dump(clusters_stats_dict, outfile)

  # output big dict to json
  with open("output/clusters_stats_n_pics_dict.json", "w") as outfile:
    json.dump(clusters_stats_n_pics_dict, outfile)

  # returns the full big dict as object
  return clusters_stats_n_pics_dict

def get_clean_clusters_stats_n_pics(clean_match_data):
  # gather data for images tagged with each cluster. 
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
    mismatches = clean_match_data[cluster_name]['mismatches']
    cluster_words = cluster["symbols"]
    cluster_pic_ids = []
    rows = []

    for key, value in data.items(): #for each picture and its list of annotations
      for annotation in value: #for each annotation (itself a dict) in the list of annotations
        for item, item_value in annotation.items(): # for each key, value pair in the annotation dict
          if item == 'utterance': # item_value is a list of lemmatized strings
            for cluster_word in cluster_words: # for each of the symbols in the cluster
              for lemma in item_value: # for each lemma in the utterance list
                if cluster_word in lemma.lower():# if the symbol is in the one of the lemmas in the utterance
                  if lemma not in mismatches: #make sure that it is not a mismatch
                    if key not in cluster_pic_ids: # make sure that it is not a duplicate
                      row = []
                      cluster_pic_ids.append(key)
                      counter = counter + 1
                      row.append(key)
                      row.append(cluster_word)
                      row.append(item_value)
                      rows.append(row)
                  else: #if it is a mismatch, print it
                    print(lemma, " is a mismatch to ", cluster_word, "so pic ", key, "should not be added to", cluster_name) 
  
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
      writer.writerow(['pic_ID', 'symbol_word', 'utterance_lemmas'])
      writer.writerows(rows)
    
  # output small dict to json
  with open("output/clusters_stats.json", "w") as outfile:
    json.dump(clusters_stats_dict, outfile)

  # output big dict to json
  with open("output/clusters_stats_n_pics_dict.json", "w") as outfile:
    json.dump(clusters_stats_n_pics_dict, outfile)

  # returns the full big dict as object
  return clusters_stats_n_pics_dict

clean_match_data = get_cleaned_matched_words_dict()
get_clean_clusters_stats_n_pics(clean_match_data)

