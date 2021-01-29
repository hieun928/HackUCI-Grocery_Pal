let http = require('http');
let mysql = require('mysql');
let fs = require('fs');
let qs = require('querystring');
let events = require('events');
let cardLoad = require('./loadData.js');

const itemsPerPage = 319;
//Login Form Promises:
let generateLoginFormPromise = new Promise(function(resolve,reject)
{
  let loginForm = fs.readFileSync(__dirname + "/html/login_form.html",'utf8');
  resolve(loginForm);
});

let handleLogin = new events.EventEmitter();
handleLogin.on('checkLogin',function(res,formData)
{
  let data = qs.parse(formData);
  let con = mysql.createConnection(
    {
      host : "127.0.0.1",
      user : "root",
      password: "Night_thi3f",
      database: "login_info"
    }
  );

  con.connect(function(err){
    if (err) throw err;
  });

  con.query("SELECT * FROM login l1 WHERE l1.username = \"" + data.username + "\"", function(err,result)
{
  let shouldRedirect = true;
  if (result.length !== 0)
  {
    if (result[0].username == data.username && result[0].password == data.password)
      {
        res.writeHead(302,{'Location' : '/mainPage'});
        res.end();
        shouldRedirect = false;
      }
  }
    if (shouldRedirect)
    {
    res.writeHead(302, {
    'Location': '/login'});
    res.end();
    }
  });
});

function createCSSLink(cssFile)
{
  return "<link rel=\"stylesheet\" type=\"text/css\" href=\"" + cssFile + "\"/>";
}

function generateMarketLink(store)
{
  // <li><button>Albertsons</button></li>
  // <li><button>Vons</button></li>
  // <li><button> Pavilion</button></li>
  let result = "";
  for (let i = 0; i < store.length; ++i)
    result += `<li><a href = ${"#"+store[i]+"Link"}>${store[i]}</a></li>`
  return result;
}


function createMainPage(store, start)
{
    let mainPageHtml = `<head>
      <title>MyGroceryPal</title>
    </head>
    ${createCSSLink("homepage.css")}
    <body>

    <div class = "menu">
      <header>
      <ul>
        <li><a href="/selectionMenu">Home</a></li>
        ${generateMarketLink(store)}
      </ul>
    </header>
    <h1>MyGroceryPal</h1>
    </div>`
      for (let i = 0; i < store.length; ++i)
      {
        mainPageHtml += `<h1 id = ${store[i] + "Link"}>` + store[i] + "</h1>";
        mainPageHtml += cardLoad.genCardTags(store[i],start, start + itemsPerPage);
        console.log(store[i]);
      }
      mainPageHtml += "</body>";
      return mainPageHtml;
}


function main(req,res)
{
  res.writeHead(200,{'Content-Type':'text/html'});
  console.log(req.url);
  if (req.url == "/login")
  {
      generateLoginFormPromise.then(function(value)
    {
      let header = "<head>" + createCSSLink("/login.css") + " </head>";
      res.write(header);
      res.write(value);
      res.end();
    });
  }
  else if (req.url == "/login.css")
  {
    res.writeHead(200,{'Content-Type':'text/css'})
    let readStream = fs.createReadStream(__dirname + "/login.css","utf8");
    readStream.pipe(res);

  }
  else if (req.url == "/loggingIn")  {
    let formData = '';
    req.on('data',function(data){formData += data;});
    req.on('end',function(){handleLogin.emit('checkLogin',res,formData)});
  }
  else if (req.url.split("?")[0] == "/mainPage"){
    res.write(createMainPage(req.url.split("?")[1].split("&"), 0));
    res.end();
  }
  else if(req.url == "/homepage.css")
  {
      res.writeHead(200,{'Content-Type':'text/css'});
      let readStream = fs.createReadStream(__dirname + "/homepage.css","utf8");
      readStream.pipe(res);
      readStream.on('close',function(err){res.end()});
  }
  else if(req.url == "/selectionMenu" || req.url == "/selectionMenu?")
  {
    let readStream = fs.createReadStream(__dirname + "/featured.html","utf8");
    readStream.pipe(res);
    readStream.on('close',function(err){res.end();});
  }
  else if(req.url =="/featured.css")
  {
    res.writeHead(200,{'Content-Type': 'text/css'});
    let readStream = fs.createReadStream(__dirname + "/featured.css","utf8");
    readStream.pipe(res);
    readStream.on('close',function(err){res.end();});
  }
  else if (req.url.split("?")[0] == "/selection")
  {
    let storeToShow = req.url.split("?")[1].split("&");
    let redirectPage = "/mainPage?"
    for (let i = 0; i < storeToShow.length - 1; ++i)
      redirectPage += storeToShow[i].split("=")[0] + "&";
    if (storeToShow.length > 0)
      redirectPage += storeToShow[storeToShow.length-1].split("=")[0];
    res.writeHead(302,
      {'Location' : redirectPage})
    res.end();
  }
  else if(req.url == "/welcome")
  {
    let readStream = fs.createReadStream(__dirname + "/welcome.html","utf8");
    readStream.pipe(res);
    readStream.on('close',function(err){res.end();});
  }
  else if(req.url =="/welcome.css")
  {
    res.writeHead(200,{'Content-Type': 'text/css'});
    let readStream = fs.createReadStream(__dirname + "/welcome.css","utf8");
    readStream.pipe(res);
    readStream.on('close',function(err){res.end();});
  }
}

let server = http.createServer(main);

server.listen(8080,'127.0.0.1');
