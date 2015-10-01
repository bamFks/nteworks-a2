import json
import unicodedata
harfile='nytimes.har'
harFile = open(harfile,"r")
download_tree_file=open('download_tree.txt','r')


fileToString=""
for line in harFile:
	fileToString+=line
stringToJson = json.loads(fileToString)
entries=stringToJson['log']['entries']

fileToString=""
for line in download_tree_file:
	fileToString+=line
download_tree= json.loads(fileToString)['tree']
def intersectinSlots(times):
	max_connection=0
	for time_slot in times:
		for time in time_slot:
			temp_max_connection=0
			for time_slot_2 in times:
				s_comp=comparetime(time_slot_2[0],time)
				e_comp=comparetime(time_slot_2[1],time)
				if s_comp>=0 and e_comp<=0:
					temp_max_connection+=1
			if temp_max_connection>max_connection:
				max_connection=temp_max_connection
	return max_connection

def comparetime(time1,time2):
	if(time1[0]>time2[0]):
		return  -1
	if(time1[0]<time2[0]):
		return 	1

	if(time1[1]>time2[1]):
		return -1
	if(time1[1]<time2[1]):
		return 1

	if(time1[2]>time2[2]):
		return  -1
	if(time1[2]<time2[2]):
		return 1


	if(time1[3]>time2[3]):
		return -1
	if(time1[3]<time2[3]):
		return 1

	return 0

url_check=[]
domain_tcp_timings={}
domain_max_connection={}
for entry in entries:
	url=unicodedata.normalize('NFKD', entry['request']['url']).encode('ascii','ignore')
	if url not in url_check:
		url_check.append(url)
		domain=''
		for header in entry['request']['headers']:
			if(header['name']=='Host'):
				domain=unicodedata.normalize('NFKD', header['value']).encode('ascii','ignore')
		start_time=unicodedata.normalize('NFKD', entry['startedDateTime']).encode('ascii','ignore').split('T')[1].split('+')[0]
		start_time_hour=int (start_time.split(':')[0])
		start_time_min=int(start_time.split(':')[1])
		start_time_sec=int (start_time.split(':')[2].split('.')[0])
		start_time_msec=int (start_time.split(':')[2].split('.')[1])

		blocked_time=entry['timings']['blocked']
		wait_time=entry['timings']['wait']
		dns_time=entry['timings']['dns']
		connect_time=entry['timings']['connect']
		send_time=entry['timings']['send']
		recieve_time=entry['timings']['receive']
		total_time=blocked_time+wait_time+dns_time+connect_time+send_time+recieve_time
	 
		end_time_msec=(start_time_msec+total_time)%1000
		end_time_sec=((start_time_msec+total_time)/1000 + start_time_sec) %60
		end_time_min=(((start_time_msec+total_time)/1000 + start_time_sec)/60+start_time_min)%60
		end_time_hour=((((start_time_msec+total_time)/1000 + start_time_sec)/60+start_time_min)/60 + start_time_hour)

		stime=[start_time_hour,start_time_min,start_time_sec,start_time_msec]
		etime=[end_time_hour,end_time_min,end_time_sec,end_time_msec]

		for node_tuple in download_tree:
			url_from_tree=unicodedata.normalize('NFKD', node_tuple[2]).encode('ascii','ignore')
			if url_from_tree==url:
				domain_from_tree=unicodedata.normalize('NFKD', node_tuple[0]).encode('ascii','ignore')
				connid_from_tree=node_tuple[1]
				if domain_from_tree not in domain_tcp_timings:
					domain_tcp_timings[domain_from_tree]={}
					domain_tcp_timings[domain_from_tree][connid_from_tree]=[stime,etime]

				else:
					if connid_from_tree not in domain_tcp_timings[domain_from_tree]:
						domain_tcp_timings[domain_from_tree][connid_from_tree]=[stime,etime]
					else:
						prevstime=domain_tcp_timings[domain_from_tree][connid_from_tree][0]
						prevetime=domain_tcp_timings[domain_from_tree][connid_from_tree][1]
						if comparetime(prevstime,stime)==-1:
							domain_tcp_timings[domain_from_tree][connid_from_tree][0]=stime
						if comparetime(prevetime,etime)==1:
							domain_tcp_timings[domain_from_tree][connid_from_tree][1]=etime

# print domain_tcp_timings
all_slot=[]
File = open('browser_scheduling.txt',"w")
for domain in domain_tcp_timings:
	print len(domain_tcp_timings[domain])
	times=[]
	for connId in domain_tcp_timings[domain]:
		times.append(domain_tcp_timings[domain][connId])
		all_slot.append(domain_tcp_timings[domain][connId])
	max_count=intersectinSlots(times)
	domain_max_connection[domain]=max_count
	File.write(domain + ' : '+str(max_count)+'\n')
File.write('maximum simultaneous connection from browser is : '+str(intersectinSlots(all_slot)))
