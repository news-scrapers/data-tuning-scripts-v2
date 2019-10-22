import pandas as pd
import json
import os
from datetime import date, timedelta, datetime

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
    result = suicide_data.merge(suicide_ine_clean, left_on='month', right_on='mes',left_index=True, how='left').reset_index()
    result = result.rename(index=str, columns={"Todas las edades": "suicidios"})
    result = result.rename(index=str, columns={"count": "noticias_suicidio"})
    result = result.rename(index=str, columns={"sentiment_analysis_comparative": "media_sentimiento_noticias"})
    for col in result.columns: 
        result = result.rename(index=str, columns={col: col.replace(" ", "_")})

    return result

def create_table_moved(suicide_data, n):
    suicide_ine = pd.read_csv("../data/processed/processed_ine_data/procesado_suicidio_edad_ambos.csv",sep=";",error_bad_lines=False, encoding="utf-8")
    suicide_ine_moved = suicide_ine[["mes", "Todas las edades"]]
    suicide_ine_moved['date_minus_'+str(n)+'moths'] = suicide_ine_moved['mes'].apply(lambda x: minus_months(x,n))
    del suicide_ine_moved['mes']
    suicide_ine_moved = suicide_ine_moved.rename(index=str, columns={"Todas las edades": "suicidios_"+ str(n) + "_meses_despues"})
    print(suicide_ine_moved)

    #result = suicide_ine_moved.merge(suicide_data, left_on='date_minus_5moths', right_on='month',left_index=True, how='left').reset_index()
    result = suicide_data.merge(suicide_ine_moved, right_on='date_minus_'+str(n)+'moths', left_on='month', left_index=False)

    return result


def minus_months(x,n):
    date = ((datetime.strptime(x, '%Y-%m-%d') - timedelta(days=n*30))).strftime('%Y-%m-01')
    return date

def main():
    

    with open('../config.json') as outfile:
        config = json.load(outfile)

    with open('../query.json') as outfile2:
        query = json.load(outfile2)

    data = read_from_dir('../data/processed/processed_news.json')

    suicide_data = group_data(data)

    result_hombres = merge_with_ine(suicide_data, "hombres")
    result_hombres.to_csv("../data/processed/all_hombres.csv", sep=";", index=False)

    result_mujeres = merge_with_ine(suicide_data, "mujeres")
    result_mujeres.to_csv("../data/processed/all_mujeres.csv", sep=";", index=False)

    result_ambos = merge_with_ine(suicide_data, "ambos")
    result_ambos.to_csv("../data/processed/all.csv", sep=";", index=False)

    result_table_moved_ambos = create_table_moved(result_ambos, 3)
    result_table_moved_ambos = create_table_moved(result_table_moved_ambos, 4)
    result_table_moved_ambos = create_table_moved(result_table_moved_ambos, 5)


    result_table_moved_ambos.to_csv("../data/processed/all_moved.csv", sep=";", index=False)


if __name__== "__main__":
  main()