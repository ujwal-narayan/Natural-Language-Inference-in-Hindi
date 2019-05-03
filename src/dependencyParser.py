from __future__ import unicode_literals
from isc_parser import Parser
import io
parser = Parser(lang='hin')
f = open("hindi.csv")
data = readlines()
splitData = []
for line in data:
    x = line.dplit(',')
    splitData.append(x)
f = io.open("s1_dp.txt", mode="w", encoding="utf-8")
for i in range(1,len(splitData)):
    text = splitData[i][6]
    u = unicode(text, "utf-8")
    text = u
    text = text.split()
    tree =parser.parse(text)
    f.write("Sentence:\n")
    f.write('\n'.join(['\t'.join(node) for node in tree]))
    f.write("\n")

    
f = io.open("s2_dp.txt", mode="w", encoding="utf-8")
for i in range(1,len(splitData)):
    text = splitData[i][7]
    u = unicode(text, "utf-8")
    text = u
    text = text.split()
    tree =parser.parse(text)
    f.write("Sentence:\n")
    f.write('\n'.join(['\t'.join(node) for node in tree]))
    f.write("\n")

    

