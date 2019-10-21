
const sentiment = require('multilang-sentiment');
const fs = require('fs');


const path = "../data/raw_results.json";
const pathout = "../data/processed/processed_news_suicide_data/temp/";

const newsResult = require(path);

if (!fs.existsSync(pathout)){
    fs.mkdirSync(pathout);
}

for (const new_item of newsResult){
    //const sentimentAnalysis = sentiment(new_item.content, 'es')
    fs.writeFileSync(pathout+new_item.date +"__"+ new_item.id + ".json", JSON.stringify(new_item));
}




//node --max-old-space-size=4096 separate_files_news.js
