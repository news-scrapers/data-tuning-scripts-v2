const MongoClient = require('mongodb').MongoClient;
const sentiment = require('multilang-sentiment');

const url = "mongodb://localhost:27017/";
const config = require("../config.json");
const query = require("../query.json");

const saveNew = (newScraped, dbo) => new Promise ((resolve, reject) => {
    var myquery = { "id": newScraped.id };
    var newvalues = { $set: {sentiment_analysis_obj:  
        newScraped.sentiment_analysis_obj,
        sentiment_analysis_score: newScraped.sentiment_analysis_score,
        sentiment_analysis_comparative: newScraped.sentiment_analysis_comparative} };
    dbo.collection(config.collection).updateOne(myquery, newvalues, function(err, res) {
        if (err) reject(err);
        console.log("1 document updated " + newScraped.id);
    resolve();
  });
})

const analyzeNew = (newScraped) => {
    sentimentAnalysis = sentiment(newScraped.content, 'es');
    newScraped.sentiment_analysis_obj = sentimentAnalysis;
    newScraped.sentiment_analysis_score = sentimentAnalysis.score
    newScraped.sentiment_analysis_comparative = sentimentAnalysis.comparative
    console.log("1 document analyzed " + newScraped.id);

    return newScraped;
}

MongoClient.connect(url,  function(err, db) {
  if (err) throw err;
  const dbo = db.db(config.db);
  dbo.collection(config.collection).find(query).toArray(async function(err, result) {
    if (err) throw err;
    console.log(result);
    await result.map( async item => {
        item = analyzeNew(item)
        await saveNew(item, dbo)
    })

    db.close();
  });
});