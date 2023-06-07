import subprocess
import time
import os
import clr
import math

clr.AddReference(r'C:\Users\Owner\Desktop\Pythonstuff\powerReader\OpenHardwareMonitorLib.dll') 

from OpenHardwareMonitor.Hardware import Computer


def float_check(n):
    try:
        float(n)
        return True
    except ValueError:
        return False

def getGPUPowerDataNumber(value,category=None):
    if category==None:
        nvsmioutput=subprocess.run(["nvidia-smi","--query"], text=True, stdout=subprocess.PIPE)
    else:
        nvsmioutput=subprocess.run(["nvidia-smi","--query",f"--display={category}"], text=True, stdout=subprocess.PIPE)
    linebreaked=(nvsmioutput.stdout).split("\n")
    for i in linebreaked:
        if " "+value.lower()+"  " in i.lower():
            seperated1=i.split(":")
            seperated1[1]=seperated1[1][1:]
            for ii in range(50):
                if not float_check(seperated1[1]):
                    seperated1[1]=seperated1[1][:-1]
                else:
                    return float(seperated1[1])
            break
    return False
    
def writeLog(fileLocation,folder,data):
    log=open(folder+"\\"+fileLocation,"a")
    log.write(data)
    log.close()


def main():
    startTime=time.time()
    iteration=0
    waitTime=1
    folderLocation=r"C:\Users\Owner\Desktop\Pythonstuff\powerReader\LogDataSustainPower"
    fileLocation=f"log-{math.floor(startTime)}.csv"
    detectionmessage=True
    #csv header
    writeLog(fileLocation,folderLocation,"ID,epochTime,GPUPower(Watt),GPUTemp(c),GPUFan Speed(%),CPUCorePower(Watt),CPUPackagePower(Watt),CPUFan(RPM),GeneralFans(RPM),AvgCoreTemp(c)\n")
    c = Computer()
    c.CPUEnabled = True # get the Info about CPU
    c.MainboardEnabled = True
    c.Open()
    while (1):
        #time sync keeper
        while (1):
            time.sleep(0.001)
            if time.time()>=startTime+(iteration*waitTime):
                iteration+=1
                break
        #timestamp
        c.Hardware[0].Update()
        c.Hardware[1].Update()
        logTime=time.time()
        #GPU data record
        powerDraw=getGPUPowerDataNumber("power draw","power")
        temperature=getGPUPowerDataNumber("GPU Current Temp","temperature")
        fanSpeed=getGPUPowerDataNumber("fan speed")
        #CPU data record
        tempAvg=0
        tempSenCount=0
        PackagePower=0
        IACorePower=0
        CPUFan=0
        Fans=0
        for hardwareI in range(2):
            if (str(c.Hardware[hardwareI].HardwareType)=="CPU"):
                if detectionmessage:
                    print("CPU DETECTED")
                for a in range(0, len(c.Hardware[hardwareI].Sensors)):
                    if "/power/0" in str(c.Hardware[hardwareI].Sensors[a].Identifier):
                        PackagePower=float(c.Hardware[hardwareI].Sensors[a].get_Value())
                    elif "/power/1" in str(c.Hardware[hardwareI].Sensors[a].Identifier):
                        IACorePower=float(c.Hardware[hardwareI].Sensors[a].get_Value())
                    elif "/temperature" in str(c.Hardware[hardwareI].Sensors[a].Identifier):
                        tempSenCount+=1
                        tempAvg+=float(c.Hardware[hardwareI].Sensors[a].get_Value())
            if (str(c.Hardware[hardwareI].HardwareType)=="Mainboard"):
                if detectionmessage:
                    print("MOTHERBOARDDETECTED")
                for subHardwareI in range(0, len(c.Hardware[hardwareI].SubHardware)):
                    c.Hardware[hardwareI].SubHardware[subHardwareI].Update()
                    for SensorI in range(0, len(c.Hardware[hardwareI].SubHardware[subHardwareI].Sensors)):
                        if "/fan/0" in str(c.Hardware[hardwareI].SubHardware[subHardwareI].Sensors[SensorI].Identifier):
                            CPUFan=float(c.Hardware[hardwareI].SubHardware[subHardwareI].Sensors[SensorI].get_Value())
                        elif "/fan/2" in str(c.Hardware[hardwareI].SubHardware[subHardwareI].Sensors[SensorI].Identifier):
                            Fans=float(c.Hardware[hardwareI].SubHardware[subHardwareI].Sensors[SensorI].get_Value())
        
        detectionmessage=False
        tempAvg/=tempSenCount
        output=str(iteration)+","+str(logTime)+","+str(powerDraw)+","+str(temperature)+","+str(fanSpeed)+","+str(IACorePower)+","+str(PackagePower)+","+str(CPUFan)+","+str(Fans)+","+str(tempAvg)
        print(output)
        writeLog(fileLocation,folderLocation,output+"\n")

        
    



if __name__=="__main__":
    main()
    
