#Derik Colucci

import re

finalLength = 0

def readKeylog():
    with open("logfile.txt", 'r') as logReader:
        inputFile = logReader.read()
    print(inputFile) #testing line: here to confirm what the program is seeing in the input file
    return findBackspaces(inputFile)

def editKeylog(inputFile):
    with open("logfile.txt", 'w') as logEditor:
        logEditor.write(inputFile)

def findBackspaces(inputFile): #my backspace representation is {<Key.backspace: <8>>}, replace or add whatever different to improve program. 
    processedData = [] #new list to store and change contents of string
    i = 0
    while(i < len(inputFile)): # looping through the input file
        char = inputFile[i] #create a variable to append to the new list
        if(inputFile[i:i+22] == "{<Key.backspace: <8>>}") and processedData: #checking for backspaces and the existance of data in the list
            processedData.pop() #create a backspace by removing the previous letter from the list
            i += 22 #skip the extended backspace representation
        else:
            processedData.append(inputFile[i]) #add the letter to the list
            i += 1 #move to the next character in the string

    editedData = ''.join(processedData) #revert the list back to a string
    return editedData #return the backspaced string

def processKeylog():
    global finalLength
    try:
        finalString = readKeylog() #read the input file and process
        if finalString: #checking if finalString has any contents
            #print("File opened.") #for testing 
            editKeylog(finalString) #change contents of input file by applying backspaces
        else:
            print("Error processing file.")
    except FileNotFoundError: #error handling for file not opening
        print("Could not find the input file.")
    except IOError: #error handling reading and writing into features
        print("Could not open file for reading and writing.")
    
    finalLength = len(finalString)

if __name__ == "__main__":
    processKeylog()
    print(finalLength)
    
