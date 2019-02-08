import requests
import urllib.request
import bs4 as bs #sudo apt-get install python3-bs4
import os.path
import csv
import time

URL = 'https://developers.google.com/android/images'
titlesIndex = 2
fname = "output.csv"
strHtml = ""
listCsv  =[]
listHtml =[]
downloadImage = False


    

def updateCSV():
    global listHtml
    global listCsv
    csvUpdate = []
    updateFound = False
    title = ""
    listCsvLen = len(listCsv)
    listHtmlLen = len(listHtml)
    for i in range(listHtmlLen):
        if len(listHtml[i]) == 3 :
            for j in range(listCsvLen):
                if len(listCsv[j]) == 3:
                    if(str(listCsv[j][2]) ==  str(listHtml[i][2])):
                        csvUpdate.append(listCsv[j])
                        break
                    if j == listCsvLen -1:
                        updateFound = True
                        csvUpdate.append(listCsv[j])
                        csvUpdate.append(listHtml[i])
                        print(".............update found.............")
                        print("SHA-256: "+listHtml[i][2])
                        
        else:           
            title = listHtml[i]
            #print(title)
            csvUpdate.append(title)
    if updateFound:
        creatCsvFile(csvUpdate)
    else:
        print(".............update not found.............")


def creatCsvFile(data):
    fw = open(fname,"w")
    fw.write("Version,Link,SHA-256 Checksum"+"\n")
    #get the data from the web and write to csv file       
    for i in range(len(data)):
        if len(data[i]) == 3:
            fw.write(data[i][0]+","+data[i][1]+","+data[i][2]+"\n")
        else:
            fw.write(str(data[i])+"\n")
    #print(strHtml)
    fw.close


def downloadFiles():
    global listCsv
    for row in listCsv:
        if len(row) ==3:
            link = row[1]
            #print(link)
            fileNmae = link.replace("https://dl.google.com/dl/android/aosp/","")
            if os.path.isfile("images"):
                os.mkdir("images")
            if not os.path.isfile("images/"+fileNmae):
                urllib.request.urlretrieve(link,"images/"+fileNmae)  

def fileExists():
    global listCsv
    fr = open(fname,"r")
    fcsv = csv.reader(fr,delimiter=",")
    for row in fcsv:
        listCsv.append(row)
    fr.close
    listCsv = listCsv[1:]


def main():
    global strHtml
    global listHtml
    global downloadImage
    #countDown()
    downImage = input("download images?(y/n): ")
    if downImage == "y" or downImage == "Y":
        downloadImage = True
    
    
    
    #global listHtml
    #get the html code from the url
    sauce = urllib.request.urlopen(URL).read()
    soup = bs.BeautifulSoup(sauce,'lxml')
    div = soup.select('div')
    tableLen = len(div)
    tableTitles = soup.select('div')[0].find_all('h2')[titlesIndex:tableLen+titlesIndex]



    for i in range(len(tableTitles)):
        titles = tableTitles[i].string.replace('"',"").replace(","," ")
        #print(titles)
        strHtml += titles+ "\n"
        listHtml.append(titles)  
        table = div[0].find_all("table")
        #split the data in the table 
        splitTable = table[i].text.split("\n\n")
        splitTable = splitTable[2:]
        for j in range(len(splitTable)-1):
            allData = splitTable[j].split("\n")[1:]
            allData[1] = table[i].find_all('tr')[j].a.get("href") 
            allData[0] = allData[0].replace(","," ")
            #print(allData[0]+","+allData[1]+","+allData[2])
            strHtml += allData[0]+","+allData[1]+","+allData[2]+"\n"
            listHtml.append([allData[0],allData[1],allData[2]])

    if not os.path.isfile(fname):     
        print("create csv file: "+fname)
        creatCsvFile(listHtml)

    else:#if file exists
        print(".............searching for updates.............")
        fileExists()#adding data to list from csv file
        updateCSV()

    if downloadImage:
        downloadFiles()


if __name__ == "__main__":
    main()