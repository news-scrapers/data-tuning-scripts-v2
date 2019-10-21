// tar -cJf resultsSuicideSentiment.tar.xz resultsSuicide
// 7z a -mm=Deflate -mfb=258 -mpass=15 -r foo.zip resultsSuicide
const sentiment = require('multilang-sentiment');
const fs = require('fs');

const content = 'los gatos son tontos';

const path = "../data/processed/processed_news_suicide_data/temp/";
const output = "../data/processed/processed_news.json";

let outputJson ="["

const readFile = (path,element, outputJson) => new Promise((resolve, reject) => {
    fs.readFile(path + "/" + element, 'utf8', function(err, data) {
        if (err) reject(err);
        console.log("processed file ")
        resolve(outputJson+"\n" +data + ",")
      });
});

fs.readdir(path, async function(err, list) {
    if (err) console.log(err);
    for (const element of list) {
        outputJson = await readFile(path,element, outputJson)
    };
    outputJson = outputJson+"\n null ]";

    fs.writeFileSync(output, outputJson);    

}
)



//node --max-old-space-size=8096 analyze_from_file_old.js



