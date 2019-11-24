import sys 
import re
import json

input_string = "he replies on Slack, then save response into Google Sheets else make document on Google Sheets and hosting it on Slack"
final_string = "Text Keith, 'Hey, did we get flights approved? If Keith replies 'yes' on twilio then message Alex on slack 'what is the total cost of flights', and save her response on the expense report on Google Sheets and send Keith on twilio 'all done!' Else text Keith on twilio 'no probs'"
#input_string = "if Annie texts me on Slack, then tell her I am busy on Gmail"

if_string = 'one If two if three If four if five'


from collected_parse import getCondAndActionTag
import json

def actionToJson(actionList,api_list):
	for d in actionList:
			actdict = {}

			#for matching the API keys with request
			for api in api_list:
				for key in d:
					if key == api:
						actdict['api'] = api
					elif api in key:
						actdict['api'] = api
					else:
						actdict['api'] = 'none'
			for key in d:
				actdict['action'] = d[key][0]

			actdict['tag'] = 'action'
			actdict['body'] = '#save'
			actdict['response'] = 'none'
			
			#actList.append(actdict)
			for key in d:
				actdict['action'] = d[key][0]



def split_it(istring):

	#Parse out the if statements

	ss = istring.lower().split('if')
	ss = list(filter(None, ss)) # fastest
	for i in range(1,len(ss)):
		ss[i] = 'if' + ss[i]
	ss = [i.split('else') for i in ss]
	for sub in ss:
		if len(sub) == 2:
			sub[1] = "else" + sub[1]
	#ss = [item for sublist in ss for item in sublist]
	#print(ss)
	return ss

st = "If abc then xyz, else pqr is the best, if I am happy then I will feel good else I will feel sad"

#print(split_it(final_string))






