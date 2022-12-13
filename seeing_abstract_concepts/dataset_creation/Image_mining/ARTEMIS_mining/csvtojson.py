import csv
import json
import nltk
from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()



csvFilePath = 'input/artemis_dataset_release_v0_with_ids.csv'
jsonFilePath = 'input/artemis_dataset.json'
data = {}

# with open(csvFilePath) as csvFile:
#     csvReader = csv.DictReader(csvFile)
#     for rows in csvReader:
#         painting_id = rows['id']
#         # painting_id = str(rows['painting'] + '.jpg').replace('_', '/')
#         data[painting_id] = rows

# with open(jsonFilePath, 'w') as jsonFile:
#     jsonFile.write(json.dumps(data, indent=4))


def get_input_json():
  f = open('input/artemis_dataset.json')
  data = json.load(f)
  return data


def collapse_annotations(data):
    print("old artemis dict had length:", len(data))
    artemis_dict = {}
    for annotation_id, value in data.items():
        painting_ID = value['painting'].replace('_', '/')
        # pic_ID = (value['art_style'] + '/' + value['painting'] + '.jpg').encode('utf-8').strip()
        pic_ID = value['art_style'] + '/' + painting_ID + '.jpg'
        if pic_ID in artemis_dict:
            artemis_dict[pic_ID].append(value)
        elif pic_ID not in artemis_dict:
            artemis_dict[pic_ID] = []
            artemis_dict[pic_ID].append(value)
    for pic_ID, annotations_list in artemis_dict.items():
        for annotation in annotations_list:
            annot_utterance = annotation['utterance']
            lemmatized_utterance = []
            tokenized_utterance = nltk.word_tokenize(annot_utterance)
            for w in tokenized_utterance:
              w = wordnet_lemmatizer.lemmatize(w)
              lemmatized_utterance.append(w)
            annotation['utterance'] = lemmatized_utterance

    with open('input/LEMMA_artemis_dict.json', 'w') as jsonFile:
        jsonFile.write(json.dumps(artemis_dict, indent=4))


data = get_input_json()
collapse_annotations(data)