#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import re

# current work directory
curr_path = os.getcwd()

# the pattern string to verify the file name format
pattern = re.compile(r'^(SU-TETM-)([A-Z])(\d{5}-\d{2}-)(?P<id>\d{4})(-[A-Z]-\d{3}-\d{4}-\d{2}-\d{2}-\d{2}-\d{2})')

'''
Load the raw data files
'''
def loadFiles():
	files_list = []

	# list all files in the path defined by 'cwd'
	for file in os.listdir(curr_path):
		if os.path.isdir(file) == False:
			# file name without extension
			file_name = os.path.splitext(file)[0]
			# file extension
			ext = os.path.splitext(file)[1]
			# check the extension of the file
			if ext == '.dat':
				#check if the file name matches the rule
				m = pattern.match(file_name)
				if m is not None:
					# create new file name
					new_file_name = '{0}0{1}-0{2}-S01{3}.dat'.format(m.group(1) + m.group(3), m.group(4)[0:2], m.group(4)[2:4], m.group(5))

					files_list.append([file, new_file_name])

	return files_list

def format(old_file, h_new_file):
	# open the file to be formated
	with open(old_file, 'r') as h_fread:
		# read each line in the file
		while True:
			line = h_fread.readline()
			if not line: # EOF
				break
			else:
				if line.startswith('Wavelength (nm)'):
					# this is the line needed to be formated
					h_new_file.write('Wavelength (nm)\tCH01_TE\tCH01_TM\tCH02_TE\tCH02_TM\tCH03_TE\tCH03_TM\tCH04_TE\tCH04_TM\t\n')
				else:
					# append the other lines to the new file directly
					h_new_file.write(line)


if __name__ == '__main__':
	# get the dat files in the folder
	print('Loading raw data files ...')
	old_files_list = loadFiles()

	# create a new folder named by current datetime
	# the format of the folder name should be 'formated_yyyyMMddHHMMSS'
	ext_folder = os.path.join(curr_path, 'formated_{0}'.format(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))))
	# check if the folder exists or create it
	if os.path.exists(ext_folder) == False:
		os.makedirs(ext_folder)

	print('Export folder %s has been created !' % ext_folder)

	for file in old_files_list:
		old_file = os.path.join(curr_path, file[0])
		new_file = os.path.join(ext_folder, file[1])

		# create a new file to save the formated content
		print('Reformating %s ...' % old_file)
		with open(new_file, 'w') as h_fwrite:
			# format each file
			format(old_file, h_fwrite)

			# save the file to the new folder named by ext_folder
			h_fwrite.close()

		print('%s created !' % new_file)

	print('Done !')



