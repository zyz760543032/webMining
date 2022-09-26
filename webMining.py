import math
import re

def processing():
    dic = {}
    length = {}
    for i in range(1, 4): #依次读取文件
        f = open("d" + str(i) + ".txt", 'r')
        line = f.readline()
        while line: #按行读取
            line = line.strip('\n') #删除换行符
            words = line.split(' ')
            for word in words:
                if re.match("\w*[?.,!]", word): #删除标点符号
                    word = word[:-1]
                word = word.lower()  #大写转换为小写
                if word not in dic.keys():  #建立单词到文件的字典
                    dic[word] = {str(i)}
                    length[word] = 1
                else:
                    length[word] += 1
                    dic[word].add(str(i))
            line = f.readline()
    fw = open("precessedFile.txt", 'w')  #将两个字典写入文件
    for word in dic.keys():
        fw.write(str(word))
        for fileNum in dic[word]:
            fw.write(' '+fileNum)
        fw.write('\r')
    fw.close()

def query():
    dic = {}
    lenList = {}
    fr = open("precessedFile.txt",'r')
    line = fr.readline()
    while line:
        line = line.strip('\n')
        line = line.split(' ')
        word = line[0]  #分别获取单词，长度，文件列表
        for doc in line[1:]: #建立单词到文件，单词到长度的字典
            if word not in dic.keys():
                dic[word] = [doc]
            else:
                dic[word].append(doc)
        line = fr.readline()
    query = input("输入：").lower()  #执行查询操作
    if query not in dic.keys():
        print("没有文件包含这个单词")
    else:
        for fileNum in dic[query]:
            print('d'+fileNum)


def multiQuery(wordList):
    dic = {}
    lenList = {}
    fr = open("precessedFile.txt", 'r')
    line = fr.readline()
    while line:
        line = line.strip('\n')
        line = line.split(' ')
        word = line[0]  # 分别获取单词，长度，文件列表
        length = line[-1]
        line = line[1:-1]
        for doc in line:  # 建立单词到文件，单词到长度的字典
            doc = doc.strip('{},\'')
            if word not in dic.keys():
                dic[word] = [int(doc)]
            else:
                dic[word].append(int(doc))
        dic[word] = sorted(dic[word])
        lenList[word] = length
        line = fr.readline()
    ans = []
    points = []
    for keyWord in wordList:#123 13 12
        if keyWord.lower() not in dic.keys():
           return []
        points.append([keyWord.lower(), 0])
    while(True):
        minDocId = int(dic[points[0][0]][points[0][1]])
        maxDocId = int(dic[points[0][0]][points[0][1]])
        minkey = 0
        for point in range(len(points)):
            curDocId = int(dic[points[point][0]][points[point][1]])
            if(curDocId < minDocId):
                minDocId = curDocId
                minkey = point
            if (curDocId > maxDocId):
                maxDocId = curDocId
        if(minDocId == maxDocId):
            ans.append(minDocId)
        points[minkey][1] += 1
        if points[minkey][1] == len(dic[points[minkey][0]]):
            break
    return ans

def sortQuery():
    global idft
    doc = []
    count = {}
    f = open("doc.txt", 'r')
    line = f.readline()
    while line: #按行读取
        temp = []
        line = line.strip('\n').lower().split() #删除换行符
        docline = []
        for i in range(2,len(line)):
            if re.match("\w*[?.,!]", line[i]): #删除标点符号
                line[i] = line[i][:-1]
            docline.append(line[i])
            if line[i] not in count.keys():
                count[line[i]] = 1
                temp.append(line[i])
            else:
                if line[i] not in temp:
                    count[line[i]] += 1
                    temp.append(line[i])
        doc.append(docline)
        line = f.readline()
    query = "watch the sunset".lower().split()
    score = []
    i = 1
    for document in doc:
        tf = 0
        score1 = 0
        for word in query:
            tftd = 0
            for word1 in document:
                if word1 == word:
                    tftd += 1
            if tftd > 0:
                tf += 1 + math.log10(tftd)
            if word in count.keys():
                idft = math.log10(len(doc)/count[word])
            score1 += tf * idft
        score.append([i, score1])
        i += 1
    score = sorted(score, key=lambda x:x[1],reverse=True)
    for s in score:
        print(s)
processing()
query()

