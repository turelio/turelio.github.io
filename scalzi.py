#!/usr/bin/env python3
from datetime import datetime

# returns scalzi list as line-by-line list
def get_db(source):
	with open(source) as f:
		db = f.read().splitlines() 
	return db

# returns database as 2d list with id names: date, hour, cat, sub, project, title, desc
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


# draws simple html table from database
def draw_table(data):
	table = '<table><tr><th>Date</th><th>Time spent</th><th>Categories</a></th><th>Project</a></th><th>Info</th></tr>'
	for i in data:
		row = '<tr><td>'+str(i['date'])+'</td><td>'+i['hour']+'h</td><td>'+i['cat']+'<br>'+i['sub']+'</td><td>'+i['project']+'</td><td>'+i['title']+'<br>'+i['desc']+'</td></tr>'
		table = table+row
	table = table+'</table>'
	return table


# returns total hours in database
def count_hours(data):
	total=0
	for i in data:
		total+=eval(i['hour'])
	return total

# filter database by specified column id
def filter_db(data, column, string=''):
	newdata = []
	for i in data:
		if i[column] == string:
			newdata.append(i)
	return newdata

# input must be total data
def filter_year(data, year):
	newdata = []
	for i in data:
		if str(i['date'])[0 : 4] == str(year):
			newdata.append(i)
	return newdata

# input must be yearly data
def filter_month(data, month):
	newdata = []
	for i in data:
		if str(i['date'])[5 : 7] == str(month):
			newdata.append(i)
	return newdata


# returns a list of unique values in specified column - all categories, subcategories, project names etc.
def get_unique_values(data, column):
	value_list = []
	for i in data:
		value_list.append(i[column])
	return sorted(set(value_list))

# small summary table - last/first log, total number of logs, total hours, hours by category
def draw_summary(data):
	summary="<table style='width: 500px;'><tr><td>last log</td><td>first log</td><td>total logs</td><td>total hours</td><td style = 'background-color:#6fa8dc'>DATA</td><td style = 'background-color:#ffd966'>RESR</td><td style = 'background-color:#e06666'>CREA</td><td style = 'background-color:#93c47d'>PHYS</td></tr><tr><td>"+str(max(get_unique_values(data, 'date')))+"</td><td>"+str(min(get_unique_values(data, 'date')))+"</td><td>"+str(len(data))+"</td><td>"+str(count_hours(data))+"h</td><td>"+str(count_hours(filter_db(data, 'cat', 'DATA')))+"h</td><td>"+str(count_hours(filter_db(data, 'cat', 'RESR')))+"h</td><td>"+str(count_hours(filter_db(data, 'cat', 'CREA')))+"h</td><td>"+str(count_hours(filter_db(data, 'cat', 'PHYS')))+"h</td></tr></table>"
	return summary

# returns a list of total hours by column, sorted descending
def get_hours(data, column):
	stats = dict()
	stats['total'] = count_hours(data)
	column_list = get_unique_values(data, column)
	for i in column_list:
		stats[i] = count_hours(filter_db(data, column, i))
	return sorted(stats.items(), key=lambda x: x[1], reverse=True)  

# same as above, but list. column can be project- sub- or cat-
def draw_hour_list(stats, column=''):
	lista='<ul style="columns: 2">'
	for i in stats:
		 lista+='<li><a href="'+column+str(i[0]).lower()+'.html">'+str(i[0])+'</a>	- '+str(i[1])+'h</li>'
	lista+='</ul>'
	return lista

# glossary database for expand function
def get_glossary():
	with open('glossary.txt') as f:
		db = f.read().splitlines()
	for i in range(len(db)):
		db[i] = db[i].split('-')
	return db

# expands acronyms if they're found in glossary.txt 
def expand(word):
	for i in get_glossary():
		if i[0]==word:
			return i[1]
	else:
		return word

# TEMPLATES

def temp_header():
	header = '<!DOCTYPE html><html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><title>scalzi</title><meta charset="UTF-8&gt;&lt;meta name=" viewport"="" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" type="text/css" href="../style/style1.css"></head><body><p>by <a href="date.html">date</a> - <a href="cat.html">category</a> - <a href="sub.html">subcategory</a> - <a href="project.html">project</a></p><hr>'
	return header

def temp_date_nav():
	nav=''
	year_end=datetime.today().strftime('%Y')
	month_end=datetime.today().strftime('%m')
	log_end = (year_end)+str(month_end)
	log_start = '201707'
	list_year = ['2021', '2020', '2019', '2018', '2017']
	list_month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
	for i in list_year:
		nav+='<p><a href="date-'+i+'.html">'+i+'</a> ( '
		for j in list_month:
			if int(i+j)<= int(log_end) and int(i+j)>=int(log_start):
				nav+='<a href="date-'+i+'-'+j+'.html">'+j+'</a> '
		nav+=')</p>'
	nav += '<hr>'
	return nav

