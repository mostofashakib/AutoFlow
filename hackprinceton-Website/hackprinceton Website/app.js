var express        = require("express"),
    app            = express(),
    bodyParser     = require("body-parser"),
    cookieParser   = require("cookie-parser"),
    methodOverride = require("method-override");
    
app.use(bodyParser.urlencoded({extended: true}));
app.set("view engine", "ejs");
app.use(express.static(__dirname + "/public"));
app.use(methodOverride('_method'));
app.use(cookieParser('secret'));

// Restful routing

app.get("/", function(req, res){
    res.render("index");
});

// contact

app.get("/contact", function(req, res){
    res.render("contact");
});


app.get("/result", callName);

function callName(req, res) { 
   var spawn = require("child_process").spawn; 
      
   var process = spawn('python',["C:/Users/Aditya/PycharmProjects/MyProjects/HackPrinceton/hackprinceton Website/hackprinceton Website/app.py", req.query.message] ); 
  
   process.stdout.on('data', function(data) { 
       res.send(data.toString()); 
    } ) 
};

// privacy policy

app.get("/policy", function(req, res){
    res.render("policy");
});

// server Listen 

app.listen(3000, function(){
   console.log("The server has started!");
});
