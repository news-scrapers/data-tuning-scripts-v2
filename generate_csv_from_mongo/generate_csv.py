import pandas as pd
import json
from pymongo import MongoClient

# https://stackoverflow.com/questions/16249736/how-to-import-data-from-mongodb-to-pandas
def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)


    return conn[db]


def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id:
        del df['_id']

    return df

def group_data(data):
    data['month'] = data.date.map(lambda x: x.strftime('%Y-%m-01'))
    count = data.groupby(['month'])['month'].agg('count').to_frame('count').reset_index()
    mean = data.groupby(['month']).mean().reset_index()
    mean = mean[["month", "sentiment_analysis_comparative", "sentiment_analysis_score"]]
    result = count.merge(mean, left_on='month', right_on='month',left_index=True, how='left')
    return result

def merge_with_ine(suicide_data):
    suicide_ine = pd.read_csv("../data/processed/processed_ine_data/procesado_suicidio_edad_ambos.csv",sep=";",error_bad_lines=False, encoding="utf-8")
    suicide_ine_clean = suicide_ine[["mes", "descrip", "Todas las edades"]]
    result = suicide_data.merge(suicide_ine_clean, left_on='month', right_on='mes',left_index=True, how='left')
    result = result.rename(index=str, columns={"Todas las edades": "suicidios"})
    result = result.rename(index=str, columns={"count": "noticias_suicidio"})
    result = result.rename(index=str, columns={"sentiment_analysis_comparative": "media_sentimiento_noticias"})
    
    return result

def main():
    query = {}
    host = 'localhost'
    port = 27017
    username = None
    password = None
    no_id = True
    config = {}

    with open('../config.json') as outfile:
        config = json.load(outfile)

    with open('../query.json') as outfile2:
        query = json.load(outfile2)

    data = read_mongo(config["db"], config["collection"], query, host, port, username, password, no_id)
    suicide_data = group_data(data)

    result = merge_with_ine(suicide_data)
    result.to_csv("../data/processed/all.csv", sep=";", index=False)

    print(result)

if __name__== "__main__":
  main()