let  request = require('request');
const { exec } = require('child_process');

var sendMessage = async function(number, message){
    var propertiesObject = { number:number, msgBody:message };
    var newpromise = new Promise(function(resolve, reject) {
        request({url:"https://finnthedawg.api.stdlib.com/http-project@dev/SendTwilio2/", qs:propertiesObject}, function(err,res, body){
            if(err){
                console.log(err);
                reject(err);
            } else {
                resolve(body);
            }
          });
    });
    return(newpromise);
}

var messageUserSlack = async function(username, message){
    var propertiesObject = { username:username, msgBody:message };
    var newpromise = new Promise(function(resolve, reject) {
        request({url:"https://finnthedawg.api.stdlib.com/http-project@dev/MessageUserSlack/", qs:propertiesObject}, function(err,res, body){
            if(err){
                console.log(err);
                reject(err);
            } else {
                resolve(body);
            }
          });
    });
    return(newpromise);
}

var addRowSheets = async function(category, amount){
    var propertiesObject = {amount:amount, category:category };
    var newpromise = new Promise(function(resolve, reject) {
        request({url:"https://finnthedawg.api.stdlib.com/http-project@dev/update-invoice/", qs:propertiesObject}, function(err,res, body){
            if(err){
                console.log(err);
                reject(err);
            } else {
                resolve(body);
            }
          });
    });
    return(newpromise);
} 

//Returns true or false for sentiment positive or negative.
var parseSentiment = async function(text){
    console.log("Sentiment on", text)
    var newPromise = new Promise(function(resolve, reject) {
        exec(`echo ${text} | python ../parserPython/analyze.py`, (err, stdout, stderr) => {
            if (err) {
              // node couldn't execute the command
              reject(err);
            }
            let sentiment = JSON.parse(stdout.replace(/\'/g, "\""));
            console.log(sentiment);
            if (sentiment.neg > sentiment.pos){
                resolve(false);
            } else {
                resolve(true)
            }
          });
    });

    return(newPromise);

}

//Returns true or false for sentiment positive or negative.
var extractValue = function(text){
    text = text.toString()
    text = text.replace(/^\D+/g, '');
    let amount = parseInt(text);
    return(amount*100)
}

module.exports = {
    sendMessage:sendMessage,
    parseSentiment:parseSentiment,
    extractValue:extractValue,
    addRowSheets:addRowSheets,
    messageUserSlack:messageUserSlack,
}