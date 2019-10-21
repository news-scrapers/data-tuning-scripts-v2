import json
import os

def read_from_dir(path):
    json_files = [pos_json for pos_json in os.listdir(path) if pos_json.endswith('.json')]
    dictionary = []
    for fileNew in json_files:
        with open(path + "/" + fileNew) as json_file:
            data = json.load(json_file)
            del data['sentiment_analysis_obj']
            dictionary = dictionary + [data]
            print("reading json from dir " + data["id"])
    return dictionary


def main():
   

    data = read_from_dir('../data/processed/processed_news_suicide_data/temp')

    with open('../data/processed/processed_news.json', 'w') as fp:
        json.dump(data, fp)

    print('file saved')    

if __name__== "__main__":
  main()