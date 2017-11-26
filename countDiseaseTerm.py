# -*- coding: UTF-8 -*-  
import os
import csv
import copy
import pandas as pd
import nltk
import nltk.data  

# 判断文本中是否含有真的情感
def hasReallySentiment(sentimentWord ,content):
	#若文本中没有情感词，则返回false；若文本中有情感词，进一步判断否定词
	if sentimentWord  in nltk.tokenize.word_tokenize(content) : 
		sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')  
		sentences = sent_tokenizer.tokenize(content) #对文本分句 
		# print(sentences)  
		for sentence in sentences:  #遍历句子，判断情感词和否定词是否在句子窗口共现
			if sentimentWord  in nltk.tokenize.word_tokenize(sentence) :
				if ( hasNotWord (sentence) == True ) :
					return False #若否定词在该句出现，python中 true和false的首字符要大写
			else:
				continue
		return True #所有句子中，情感词与否定词都不共现

	else:
		return False 

# 判断句子中是否出现否定词	 	
def hasNotWord ( sentence ) :
	with open('notWord.txt', 'r') as f:
		
		for notWord in f.readlines():
			notWord = notWord.strip('\n') # 去掉行末换行符
			if notWord in sentence.split() :
				return True
			else :
				continue
		return False

# 读取疾病词文件,疾病名词保存为list，每种疾病的主要表达方式保存为字典类型，value设为0
def readDiseaseTerm (keydict,keylist):	
	with open('diseaseWord.txt', 'r',encoding = 'UTF-8') as f:
		
		for line in f.readlines():
			line = line.strip('\n') # 去掉行末换行符
			linelist = line.split('|') #每行表示一种疾病，不同的表述以‘|’分割
			keylist.append(linelist)  
			key = linelist[0]
			keydict[key] = 0
		# print(keylist)

# 判断摘要中是否出现疾病词并计数，即content中是否含有疾病列表keylist中的名词
def countDiseaseTerm(keydict , keylist, content):
	for linelist in keylist :
		for key in linelist : 
			if key in nltk.tokenize.word_tokenize(content) :
				
				keydict[linelist[0] ] +=1 #若出现该种疾病的表述，对应的计数加1

# 所有年份，每一年各种疾病出现的对应次数，写入文件
def writerkeydictTofile (keydict,countlist) :
	fieldnames = [] # 保存列名，每种疾病为一列
	for key in keydict.keys():
		fieldnames.append (key)
	fieldnames.sort()
	fieldnames.remove("year")
	fieldnames.insert(0,'year') # 排序，并使年份在第一列
	# print(fieldnames)
	csvFile = open('countDiseaseTerm.csv','w', newline ='', encoding = 'UTF-8') # 设置newline，否则两行之间会空一行
	dict_writer = csv.DictWriter(csvFile,fieldnames = fieldnames) 
	dict_writer.writeheader() # 写入列名
	dict_writer.writerows(countlist)  #按行写入文件
	csvFile.close()

def main():
	sentimentWord = "amazing"
	keydict = {} 
	keylist = []
	countlist = []
	readDiseaseTerm(keydict,keylist) #获得疾病名词
	
	#读取文件夹下按年份解析之后的文件，
	path = "pubmedAllFiles//resultYear"  #文件夹目录
	files = os.listdir(path) #得到文件夹下的所有文件名称  
	for file in files : #遍历文件夹  
		filePath = path + "//" + file
		print(filePath)
		with open(filePath, 'r' ,encoding = 'UTF-8') as f: #读入一年
			for line in f.readlines() :
				line = line.strip('\n')
				str = line.split('|')
				if( len(str) == 5):
					content = str[1] + "." + str[2] #取出每篇的标题和摘要
				else:
					continue # 异常数据不做处理
				if ( hasReallySentiment(sentimentWord ,content) == True ):
					countDiseaseTerm (keydict , keylist, content) #若该行文本含有情感，则查找是否出现疾病名词并计数
				else:
					continue #不含有情感词则继续下一行

		#一年读取完毕，将该年疾病名词的计数保存到list
		keydict["year"] = filePath[-8:-4]
		countlist.append(copy.copy(keydict))
		# print(countlist)
		
		for key in keydict:
			keydict[key] = 0  #疾病名词的计数归0，开始下一年的计数

	writerkeydictTofile(keydict,countlist) #所有文件读取计数完成，写入新文件
		
	
if __name__ == '__main__':  
	main()
    #为了查看方便，转置为以年份为列
	# df = pd.read_csv('countDiseaseTerm.csv')
	# df_T = df.T #获得转置
	# df_T.to_csv('countDiseaseTermTranspose.csv', header=False)
	print ("end")
	