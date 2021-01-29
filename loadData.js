let fs = require('fs');

function parseFile(location)
{
  let readFile = fs.readFileSync(__dirname + "/" +location,"utf8");
  let groceriesArray = readFile.split("\n");
  for (let i = 0; i < groceriesArray.length-1; ++i)
    groceriesArray[i] = groceriesArray[i].split("\t");
  return groceriesArray;
}

function genCard(cardArray)
{
    let cardHtml = "";
  if (cardArray !== undefined && cardArray[0] !== undefined)
  {
    cardHtml += `<div class = "card">
      <img src = "${cardArray[2]}">
      <div class = "container">
        <div id = "title">
          <h4><b>${cardArray[0]}</b></h4>
        </div>
        <div id = "deal">
          <p>${cardArray[1]}</p>
        </div>
        </div>
      </div>\n`;
    }
    return cardHtml;
}

function genAllCards(gArray, start, end){
  let outer = "<div class = \"items\">\n";
  for(let line = start; line < end; ++line)
    outer += genCard(gArray[line]);
  outer += "</div >";
  return outer;
}

function genCardTags(location,start,end){
    return genAllCards(parseFile(location),start,end);
}

module.exports.genCardTags= genCardTags;
