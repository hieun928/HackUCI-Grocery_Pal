var request = require('request');
var cheerio = require('cheerio');

var url = "http://gelsons.mywebgrocer.com/Circular.aspx?c=15204821&n=1&s=413283377&g=455731bd-9b02-4dd0-b7db-18d301025e6b&uc=3230D101";

request(url, function (error, response,  body) {
  if (!error) {
    var $ = cheerio.load(body)

    var title = $('title').text();
    var content = $('body').text();
    var freeArticles = $('.central-featured-lang.lang1 a small').text()

    console.log('URL: ' + url);
    console.log('Title:' + title);
    console.log('Body' + freeArticles)
  }
  else{
    console.log('Error: ' + error);
  }
});
