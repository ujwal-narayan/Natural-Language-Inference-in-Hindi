ctionary format: {Verb1 : {Sense_1:[List of argument types], ..., Sense_n:[]}, ..., Verb_n:{} }
"""

import os

frame_files = os.listdir('.')

dictionary = {}
verb = ''
sid = ''
for file in frame_files:
	#print(file)
	dash_count = 0
	with open(file, 'r') as f:
		for line in f:
			if line == '\n':
				continue
			if 'Verb::' in line:
				dictionary[line.split('::')[1].strip()] = {}
				verb = line.split('::')[1].strip()
			elif 'SID::' in line:
				dictionary[verb][line.split('::')[1].strip()] = []
				sid = line.split('::')[1].strip()
			if dash_count == 2 and '---' not in line and len(line.split()) == 6:
				# print(line)
				dictionary[verb][sid].append(line.split()[0])
				dictionary[verb][sid] = list(set(dictionary[verb][sid]))
			if '---' in line:
				dash_count = (dash_count + 1) % 3
	#print(dictionary)
