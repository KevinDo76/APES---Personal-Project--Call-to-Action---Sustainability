import os
def csvParse(fileName):
  #homemade csv parser
  file = open(fileName,"r")
  csvDict=[]
  #reading header  
  header=file.readline()
  header=(header[:-1]).split(",")

  while (1):
    data=file.readline()[:-1]
    if (data==""):
      break
    data=data.split(",")
    dataI=0
    csvDict.append({})
    for i in header:
      csvDict[len(csvDict)-1][i]=float(data[dataI])
      dataI+=1
    if (len(csvDict)%10==0):
      print(len(csvDict))
  print(len(csvDict))
  file.close()
  return csvDict,header
    
def writeCSV(fileName,headerDict,bodyDict):
  finalOutText=""
  finalOutText+=",".join(headerDict)+"\n"
  for record in bodyDict:
    tempRecord=""
    for field in record:
      tempRecord+=str(record[field])+","
    finalOutText+=tempRecord[:-1]+'\n'
  print(os.getcwd())
  csvFile=open(os.getcwd()+"/"+fileName,"w")
  csvFile.write(finalOutText)
  csvFile.close()
  

def main():
  parsed, header=csvParse("output.csv")
  print((parsed[0]["epochTime"]+parsed[1]["epochTime"])/2)
  ShrinkedData=[]
  if len(parsed)%2!=0:
    print("bro i can't be ask to handle non-even data set. It's too annoying")
  else:
    for i in range(int(len(parsed)/2)):
      fobj = parsed[i*2]
      sobj = parsed[i*2+1]
      ShrinkedData.append({})
      for field in fobj:
        if field!="ID":
          ShrinkedData[i][field]=(fobj[field]+sobj[field])/2
        else:
          ShrinkedData[i]["ID"]=i   
    print(len(parsed),len(ShrinkedData))
    writeCSV("output.csv",header,ShrinkedData)
if __name__ == "__main__":
  main()