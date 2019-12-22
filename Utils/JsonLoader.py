#Import main library
import json
import os
from Utils.Secure import Secure


class JsonLoader:
    #Init class JsonLoader
    def __init__(self, directory):

        self.file = "settings.json" #Settings file name
        self.data = "data.json" #Data file name
        self.dir = directory #Directory of program
        self.settings = f'{self.dir}/{self.file}' #Directory of settings file
        self.dataJson = f'{self.dir}/{self.data}' #Directory of data file
<<<<<<< HEAD:Utils/JsonLoader.py
        self.secure = Secure(f"{self.dir}") #Send directory at Class
=======
>>>>>>> e5f116eaad1a47a48032fdb81c3e61428178dc18:Models/JsonLoader.py

        if self.file not in os.listdir(self.dir):
            #Write settings file
            with open(self.settings, "w") as settingsFile:
                data = {
                "project": "PasswordRemainder",
                "author": "KyrosDesign",
                "copyright": "2019-2020",
                "program": {
                    "firstExecution": "true"
                },
                "messages": {
                    "returns": {
                    "errors": {
                        "401": "\nEmail already registrated at this service. Retry.",
                        "402": "\nPin invalid or incorrect. Retry.",
                        "403": "\nYou haven't registrated an account on this program.",
                        "404": "\nThat email isn't registrated at this service. Retry.",
                        "406": "\nNo accounts registrated. Start now with register."
                    },
                    "corrects": {
                        "100": "\nPin is correct.",
                        "101": "\nService added correctly.",
                        "102": "\nService Founded.",
                        "104": "\nPin setted correctly."
                    }
                    },
                    "startMessage": "- Hello from PasswordRemainder.\n--> Digit '/start' to init\n--> Digit /exit to end the exectuion.",
                    "pinInsert": "Before start type a name and a pin. (Pin = only integers password)",
                    "credentialSuccesSetted": "\nNice! Now let's start",
                    "getStarted": "\n--- Type '/register' to register new credentials for a determined service\n--- Type '/services' to get password or email from determined registred service\n--- Type '/exit' to cancel execution of the program.",
                    "startRegister": "\n---> Good. Insert required credentials in input fields",
                    "getPin": "\n---> Insert pin to check your identity.",
                    "getServiceMethod": "\n---> Now select one of options with his index.\n\n-- [1] - Get password from service.\n-- [2] - Get password from email.\n-- [3] - Get all registrated services accounts.",
                    "exitMessage": "Have a good day ;D. Remaind the pin!!!"
                },
                "user": {
                    "registred": "false"
                }
                }
                json.dump(data, settingsFile)

        if self.data not in os.listdir(self.dir):
            #Write data file
            with open(self.dataJson, "w") as dataFile:
                data = []
                json.dump(data, dataFile)
        
        #Get pin value from settings file as userPin
        with open(self.settings) as userPin:
            #Transform data in json
            data = json.load(userPin)

            #If user is logged get pin
            if data["user"]["registred"] == "true":
                self.pin = data["user"]["pin"]
            
            else:
                self.pin = None #Set pin to None

    #Set new pin
    def setPin(self, pin):
        self.pin = pin
        return 104 #Return 104 as Pin Setted
    
    #Check if pin is correct
    def checkPin(self, pin):
        if self.pin != pin:
            return 402 #Return 402 as Pin Invalid or Incorrect
        else:
            return 100 #Return 100 as Pin is correct

    #Transform errors code in messages
    def sendError(self, ris):
        with open(self.settings) as settingsFile:
            data = json.load(settingsFile)
            if (int(ris) >= 400):
                return data["messages"]["returns"]["errors"][str(ris)] #Return error message
            elif (int(ris) <= 200):
                return data["messages"]["returns"]["corrects"][str(ris)] #Return success message


    #Take user Name
    def getNameFromJson(self):
        with open(self.settings) as settingsJson:
            value = json.load(settingsJson) #Load json
            return value['user']['name'] #Return the value of key
            settingsJson.close() #Close file

    #Extract data from json and return the value
    def takeDataFromJson(self, mother, key):

        #Open file 'settings.json' as settingsJson
        with open(self.settings) as settingsJson:
            value = json.load(settingsJson) #Load json
            return value[mother][key] #Return the value of key
            settingsJson.close() #Close file

    #Check if program is started for the first time
    def checkFristExec(self):

        #Open file 'settings.json' as settingsJson
        with open(self.settings) as settingsJson:
            value = json.load(settingsJson) #Load all file
            return value['program']['firstExecution'] #Return the value of firstExectution
            settingsJson.close() #Close file

    #Rewrite json with new Params: {name, pin, firstExecution: false}
    def setExecution(self, name, pin):
        #Open file to load the json
        with open(self.settings) as settings:
            jsonSettings = json.load(settings) #Load json
            jsonSettings['program']['firstExecution'] = "false" #Set firstExecution to false

            #Open 'settings.json' to add USER branch as output
            with open(self.settings, 'w') as output:
                jsonSettings['user'] = {"registred": "true","name": name, "pin": pin} #Set name and pin
                json.dump(jsonSettings, output, indent=2) #Rewrite json file
                output.close() #Close file

            settings.close() #Close file

    #Create schema data in json file
    def setService(self, service, email, password):

        password = self.secure.encrpytData(password) #Encrypt password

        isServiceExistent = False

        #Open file to load the json
        with open(self.dataJson) as data:

            jsonData = json.load(data) #Load json
            if type(jsonData) is dict: #Convert jsonData in array
                jsonData = [jsonData]

            #For every line check if SERVICE key contains EMAIL value
            for i in range(len(jsonData)):
                try:
                    if jsonData[i][service]: #If jsonData line I service has email
                        if jsonData[i][service][0] == email:
                            isServiceExistent = True #Set isServiceExistent to True
                            return 401 #Return 401 Already exist
                        else:
                            isServiceExistent = False
                except:
                    pass

            #Check if service not exist
            if not isServiceExistent:
                #Open 'data.json' to add service branch as output
                with open(self.dataJson, 'w') as output:
                    jsonData.append({service: [email,password]}) #Set service with array: email password
                    json.dump(jsonData, output, indent=2) #Rewrite json file

                    output.close() #Close file

                return 101 #Return 101 Service added

            #If isServiceExistent = true return 401
            else:
                return 401 #Return 402 Email already registred at this service
                
            data.close() #Close file

    def getPassword(self, service="", email="", method=""):
        with open(self.dataJson) as data:

            jsonData = json.load(data) #Load json
            if type(jsonData) is dict: #Convert jsonData in array
                jsonData = [jsonData]

            serviceCounter = 0 #counter
            moreServices = [] #services list

            if jsonData == []:
                return [406] #No accounts registrateds. Start now with register

            else:
                #If program find Service element in file increment by one the counter
                for i in range(len(jsonData)):
                    if service in jsonData[i]: #find service in file
                        serviceCounter += 1 #increment counter
                
                #For every line in jsonData do:
                for i in range(len(jsonData)):

                    #If service is declared and email is null
                    if service != "" and email == "":
                        #Sometimes i've got error beacouse some keys don't content "services" string
                        try:
                            #Append service dict if it is founded in file
                            if jsonData[i][service]:
                                moreServices.append([jsonData[i][service][0], self.secure.decryptData(jsonData[i][service][1])]) #Append entire service
                        except KeyError:
                            continue #Don't do nothing and continue

                    #If Email is declared and service is null append in moreService dict of emial.
                    if service == "" and email != "":
                        #Sometimes i've got error beacouse some keys don't content "email" string
                        try:
                            #For every service read line
                            for k in jsonData[i]:
                                #If line K in pos 0 is email append all line
                                if jsonData[i][k][0] == email:
                                    #Take the name of the service
                                    for t in jsonData[i]:
                                        serviceFromEmail = t #Name of service
                                    moreServices.append({t: [jsonData[i][k][0], self.secure.decryptData(jsonData[i][k][1])]})#Append line
                        except KeyError:
                            continue #Don't do nothing and continue

                    #If method is equals to all return all datas
                    if method == "all":
                        moreServices.append(jsonData[i]) #Append all data to return array

                        

                
                #Check if list of services is grather equals 0
                if len(moreServices) == 0:
                    return [403] #Return No Account at this service Error
                else:
                    return [102, 105, moreServices] #Return 102 = Service Founded, 105 idk but it works, And list of services
