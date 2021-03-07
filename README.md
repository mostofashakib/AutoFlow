# AutoFlow

Autoflow is a personal assistant that allows you to automate your workflow easily through voice commands. 

# How it works.

1. User input is recorded as voice, and through text to speech is converted into a text query.
2. The text queries are passed through our syntax analyzer which breaks down constituent components.
3. Each component is then passed through our intent parser. This is trained using ntlkt's POS tagging to identify the noun,verb etc.. of each component. 
4. After classifying the target API then add this parsed component into a language constructor which builds a specification that can be sent to the dispatcher.
5. The dispatcher parses the specification and recursively calling relevent APIs, QueryParsers and other endpoints.

# Build 

**note that the API and the web server are intended to be dockerized**


### Run the website + NLP backend.

`cd website` 
`npm install`
`node app.js`

Which should start up your server on localhost:3030

### Run the API/Dispatcher

To run the API service, place a `.env` file in the root folder with the relevant API keys. 

Sample configuration.

```
TWILIO_ACCOUNT_SID=YOURSIDHERE
TWILIO_AUTH_TOKEN=YOURAUTHHERE
```

Then start up the API service 
`cd API`

`npm install`

`node index.js`

Which should start up the API service on localhost:3000

# Team Members:
1. Mostofa Adib Shakib
2. Anthony Lowhur
3. Bokang Jia.
4. Aditya Pethe

# Achievements.

Finalist and Winner of HackPrinceton's Title Sponsor
