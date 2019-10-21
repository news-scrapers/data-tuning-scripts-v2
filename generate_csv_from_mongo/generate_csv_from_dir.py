import pandas as pd
import json
import os

def read_from_dir(path):
    with open(path) as json_file:
        dictionary = json.load(json_file)
        return pd.DataFrame.from_dict(dictionary)


def group_data(data):
    data['date'] = data['date'].astype('datetime64[ns]')
    data['month'] = data.date.map(lambda x: x.strftime('%Y-%m-01'))
    count = data.groupby(['month'])['month'].agg('count').to_frame('count').reset_index()
    mean = data.groupby(['month']).mean().reset_index()
    mean = mean[["month", "sentiment_analysis_comparative", "sentiment_analysis_score"]]
    result = count.merge(mean, left_on='month', right_on='month',left_index=True, how='left')
    return result

def merge_with_ine(suicide_data, sex):
    suicide_ine = pd.read_csv("../data/processed/processed_ine_data/procesado_suicidio_edad_" + sex + ".csv",sep=";",error_bad_lines=False, encoding="utf-8")
    #suicide_ine_clean = suicide_ine[["mes", "descrip", "Todas las edades"]]
    suicide_ine_clean = suicide_ine
    result = suicide_data.merge(suicide_ine_clean, left_on='month', right_on='mes',left_index=True, how='left')
    result = result.rename(index=str, columns={"Todas las edades": "suicidios"})
    result = result.rename(index=str, columns={"count": "noticias_suicidio"})
    result = result.rename(index=str, columns={"sentiment_analysis_comparative": "media_sentimiento_noticias"})
    for col in result.columns: 
        result = result.rename(index=str, columns={col: col.replace(" ", "_")})
 
    
    return result

def main():
    

    with open('../config.json') as outfile:
        config = json.load(outfile)

    with open('../query.json') as outfile2:
        query = json.load(outfile2)

    data = read_from_dir('../data/processed/processed_news.json')
    print(data)
    suicide_data = group_data(data)

    result_hombres = merge_with_ine(suicide_data, "hombres");
    result_hombres.to_csv("../data/processed/all_hombres.csv", sep=";", index=False)

    result_mujeres = merge_with_ine(suicide_data, "mujeres");
    result_mujeres.to_csv("../data/processed/all_mujeres.csv", sep=";", index=False)

    result_ambos = merge_with_ine(suicide_data, "ambos");
    result_ambos.to_csv("../data/processed/all.csv", sep=";", index=False)

    print(result_ambos)

if __name__== "__main__":
  main()