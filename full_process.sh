cd sentiment-analysis-news-node
npm i
node --max-old-space-size=8096 saveToFile.js
node --max-old-space-size=8096 separate_files_news.js
node --max-old-space-size=8096 analyze_from_directory.js

cd ..
cd generate_csv_from_mongo
pipenv install 
pipenv run python3 join_into_json.py
pipenv run python3 generate_csv_from_dir.py