def method2(istring):

	#Parse out the if statements
	ss = split_it(istring)


	#print('ss: ',ss)
	#ss = [item for sublist in ss for item in sublist]
	#print(ss)
	print("\n")

	api_list = ['slack','twilio','googl','sheet','doc','gmail']
	
	papa_list = []	


	# Deal with root sentence
	rootSent = ss[0]

	for i,s in enumerate(ss):
		
		if i == 0:
			continue

		
		jdict = {}
		actList = []
		elseList =[]
		print('----------------------------')
		print('s: ',s)
		
		
		if len(s[0].split('then')) < 2:
			
			# We want to get any possible quotations from query
			# If len(quoteList) == 1, then that means there were no quotations
			actionQuoteList = s[0].split('"')[1::2]
			if len(actionQuoteList) == 0:
				actionQuoteList = s[0].split("'")[1::2]

			actionList = getCondAndActionTag(s[0])
			

			actionInfo = (actionList,actionQuoteList)

			print('actionInfo: ',actionInfo)
			###############################good stuff
			single_action_dict = {}

			for action in actionInfo[0]:#to list
				for d in action:#to dict
					for key in d:#to key
						for i in api_list:
							if i == key or key in i:
								single_action_dict['api'] = i

						single_action_dict['action'] = d[key][0]	

			single_action_dict['body'] = actionInfo[1][0]
			if single_action_dict['api'] == 'twilio':
				single_action_dict['number'] = '8328140815'
			
			actList.append(single_action_dict)
			"""
			###################################
			for d in actionList:
				actdict = {}

				#for matching the API keys with request
				for api in api_list:
					for key in d:
						if key == api:
							actdict['api'] = api
						elif api in key:
							actdict['api'] = api
						else:
							actdict['api'] = 'none'
				for key in d:
					actdict['action'] = d[key][0]

				actdict['tag'] = 'action'
				actdict['body'] = '#save'
				actdict['response'] = 'none'
				
				print('This is the api: ',actdict['api'])
				if actdict['api'] == 'twilio':
					print('\nits twilio')
					actdict['number'] = '8328140815'
					actdict['body'] = actionQuoteList[0]

				actList.append(actdict)
				for key in d:
					actdict['action'] = d[key][0]
			
			"""
			papa_list.append(actList)
		else:
			#print('top: ',s[0].split('then')[1].split("'")[1::2])
			condQuoteList = s[0].split('then')[0].split('"')[1::2]
			if len(condQuoteList) == 0:
				condQuoteList = s[0].split('then')[0].split("'")[1::2]
			
			actionQuoteList = s[0].split('then')[1].split('"')[1::2]
			if len(actionQuoteList) == 0:
				actionQuoteList = s[0].split('then')[1].split("'")[1::2]
			
			print('condQuoteList: ', condQuoteList)
			print('actionQuoteList: ', actionQuoteList)

			condTag, actionList = getCondAndActionTag(s[0])
		
			condInfo = (condTag,condQuoteList)
			actionInfo = (actionList,actionQuoteList)

			print('condInfo: ',condInfo)
			print('actionInfo: ',actionInfo)
			##################################
			jdict = {}

			for cond in condInfo[0]:#to list
				print(cond)
				for i in api_list:
					if i == cond or cond in i:
						jdict['api'] = i
				jdict['action'] = condInfo[0][cond][0]
				print(jdict['action'])
				print(jdict)
			###################################
			single_action_dict = {}

			for action in actionInfo[0]:#to list
				print(actionInfo[0])
				print(action)
				
				for i in api_list:
					for key in action:
						if i == str(key) or str(key) in i:
							single_action_dict['api'] = i
						single_action_dict['action'] = action[str(key)][0]
				#print(single_action_dict['action'])

			single_action_dict['body'] = actionInfo[1][0]			

			if single_action_dict['api'] == 'twilio':
				single_action_dict['number'] = '8328140815'

			#print('NUBMER',single_action_dict['number'])
			actList.append(single_action_dict)
			print(actList)
			###################################################
			if len(s) == 2:
				elseQuoteList = s[1].split('"')[1::2]
				if len(elseQuoteList) == 0:
					elseQuoteList = s[1].split("'")[1::2]

				elseAct = getCondAndActionTag(s[1])
				elseInfo = (elseAct,elseQuoteList)
				
				print('Else Info: ', elseInfo)

				else_action_dict = {}
				
				for action in elseInfo[0]:#to list
					print(action)
					for key in action:#to key
						for i in api_list:
							if i == key or key in i:
								else_action_dict['api'] = i

						else_action_dict['action'] = action[key][0]	
						#print(else_action_dict['action'])
				else_action_dict['body'] = actionInfo[1][0]
				#print(else_action_dict['body'])
				if else_action_dict['api'] == 'twilio':
					else_action_dict['number'] = '8328140815'
				elseList.append(else_action_dict)

				print(elseList)
			else:

				elseList = [{
					"tag": "none",
					"api": "none",
					"action": "none",
					"body": "none",
					"response": "none"
				}]
			#################################################
			jdict['false'] = elseList
			jdict['true'] = actList
			jdict['tag'] = 'elif'
			jdict['condition'] = 'responded'
			jdict['response'] = 'none'
			jdict['save'] = 'true'

			print(jdict)

			###################################
			"""
			for i in condTag.keys():
				if i in api_list:
					jdict['api'] = i

			#We going through the action list- making it into json itself
			for d in actionList:
				actdict = {}

				#for matching the API keys with request
				for api in api_list:
					for key in d:
						if key == api:
							actdict['api'] = api
						elif api in key:
							actdict['api'] = api
						else:
							actdict['api'] = 'none'
				for key in d:
					actdict['action'] = d[key][0]

				actdict['tag'] = 'action'
				actdict['body'] = '#save#'
				actdict['response'] = 'none'

				
				actList.append(actdict)
				for key in d:
					actdict['action'] = d[key][0]
			
			#If there is an else condition
			if len(s) == 2:

				elseQuoteList = s[1].split('"')[1::2]
				if len(elseQuoteList) == 0:
					elseQuoteList = s[1].split("'")[1::2]

				elseAct = getCondAndActionTag(s[1])
				elseInfo = (elseAct,elseQuoteList)
				
				print('Else Info: ', elseInfo)

				#print(elseAct)
				for d in elseAct:
					elsedict = {}

					#for matching the API keys with request
					for api in api_list:
						for key in d:
							if key == api:
								elsedict['api'] = api
							elif api in key:
								elsedict['api'] = api
							else:
								elsedict['api'] = 'none'
						for key in d: 
							elsedict['action'] = d[key][0]

					elsedict['tag'] = 'action'
					elsedict['body'] = '#save'
					elsedict['response'] = 'none'

					elseList.append(elsedict)
					for key in d:
						elsedict['action'] = d[key][0]
			else:

				elseList = [{
					"tag": "none",
					"api": "none",
					"action": "none",
					"body": "none",
					"response": "none"
				}]
			#print(elseList)
			#for the conditional JSON - assigning vars
			jdict['false'] = elseList
			jdict['true'] = actList
			jdict['tag'] = 'elif'
			jdict['condition'] = 'responded'
			jdict['response'] = 'none'
			jdict['action'] = 'recieve'
			jdict['save'] = 'true'
			"""
			#print(jdict)
			papa_list.append((jdict))
	
	with open('test_out.json','a') as j:
		for js in papa_list:
			json.dump(js,j)
			j.write('\n')

	
	



	#print(condTag)
method2(final_string)






















































































