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
  parsed1, header1=csvParse("log-hungry.csv")
  parsed2, header2=csvParse("log-sustain.csv")
  combineField="CPUFan(RPM)"
  combinedData=[]
  print(max(len(parsed1),len(parsed2)))
  lparsed1 = len(parsed1)
  lparsed2 = len(parsed2)
  for record in range(max(lparsed1,lparsed2)):
    combinedData.append({})

    combinedData[record]["ID"]=record

    if record%100==0:
        print(record)
    
    if record < lparsed1:
      combinedData[record][f"{combineField}hungry"]=parsed1[record][combineField]
    else:
      combinedData[record][f"{combineField}hungry"]="no data"

    if record < lparsed2:
      combinedData[record][f"{combineField}sustain"]=parsed2[record][combineField]
    else:
      combinedData[record][f"{combineField}sustain"]="no data"
    
  writeCSV("output.csv",["ID",f"{combineField}hungry",f"{combineField}sustain"],combinedData)
if __name__ == "__main__":
  main()