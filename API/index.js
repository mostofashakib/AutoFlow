var express = require('express'),
  session = require('express-session'),
  bodyParser = require('body-parser'),
  hbs = require('express-handlebars'),
  api = require('./apiService.js'),
  tasks = require('./jsonParser'),
  fs = require('fs');

var app = express();
var server = require('http').createServer(app)
require('dotenv').config({ path: __dirname + '/../.env' }) //Import the process.env configurations


//Middleware
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.engine('.hbs', hbs({ extname: '.hbs' }));
app.set('view engine', '.hbs');


//Serve static files
app.use(express.static('public'));
app.use(session({ secret: 'HackPrinceton', cookie: { maxAge: 60000 }, resave: false, saveUninitialized: false }));

let taskJson = {}; //Our script
let responseQueue; //Response queue.
let save;



//Processes a single API job.
var processJob = async function (job) {
  let response;

  //If we are using #save# in the body, then retrieve a saved response.
  let body = job.body;
  if(body === "#save#"){
    body = save;
  }

  //Twilio messages
  if (job.api === "twilio") {

    if (job.action === "send") {
      response = await api.sendMessage(job.number, body);
      console.log("Sent a message");
    }

    if (job.action === "recieve") {
      while (responseQueue === undefined) {
        console.log("Waiting for twilio response.");
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
      response = responseQueue;
      responseQueue = undefined;
    }

  }

  //Slack messaging
  if(job.api === "slack"){

    if(job.action === "messageUser"){
      response = await api.messageUserSlack(job.username, body);
      while (responseQueue === undefined) { //We read a message back to stop messageUser
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
      console.log("Messaged", responseQueue, "On slack");
      responseQueue = undefined;
    }

    if(job.action === "recieve"){
      while (responseQueue === undefined) {
        console.log("Waiting for slack response.");
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
      response = responseQueue;
      responseQueue = undefined;
    }

  }

  //Sheets
  if(job.api === "sheets"){
    response = await api.addRowSheets(job.category, body);
    console.log("Added to sheets");
  }

  //API parsing
  if (job.api === "parser"){

      if(job.action === "parseSentiment"){
        response = await api.parseSentiment(JSON.parse(body.message).Body);

        if(response === true){
          job.response = "true"; //Will be used in the next selection
        } else {
          job.response = "false";
        }

      }

      if(job.action === "extractValue"){
        console.log("Extracting values")
        response = api.extractValue(body.message);
      }
  }


  //If we need to save response.
  if (job.save === "true"){
    console.log("saving this response");
    save = response;
  }

  return (response);
}


//Get our task json file.
app.get('/', async function (req, res) {
  let rawdata
  if(req.query.path){
    rawdata = fs.readFileSync(req.query.path);
  } else {
    rawdata = fs.readFileSync('../example_keith.json');
  }
  taskJson = JSON.parse(rawdata);

  let currentJob = tasks.getCurrentTask(taskJson);
  while (currentJob !== undefined) {
    console.log("Processing a job");
    console.log(currentJob);
    let response = await processJob(currentJob);
    console.log("Job response", response);
    if(currentJob.response === "none"){
      currentJob.response = "complete";
    }
    currentJob = tasks.getCurrentTask(taskJson);
  }

  console.log("No more jobs");
  res.render('index', {});
});


app.get('/test', async function(req, res) {
  let ans = api.extractValue(500)
  console.log(ans);
})

app.get('/begin', async function (req, res) {

  let currentJob = tasks.getCurrentTask(taskJson);
  while (currentJob !== undefined) {
    console.log("Processing a job");
    console.log(currentJob);
    let response = await processJob(currentJob);
    console.log("Job response", response);
    if(currentJob.response === "none"){
      currentJob.response = "complete";
    }
    currentJob = tasks.getCurrentTask(taskJson);
  }

  console.log("No more jobs");
  res.render('index', {});

  // let currentJob = tasks.getCurrentTask(taskJson);
  // if(currentJob === undefined){
  //   console.log("No more jobs");
  //   res.render('index', {});
  // } else {
  //   console.log(JSON.stringify(taskJson));
  //   processJob(currentJob);
  // }
  // currentJob.response = "complete";
  // console.log(JSON.stringify(taskJson));
  // res.render('index', {});
});

app.get('/sendMessage', async function (req, res) {
  console.log("Sending message");
  let response = await api.sendMessage(9293314794, 'MessageBody4');
  console.log("Response", response);
  res.render('index', {});
});

app.get('/newMessage', function (req, res) {
  console.log("we recieved a new message");
  let newResponse = {
    "message": req.query.msgBody,
    "time": Date.now()
  };
  responseQueue = newResponse;
  res.status(200);
  res.send();
});

app.get('/newSlackMessage', function (req, res) {
  console.log("we recieved a DM on slack");
  let newResponse = {
    "message": req.query.msgBody,
    "time": Date.now()
  };
  responseQueue = newResponse;
  console.log(JSON.stringify(newResponse));
  res.status(200);
  res.send();
});

server.listen(process.env.PORT || 3000, function () {
  console.log('Listening on port ' + server.address().port);
});
