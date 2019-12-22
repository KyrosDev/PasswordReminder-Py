"""

            Created by KyrosDesign

"""

from Utils.JsonLoader import JsonLoader #My library
from Utils.Secure import Secure #Encryp and Decrypt data file
import os #Os library
import json #Json library
import sys #Sys library
import getpass #Library to hide line

localPasswordsPath = "/tmp/psr" #Path of this file
secure = Secure(localPasswordsPath) #Send path to Secure Class

try:
    os.chdir("/tmp/") #Change directory
    os.mkdir("psr") #Create directory
except FileExistsError as fee:
    pass

inputTemplate = "~$: " #Input template
username = "" #Username initialization

#Function to clear term/console
def clearTerm():
    os.system("clear")

#Initialize JsonLoader library
jsonLoader = JsonLoader(localPasswordsPath)

#If settings.json contain name key set the value at username var
try:
    username = jsonLoader.getNameFromJson() #Use getNameFromJson to set the name
#If settings.json don't contain name key do nothing
except:
    pass #Do nothing

#Get services function
def getService():
    
    print(jsonLoader.takeDataFromJson("messages", "getPin")) #Print message to get the pin

    pinInput = "\n" + username + "@pin" + inputTemplate

    hidePin = getpass.getpass(prompt=pinInput) #Pin input
    
    pin = int(hidePin)

    pinChecker = jsonLoader.checkPin(pin) #Check if pin == to pin of settings.json

    #If pinChecker var return 100 (Pin correct) do this:
    if pinChecker == 100:

        clearTerm() #Clear term/console

        print(jsonLoader.takeDataFromJson("messages", "getServiceMethod")) #Print how to get service methods

        opt = str(int(input("\n" + username + "@option" + inputTemplate))) #Methods selector input

        #If user typed 1 do:
        if opt == "1":

            clearTerm() #Clear term/console
            
            service = str(input("\n" + username + "@service" + inputTemplate)) #Name of the service input

            data = jsonLoader.getPassword(service=service) #Get value of getPasswords at data
            clearTerm() #Clear term/console

            #Check if response of data in index 0 is equal to 102 (service Founded) 
            if data[0] == 102:
                if data[1] == 105: #Idk what it checks but it's working
                    
                    print()
                    print("You're data:\n")

                    #For every respons of data print with this pattern
                    for i in range(len(data[2])):
                        #Pattern
                        print(f"- {1+i}) Service: {service}, Email: {data[2][i][0]}, Password: {data[2][i][1]}")

                    print("\n#----------------------------------------#")

            else:
                print(jsonLoader.sendError(data[0])) #Send error
            
            getStarted() #Callback of main function

        #Check if user typed 2 and do
        elif opt == "2":
            
            email = str(input("\n" + username + "@email" + inputTemplate)) #Email selector

            data = jsonLoader.getPassword(email=email) #Get response of method to data var
            clearTerm() #Clear term/console

            #Check if response in index 0 is equals to 102 (service founded)
            if data[0] == 102:
                if data[1] == 105: #Idk but it's working
                    print()
                    print("You're data:\n")

                    #For every response of data get service name
                    print()
                    for i in range(len(data[2])):
                        for k in data[2][i]: #Get service name
                            #Pattern of message
                            print(f"- {1+i}) Service: {list(data[2][i].keys())[0]}, Email: {data[2][i][k][0]}, Password: {data[2][i][k][1]}") #Message pattern
                    
                    print("\n#----------------------------------------#")
            else:
                print(jsonLoader.sendError(data[0])) #Send error

            getStarted() #Callback to main Function

        #If user typed 3 do:
        elif opt == "3":

            clearTerm() #Clear term/console
        
            data = jsonLoader.getPassword(method="all") #Get response to data var

            #Check if response in index 0 is equals to 102 (service founded)
            if data[0] == 102:
                if data[1] == 105: #Idk what i check, but it's working
                    #For every element in response
                    for i in range(len(data[2])):
                        #For every element in element
                        for k in data[2][i]:
                            #Print pattern
                            print(f"- {1+i})Service: {list(data[2][i].keys())[0]}, Email: {data[2][i][k][0]}, Password: {secure.decryptData(data[2][i][k][1])}") #Message pattern
                    print("\n#----------------------------------------#")
            
            else:
                print(jsonLoader.sendError(data[0])) #Send error

            getStarted() #Callback to main function

        #If user typed something else of 1,2 or 3 return to getService function
        else:
            getService() #Callback get Service function
    
    #If response of pinChecker is equal to 402 (Pin incorrect or invalid)
    elif pinChecker == 402:
        #clearTerm() #Clear term/console
        print(jsonLoader.sendError(pinChecker)) #Print error message
        getService() #Callback to get Service function

