const MongoClient = require('mongodb').MongoClient;
const sentiment = require('multilang-sentiment');

const url = "mongodb://localhost:27017/";
const config = require("../config.json");
const query = require("../query.json");
const fs = require('fs')

const storeData = (data, path) => {
    try {
      fs.writeFileSync(path, JSON.stringify(data))
    } catch (err) {
      console.error(err)
    }
  }

MongoClient.connect(url,  function(err, db) {
    if (err) throw err;
    const dbo = db.db(config.db);
    dbo.collection(config.collection).find(query).toArray(async function(err, result) {
      storeData(result,"./raw_results.json")
      db.close();
    });
  });