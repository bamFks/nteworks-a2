#!/usr/bin/env python
import subprocess
import os
import json
import unicodedata
# harFile=raw_input()
# pcapFile=raw_input()
pcapFile='nytimes.pcap'
harfile='nytimes.har'
harFile = open(harfile,"r")

fileToString=""
for line in harFile:
	fileToString+=line
stringToJson = json.loads(fileToString)
entries=stringToJson['log']['entries']
ips=[]
domainIp={}
objects=[]

for entry in entries:
	# taking data for object tree
	url=unicodedata.normalize('NFKD', entry['request']['url']).encode('ascii','ignore')
	referer=url
	for header in entry['request']['headers']:
		if(header['name']=='Referer'):
			referer=unicodedata.normalize('NFKD', header['value']).encode('ascii','ignore')
			break
	new_object={}
	new_object['url']=url
	new_object['referer']=referer
	objects.append(new_object)


	# taking data for download tree
	serverIpAddres=unicodedata.normalize('NFKD', entry['serverIPAddress']).encode('ascii','ignore')
	domainName=""
	for header in entry['request']['headers']:
		if(header['name']=='Host'):
			domainName=unicodedata.normalize('NFKD', header['value']).encode('ascii','ignore')
			break
	if domainName not in domainIp:
		domainIp[domainName]=serverIpAddres
	if serverIpAddres not in ips:
		ips.append(serverIpAddres)

ipToConn={}
domainToConn={}
for ip in ips:
	cmd='tshark -r '+pcapFile+' -Y'
	cmd+='"ip.dst== ' +ip+' && http"'
	cmd+=' -T fields -e tcp.stream -e tcp.port -e http.request.full_uri'
	out = subprocess.check_output(cmd,shell=True)
	ipToConn[ip]={}
	list1=out.split("\n")
	list1.remove('')
	for entry in list1:
		list2=entry.split("\t")
		list3=list2[1].split(",")
		Id=list2[0]
		connId=int(Id)
		if connId not in ipToConn[ip]:
			ipToConn[ip][connId]=[]
		connection={}
		connection['port']=int(list3[0])
		connection['url']=list2[2]
		ipToConn[ip][connId].append(connection)
		


for key in domainIp:
	ip=domainIp[key]
	for key2 in ipToConn[ip]:
		pairs=ipToConn[ip][key2]
		for pair in pairs: 	
			url=pair['url']
			if(key  in url ):
				if(key not in domainToConn):
					domainToConn[key]={}
					domainToConn[key][key2]=[]
					domainToConn[key][key2].append(url)
				else:
					if(key2 not in domainToConn[key]):
						domainToConn[key][key2]=[]
						domainToConn[key][key2].append(url)
					else:
						domainToConn[key][key2].append(url)
tcp_stream=0
download_tree={}
tree=[]
for domain in domainToConn:
	for key in domainToConn[domain]:
		urls=domainToConn[domain][key]
		for url in urls:
			tree_tuple=[]
			tree_tuple.append(domain)
			tree_tuple.append(tcp_stream)
			tree_tuple.append(url)
			tree.append(tree_tuple)
		tcp_stream+=1
download_tree['tree']=tree

object_id=0
urlToId={}
object_tree={}
objectTree=[]
for new_object in objects:
	urlToId[new_object['url']]=object_id
	object_id+=1
for new_object in objects:
	nodeid=urlToId[new_object['url']]
	parentid=urlToId[new_object['referer']]
	nodeTuple=[]
	nodeTuple.append(nodeid)
	nodeTuple.append(new_object['url'])
	nodeTuple.append(parentid)
	objectTree.append(nodeTuple)
object_tree['tree']=objectTree



json.dump(download_tree,open('download_tree.txt','w'))
json.dump(object_tree,open('object_tree.txt','w'))

