
var Sentiment = require('sentiment');
var sentiment = new Sentiment();
var result = sentiment.analyze('This is a very sad new');
console.dir(result);

var result = sentiment.analyze('I am very happy to hear this');
console.dir(result);
