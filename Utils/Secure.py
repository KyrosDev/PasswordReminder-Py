from cryptography.fernet import Fernet #Encrypt/Decrypt library
import json #Json Library
import os #Os library

class Secure:

    #Init class
    def __init__(self, directory):
        self.dir = directory #Take directory to read or write KEY.K file
        self.file = f"{self.dir}/key.k" #File name + directory

        #Check if key.k exists in directory folder
        if "key.k" not in os.listdir(self.dir):
            #If it isn't exists create file
            with open(f"{self.file}", "wb") as keyK:
                keyK.write(Fernet.generate_key()) #Write key
        else:
            #If file exists read file
            with open(f"{self.file}", "rb") as keyK:
                keyK.read() #Read key

    #Encrypt password method
    def encrpytData(self, password):

        message = password.encode() #Encode the password and give value to Message
        
        #Open file to take key
        with open(f"{self.file}", "rb") as keyK:
            key = keyK.read().decode() #Read key
        
        f = Fernet(key) #Init istance
        ePassword = f.encrypt(message) #Encrypt password
        return str(ePassword) #Return password to JSON file as string
        
    #Decrypt password method
    def decryptData(self, password):
        #Open file to take key
        with open(f"{self.file}", "rb") as keyFile:
            key = keyFile.read().decode() #Read and decode the key
        f = Fernet(key) #Init istance
        message = bytes(password.replace("b'", "").replace("'", ""), 'utf-8') #Transform string into bytes and replace b'<string>' with nothing
        decrpyted = decrpyted = f.decrypt(message) #Decrypt message
        decrpyted.decode() #Decode message
        return decrpyted.decode() #Return to JsonLoader message decrypted and decode it again