import os

temp_head='<!DOCTYPE html><html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><title>tomasz stecko</title><meta charset="UTF-8&gt;&lt;meta name=" viewport"="" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" type="text/css" href="../style/style2.css"></head>'
temp_header='<body><header><b><a href="index.html">tomasz stecko</a></b></header>'
temp_footer='<hr><footer><a href="http://webring.xxiivv.com/#" target="_blank">webring</a> * <a href="https://merveilles.town/@tomasteck">mastodon</a> * <a href="https://twitter.com/turelio">twitter</a><br><i>2016-2020</i></footer></body></html>'
nav_default ='index.html now.html projects.html logs.html personal.html about.html'

def get_pagelist():
	return os.listdir('src/')

def get_title(source):
	return source[source.index('<h1>')+len('<h1>'):source.index('</h1>')]

def get_parent(source):
	return source[source.index('<!--')+len('<!--'):source.index('-->')]

def build_head(source_str):
	return '<!DOCTYPE html><html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><title>'+get_title(source_str)+'</title><meta charset="UTF-8&gt;&lt;meta name=" viewport"="" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" type="text/css" href="../style/style2.css"></head>'	
	
def build_navlist(source):
	list1 = ['<nav><p><a href="now.html">now</a>  <a href="projects.html">projects</a> <a href="logs.html">logs</a> <a href="personal.html">personal</a> <a href="about.html">about</a> </p><p>']
	for i in get_pagelist():
		if get_parent(build_main(i))==get_parent(build_main(source)):
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

def build_page(source):
	temp_main=build_main(source)
	temp_head=build_head(temp_main)
	temp_nav=build_navlist(source)
	return(temp_head+temp_header+temp_nav+temp_main+temp_footer)

def write_tofile(source, filename):
	f = open("site/"+filename, "w")
	f.write(source)
	f.close()

def build_directory_src():
	list1 = ['<!--about.html--><h1>Directory</h1><ul>']
	for i in get_pagelist():
		list1.append('<li><a href="'+i+'">'+get_title(build_main(i))+'</a></li>')
	list1.append('</ul>')
	slist = ''.join(list1)
	f = open("src/directory.html", "w")
	f.write(slist)
	f.close()	

def build_all(list1):
	build_directory_src()
	for i in list1: 
		write_tofile(build_page(i), i)


# build all pages
build_all(get_pagelist())
