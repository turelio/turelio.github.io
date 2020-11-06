#!/usr/bin/env python3
from datetime import datetime

def get_db(source):
	with open(source) as f:
		db = f.read().splitlines() 
	return db

def parse_db(data):
	for i in range(len(data)):
		data2 = data[i].split('-')
		data[i]= dict(date=0, hour=0, cat=0, sub=0, project=0, title='', desc='')
		data[i]['date']=datetime.strptime(data2[0], '%y/%m/%d').date()
		data[i]['hour']=data2[1]
		data[i]['cat']=expand(data2[2])
		data[i]['sub']=expand(data2[3])
		data[i]['project']=expand(data2[4])
		if len(data2)>=6:
			data[i]['title']=data2[5]
		if len(data2)==7:
			data[i]['desc']=data2[6]
	return data

def draw_table(data):
	table = '<table><tr><th>Date</th><th>Hours spent</th><th>Categories</a></th><th>Project</a></th><th>Info</th></tr>'
	for i in data:
		row = '<tr><td>'+i['date']+'</td><td>'+i['hour']+'</td><td>'+i['cat']+'<br>'+i['sub']+'</td><td>'+i['project']+'</td><td>'+i['title']+'<br>'+i['desc']+'</td></tr>'
		table = table+row
	table = table+'</table>'
	return table

def write_tofile(source):
	f = open("scalzitest.html", "w")
	f.write(source)
	f.close()



def count_hours(data):
	total=0
	for i in data:
		total+=eval(i['hour'])
	return total

def filter_db(data, column, string=''):
	newdata = []
	for i in data:
		if i[column] == string:
			newdata.append(i)
	return newdata

def get_unique_values(data, column):
	value_list = []
	for i in data:
		value_list.append(i[column])
	return sorted(set(value_list))

def draw_summary(data):
	summary="<table style='width: 500px;'><tr><td>last log</td><td>first log</td><td>total logs</td><td>total hours</td><td style = 'background-color:#6fa8dc'>DATA</td><td style = 'background-color:#ffd966'>RESR</td><td style = 'background-color:#e06666'>CREA</td><td style = 'background-color:#93c47d'>PHYS</td></tr><tr><td>"+str(max(get_unique_values(data, 'date')))+"</td><td>"+str(min(get_unique_values(data, 'date')))+"</td><td>"+str(len(data))+"</td><td>"+str(count_hours(data))+"h</td><td>"+str(count_hours(filter_db(data, 'cat', 'DATA')))+"h</td><td>"+str(count_hours(filter_db(data, 'cat', 'RESR')))+"h</td><td>"+str(count_hours(filter_db(data, 'cat', 'CREA')))+"h</td><td>"+str(count_hours(filter_db(data, 'cat', 'PHYS')))+"h</td></tr></table>"
	return summary


def get_hours(data, column):
	stats = dict()
	stats['total'] = count_hours(data)
	column_list = get_unique_values(data, column)
	for i in column_list:
		stats[i] = count_hours(filter_db(data, column, i))
	return sorted(stats.items(), key=lambda x: x[1], reverse=True)  

def draw_hour_table(stats, column):
	table='<table style="float: left"><tr><th>'+column+'</th><th>Hours</th></tr>'
	for i in stats:
		 table+='<tr><td>'+str(i[0])+'</td><td>'+str(i[1])+'h</td></tr>'
	table+='</table>'
	return table

def draw_hour_list(stats):
	lista='<ul style="columns: 2">'
	for i in stats:
		 lista+='<li>'+str(i[0])+'	- '+str(i[1])+'h</li>'
	lista+='</ul>'
	return lista

def get_glossary():
	with open('glossary.txt') as f:
		db = f.read().splitlines()
	for i in range(len(db)):
		db[i] = db[i].split('-')
	return db

def expand(word):
	for i in get_glossary():
		if i[0]==word:
			return i[1]
	else:
		return word

# commands, do not use
#data1 = get_db("scalzi_source.txt")
#data2= parse_db(data1)
#projectlist = draw_hour_list(get_hours(data2, 'project'), 'Projects')
#catlist = draw_hour_list(get_hours(data2, 'cat'), 'Categories')
#sublist = draw_hour_list(get_hours(data2, 'sub'), 'Subcategories')
# print(projectlist)
#write_tofile(projectlist+catlist+sublist)
#print(get_glossary())
#print(expand('DATA'))
#print(get_stat2(data2, 'cat'))
#print(get_stat2(data2, 'sub'))
# data_phys = filter_db(data2, 'project', 'rpg')
# write_tofile(draw_summary(data2))

# print(len(data_phys))
# print(count_hours(data_phys))
#print(len(data2))
# print(count_hours(data2))
# TO GET NUMBER OF LOGS IN LIST
# number_of_logs = len(data_phys))

# print(get_unique_values(data2, 'project'))