# NEW BUILD FUNCTIONS

# inputs body sourcecode, writes to file
def build_page(body_code, title):
	html_code = temp_header()
	html_code += body_code
	html_code += '</body></html>'
	f = open("scalzi/"+title+".html", "w")
	f.write(html_code)
	f.close()

# Project pages

def build_page_project_summary(data):
	list = '<h1>Projects</h1>'
	list += draw_hour_list(get_hours(data, 'project'), 'project-')
	build_page(list, 'project')

def build_page_project(data, title):
	list1 = "<h1>"+str(title)+"</h1>"
	catlist = draw_hour_list(get_hours(data, 'cat'), 'cat-')
	sublist = draw_hour_list(get_hours(data, 'sub'), 'sub-')
	list1+= '<h2>Categories</h2><p>'+catlist+'</p>'
	list1+= '<h2>Subcategories</h2><p>'+sublist+'</p>'
	list1+= draw_table(data)
	prefix='project-'+title
	build_page(list1, prefix)

def build_page_project_all(data):
	projectlist = get_hours(data, 'project')
	for i in projectlist:
		build_page_project(filter_db(data, 'project', i[0]), i[0])

# Subcategory pages

def build_page_sub_summary(data):
	list = '<h1>Subcategories</h1>'
	list += draw_hour_list(get_hours(data, 'sub'), 'sub-')
	build_page(list, 'sub')


def build_page_sub(data, title):
	list1 = "<h1>"+str(title)+"</h1>"
	catlist = draw_hour_list(get_hours(data, 'cat'), 'cat-')
	projectlist = draw_hour_list(get_hours(data, 'project'), 'project-')
	list1+= '<h2>Projects</h2><p>'+projectlist+'</p>'
	list1+= '<h2>Categories</h2><p>'+catlist+'</p>'
	list1+= draw_table(data)
	prefix='sub-'+title.lower()
	build_page(list1, prefix)

def build_page_sub_all(data):
	projectlist = get_hours(data, 'sub')
	for i in projectlist:
		build_page_sub(filter_db(data, 'sub', i[0]), i[0])

# Build category page

def build_page_cat_summary(data):
	list = '<h1>Categories</h1>'
	list += draw_hour_list(get_hours(data, 'cat'), 'cat-')
	build_page(list, 'cat')

# Build date pages
def build_page_date_summary(data):
	list1 = temp_date_nav()
	list1 += '<h1>All time</h1>'
	catlist = draw_hour_list(get_hours(data, 'cat'), 'cat-')
	sublist = draw_hour_list(get_hours(data, 'sub'), 'sub-')
	projectlist = draw_hour_list(get_hours(data, 'project'), 'project-')
	list1+= '<h2>Projects</h2><p>'+projectlist+'</p>'
	list1+= '<h2>Categories</h2><p>'+catlist+'</p>'
	list1+= '<h2>Subcategories</h2><p>'+sublist+'</p>'
	list1+= draw_table(data)
	build_page(list1, 'date')

def build_page_date(data, title):
	list1 = temp_date_nav()
	list1 += "<h1>"+str(title)+"</h1>"
	catlist = draw_hour_list(get_hours(data, 'cat'), 'cat-')
	sublist = draw_hour_list(get_hours(data, 'sub'), 'sub-')
	projectlist = draw_hour_list(get_hours(data, 'project'), 'project-')
	list1+= '<h2>Projects</h2><p>'+projectlist+'</p>'
	list1+= '<h2>Categories</h2><p>'+catlist+'</p>'
	list1+= '<h2>Subcategories</h2><p>'+sublist+'</p>'
	list1+= draw_table(data)
	prefix='date-'+title
	build_page(list1, prefix)

def build_page_date_all(data):
	list_year = [2017, 2018, 2019, 2020, 2021]
	list_month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
	for i in list_year:
		data_year=filter_year(data, i)
		build_page_date(data_year, str(i))
		for j in list_month:
			data_month=filter_month(data_year, j)
			month_title = str(i)+'-'+str(j)
			build_page_date(data_month, month_title)
# commands, do not use

data1 = parse_db(get_db("scalzi_source.txt"))

build_page_project_summary(data1)
build_page_sub_summary(data1)
build_page_cat_summary(data1)
build_page_date_summary(data1)
build_page_project_all(data1)
build_page_sub_all(data1)
build_page_date_all(data1)


#
# old version of building pages
# build_yearly_page(data1, "date")
# build_yearly_page(filter_year(data1, 2020), "2020")
# build_yearly_page(filter_year(data1, 2019), "2019")
# build_yearly_page(filter_year(data1, 2018), "2018")
# build_yearly_page(filter_year(data1, 2017), "2017")
# build_cat_page(data1)
# build_subcat_page(data1)
# build_project_page(data1)
# build_all_project_summary(data1)

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

