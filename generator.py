import os
import scalzi as sc

# TEMPLATES

temp_head='<!DOCTYPE html><html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><title>tomasz stecko</title><meta charset="UTF-8&gt;&lt;meta name=" viewport"="" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" type="text/css" href="../style/style2.css"></head>'
temp_header='<body><header><b><a href="index.html">tomasz stecko</a></b></header>'
temp_footer='<hr><footer><a href="http://webring.xxiivv.com/#" target="_blank">webring</a> * <a href="https://merveilles.town/@tomasteck">mastodon</a> * <a href="https://twitter.com/turelio">twitter</a><br><i>2016-2020</i></footer></body></html>'
nav_default ='index.html now.html projects.html logs.html personal.html about.html'

# GET ADDITIONAL INFO

def get_title(source):
	try:
		return source[source.index('<h1>')+len('<h1>'):source.index('</h1>')]
	except ValueError:
		return 'NOTITLE'
def get_parent(source):
	try:
		return source[source.index('<!--parent:')+len('<!--parent:'):source.index('-->')]
	except ValueError:
		return 'about.html'

def get_scalzi_id(source):
	try:
		return source[source.index('<!--scalzi:')+len('<!--scalzi:'):source.index('_-->')]
	except ValueError:
		return "noentry"


# GET DATABASE

def get_pagelist():
	return os.listdir('src/')

def get_database(filename):
	data = []
	for i in filename:
		d_main=build_main(i)
		d_title=get_title(d_main)
		d_parent=get_parent(d_main)
		d_scalzi_id=get_scalzi_id(d_main)
		data_entry = dict(link=i, title=d_title, parent=d_parent, scalzi_id=d_scalzi_id, main=d_main)
		data.append(data_entry)
	return data

# BUILD HTML PARTS

def build_head(title):
	return '<!DOCTYPE html><html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><title>'+title+'</title><meta charset="UTF-8&gt;&lt;meta name=" viewport"="" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" type="text/css" href="../style/style2.css"></head>'	

# re-add <a href="projects.html">projects</a> <a href="personal.html">personal</a>  later!
def build_navlist(data_entry):
	list1 = ['<nav><p><a href="now.html">now</a> <a href="logs.html">logs</a> <a href="about.html">about</a></p><p>']
	for i in get_pagelist():
		if get_parent(build_main(i))==data_entry['parent']:
			if nav_default.find(i) == -1:
				list1.append('<a href="'+i+'">'+get_title(build_main(i)).lower()+'</a> ')
	list1.append('</p></nav><hr>')
	slist = ''.join(list1)
	return slist

def build_main(source):
	with open("src/"+source, 'r') as file:
		data = file.read().replace('\n', '')
	data='<main>'+data
	data = ''.join(data)
	return data

def build_scalzi_summary(data_entry):
	if data_entry['scalzi_id']=='noentry':
		return '</main>'
	elif str(data_entry['scalzi_id']) in sc.get_unique_values(scalzi_db, 'project'):
		data_aux = sc.filter_db(scalzi_db, 'project', data_entry['scalzi_id'])
		return '<hr><p><i><a href="scalzi.html">scalzi</a> summary for <strong>'+data_entry['scalzi_id']+'</strong>: '+str(sc.count_hours(data_aux))+' hours over '+str(len(data_aux))+' logs, last update '+str(max(sc.get_unique_values(data_aux, 'date')))+'</i></p></main>'
	else:
		return '<hr><p>project id is wrong</p></main>'

def build_page(data_entry):
	temp_main=data_entry['main']
	temp_head=build_head(data_entry['title'])
	temp_nav=build_navlist(data_entry)
	temp_scalzi=str(build_scalzi_summary(data_entry))
	return(temp_head+temp_header+temp_nav+temp_main+temp_scalzi+temp_footer)

# BUILD SPECIAL PAGES

def build_directory_src():
	list1 = ['<!--parent:about.html--><h1>Directory</h1><ul>']
	for i in get_pagelist():
		list1.append('<li><a href="'+i+'">'+get_title(build_main(i))+'</a></li>')
	list1.append('</ul>')
	slist = ''.join(list1)
	f = open("src/directory.html", "w")
	f.write(slist)
	f.close()	

def build_scalzi_src():
	list1 = "<!--parent:logs.html--><!--scalzi:scalzi_--><img src='../media/scalzi-graph.png'><h1>Scalzi</h1><p>Scalzi is a time tracker for productive / creative output. The entries are stored in a simple text file for ease of access:</p><blockquote>date-hours spent-category-subcategory-project-title-description<br>20/10/12-1-RESR-MEM-japanese-anki-grammar revision</blockquote><p>Logs are then parsed so i can extract information and visualize it. Generally i log anything that requires some effort on my part and isn't purely recreational.</p><p>More features to follow as i port them from a spreadsheet (pictured above) that served as a prototype!"
	projectlist = sc.draw_hour_list(sc.get_hours(scalzi_db, 'project'))
	catlist = sc.draw_hour_list(sc.get_hours(scalzi_db, 'cat'))
	sublist = sc.draw_hour_list(sc.get_hours(scalzi_db, 'sub'))
	list1+= '<h2>Projects</h2><p>'+projectlist+'</p>'
	list1+= '<h2>Categories</h2><p>'+catlist+'</p>'
	list1+= '<h2>Subcategories</h2><p>'+sublist+'</p>'
	list1+="<p>Pages that feature projects i track in Scalzi have additional info at the bottom, just like this one:</p>"
	f = open("src/scalzi.html", "w")
	f.write(list1)
	f.close()

# BUILD ALL PAGES

def write_tofile(source, filename):
	f = open("site/"+filename, "w")
	f.write(source)
	f.close()


def build_all(database):
	build_directory_src()
	build_scalzi_src()
	for i in database: 
		write_tofile(build_page(i), i['link'])



# COMMANDS
scalzi_db = sc.parse_db(sc.get_db('scalzi_source.txt'))
build_all(get_database(get_pagelist()))

