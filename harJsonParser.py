import json
import unicodedata
harfile=raw_input()
fileToString =""
totalObjectDownloaded=0
totalObjectSize=0

objects=[]
domains={}
domainsList=[]
typesCount={}
typesList=[]
tcpConnections={}




harFile = open(harfile,"r")
for line in harFile:
	fileToString+=line
stringToJson = json.loads(fileToString)

# print stringToJson['log']
# print len(stringToJson['log']['entries'])
entries=stringToJson['log']['entries']
for entry in entries:
	totalObjectDownloaded+=1
	time=entry['time']
	size=0
	contentType=""
	serverIpAddres=entry['serverIPAddress']
	serverIpAddres=unicodedata.normalize('NFKD', serverIpAddres).encode('ascii','ignore')
	portNo=entry['connection']


	request=entry['request']
	response=entry['response']
	timings=entry['timings']

	if(response['headersSize']>=0):
		size+=response['headersSize']
	if(response['bodySize']>=0):
		size+=response['bodySize']
	
	contentType=response['content']['mimeType']
	contentType=unicodedata.normalize('NFKD', contentType).encode('ascii','ignore')
	url=unicodedata.normalize('NFKD', request['url']).encode('ascii','ignore')
	Referer=url
	for header in request['headers']:
		if(header['name']=='Referer'):
			Referer=unicodedata.normalize('NFKD', header['value']).encode('ascii','ignore')


			
	objectInfo={}
	objectInfo["time"]=time
	objectInfo["size"]=size
	objectInfo["type"]=contentType
	objectInfo["server"]=serverIpAddres
	objectInfo["port"]=portNo
	objectInfo["timings"]=timings
	objectInfo["url"]=url
	objectInfo["referer"]=Referer
	objects.append(objectInfo)


	# maintaining the object count form different domains
	if(serverIpAddres not in domainsList):
		domainInfo={}
		connections=[]
		connectionInfo={}
		subConnections=[]
		subConnections.append(url)
		connectionInfo["time"]=timings['connect']
		connectionInfo["urls"]=subConnections
		connections.append(connectionInfo)

		domainInfo["connections"]=connections
		domainInfo["objectCount"]=1
		domainInfo["size"]=size
		domainInfo["totalNewConnections"]=0

		
		if(timings['connect']!=0):
			domainInfo["totalNewConnections"]+=1 

		
		domainsList.append(serverIpAddres)
		domains[serverIpAddres]=domainInfo
	else:
		domains[serverIpAddres]["objectCount"]+=1
		domains[serverIpAddres]["size"]+=size
		if(timings['connect']!=0):
			domains[serverIpAddres]["totalNewConnections"]+=1
			connectionInfo={}
			connectionInfo["time"]=timings['connect']
			subConnections=[]
			subConnections.append(url)
			connectionInfo["urls"]=subConnections
			domains[serverIpAddres]['connections'].append(connectionInfo)
		else:
			length =len(domains[serverIpAddres]['connections'])
			domains[serverIpAddres]['connections'][length-1]['urls'].append(url)

	# maintaining the list of object of particular type
	if(contentType not in typesList):
		typesCount[contentType]=1
		typesList.append(contentType)
	else:
		typesCount[contentType]+=1




def createObjectTree(objects):
	objectId=0
	urlToNodeId={}
	objectTree=[]

	for objectInfo in objects:
		urlToNodeId[objectInfo['url']]=objectId
		objectId+=1

	for objectInfo in objects:
		nodeid=urlToNodeId[objectInfo['url']]
		parentid=urlToNodeId[objectInfo['referer']]
		nodeTuple=[]
		nodeTuple.append(nodeid)
		nodeTuple.append(objectInfo['url'])
		nodeTuple.append(parentid)
		print nodeTuple
		objectTree.append(nodeTuple)
	return objectTree


def createDownloadTree(domainsList, domains):
	nodeId=0
	count=0
	downloadTree=[]
	for domain in domainsList:
		for connection in domains[domain]['connections']:
			for url in connection['urls']:
				nodeTuple=[]
				nodeTuple.append(domain)
				nodeTuple.append(count)
				nodeTuple.append(url)
				downloadTree.append(nodeTuple)
				print nodeTuple
			count+=1
	return downloadTree
createDownloadTree(domainsList,domains)
# print len(domainsList)
# for domain in domainsList:
# 	print domain
# 	print domains[domain]['connections'][0]
# 	print len(domains[domain]['connections'][0])
# 	print domains[domain]['objectCount']
# 	print domains[domain]['totalNewConnections']
# 	print '\n'











