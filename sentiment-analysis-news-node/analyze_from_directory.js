// tar -cJf resultsSuicideSentiment.tar.xz resultsSuicide
// 7z a -mm=Deflate -mfb=258 -mpass=15 -r foo.zip resultsSuicide
const sentiment = require('multilang-sentiment');
const fs = require('fs');

const content = 'los gatos son tontos';

const path = "../data/processed/processed_news_suicide_data/temp/";

const analyzeNew = (newScraped) => {
    sentimentAnalysis = sentiment(newScraped.content, 'es');
    newScraped.sentiment_analysis_obj = sentimentAnalysis;
    newScraped.sentiment_analysis_score = sentimentAnalysis.score
    newScraped.sentiment_analysis_comparative = sentimentAnalysis.comparative
    console.log("1 document analyzed " + newScraped.id);

    return newScraped;
}


fs.readdir(path, function(err, list) {
    if (err) console.log(err);
    list.forEach(element => {
        let filecontents = require(path + "/" + element);
        if (element.indexOf("sent_")===-1){
            filecontents = analyzeNew(filecontents);
            fs.writeFileSync(path+"/"  + element, JSON.stringify(filecontents));    
            fs.renameSync( path+"/"  + element, path+"/sent_"  + element)
            console.log(element)
        }
        
        
    });

}
)

//node --max-old-space-size=8096 analyze_from_file_old.js