#Set service function
def setService():

    service = str(input("\n" + username + "@service" + inputTemplate)) #Set service
    email = str(input(username + "@email" + inputTemplate)) #Set email
    password = str(input(username + "@password" + inputTemplate)) #Set password
        
    setService = jsonLoader.setService(service, email, password) #Set service credentials

    #If response of setService >= of 400 print message
    if (setService >= 400):
        clearTerm() #Clear term/console
        print(jsonLoader.sendError(setService)) #Print mesage
        getStarted() #Callback to mainFunct

    #If response of setService >= of 100 and < of 200 print message 
    elif (setService >= 100 and setService < 200):
        clearTerm() #Clear term/console
        print(jsonLoader.sendError(setService)) #Print message
        getStarted() #Callback main function

#Main function
def getStarted():
    print(jsonLoader.takeDataFromJson('messages', 'getStarted')) #Print message where you can choice the action

    initInput = str(input("\n" + username + inputTemplate)) #Action input

    #If user type register or /register print start register message and callback setService function
    if initInput == "register" or initInput == "/register":
        clearTerm() #Clear term/console
        print("\n"+ jsonLoader.takeDataFromJson('messages','startRegister')) #Print message
        setService() #Callback

    #If user type services or /services clear term and callback getService function
    elif initInput == "services" or initInput == "/services":
        clearTerm() #Clear term/console
        getService() #Callback
    
    #If user type exit or /exit clear term and end the program
    elif initInput == "exit" or "/exit":
        clearTerm() #Clear term
        sys.exit() #End program

    #If user type something else of register services or exit return to getStarted function.
    else:
        clearTerm() #Clear term/console
        getStarted() #Callback

#Program start from here with start message 
print(jsonLoader.takeDataFromJson('messages','startMessage'))

startExecution = str(input("\n" + inputTemplate)) #Input to start program

#Check if user typed start or /start
if startExecution == "start" or startExecution == "/start":

    #Check if jsonLoader.checkFirstExec return True... this mean it's first execution on the pc
    if jsonLoader.checkFristExec() == "true":
        print("\n" + jsonLoader.takeDataFromJson('messSiages','pinInsert')) #Print message to insert a name and a pin
        name = str(input(inputTemplate + "Name: ")) #Name Input
        pin = int(input(inputTemplate + "Pin: ")) #Pin input
        jsonLoader.setPin(pin) #Set pin with pin input
        jsonLoader.setExecution(name, pin) #With this line i set the name, pin and the execution. So firstExec = false beacouse it's started
        print(jsonLoader.takeDataFromJson('messages','credentialSuccesSetted')) #Send message where credentials will be setted correctly
        clearTerm() #Clear terminal console
        username = jsonLoader.getNameFromJson() #Take user name from getNameFromJson method in jsonLoader
        getStarted() #Callback Main Start Function
    #If user is logged on callback getStarted, main Function 
    else:
        clearTerm() #Clear terminal/console
        getStarted() #Callback

#If user type other character close the program
else:
    clearTerm() #Clear terminal/console
    sys.exit() #End program"""
