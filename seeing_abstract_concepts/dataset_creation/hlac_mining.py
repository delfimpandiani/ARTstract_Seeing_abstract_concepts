
import json
import csv




# ADVISE mining
def get_input_json():
  f = open('input/data.json')
  data = json.load(f)
  return data

def get_odor_words():
  odor_words = []
  with open('input/stringified_odor_words.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
      odor_words.append(row[0])
  return odor_words

def odor_mining(odor_words, data):
  counter = 0
  odor_pics = []
  rows = []
  for key, value in data.items():
    for annotation in data[key]:
      for item in annotation:
        if type(item) is str:
          for odor_word in odor_words:
            if odor_word in item.lower():
              if (counter == 0):
                print("The following pictures have a symbol for an odor word:")              
              if key not in odor_pics:
                print(key)
                row = []
                odor_pics.append(key)
                counter = counter + 1
                row.append(key)
                row.append(odor_word)
                row.append(annotation)
                other_words = []
                for x in value:
                  other_words.append(x[4])
                row.append(other_words)
                rows.append(row)
  print("Total number of pics:", counter)
  with open('output/odor_pics_and_annotations.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['pic_ID', 'odor_word', 'odor_coordinates', 'other_words'])
    writer.writerows(rows)
  if (counter == 0):
    print("No images tagged with symbol for an odor word")
  return

def fresh_mining(data):
  counter = 0
  freshness_pics = []
  rows =[]
  for key, value in data.items():
    for annotation in data[key]:
      for item in annotation:
        if type(item) is str:
          if "fresh" in item.lower():
            if (counter == 0):
              print("The following pictures have a symbol for 'freshness':")
            if key not in freshness_pics:
              print(key)
              counter = counter + 1
              row = []
              freshness_pics.append(key)
              row.append(key)
              row.append("fresh")
              row.append(annotation)
              other_words = []
              for x in value:
                other_words.append(x[4])
              row.append(other_words)
              rows.append(row)
  print("Total number of pics:", counter)
  with open('output/fresh_pics_and_annotations.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['pic_ID', 'freshness_word', 'freshness_coordinates', 'other_words'])
    writer.writerows(rows)
  if (counter == 0):
    print("No images tagged with symbol for 'freshness'")
  return

def AC_mining(AC_list, data):
  counter = 0
  AC_dict = dict(zip(AC_list, [[]] * len(AC_list)))
  for AC in AC_list:
    rows =[]
    print("The following pictures have a symbol for ", AC, ":")
    for pic_ID, pic_annotations in data.items():
      for annotation in pic_annotations:
        for item in annotation:
          if type(item) is str:
            if AC in item.lower():
              if pic_ID not in AC_dict[AC]:
                print(pic_ID)
                counter = counter + 1
                row = []
                row.append(pic_ID)
                row.append(AC)
                row.append(annotation)
                other_words = []
                for x in pic_annotations:
                  other_words.append(x[4])
                row.append(other_words)
                rows.append(row)
    with open('output/' + AC +'_pics_and_annotations.csv', 'w', encoding='UTF8', newline='') as f:
      writer = csv.writer(f)
      writer.writerow(['pic_ID', 'AC_word', 'AC_coordinates', 'other_words'])
      writer.writerows(rows)
  if (counter == 0):
    print("No images tagged with symbol for", AC)
  return


AC_list = ['freshness', 'pollution', 'smoking', 'sweetness']

data = get_input_json()
odor_words = get_odor_words()

odor_mining(odor_words, data)
fresh_mining(data)
AC_mining(AC_list, data)
