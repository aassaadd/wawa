#!/usr/bin/python
#-*coding:utf-8-*-
#Filename:tomcat_stop.py
#Author:zhc
import os
import sys
def get_dir(path):
	print path,'\n'
	return os.listdir(path)

def bak_file(path,path_bak):
	list=os.listdir(path)
	for l in list:
		file_path=os.path.join(path,l)
		file_path_bak=os.path.join(path_bak,l)
		print file_path
		#如果文件路径为目录
		if os.path.isdir(file_path):
			#如果在备份目录中文件夹不存在则创建
			if not os.path.isdir(file_path_bak):
				create_com='''mkdir -p %s''' \
				        %(file_path_bak)
				if os.system(create_com) == 0:
					print create_com
				else:
					print 'create folder failure!'
					#os._exit(0)
			bak_file(file_path,file_path_bak)
		else:
			#如果文件已经存在，则比较文件修改时间
			if os.path.isfile(file_path_bak):
				stat_bak =os.stat(file_path_bak)
				stat_source =os.stat(file_path)
				if stat_source.st_mtime<=stat_bak.st_mtime:
					continue
			cp_com ='''cp '%s' '%s' ''' \
				 %(file_path,file_path_bak)
			if os.system(cp_com)==0:
				print cp_com
			else:
				print 'create folder failure!'
				os._exit(0)

#启动tomcat
tomcat_com='''sh /var/lib/apache-tomcat-7.0.57/bin/shutdown.sh'''
if os.system(tomcat_com) == 0:
	print tomcat_com
else:
	print 'tomcat stop failure!'
	
#要备份的文件目录
path='/var/lib/apache-tomcat-7.0.57/webapps/whp/upload/kindeditor'
#备份文件目录
path_bak='/var/lib/apache-tomcat-7.0.57/webapps/upload_bak/kindeditor'
#备份
bak_file(path, path_bak)	

				