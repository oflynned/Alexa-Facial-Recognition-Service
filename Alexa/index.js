var alexa = require('alexa-app');


// Allow this module to be reloaded by hotswap when changed
module.change_code = 1;

// Define an alexa-app
var app = new alexa.app('facialrecognition');

var Client = require('node-rest-client').Client;

var client = new Client();

app.launch(function(request,response){
    var prompt = "Hello, what would you like me to do?";
    response.say(prompt).reprompt(prompt).shouldEndSession(false);
});

app.intent('retrieveFaceIntent', {
    "utterances": [
        "Recognise me"
    ]
}, function(request, response) {

    var url = "http://ec2-54-210-185-131.compute-1.amazonaws.com/WebServer/rest/image/name";

    client.get(url, function (data, callback) {
        console.log(data);
		
        var name = data.name;
        var confidence = data.confidence;
        var speechOutput;

        if(name != null) {
            speechOutput = "I'm about " + confidence + " percent sure that your name is " + name + ". Welcome to Accenture.";
        } else {
            speechOutput = "I didn't recognise you unfortunately."
        }

        console.log(speechOutput);
        response.say(speechOutput).shouldEndSession(true);
        response.send();  


    }).on('error', function (err) {
        console.log('something went wrong on the request', err.request.options);
    });

    return false;

});

module.exports = app;


