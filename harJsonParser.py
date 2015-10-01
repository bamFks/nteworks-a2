import json
import unicodedata
# harfile=raw_input()
harfile='nytimes.har'
fileToString =""
harFile = open(harfile,"r")
for line in harFile:
	fileToString+=line
stringToJson = json.loads(fileToString)
totalObjectDownloaded=0
totalSizeOfObjectDownloaded=0
domains={}
object_types=[]
entries=stringToJson['log']['entries']
# for entry in entries:
# 	totalObjectDownloaded+=1
# 	size=0
# 	if(entry['response']['headersSize']>=0):
# 		size+=entry['response']['headersSize']
# 	if(entry['response']['bodySize']>=0):
# 		size+=entry['response']['bodySize']
# 	totalSizeOfObjectDownloaded+=size

# 	for header in entry['request']['headers']:
# 		if(header['name']=='Host'):
# 			domain=unicodedata.normalize('NFKD', header['value']).encode('ascii','ignore')
# 			if(domain not in domains):
# 				domains[domain]={}
# 				domains[domain]['objects_count']=1
# 				domains[domain]['objects_size']=size
# 			else:
# 				domains[domain]['objects_count']+=1
# 				domains[domain]['objects_size']+=size
# 			break
 
# 	content_type=unicodedata.normalize('NFKD', entry['response']['content']['mimeType']).encode('ascii','ignore')
# 	if(content_type not in object_types):
# 		object_types.append(content_type)







typesList=[]
typesCount={}

for entry in entries:
	# totalObjectDownloaded+=1
	# time=entry['time']
	# size=0
	contentType=""
	# serverIpAddres=entry['serverIPAddress']
	# serverIpAddres=unicodedata.normalize('NFKD', serverIpAddres).encode('ascii','ignore')
	# portNo=entry['connection']


	# request=entry['request']
	response=entry['response']
	# timings=entry['timings']

	# if(response['headersSize']>=0):
	# 	size+=response['headersSize']
	# if(response['bodySize']>=0):
	# 	size+=response['bodySize']
	
	contentType=response['content']['mimeType']
	contentType=unicodedata.normalize('NFKD', contentType).encode('ascii','ignore')
	print contentType
	# url=unicodedata.normalize('NFKD', request['url']).encode('ascii','ignore')
	# Referer=url
	# for header in request['headers']:
	# 	if(header['name']=='Referer'):
	# 		Referer=unicodedata.normalize('NFKD', header['value']).encode('ascii','ignore')


			
	# objectInfo={}
	# objectInfo["time"]=time
	# objectInfo["size"]=size
	# objectInfo["type"]=contentType
	# objectInfo["server"]=serverIpAddres
	# objectInfo["port"]=portNo
	# objectInfo["timings"]=timings
	# objectInfo["url"]=url
	# objectInfo["referer"]=Referer
	# objects.append(objectInfo)


	# # maintaining the object count form different domains
	# if(serverIpAddres not in domainsList):
	# 	domainInfo={}
	# 	connections=[]
	# 	connectionInfo={}
	# 	subConnections=[]
	# 	subConnections.append(url)
	# 	connectionInfo["time"]=timings['connect']
	# 	connectionInfo["urls"]=subConnections
	# 	connections.append(connectionInfo)

	# 	domainInfo["connections"]=connections
	# 	domainInfo["objectCount"]=1
	# 	domainInfo["size"]=size
	# 	domainInfo["totalNewConnections"]=0

		
	# 	if(timings['connect']!=0):
	# 		domainInfo["totalNewConnections"]+=1 

		
	# 	domainsList.append(serverIpAddres)
	# 	domains[serverIpAddres]=domainInfo
	# else:
	# 	domains[serverIpAddres]["objectCount"]+=1
	# 	domains[serverIpAddres]["size"]+=size
	# 	if(timings['connect']!=0):
	# 		domains[serverIpAddres]["totalNewConnections"]+=1
	# 		connectionInfo={}
	# 		connectionInfo["time"]=timings['connect']
	# 		subConnections=[]
	# 		subConnections.append(url)
	# 		connectionInfo["urls"]=subConnections
	# 		domains[serverIpAddres]['connections'].append(connectionInfo)
	# 	else:
	# 		length =len(domains[serverIpAddres]['connections'])
	# 		domains[serverIpAddres]['connections'][length-1]['urls'].append(url)

	# maintaining the list of object of particular type
	if(contentType not in typesList):
		typesCount[contentType]=1
		typesList.append(contentType)
	else:
		typesCount[contentType]+=1















