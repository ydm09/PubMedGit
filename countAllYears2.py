# -*- coding: UTF-8 -*-  
import os
import csv

def countAllYears(filePath):
	pmidCount,titleCount,absCount,meshCount,keyCount,errorCount = 0,0,0,0,0,0
	# 按行读取，计算每年的文章、标题、摘要、mech词、关键词的数量
	with open(filePath, 'r' ) as f:
		for line in f.readlines() :
			line = line.strip('\n')
			str = line.split('|')
			if( len(str) != 5):
				print(len(str))
				print(line)
				errorCount +=1 
				continue
			# 文件中每一行为一篇文章，第一列是pmid ，第二列为title，第三列为abstract,第四列为mesh词，第五列为keyword
			if ( str[0] != " ") :
				pmidCount += 1
			if ( str[1] != " ") :
				titleCount += 1
			if ( str[2] != " ") :
				absCount += 1
			if ( str[3] != " ") :
				meshCount += 1
			if ( str[4] != " ") :
				keyCount += 1
	# 每列代表的含义依次为年份，该年份的文章数量，标题数量，摘要数量，mech词、关键词的数量
	str=[filePath[-8:-4],pmidCount,titleCount,absCount,meshCount,keyCount,errorCount]							
	return str

# 写入列名,
countFile = open('pubmedAllFiles//countAllYears.csv','wb') #w,覆盖写入 设置newline，否则两行之间会空一行
writer = csv.writer(countFile)
writer.writerow(["year","pmidCount","titleCount","absCount","meshCount","keyCount","errorCount"])

#读取文件夹下文件，
path = "pubmedAllFiles//resultYear" #文件夹目录
files = os.listdir(path) #得到文件夹下的所有文件名称  
for file in files : #遍历文件夹  
	filePath = path + "//" + file
	print(filePath)
	writer.writerow(countAllYears(filePath)) # 每篇文章写一行
countFile.close()
print("END")





