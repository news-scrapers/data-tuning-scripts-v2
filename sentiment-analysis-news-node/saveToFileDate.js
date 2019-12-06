const MongoClient = require('mongodb').MongoClient;
const sentiment = require('multilang-sentiment');

const url = "mongodb://localhost:27017/";
const config = require("../config.json");
let query = require("../query_date.json");
const pathout = "../data/processed/processed_news_suicide_data/temp_by_date/";

const fs = require('fs')

const storeData = (data, path) => {
    try {
      fs.writeFileSync(path, JSON.stringify(data))
    } catch (err) {
      console.error(err)
    }
  }

  const createFile = (filename) => {
    try{
      fs.writeFileSync(filename, '');
    } catch (err) {
      console.log(err)
    }
     
  }

query = {"date":{
  "$gte": new Date("2018-11-01T00:00:00.000Z"),
  "$lt": new Date("2019-12-31T00:00:00.000Z")
}
}

MongoClient.connect(url,  function(err, db) {
    if (err) throw err;
    const dbo = db.db(config.db);
    dbo.collection(config.collection).find(query).toArray(async function(err, results) {
      //createFile("../data/raw_results_date.json")
      //storeData(results,"../data/raw_results_date.json")

      for (const new_item of results){
        //const sentimentAnalysis = sentiment(new_item.content, 'es')
        fs.writeFileSync(pathout+new_item.date.toISOString().substring(0, 10) +"__"+new_item.newspaper + "__" + new_item.id + ".json", JSON.stringify(new_item));
    }

      db.close();
    });
  });