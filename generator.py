import os

# TEMPLATES

temp_head='<!DOCTYPE html><html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><title>tomasz stecko</title><meta charset="UTF-8&gt;&lt;meta name=" viewport"="" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" type="text/css" href="../style/style2.css"></head>'
temp_header='<body><header><b><a href="index.html">tomasz stecko</a></b></header>'
temp_footer='<hr><footer><a href="http://webring.xxiivv.com/#" target="_blank">webring</a> * <a href="https://merveilles.town/@tomasteck">mastodon</a> * <a href="https://twitter.com/turelio">twitter</a><br><i>2016-2020</i></footer></body></html>'
nav_default ='index.html now.html projects.html logs.html personal.html about.html'

# GET ADDITIONAL INFO

def get_title(source):
	return source[source.index('<h1>')+len('<h1>'):source.index('</h1>')]

def get_parent(source):
	return source[source.index('<!--')+len('<!--'):source.index('-->')]

# GET DATABASE

def get_pagelist():
	return os.listdir('src/')

def get_database(filename):
	data = []
	for i in filename:
		d_main=build_main(i)
		d_title=get_title(d_main)
		d_parent=get_parent(d_main)
		data_entry = dict(link=i, title=d_title, parent=d_parent, main=d_main)
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
	data='<main>'+data+'</main>'
	data = ''.join(data)
	return data


def build_page(data_entry):
	temp_main=data_entry['main']
	temp_head=build_head(data_entry['title'])
	temp_nav=build_navlist(data_entry)
	return(temp_head+temp_header+temp_nav+temp_main+temp_footer)

# BUILD SPECIAL PAGES

def build_directory_src():
	list1 = ['<!--about.html--><h1>Directory</h1><ul>']
	for i in get_pagelist():
		list1.append('<li><a href="'+i+'">'+get_title(build_main(i))+'</a></li>')
	list1.append('</ul>')
	slist = ''.join(list1)
	f = open("src/directory.html", "w")
	f.write(slist)
	f.close()	

# BUILD ALL PAGES

def write_tofile(source, filename):
	f = open("site/"+filename, "w")
	f.write(source)
	f.close()


def build_all(database):
	build_directory_src()
	for i in database: 
		write_tofile(build_page(i), i['link'])


# COMMANDS
build_all(get_database(get_pagelist()))


