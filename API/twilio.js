var http = require('http')
VoiceResponse = require('twilio').twiml.VoiceResponse;


runServer = function() {
    //Twilio listining server
    http
    .createServer((req, res) => {
        // Create TwiML response
        const twiml = new VoiceResponse();

        twiml.say('Hello from your pals at Twilio! Have fun.');

        res.writeHead(200, { 'Content-Type': 'text/xml' });
        res.end(twiml.toString());
    })
    .listen(1337, '127.0.0.1');
    console.log('TwiML server running at http://127.0.0.1:1337/');

}


module.exports = { 
    'runServer' : runServer,
    };