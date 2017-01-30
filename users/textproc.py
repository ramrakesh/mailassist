import requests
import sys
import nltk
nltk.data.path.append('./nltk_data/')
import time
from textblob import TextBlob
from textblob import Word
from textblob import *
from nltk.tokenize import sent_tokenize
# import enchant
# from enchant.checker import SpellChecker
import datetime
import re
import calendar
import datefinder


def getRemsTextProc(textInp,input_key):
	# txt=""
	# for words_fin in textInp:
	# 	if words_fin
	


	textInp=textInp.replace('\t','').replace('\n','')
	# txt = textInp
	txt = textInp.encode('utf-8')
	main_txt=""
	rem99=[]


	#     print each['id'],each['suggest'],each['reminders'],each['flag']
	# # for words_fin in txt:
	# #     while words_fin != '> wrote:' :
	# #         txt90=txt90+str(txt)
	# # print txt90
	# txt_find=re.search(r"(---------- Forwarded message ----------(.*?)From:(.*?)([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)(.*?)To:(.*?)([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?))?(.*?)On [A-Z][a-z]{2}, [A-Z][a-z]{2} \d{1,2}, \d{4} at \d{1,2}:\d{1,2}(.*?)wrote:",txt,re.M)
	# # txt_find2=re.search(r"(---------- Forwarded message ----------(.*?)From:(.*?)([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)(.*?)To:(.*?)([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)(.*?)Cc:(.*?)([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?))(.*?)On [A-Z][a-z]{2}, [A-Z][a-z]{2} \d{1,2}, \d{4} at \d{1,2}:\d{1,2}(.*?)wrote:",txt,re.M)
	# # txt_find3=re.search(r"(---------- Forwarded message ----------(.*?)From:(.*?)([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)(.*?)To:(.*?)([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)(.*?)Cc:(.*?)([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)(.*?)Bcc:(.*?)([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?))(.*?)On [A-Z][a-z]{2}, [A-Z][a-z]{2} \d{1,2}, \d{4} at \d{1,2}:\d{1,2}(.*?)wrote:",txt,re.M)
	# # txt_find4=re.search(r"(---------- Forwarded message ----------(.*?)From:(.*?)([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)(.*?)To:(.*?)([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)(.*?)Bcc:(.*?)([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?))(.*?)On [A-Z][a-z]{2}, [A-Z][a-z]{2} \d{1,2}, \d{4} at \d{1,2}:\d{1,2}(.*?)wrote:",txt,re.M)

	# # txt_find1=re.search(r'(.*?)(On [A-Z][a-z]{2}, [A-Z][a-z]{2} \d{1,2}, \d{4} at \d{1,2}:\d{1,2})(.*?)wrote:',txt,re.M)
	# # if txt_find <txt
	# # print txt_find
	# txt90=""
	# txt91=""
	# if txt_find is not None:
		
	#     txt90=txt_find.group(12)
	#     txt91=txt_find.group(0)
	#     # print "hello"
	# # elif txt_find2 is not None :
	# # 	txt90=txt_find1.group(1)
	# # 	txt91=txt_find1.group(0)
	# # 	print "hi"
	# # elif txt_find3 is not None :
	# # 	txt90=txt_find1.group(1)
	# # 	txt91=txt_find1.group(0)
	# # 	print "how"
	# # elif txt_find4 is not None :
	# # 	txt90=txt_find1.group(1)
	# # 	txt91=txt_find1.group(0)
	# # 	print "are you?"
	# # elif txt_find1 is not None :
	# # 	txt90=txt_find1.group(1)
	# # 	txt91=txt_find1.group(0)
	# 	# print "how are you?"
	# else :
	# 	txt90=text_Inp
	# 	txt91=text_Inp

	# print txt90
	# print txt91
	# txt90=textInp
	# txt91=textInp
	###############################
	sentInd = txt.find("wrote:")
	frwdInd = txt.find("---------- Forwarded message ----------")
	txt90=""
	txt91=""
	sent = False
	frwd = False
	checkSent = False
	checkFrwd = False
	if sentInd != -1:
		sent = True
	if frwdInd != -1:
	    frwd = True
	if sent and frwd:
	       
	    if sentInd < frwdInd:
	        # print "hello"
	        txt_find1=re.search(r"(.*?)(On [A-Z][a-z]{2}, [A-Z][a-z]{2} \d{1,2}, \d{4} at \d{1,2}:\d{1,2})(.*?)wrote:",txt,re.M)
	        # print txt_find1.groups()
	        checkSent = True
	        if txt_find1 is not None:

	            txt90=txt_find1.group(1)
	            main_txt=txt_find1.group(1)
	            txt91=txt_find1.group(0)
	    else:
	        # print "hello1"
	        txt_find1=re.search(r"(---------- Forwarded message ----------(.*?)From:(.*?)([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)(.*?)To:(.*?)([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?))?(.*?)On [A-Z][a-z]{2}, [A-Z][a-z]{2} \d{1,2}, \d{4} at \d{1,2}:\d{1,2}(.*?)wrote:",txt,re.M)
	        checkFrwd = True
	        # print txt_find1.groups()
	        if txt_find1 is not None:
	            txt90=txt_find1.group(12)
	            main_txt=txt_find1.group(12)
	            txt91=txt_find1.group(0)
	elif sent:
	    checkSent = True
	    # print "hello2"
	    txt_find1=re.search(r"(.*?)(On [A-Z][a-z]{2}, [A-Z][a-z]{2} \d{1,2}, \d{4} at \d{1,2}:\d{1,2})(.*?)wrote:",txt,re.M)
	    # print txt_find1.groups()
	    if txt_find1 is not None:
	        txt90=txt_find1.group(1)
	        main_txt=txt_find1.group(1)
	        txt91=txt_find1.group(0)
	    # print txt90

	elif frwd:
	    print "hello3"
	    # checkFrwd =True
	    txt_find1=re.search(r"(---------- Forwarded message ----------(.*?)From:(.*?)([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)(.*?)To:(.*?)([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?))?(.*)",txt,re.M)
	    # print txt_find1.groups()
	    if txt_find1 is not None:
	        txt90=txt_find1.group(11)
	        main_txt=txt_find1.group(11)
	        txt91=txt_find1.group(0)
	else:
		# print "hello4"
		txt90=txt
		main_txt=txt
		txt91=txt
	# print txt90

	    # if txt90 == '':
	    #     print "No"
	    # if checkSent:
	    #     resp = content[0:sentInd]
	    # elif checkFrwd and frwdInd != 0:
	    #     resp = content[0:frwdInd]
	    # elif checkFrwd and frwdInd == 0:
	    #     resp = 'Check'
	    # else:
	    #     resp = content
	    # return txt90






	today = datetime.date.today()
	input_key={}
	excep=['please','kindly','sincerely','obediently']
	tex2in={'one ':1,'two ':2,'three ':3,'four ':4,'five ':5,'six ':6,'seven ':7,'eight ':8,'nine ':9,'ten ':10}
	dicti={'monday':0,'tuesday':1,'wednesday':2,'thursday':3,'friday':4,'saturday':5,'sunday':6}
	tmda=[' this ',' on ',' before ',' by ', ' coming ','this ','on ','before ','by ', ' coming',' this',' on',' before',' by', ' coming','between','between ',' between']
	tmdan=['next ']
	befw=['in','within','next','next ','after','in ','within ','after ','before ','before','between','between ']
	aftw=['later',' later']
	prs=['a','next','a ','next ']
	daystr={'today':0,'tomorrow':1,'day after tomorrow':2,'dayafter tomorrow':2}
	auth=['Director','Dean','Registrar','Professor','HOD','Head of the department','Head','MHRD','UGC','AICTE','Minister','Ministry','University grants commission','chairman','officer']
	# auth_find=re.findall(r'(\bDirector(s(\'s)?)?\b|\bDean(s(\'s)?)?\b|\bRegistrar(s(\'s)?)?\b|\bProfessor(s(\'s)?)?\b|\bHOD(s(\'s)?)?\b|\bHead of the department(s(\'s)?)?\b|\bHead(s(\'s)?)?\b|\bMHRD(\'s)?\b|\bUGC(\'s)?\b|\bAICTE(\'s)?\b|\bMinister(s(\'s)?)?\b|\bMinistry(\'s)?\b|\bUniversity grants commission(\'s)?\b|\bchairman(s(\'s)?)?\b|\bchairperson(s(\'s)?)?\b)',txt,re.M|re.I)
	neg=['rescheduled','revised','postponed','preponed','cancelled','abandoned','changed','delayed','shifted','suspended','concluded']
	trav=['car ','cab ','taxi ','flight ','airbus','bus ','train ']
	# countd_find6=
	# id_ty=['proof','college','university','branch','roll','enrollment','unique','id','student','employment','employee','no.','number','transaction','card']
	enidty_find=['proof ','college ','university ','branch ','roll ','enrollment ','unique ','student ','employment ','employee ','employer ','transaction ','card ','candidate ', 'application ','transaction ','teacher ','registration ','article ','journal ','ISBN ']
	# for sent in nltk.sent_tokenize(txt):
	#     for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
	#         print chunk
	#         for rt,ty in chunk :
	#             if ty=='NNP' :
	#                 print rt
			# if hasattr(chunk, 'node'):
			# print "hello"
			# print chunk.leaves()
			# print chunk.node, ' '.join(c[0] for c in chunk.Leaves())
	tagse_find=[' ',' process',' procedure',' schedule',' notification',' results',' pattern',' syllabi',' syllabus',' topics',' details',' fees',' application',' dress',' regulations',' rules']
	# exmta_find['schedule','notification','process','results']

	keys=['id','suggest','reminders','flag']
	fmt=['%d-%m-%Y','%d/%m/%Y','%Y-%m-%d','%Y/%m/%d']
	flag=0
	# keys=['id','suggest','reminders']
	txt007=[]
	# main_txt=txt90
	main_dict=[]
	main_dict2=[]
	rem4=[]
	# print main_txt
	# print main_txt
	senten1 = sent_tokenize(main_txt)
	# print senten1
	print'\n'
	txt1=TextBlob(main_txt)
	senten=txt1.sentences
	# print senten
	txt=""
	suggester=""
	suggester_fin=[]
	suggester_fin1=[]
	em_not=[]
	id_ch=0
	# chkr = SpellChecker("en_US",main_txt)
	# d = enchant.request_dict("en_US")
	# for err in chkr :
	#     suggester=""
	#     suggester1=""
	#         # print "Error might be in text {0} :".format(txt.find(err.word)) 
	#         # print "suggestions to be considered are {0} :".format(d.suggest(err.word))
	#         # suggester_fin.append("Error might be in text {0} :".format(txt.find(err.word)))
	#     suggester="suggestions to be considered are {0} :".format(d.suggest(err.word)) + "at {0}".format(main_txt.find(err.word))
	#     suggester_fin.append(suggester)
		# suggester1='\n'.join(suggester)
		# suggester_fin1.append(suggester1)
		# suggester_fin.append('\n')   
	# print suggester_fin
	#print '\n'
	rem1=" "
	rem3=" "
	rem2=[]
	rem6=" "
	rem20=[]
	# url = "http://api.meaningcloud.com/topics-2.0"
	# payload = "key=1874cd60759c34f1c7e5e43f659f6a77&lang=en&txt="+main_txt+"&tt=a&timeref=DD-MM-YYYY HH:MM:SS GMT+05:30"
	# headers = {'content-type': 'application/x-www-form-urlencoded'}
	# response = requests.request("POST", url, data=payload, headers=headers)
	# b=response.json() 
	# print b
	# today_uni=today

	# rem1=""
	rem5=[]
	values24=[]
	reminders10=[]
	# for each in input_key:
		
	# keywords = {
	# 	'key1': ['Action'],
	# 	'key2': ['Action'],
	# 	'key3': ['Action'],
	# 	'key4': ['Action'],
	# 	'key5': ['Action'],
	# 	'key6': ['Action1', 'Action2'],
	# 	'key7': ['Action']
	# }


	if input_key:
		maindict2=[]
		# main_dict = [
		#   {id
		#   suggest_revi
		#   reminders
		#   }
		# ]
		flag=1
		values24=[]
		reminders10=[]
		# id_cou=0
		for key,val in input_key.items():
			
			for j in range(0,len(val)) :
				id_ch+=1
				# print "{}={}".format(key,val[j])
				values_user=[id_ch,val[j],reminders10,flag]
				dictio24=dict(zip(keys,values_user))
				main_dict.append(dictio24)
				main_dict2.append(dictio24)
				# if main_txt.find(key)!=-1 or main_text.lower().find(key)!=-1:
				# 	main_dict.remove(dictio24)
				# 	main_dict2.remove(dictio24)
		
		# for each in main_dict2:
		#     print each['id'],each['suggest'],each['reminders']

	flag=0
	

	for i in range(0,len(senten)) :
		txt=senten1[i]
		#print txt
		#print "\n results for sentence {0}".format(i)
		# rem1=""
		# rem3=[]
		# rem5=[]
		matches = datefinder.find_dates(txt)
		for match in matches:
			match_fin= match.date()
			if match_fin > today :
				# print match_fin
				# rem1=match_fin
				rem2.append(str(match_fin))
				rem20.append(str(match_fin))
		# matchda = re.search(r'(\b\d{4}-\d{2}-\d{1,2}\b|\b\d{1,2}-\d{2}-\d{4}\b|\b\d{4}/\d{2}/\d{1,2}\b|\b\d{1,2}/\d{2}/\d{4}\b)', txt)
		# if matchda is not None:
		# 	matchda_fin = datetime.strptime(matchda.group(), '%Y-%m-%d').date()
		# 	if matchda_fin > today:
		# 		rem2.append(str(matchda_fin))
		# 		rem20.append(str(matchda_fin))
		matchda = re.search(r'\d{4}-\d{2}-\d{1,2}|\d{1,2}-\d{2}-\d{4}|\d{4}/\d{2}/\d{1,2}|\d{1,2}/\d{2}/\d{4}', txt)
		if matchda is not None:
			print matchda.group()
			for fmt1 in fmt:
			    try:
			        matchda_fin1 = datetime.datetime.strptime(matchda.group(),fmt1)
			        matchda_fin=matchda_fin1.date()
			        print matchda_fin
			        if matchda_fin > today :
			        	rem2.append(str(matchda_fin))
			        	rem20.append(str(matchda_fin))				
			    except ValueError:
			        pass
			    else:
			      break
			else:
			  matchda_fin1 = None

		# url = "http://api.meaningcloud.com/topics-2.0"
		# payload = "key=1874cd60759c34f1c7e5e43f659f6a77&lang=en&txt="+txt+"&tt=a&timeref=DD-MM-YYYY HH:MM:SS GMT+05:30"
		# headers = {'content-type': 'application/x-www-form-urlencoded'}
		# response = requests.request("POST", url, data=payload, headers=headers)
		# b=response.json()
		# print b
		####### calculate dates of any format #########  
		# if b['time_expression_list'] :
		# 	for i in range(0,len(b['time_expression_list'])):
		# 		if 'actual_time' in b['time_expression_list'][i]:
		# 			if b['time_expression_list'][i]['precision']=='day' :
		# 			# today_uni=datetime.strptime(b['time_expression_list'], '%Y-%m-%d')
		# 			   if datetime.datetime.strptime(b['time_expression_list'][i]['actual_time'],'%Y-%m-%d').date() > today:
		# 				  rem1=(b['time_expression_list'][i]['actual_time'])
		# 				# rem3.append(rem1)
		# 				  rem2.append(rem1)
		# 				  rem20.append(rem1)
		# for i in range(0,len(b['entity_list'])):
		#     print "{0} :".format(i) + b['entity_list'][i]['form']

		####### calculate dates if words are today,tomorrow and day after tomorrow  ######### 


		simpd_find=re.search(r'(\btoday\b|\btomorrow\b|\bday after tomorrow\b|\bdayafter tomorrow\b)',txt,re.M|re.I)

		if simpd_find is not None:
			dayu=today
			if daystr.has_key(simpd_find.group(0)):
				da=daystr.get(simpd_find.group(0))
				dayu=today+datetime.timedelta(days=da)

			# print "schedule reminder to {0}".format(dayu)
				str1="{0}".format(dayu)
				rem1=str1
				#rem5.append(rem1)
				rem2.append(str1)
				rem20.append(str1)
		# print rem1
				#print '\n'    
		else :
			dayu=[]
			
		####### calculate dates if words are week days #########       
		weekd_find=re.search(r'(\S+\s+|)(\bmonday\b|\btuesday\b|\bwednesday\b|\bthursday\b|\bfriday\b|\bsaturday\b|\bsunday\b)',txt,re.M|re.I)
		# print weekd_find
		# print weekd_find.group(2)
		# print weekd_find.group(1)
		if weekd_find is not None:
			daywt=today
			if dicti.has_key(weekd_find.group(2)):
				da=dicti.get(weekd_find.group(2))
				n = abs(today.weekday() - da) % 7 
				# print n
				if weekd_find.group(1) in tmda:
					daywt = today + datetime.timedelta(days=n)
				elif weekd_find.group(1) in tmdan:
					daywt=today +datetime.timedelta(weeks=1)
					daywt=daywt + datetime.timedelta(days=n)   
			# print "schedule reminder to {0}".format(daywt)
				str1="{0}".format(daywt)
				rem1=str1
				#rem5.append(rem1)
				rem2.append(str1)
				rem20.append(str1)
			# print rem1
			#print '\n'
		else:
			daywt=[]
		####### calculate dates by counting number of days from the inut text ######### 
			
		countd_find=re.search(r'(\S+\s+|)(\S+\s+|)days?(\s+\S+|)',txt,re.M|re.I)

		# print countd_find.group(0)
		# print countd_find.group(1)
		# print countd_find.group(2)
		# print countd_find.group(3)
		# countm_find=re.search(r'(\S+\s+|)(\S+\s+|)months(\s+\S+|)',txt,re.M|re.I)
		# k= int(countd_find.group(2))
		# print k
		k=0

		if countd_find is not None:
			daft=today
			if countd_find.group(2) in prs:
				daft=today+datetime.timedelta(days=1)
					# print daft
			elif tex2in.has_key(countd_find.group(2)):
				k=tex2in.get(countd_find.group(2))
				daft=today+datetime.timedelta(days=k)

			elif countd_find.group(1) in befw:
				k=int(countd_find.group(2))
				daft=today+datetime.timedelta(days=k)   
					# print daft
			elif countd_find.group(3) in aftw:
				k=int(countd_find.group(2))
				daft=today+datetime.timedelta(days=k)
					# print daft
				
			str1="{0}".format(daft)
			rem1=str1
			#rem5.append(rem1)
			rem2.append(str1)
			rem20.append(str1)
			# print rem1
			#print '\n'
		else:
			daft=[]
			
		####### calculate dates by counting number of months from the inut text #########
		countm_find=re.search(r'(\S+\s+|)(\S+\s+|)months?(\s+\S+|)',txt,re.M|re.I)

		# if countm_find is not None:
		#   m=0
			# le=countd_find.group(2)
			# if le.isdigit():
			
		z=0
		m=0

		if countm_find is not None:
			damt=today
			if tex2in.has_key(countm_find.group(2)):
				m=tex2in.get(countm_find.group(2))
				z=m*365/12
				damt=today+datetime.timedelta(days=z)
			elif countm_find.group(2) in prs:
				damt=today+datetime.timedelta(days=365/12)
			
				
				# print m
				# damt1=datetime.date.today.year()
				
				# if calendar.isleap(damt1):
				#     z= m*366/12
				# else:
				#     z= m*365/12
				
			elif countm_find.group(1) in befw:
				m=int(countm_find.group(2))
				z=m*365/12
				damt=today+datetime.timedelta(days=z)   
					# print damt
			elif countm_find.group(3) in aftw:
				m=int(countm_find.group(2))
				z=m*365/12
				damt=today+datetime.timedelta(days=z)
					# print damt
				
					# print damt
			
				
					# print damt
			str1="{0}".format(damt)
			rem1=str1
			#rem5.append(rem1)
			rem2.append(str1)
			rem20.append(str1)
			# print rem1
			#print '\n'   
		else:
			damt=[]
			

		####### calculate dates by counting number of weeks from the inut text #########
		countw_find=re.search(r'(\S+\s+|)(\S+\s+|)weeks?(\s+\S+|)',txt,re.M|re.I)

		# print countd_find.group(0)
		# print countd_find.group(1)
		# print countd_find.group(2)
		# print countd_find.group(3)
		# countm_find=re.search(r'(\S+\s+|)(\S+\s+|)months(\s+\S+|)',txt,re.M|re.I)
		# k= int(countd_find.group(2))
		# print k
		w=0

		if countw_find is not None:
			dawt=today
			if countw_find.group(2) in prs:
				dawt=today+datetime.timedelta(weeks=1)
					# print daft
			elif tex2in.has_key(countd_find.group(2)):
				k=tex2in.get(countw_find.group(2))
				dawt=today+datetime.timedelta(weeks=k)

			elif countw_find.group(1) in befw:
				k=int(countw_find.group(2))
				dawt=today+datetime.timedelta(weeks=k)   
					# print daft
			elif countw_find.group(3) in aftw:
				k=int(countw_find.group(2))
				dawt=today+datetime.timedelta(weeks=k)
					# print dawt
			str1="{0}".format(dawt)
			rem1=str1
			#rem5.append(rem1)
			rem2.append(str1)
			rem20.append(str1)
			# print rem1
			#print '\n'
		else:
			dawt=[]
		
		rem4.append(rem2)

		
		rem6=""
		rem5=[]
		# rem5.append(rem2)
		rem3=rem2
		rem2=[]
		if rem3:
			rem6=rem3[0]
			rem5.append(rem6)
			# rem4=rem5
		
		#print "hi {0}".format(rem5)
		rem3=[]
		rem5=str(rem5)
		####### classify the  input text as urgent or confidential #########
		class_find=re.findall(r'(\burgent(ly)?\b|\bconfidential\b|\bmandatory\b|\bas soon as possible\b)',txt,re.M|re.I)
		if class_find :
			suggest_cat=""
			# suggest_catfin=[]
			# id_ch+=1
			
					
			
			#print "inner"+rem5
			for i in range(0,len(class_find)):
				id_ch+=1
				# print "Action classified as {0}".format(class_find[i])
				suggest_cat="Action classified as {0}".format(class_find[i])
				# suggest_catfin.append(suggest_cat)
				# print suggest_catfin
				# rem6=rem5
				str11="{0}".format(rem5)
				values=[id_ch,suggest_cat,rem5,flag]
				dictio=dict(zip(keys,values))
				# print dictio
				main_dict.append(dictio)
	# acad_find=re.findall(r'(\bapplications?\b|\badmissions?\b|\bregistrations?\b|\ballotment\b)(\s+\S+|)',txt,re.M|re.I)
		
		####### find exam related tasks #########
		exmt_find=re.findall(r'(\bexam(ination)?\b|\btest\b|\bconvocation\b|\bPG ordinances?\b|\bUG ordinances?\b|\bordinances?\b|\badmissions?\b|\bPG regulations?\b|\bUG regulations?\b|\bregulations?\b|\binterview?\b)(\s+\S+|)',txt,re.M|re.I)
		if exmt_find:
			#print "examination related: "
			
			
			#print "inner"+rem5
			
			

			# print rem3
			# suggest_ex=[]
			# print exmt_find
			for i in range(0,len(exmt_find)) :
				
				
				# print exmt_find[i]
				if exmt_find[i][len(exmt_find[i])-1] in tagse_find :
					# print "\t\t\tinquire/convey information regarding {0}".format(exmt_find[i][0]) +"{0}".format(exmt_find[i][len(exmt_find[i])-1])
					# print "\t\t\trevised information {0}".format(exmt_find[i][0]) +"{0}".format(exmt_find[i][len(exmt_find[i])-1])
					
				
					str1="convey information regarding {0} to ".format(exmt_find[i][0]) +"{0}".format(exmt_find[i][len(exmt_find[i])-1])
					
					str2= "convey information regarding {0} to Assistant Registrar".format(exmt_find[i][0]) +"{0}".format(exmt_find[i][len(exmt_find[i])-1])
					str3= "convey information regarding {0} to Acadamics".format(exmt_find[i][0]) +"{0}".format(exmt_find[i][len(exmt_find[i])-1])
					str4= "convey information regarding {0} to Head of Department".format(exmt_find[i][0]) +"{0}".format(exmt_find[i][len(exmt_find[i])-1])
					str5= "convey information regarding {0} to Director".format(exmt_find[i][0]) +"{0}".format(exmt_find[i][len(exmt_find[i])-1])
					# suggest_ex.append([str1,str2])
					# suggest_ex.append(str2)
					# rem6=rem5
					id_ch+=1
					str11="{0}".format(rem5)
					values=[id_ch,str1,rem5,flag]
					dictio=dict(zip(keys,values))
					main_dict.append(dictio)
					id_ch+=1
					str11="{0}".format(rem5)
					# rem7=rem5
					values1=[id_ch,str2,rem5,flag]
					dictio1=dict(zip(keys,values1)) 
					main_dict.append(dictio1)
					id_ch+=1
					str11="{0}".format(rem5)
					# rem7=rem5
					values2=[id_ch,str3,rem5,flag]
					dictio2=dict(zip(keys,values2)) 
					main_dict.append(dictio2)
					id_ch+=1
					str11="{0}".format(rem5)
					# rem7=rem5
					values3=[id_ch,str4,rem5,flag]
					dictio3=dict(zip(keys,values3)) 
					main_dict.append(dictio3)
					id_ch+=1
					str12="{0}".format(rem5)
					# rem7=rem5
					values4=[id_ch,str5,rem5,flag]
					dictio4=dict(zip(keys,values4)) 
					main_dict.append(dictio4)
			
			# print suggest_ex
			# values=[id_ch,str1,rem1]
			# dictio=dict(zip(keys,values))
			# id_ch+=1
			# values1=[id_ch,str2,rem1]
			# dictio1=dict(zip(keys,values1))
			# print dictio
			
			#print '\n'
		####### find unique id's from the input text #########
		id_ty=re.findall(r'(\bproof\b|\bcollege\b|\buniversity\b|\bbranch\b|\broll\b|\benrollment\b|\bunique\b|\bstudent\b|\bemployment\b|\bemployee\b|\btransaction\b|\bcard\b|\bcandidate\b|\bapplication\b|\btransaction|\bteacher\b|\buser\b|\badministrator\b|\barticle\b|\bISBN\b|\border\b|\bcircular\b|\bauthor\b|\bpayment\b|\breference\b)',txt,re.M|re.I)
		# print id_ty
		id_uid=re.findall(r'(\S+\s+|)(\S+\s+|)([\b\s\S]?number is[\b\s\S]?|[\b\s\S]?id is[\b\s\S]?|[\b\s\S]?no. is[\b\s\S]?|\bid[\.\:\s]?[\b]?|\bno[\.\:\s]?[\b]?|\bnumber[\.\:\s]?[\b]?|\bpassword[\:\s]?[\b]?|\bpassword is[\b\:\s\S]?[\b]?)(\w+|\d+)',txt,re.M|re.I)
		# print id_uid
		if id_ty :
			id_fin1=[]
			
			k=0
					# print rem3
			suggest_id=[]
			# print "Unique ID's for reference:"
			for i in range(0,len(id_uid)):
				
				# kl=len(id_uid[i])
				for j in range(0,len(id_uid[i])):
					
					# print id_uid[i][j]
					if id_uid[i][j] in enidty_find :
						id_ch+=1
						id_fin1.append(id_uid[i][len(id_uid[i])-1])
						# print "\t\t"+ id_uid[i][j] + "number/id :" + id_fin1[k]
						str1=id_uid[i][j] + "number/id :{0}".format(id_fin1)
						# suggest_id.append(str1)
						k=k+1
						# rem6=r
						str11="{0}".format(rem5)
						values=[id_ch,str1,rem5,flag]
						dictio=dict(zip(keys,values))
						# print dictio
						main_dict.append(dictio)
				# print suggest_id
			#print '\n'
		# uuid_find=re.findall(r'[A-Z]*[0-9]*[]]{3,8}',txt,re.M|re.I)
		# print uuid_find
		####### find if any travel related details from the input text #########
		travld_find=re.findall(r'(\bcar\b|\bcab\b|\btaxi\b|\bflight\b|\bairbus\b|\bbus\b|\btrain\b)',txt,re.M|re.I)
		# for i in range ()
		# print travld_find
		len_travld=len(travld_find)
		id_fin=[]
		jklo=[]
		rtyui=[]
		if travld_find:
			# print rem3
			# id_ch+=1
			# suggest_tra=[]
			
			# rem3=rem5
			#print "travel related details :"
			for i in range(0,len(id_uid)):
				# kl=len(id_uid[i])
				for j in range(0,len(id_uid[i])):
					# print id_uid[i][j]
					if id_uid[i][j] in trav:
						id_ch+=1
						# print id_uid[i][kl]
						id_fin.append(id_uid[i][len(id_uid[i])-1])
			   # print id_fin
			   # print len(travld_find)
			
			#print travld_find
			if len(travld_find) > 1:
				id_ch+=1
				# print rem3
				# print "hi"
				# for i in range(0,len(travld_find)-1):
					# print "hi"
				tl=len(travld_find)-1
				# print tl
				jklo=travld_find[0]
				rtyui=travld_find[tl]
				# print "\t\t\ttravel means has been changed from {0} ".format(jklo) +"to {0}".format(rtyui)
				# print "\t\t\ttravel means unique id {0} ".format(id_fin[0]) 
				str1="travel means has been changed from {0} ".format(jklo) +"to {0}".format(rtyui)
				str2="travel means unique id {0} ".format(id_fin[0])
				# suggest_tra.append([str1,str2])
				str11="{0}".format(rem5)
				values=[id_ch,str1,rem5,flag]
				dictio=dict(zip(keys,values))
			
				# print dictio
				# main_dict.append(dictio)
				# print suggest_tra
				id_ch+=1
				str12="{0}".format(rem5)
				values1=[id_ch,str2,rem5,flag]
				dictio1=dict(zip(keys,values1))
				# print dictio
				main_dict.append(dictio)
				main_dict.append(dictio1)

			else:
				# print "travelling by {0}".format(travld_find) + "with unique id {0}".format(id_fin)
				str3="travelling by {0}".format(travld_find) + "with unique id {0}".format(id_fin) 
				# suggest_tra.append(str1) 
				id_ch+=1
				str11="{0}".format(rem5)
				values=[id_ch,str3,rem5,flag]
				dictio=dict(zip(keys,values))
				main_dict.append(dictio)

		####### find if any rescheduled tasks from the input text #########
		revs_find=re.findall(r'(\brescheduled?\b|\brevis[e(ed)(ion)]?\b|\bpostponed?\b|\bpreponed?\b|\bcancel[s(led)(ation)]?\b|\babandon[s(ed)]?\b|\bchange[sd]?\b|\bdelay[s(ed)]?\b|\bsuspended\b|\bconclude[sd]?\b|\bmeet(ing)?\b|\bappointment?\b|\bsubmi[t(ssion)]?\b|\bfunction\b|\blectures?\b|\bpresentations?\b|\bcontact\b)(\s+\S+|)(\s+\S+|)(\s+\S+|)',txt,re.M|re.I)
		if revs_find :
			
			# print rem3
			id_ch+=1
			suggest_revi=[]
			#print "revised/recheduled tasks: "
			kl=" "
			# print revs_find
			for i in range(0,len(revs_find)) :
				for j in range(0,len(revs_find[i])) :
					kl=kl + (revs_find[i][j])
			# print "\t\t\tthe program is" + kl
			str1="the program is" + kl
			# suggest_revi.append(str1)
			# print suggest_revi
			str11="{0}".format(rem5)
			values=[id_ch,str1,rem5,flag]
			dictio=dict(zip(keys,values))
			# print dictio
			main_dict.append(dictio)
			#print '\n'
		####### find email related details from the input text #########
		# mail_find=re.findall(r"([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)",txt,re.M|re.I)
		# if mail_find:
		# 	w=list()
			
		# 	# rem3=rem5

		# 	# print rem3
		# 	# suggest_mail=[]
		# 	# print "acquired contact email:"
		# 	for i in range(0,len(mail_find)):
		# 		for j in range(0,len(mail_find[i])):
		# 			if len(mail_find[i][j]) >8:
						
		# 				w.append(mail_find[i][j])
		# 				# print mail_find[i][j]
		# 				at_find=re.search(r'@',mail_find[i][j],re.M|re.I)
		# 				if at_find is None :
		# 					w.remove(mail_find[i][j])
		# 	for i in range(0,len(w)) :
		# 		# id_ch+=1
		# 		# print "contact email id  is : {0}".format(w[i])
		# 		# print "\t\t\treply through email {0}".format(w[i])
		# 		# print "\t\t\tforward the mail of {0} to:".format(w[i])
		# 		# str1="contact email id  is : {0}".format(w[i])
		# 		str2="contact through email {0}".format(w[i])
		# 		# str3="forward the mail of {0} to:".format(w[i])

		# 		em_not.append(str(w[i]))
		# 		# suggest_mail.append([str1,str2,str3])
		# 		# str11="{0}".format(rem5)
		# 		# values=[id_ch,str1,rem5,flag]
		# 		# dictio=dict(zip(keys,values))
		# 		# main_dict.append(dictio)
		# 	# print dictio
		# 		id_ch+=1
		# 		str12="{0}".format(rem5)
		# 		values1=[id_ch,str2,rem5,flag]
		# 		dictio1=dict(zip(keys,values1))
		# 		main_dict.append(dictio1)
		# 	# print dictio
				
		# 		# id_ch+=1
		# 		# str13="{0}".format(rem5)
		# 		# values2=[id_ch,str3,rem5,flag]
		# 		# dictio2=dict(zip(keys,values2))
		# 		# # print dictio
		# 		# main_dict.append(dictio2)
			
			
			# print suggest_mail
			#print '\n'
		####### find telephone contact related details from the input text #########

		# tel_find=re.findall(r'(\+?\(?[(91)0]?[\)\-]?\(?[(\d{2,4})(\d{2,4}?)]+[\)\-]?\d{6}?)',txt,re.M|re.I)

		# if tel_find:
			
		# 	# rem3=rem5 
		# 	# print rem3
		# 	# suggest_tel=[]
		# 	#print "acquired telephone contact: "
		# 	for i in range(0,len(tel_find)) :
		# 		# print tel_find[i]
		# 		if len(tel_find[i])>8 :
		# 			id_ch+=1
		# 			# print "\t\t\twould you like to call {0}?".format(tel_find[i])
		# 			# print "\t\t\twould you like to message {0}".format(tel_find[i])
		# 			str1="contact number {0}?".format(tel_find[i])
		# 			# str2="forward contact number {0} to".format(tel_find[i])
		# 			# suggest_tel.append([str1,str2])
		# 			str11="{0}".format(rem5)
		# 			values=[id_ch,str1,rem5,flag]
		# 			dictio=dict(zip(keys,values))
		# 			main_dict.append(dictio)
		# 			# print dictio
		# 			# id_ch+=1
		# 			# str12="{0}".format(rem5)
		# 			# values1=[id_ch,str2,rem5,flag]
		# 			# dictio1=dict(zip(keys,values1))
		# 			# # print dictio
		# 			# main_dict.append(dictio1)
		# 			# rem3=[]
		
			#print '\n'
		####### find official authorities related details from the input text #########

		


		auth_find=re.findall(r'(\bDirector[s(\'s)]?\b|\bDean[s(\'s)]?\b|\bRegistrar[s(\'s)]?\b|\bHOD[s(\'s)]?\b|\bHead of the department[s(\'s)]?\b|\bHead[s(\'s)]?\b|\bMHRD[(\'s)]?\b|\bUGC[(\'s)]?\b|\bAICTE[(\'s)]?\b|\bMinister[s(\'s)]?\b|\bMinistry[(\'s)]?\b|\bUniversity grants commission[(\'s)]?\b|\bchairman[s(\'s)]?\b|\bchairperson[s(\'s)]?\b|\bofficer[s(\'s)]?\b|\bBoard of Directors[(\'s)]?\b|\bcouncil[(\'s)]?\b|\bAR\b|\bAssistant Registrar[s(\'s)]?\b|\bmanager[(\'s)]?\b|\bincharge[(\'s)]?\b|\badministrator[(\'s)]?\b|\badmin[(\'s)]?\b|\bconvenor[(\'s)]?\b|\bincharge[(\'s)]?\b|\bwarden[(\'s)]?\b)',txt,re.M|re.I)
		
		if auth_find:
			# print rem3
			# suggest_auth=[]
			
			# rem3=rem5
			#print "official tasks:"
			for i in range(0,len(auth_find)):
				id_ch+=1
				#print '\n'
				# print "\t\t\t schedule meeting/appointment with {0}".format(auth_find[i])
				# print "\t\t\t inform/report to {0}".format(auth_find[i])
				# print "\t\t\t request for status/grant/approval from  {0}".format(auth_find[i])
				# print "\t\t\t authorize/approve the request of {0}".format(auth_find[i])
				str1="schedule meeting/appointment with {0}".format(auth_find[i])
				str2= "inform/report to {0}".format(auth_find[i])
				str3= "request for status/grant/approval from  {0}".format(auth_find[i])
				str4= "authorize/approve the request of {0}".format(auth_find[i])
				str5= "forward the message from {0} to".format(auth_find[i])
				# suggest_auth.append([str1,str2,str3,str4])
				str11="{0}".format(rem5)
				values=[id_ch,str1,rem5,flag]
				dictio=dict(zip(keys,values))
				main_dict.append(dictio)
				# print dictio
				id_ch+=1
				str12="{0}".format(rem5)
				values1=[id_ch,str2,rem5,flag]
				dictio1=dict(zip(keys,values1))
				main_dict.append(dictio1)
				# print dictio
				id_ch+=1
				str13="{0}".format(rem5)
				values2=[id_ch,str3,rem5,flag]
				dictio2=dict(zip(keys,values2))
				main_dict.append(dictio2)
				# print dictio
				id_ch+=1
				str14="{0}".format(rem5)
				values3=[id_ch,str4,rem5,flag]
				dictio3=dict(zip(keys,values3))
				# print dictio
				main_dict.append(dictio3)
				id_ch+=1
				str15="{0}".format(rem5)
				values4=[id_ch,str5,rem5,flag]
				dictio4=dict(zip(keys,values4))
				main_dict.append(dictio4)
			# print suggest_auth
			#print '\n'    
		
		txt1=TextBlob(txt)
		# klo=extract(txt)
		# klp=analyze(txt1)
		# kli=parse(txt1)

		txt9=nltk.tag.pos_tag(txt1.split())
		# print txt9

		senten=txt1.sentences
		txt3=txt1.noun_phrases
		# print(txt3)
		# txt7=txt1.lower()
		# print txt7
		txt4=nltk.tag.pos_tag(txt3)
		txt5=list()
		for wo,po in txt4:
			if po =='NN':
				txt5.append(wo)
		txt6=[]


		for w in set(excep):
			if w in txt5:
				txt5.remove(w)
		for i in range(0,len(auth_find)):
			txt5.append(auth_find[i])
		#print txt5
		# print txt9
		for wor,pos in txt9 :
			if pos=='NNP':
				# kop=wor.lowercase
				# print wor
				for i in range(0,len(txt5)) :
					if wor.lower() in txt5[i].split() :
						txt6.append(txt5[i])

		txt6=list(set(txt6))
		prefix=["sir","respected","dear","my","madam","honourble"]
		for wor in txt6 :
			wor1=wor.lower()
			if wor1.startswith(('~' , '@' , '#' , '$' , '%' , '^' , '&' , '*' , '(' , ')' , '_' , '-' , '+' , '<' , '>' , '?' , '/' , '|' , ':' , ',' , '.' , ';' , '[' , ']' , '{' , '}' , '`' )) :
				txt6.remove(wor)
			if wor1.endswith(('~' , '@' , '#' , '$' , '%' , '^' , '&' , '*' , '(' , ')', '_' , '-' , '+' , '<' , '>' , '?' , '/' , '|' , ':' , ',' , '.' , ';' , '"' , '[' , ']' , '{' , '}' , '`' )) :
				txt6.remove(wor)
			if wor1.endswith('ion') :
				txt6.remove(wor)
			if wor1.endswith('ler') :
				txt6.remove(wor)
		for i in range(0,len(txt6)-1) :
			if txt6[i].lower().startswith(tuple(prefix)) :
				txt6.remove(txt6[i])
			# for wor2 in prefix :
			#     wor3=wor1.split()
			#     if wor2 in wor3:
			#         txt6.remove(wor)
			# if wor1.startswith(tuple(prefix)):
			#     txt6.remove(wor)
			# if wor1.endswith(' sir'):
			#     txt6.remove(wor)
			# if wor1.endswith('madam'):
			#     txt6.remove(wor)
			# if wor1.startswith('dear'):
			#     txt6.remove(wor)
			# if wor1.startswith('respected'):
			#     txt6.remove(wor)
			
	# print unicode(txt6)
		univ_find=re.findall(r'(\S+\s+|)(\S+\s+|)(\S+\s+|)(\binstitutes?\b|\buniversity\b|\bcolleges?\b|\bschools?\b)(\s+\S+|)(\s+\S+|)',txt,re.M|re.I)
		if univ_find:
			str4=""
			str5=""
			# print univ_find
			for i in range(0,len(univ_find)):
				for j in range(0,len(univ_find[i])) :
					str4=univ_find[i][j].lower()
					# print str4
					for k in range(0,len(txt6)-1):
						str5=txt6[k].lower()
						str6=str5+' '
						str7=' '+ str5
						# print str6
						if str4==str6 or str4==str5 or str4==str7:
							# print "hello"
							txt6.remove(txt6[k])
		# txt6.append('introduction')
		
		# for i in range(0,len(txt6)) :
		#   if txt6[i].endswith('ion') :
		#       txt6.remove(txt6[i])
		# txt6.append('Introduction')
		# txt7=[]
		
			# if w,1.startswith('*'):
			#     txt6.remove(wor)
			

			

		# print txt6

		####### find the person entity details from the input text #########
		
		# txt56=nltk.tag.pos_tag(txt6)
		# # print txt56
		# for wor_en,pos_en in txt56:
		#   if pos_en !='NN':
		#       txt6.remove(wor_en)
		
		if txt6 :
			# print rem3
			
			# rem3=rem5
			
			# suggest_enti=[]
			for i in range(0,len(txt6)) :
				if len(txt6[i])>4 :
					
					# for j in range(0,len(b['entity_list'])):
						# print "{0} :".format(i) + b['entity_list'][j]['form']
						# if b['entity_list'][j]['form'].lower() == txt6[i] :

					id_ch+=1
			#print '\n'
			# print "\t\t\tschedule appointment with {0}".format(txt6[i])
			# print "\t\t\trequest/inquire for status/grant/approval from {0}".format(txt6[i])
			# print "\t\t\tinform/report to {0}".format(txt6[i])
			# print "\t\t\tauthorize/approve the request of {0}".format(txt6[i])
					str1="schedule meeting appointment of {0}".format(txt6[i]) 
					str2="forward the information/request of {0} to ".format(txt6[i])
					str3= "inform/report to {0}".format(txt6[i])
					str4= "authorize/approve the request of {0}".format(txt6[i])
					str11="{0}".format(rem5)
					values=[id_ch,str1,rem5,flag]
					dictio=dict(zip(keys,values))
					main_dict.append(dictio)
					# print dictio
					id_ch+=1
					str12="{0}".format(rem5)
					values1=[id_ch,str2,rem5,flag]
					dictio1=dict(zip(keys,values1))
					main_dict.append(dictio1)
			# print dictio
					id_ch+=1
					str13="{0}".format(rem5)
					values2=[id_ch,str3,rem5,flag]
					dictio2=dict(zip(keys,values2))
					main_dict.append(dictio2)
					# print dictio
					id_ch+=1
					str14="{0}".format(rem5)
					values3=[id_ch,str4,rem5,flag]
					dictio3=dict(zip(keys,values3))
					main_dict.append(dictio3)

		# else :
		# if b['entity_list'] :
	#     for i in range(0,len(b['entity_list'])) :
	#         # for j in range(0,len(b['entity_list'][i])):
	#                 # print "{0} :".format(i) + b['entity_list'][j]['form']
	#                 # if b['entity_list'][j]['form'].lower() == txt6[i] 
	#         id_ch+=1
	#     #print '\n'
	#     # print "\t\t\tschedule appointment with {0}".format(txt6[i])
	#     # print "\t\t\trequest/inquire for status/grant/approval from {0}".format(txt6[i])
	#     # print "\t\t\tinform/report to {0}".format(txt6[i])
	#     # print "\t\t\tauthorize/approve the request of {0}".format(txt6[i])
	#         str1="schedule appointment with {0}".format(b['entity_list'][i]['form'])
	#         str2="request/inquire for status/grant/approval from {0}".format(b['entity_list'][i]['form'])
	#         str3= "inform/report to {0}".format(b['entity_list'][i]['form'])
	#         str4= "authorize/approve the request of {0}".format(b['entity_list'][i]['form'])
	#         str11="{0}".format(rem5)
	#         values=[id_ch,str1,rem5,flag]
	#         dictio=dict(zip(keys,values))
	#         main_dict.append(dictio)
	#         # print dictio
	#         id_ch+=1
	#         str12="{0}".format(rem5)
	#         values1=[id_ch,str2,rem5,flag]
	#         dictio1=dict(zip(keys,values1))
	#         main_dict.append(dictio1)
	# # print dictio
	#         id_ch+=1
	#         str13="{0}".format(rem5)
	#         values2=[id_ch,str3,rem5,flag]
	#         dictio2=dict(zip(keys,values2))
	#         main_dict.append(dictio2)
	#     # print dictio
	#         id_ch+=1
	#         str14="{0}".format(rem5)
	#         values3=[id_ch,str4,rem5,flag]
	#         dictio3=dict(zip(keys,values3))
	#         main_dict.append(dictio3)
					# print dictio
				# main_dict.append([dictio,dictio1,dictio2,dictio3])
			# print suggest_enti
			#print '\n'
		####### find certificate related details from the input text #########

		


		cert_find=re.findall(r'(\S+\s+|)(\S+\s+|)(\bcertificates?\b|\bmark[\s\S]sheets?\b|\bgrade[\s\S]cards?\b|\bletter of recommendation?\b|[\b\(]OD[\)\b]|\bbio[\-\s\S]?data\b|[\b\(]CMM[\)\b]|\bforms?\b|[\b\(]CV[\)\b]|[\b\(]LOR[\)\b]|\bresults?\b|\bresume?\b|\bcurriculum vitae?\b)',txt,re.M|re.I)
		non_use=[',','.','the','in','on','for','by','to','and','I','of','at',', ','. ','the ','in ','on ','for ','by ','to ','and ','I ','of ','at ',' ,',' .',' the',' in',' on',' for',' by',' to',' and',' I',' of',' at']
		# str3=nltk.tag.pos_tag(cert_find)
		# print str3
		if cert_find: 
			
			# print rem3  
			str1=""
			str2=[]
			wordte1=[]
			wordte2=[]
			
			suggest_cert=[]
			# rem3=[]
			# rem3=rem5
			for i in range(0,len(cert_find)):
				# print cert_find[i]
				for j in range(0,len(cert_find[i])) :
					# wordte1.append(cert_find[i][j])
					if cert_find[i][j] not in non_use:
						wordte1.append(cert_find[i][j])
				
				wordte2.append(wordte1)
				wordte1=[]
				# print wordte2    
			for k in range(0,len(wordte2)):
				str1=' '.join(wordte2[k])
				# str1=' '.join(wordte1)
				str2.append(str1)
			# print str2
			for i in range(0,len(str2)) :
				id_ch+=1
				#print '\n'
				# print "\t\t\trequest for {0}".format(str2[i])
				# print "\t\t\tstatus of the grant/approval for {0}".format(str2[i])
				# print "\t\t\tgrant/approve/authorize the request of {0}".format(str2[i])
				# print "\t\t\trequest for corrections/changes in {0}".format(str2[i])
				# print "\t\t\tconvey/update the information regarding the {0}".format(str2[i])
				str4="request for {0}".format(str2[i])
				# str5="status of the grant/approval for {0}".format(str2[i])
				str6= "grant/approve/authorize the request of {0}".format(str2[i])
				str7= "request/intimate for corrections/changes in {0}".format(str2[i])
				str8= "convey/update the information regarding {0}".format(str2[i])
				str9= "forward the information/request regarding {0} to Academics department".format(str2[i])
				# suggest_cert.append([str4,str5,str6,str7,str8])
				str11="{0}".format(rem5)
				values=[id_ch,str4,rem5,flag]
				dictio=dict(zip(keys,values))
				main_dict.append(dictio)
				id_ch+=1
				str16="{0}".format(rem5)
				values5=[id_ch,str9,rem5,flag]
				dictio5=dict(zip(keys,values5))
				main_dict.append(dictio5)
				# print dictio
				# id_ch+=1
				# str12="{0}".format(rem5)
				# values1=[id_ch,str5,rem5,flag]
				# dictio1=dict(zip(keys,values1))
				# main_dict.append(dictio1)
				# print dictio
				id_ch+=1
				str13="{0}".format(rem5)
				values2=[id_ch,str6,rem5,flag]
				dictio2=dict(zip(keys,values2))
				main_dict.append(dictio2)
				# print dictio
				id_ch+=1
				str14="{0}".format(rem5)
				values3=[id_ch,str7,rem5,flag]
				dictio3=dict(zip(keys,values3))
				main_dict.append(dictio3)
				id_ch+=1
				str15="{0}".format(rem5)
				values4=[id_ch,str8,rem5,flag]
				dictio4=dict(zip(keys,values4))
				main_dict.append(dictio4)
				
			# print suggest_cert
			#print '\n'
		#print txt5
		####### find financial related details from the input text #########

		
	# 	for i in range(0,len((b['money_expression_list']))):
	# 		id_ch+=1
	# 		str1= "Financial information with amount of " + b['money_expression_list'][i]['form']
	# 		str2= "Forward to the details to finance department of amount"+ b['money_expression_list'][i]['form']
	# 		str3= "Forward to the financial details of  amount "+ b['money_expression_list'][i]['form'] + "to"
	# 		values=[id_ch,str1,rem1]
	# 		dictio=dict(zip(keys,values))
	# # print dictio
	# 		main_dict.append(dictio)
	# 		values1=[id_ch,str2,rem1]
	# 		dictio=dict(zip(keys,values1))
	# # print dictio
	# 		main_dict.append(dictio1)
	# 		values2=[id_ch,str3,rem1]
	# 		dictio2=dict(zip(keys,values2))
	# # print dictio
	# 		main_dict.append(dictio2)


		# txt007.append(txt5)
		
	mail_find=re.findall(r"([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)",txt91,re.M|re.I)
	if mail_find:
		w=list()
		
		# rem3=rem5

		# print rem3
		# suggest_mail=[]
		# print "acquired contact email:"
		for i in range(0,len(mail_find)):
			for j in range(0,len(mail_find[i])):
				if len(mail_find[i][j]) >8:
					
					w.append(mail_find[i][j])
					# print mail_find[i][j]
					at_find=re.search(r'@',mail_find[i][j],re.M|re.I)
					if at_find is None :
						w.remove(mail_find[i][j])
		for i in range(0,len(w)) :
			# id_ch+=1
			# print "contact email id  is : {0}".format(w[i])
			# print "\t\t\treply through email {0}".format(w[i])
			# print "\t\t\tforward the mail of {0} to:".format(w[i])
			# str1="contact email id  is : {0}".format(w[i])
			str2="contact through email {0}".format(w[i])
			# str3="forward the mail of {0} to:".format(w[i])

			em_not.append(str(w[i]))
			# suggest_mail.append([str1,str2,str3])
			# str11="{0}".format(rem5)
			# values=[id_ch,str1,rem5,flag]
			# dictio=dict(zip(keys,values))
			# main_dict.append(dictio)
		# print dictio
			id_ch+=1
			str12="{0}".format(rem5)
			values1=[id_ch,str2,rem5,flag]
			dictio1=dict(zip(keys,values1))
			main_dict.append(dictio1)
		# print dictio
			
			# id_ch+=1
			# str13="{0}".format(rem5)
			# values2=[id_ch,str3,rem5,flag]
			# dictio2=dict(zip(keys,values2))
			# # print dictio
			# main_dict.append(dictio2)
	tel_find=re.findall(r'(\+?\(?[(91)0]?[\)\-]?\(?[(\d{2,4})(\d{2,4}?)]+[\)\-]?\d{6}?)',txt91,re.M|re.I)

	if tel_find:
		
		# rem3=rem5 
		# print rem3
		# suggest_tel=[]
		#print "acquired telephone contact: "
		for i in range(0,len(tel_find)) :
			# print tel_find[i]
			if len(tel_find[i])>8 :
				id_ch+=1
				# print "\t\t\twould you like to call {0}?".format(tel_find[i])
				# print "\t\t\twould you like to message {0}".format(tel_find[i])
				str1="contact number {0}?".format(tel_find[i])
				# str2="forward contact number {0} to".format(tel_find[i])
				# suggest_tel.append([str1,str2])
				str11="{0}".format(rem5)
				values=[id_ch,str1,rem5,flag]
				dictio=dict(zip(keys,values))
				main_dict.append(dictio)
				# print dictio
				# id_ch+=1
				# str12="{0}".format(rem5)
				# values1=[id_ch,str2,rem5,flag]
				# dictio1=dict(zip(keys,values1))
				# # print dictio
				# main_dict.append(dictio1)
				# rem3=[]	
	# rem21=list(set(rem20))
	em_not=list(set(em_not))
	# print rem21
	# values=[0,txt007,rem21,flag]
	# dictio=dict(zip(keys,values))
	# # print dictio
	# main_dict.append(dictio)
	# print main_dict
	if not rem20:
		finrem=""	
		finrem1=[]
		for each in main_dict:
			finrem1.append(str(today+datetime.timedelta(days=1)))
			finrem2=list(set(finrem1))
			rem20=finrem2
			each['reminders']=finrem2
	rem99.append(str(rem20[-1]))
	# print rem99
	for each in main_dict:      
	    # print each['reminders']
	    if each['reminders']=='' or each['reminders']==' ' or each['reminders']=='[]' or each['reminders'] is None or not each['reminders']:	
	    	# print each['id']
	    	each['reminders']=rem99
	    # print each['id'],each['suggest'],each['reminders'],each['flag']





	return main_dict

# if __name__ == '__main__':
#     txt = "My name is Vinay Kumar with dob 5th december 2016 . My phone no.08572235767, B.Ram Kumar a 2012 rupees M.TECH (CIVIL) pass out roll number is 08781A0411 and class 12th grade card, mark sheet, examination schedule and admission procedure, application process, aplication procedure, results. my friend Rakesh Chaterjee and ram.ultimate.knight@gmail.com and proof no.6765987. meeting with assistant registrar after three days by cab. the program is rescheduled on 05-11-2016 at kolkata. I have taken admision for higher studies in this session with flight no:2654WE , to complete my registration process I urgently need my migration certificate, provisional certificate,project completion certificate and letter of recommendation (LOR) before 2 months. Please send me the migration soonest possible before three months. on next saturday I've mentioned my address details below."
#     getRemsTextProc(txt)
