let fs = require('fs');


function parseGroceries()
{
  let groceries = fs.readFileSync("C:/Danh/Projects/HackUCI" + "/output.txt",'utf8');
  let groceriesArray = groceries.split("\n");
  for (let i = 0; i < groceriesArray.length; ++i)
    groceriesArray[i] = groceriesArray[i].trim();

  return groceriesArray;
}


var mysql = require('mysql');

var con = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "Night_thi3f",
  database: "groceryinfo"
});

con.connect(function(err) {
 let groceriesArray =  parseGroceries();
  if (err) throw err;
  var counter = 0;
  for(k = 0; k < groceriesArray.length; k++)
  {
    counter++;
    if(counter === 5)
      counter = 0;
    else
    {
    con.query("INSERT INTO grocerytable VALUES(\"" + groceriesArray[k] + "\",\"" + groceriesArray[k+1] + "\",\"" + groceriesArray[k+2] + "\",\"" + groceriesArray[k+3] + "\")",
      function (err, result, fields) {
         if (err) throw err;
        });
     }
    }
  });
