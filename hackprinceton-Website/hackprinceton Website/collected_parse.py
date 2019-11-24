import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import RegexpTokenizer

commandDict = {
  "slack": ["message","repli","call","text"],
  "twilio": ["call","text","hang up"],
    "googl": 'BI',
    "sheet": ['creat'],
    "doc": ["creat"],
    "gmail":['creat'],
    "sms":['text']

}
verbAbr = ['VBZ','VB','VBG']
nounAbr = ['NNS','NN','FW']

abbDict = {
    "googl" : "Google"
}
approvedVerbList = ["repli","text","send","messenge"]

bigramDict = {
    "googl":["sheet","doc"]
}

testStr = "he replies on Slack, then save response into Google Sheets and make document on Google Sheets and hosting it on Slack"

tokenizer = RegexpTokenizer(r'\w+')
subjectList = ['boss']

stemmer = SnowballStemmer("english")

'''
tag: else if
condition:
condition_API:
Action:
Action_API:
'''

# Work with action
# Work with Bigram

def checkBigram(word,nextWord):
    # if we encounter Googl
    #print('word: ', word)
    #print('nextWord: ', nextWord)
    resStr = abbDict[word] + ' ' + nextWord
    return resStr


def mapCondAndAPIEntities(condList, condAPIList):
    resDict = {}
    if len(condAPIList) <= 0:
        print('No APIs were detected')
        return None
    
    elif len(condAPIList) == 1:
        # Only one API in condition term
        resDict[condAPIList[0]] = condList
    else:
        # Multiple APIs in condition term
        print(condAPIList)
        
        # Corner cases
        
        for i,api in enumerate(condAPIList):
            if i >= len(condList):
                i = len(condList)-1
            
            resDict[api] = condList[i]
            
    
    return resDict


# This is for getting condition attributes
def getConditionTag(conditionSentList):
    condAPIList = []
    condList = []

    # condition API
    # condition

    # Each API should have their own list of commands

    tokenized_sent = tokenizer.tokenize(conditionSentList)
    #tokenized_sent = [stemmer.stem(w) for w in tokenized_sent]
    partsOfSpeech = nltk.pos_tag(tokenized_sent)

    continueCont = False

    


    #for w in thenList[0].split(' '):
    for i,w in enumerate(tokenized_sent):
        if continueCont:
            continue
        word = stemmer.stem(w)
        if word in commandDict and word not in condAPIList:
            # If we recognize this as an API name
            
            if commandDict[word] == 'BI':
                # This is a bigram
                nextWord = tokenized_sent[i+1]
                combWord = checkBigram(word,nextWord)
                condAPIList.append(combWord)
                continueCont = True
            else:
                condAPIList.append(word)

        verb = partsOfSpeech[i][1]
        if verb in verbAbr:
            # We recognize this as an action
            condList.append(word)
            
        
        if verb in nounAbr and word in approvedVerbList:
            # A verb could be false labeled as a noun
            # So we perform a double check
            condList.append(word)
        

        #print(partsOfSpeech[i])
        #print(word)
        #print('---------------')


    #print(partsOfSpeech)
    #print('--------------------------------------------')
    '''
    print('condition: ', condList)
    print('condition_API: ', condAPIList)

    print('\n\n\n\n\n\n')

    print(testStr)
    '''

    # This is our result
    result = mapCondAndAPIEntities(condList, condAPIList)

    return result


# This is for getting Action attributes

def getActionTag(actionSentList):
    
    actionAPIList = []
    actionList = []

    # condition API
    # condition

    # Each API should have their own list of commands

    tokenized_sent = tokenizer.tokenize(actionSentList)
    #tokenized_sent = [stemmer.stem(w) for w in tokenized_sent]
    partsOfSpeech = nltk.pos_tag(tokenized_sent)
    #print(partsOfSpeech)

    continueCont = False
    #for w in thenList[0].split(' '):
    for i,w in enumerate(tokenized_sent):
        if continueCont:
            continue
        word = stemmer.stem(w)
        if word in commandDict and word not in actionAPIList:
            # If we recognize this as an API name
            # If we recognize this as an API name
            
            if commandDict[word] == 'BI':
                # This is a bigram
                nextWord = tokenized_sent[i+1]
                combWord = checkBigram(word,nextWord)
                actionAPIList.append(combWord)
                continueCont = True
            
            else:
                actionAPIList.append(word)

        verb = partsOfSpeech[i][1]
        if verb in verbAbr:
            # We recognize this as an action
            actionList.append(word)
        #print('verb: ', verb)
        #print(nounAbr)
        
        if verb in nounAbr and word in approvedVerbList:
            # A verb could be false labeled as a noun
            # So we perform a double check
            actionList.append(word)

        #print(partsOfSpeech[i])
        #print(word)
        #print('---------------')


    #print(partsOfSpeech)
    #print('--------------------------------------------')
    '''
    print('action: ', actionList)
    print('action_API: ', actionAPIList)

    print('\n\n\n\n\n\n')

    print(testStr)
    '''

    # This is our result
    result = mapCondAndAPIEntities(actionList, actionAPIList)
    return result

# THIS WILL BE THE MAIN FUNCTION YOU WILL CALL
def getCondAndActionTag(inputStr): 
    print('Input: ',inputStr)
    #print(testStr,'\n\n\n\n')

    # THEN is a key word (for splitting if statements)
    thenList = inputStr.split('then')
    if len(thenList) == 1:
        # We assume this is a 'else' statement
        actionList = []
        for action in thenList[0].split('and'):
            actionTag = getActionTag(action)
            #print('Action Tag: ', actionTag)
            actionList.append(actionTag)
        print(actionList)
        return actionList
    assert len(thenList) == 2
    #print('---------------')
    #print(thenList)
    condTag = getConditionTag(thenList[0])
    #print('Condition Tag: ', condTag)



    actionList = []
    for action in thenList[1].split('and'):
        actionTag = getActionTag(action)
        #print('Action Tag: ', actionTag)
        actionList.append(actionTag)
    return condTag,actionList


# Sample code to run the function

condTag,actionList = getCondAndActionTag(testStr)

print('Condition Tag: ', condTag)

for action in actionList:
    print('Action: ', action)