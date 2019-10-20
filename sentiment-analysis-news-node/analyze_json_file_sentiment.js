const fs = require('fs');
const json = require('big-json');
 
const readStream = fs.createReadStream('raw_results.json');
const parseStream = json.createParseStream();

const sentiment = require('multilang-sentiment');


const analyzeNew = (newScraped) => {
    sentimentAnalysis = sentiment(newScraped.content, 'es');
    newScraped.sentiment_analysis_obj = sentimentAnalysis;
    newScraped.sentiment_analysis_score = sentimentAnalysis.score
    newScraped.sentiment_analysis_comparative = sentimentAnalysis.comparative
    console.log("1 document analyzed " + newScraped.id);

    return newScraped;
}

const storeData = (data, path) => {
    try {
      fs.writeFileSync(path, JSON.stringify(data))
    } catch (err) {
      console.error(err)
    }
  }

/*
parseStream.on('data', function(result) {
  let count = 0
    for (let item of result){
        if (!item.sentiment_analysis_obj){
          console.log("processing new " + count);
          item = analyzeNew(item);
          result[count] = item;
          if (count%10 === 0){
            console.log("saving results as file")
            storeData(result, "raw_results.json")
          }
        }
      }
      count = count + 1;
});
 */

 /*
parseStream.on('data', function(pojo) {
  const stringifyStream = json.createStringifyStream({
    body: pojo
  });
  
  stringifyStream.on('data', function(strChunk) {
    console.log(strChunk)
  });
  
});

readStream.pipe(parseStream);

*/
 
const path= 'raw_results.json';
const contents = fs.readFileSync(path, 'utf8');
const result = JSON.parse(contents);
console.log(result[1])

let i = 0;
for (let item of result){
  if (!item.sentiment_analysis_obj){
    console.log("processing new " + i);
    result[i] = analyzeNew(item);
    if (i%1000===0){
      console.log("saving results ");
      storeData(result,path)
    }
  }
  i = i+1;
}
console.log("saving final results ");
storeData(result,path)
//node --max-old-space-size=4096


