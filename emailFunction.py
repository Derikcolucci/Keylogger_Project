#Derik Colucci

from dotenv import load_dotenv #used to access the variables from the env file
from email.message import EmailMessage
import os, ssl, smtplib

#when using gmail, two step verification needs to be enabled to allow the sender email to work properly. After verification is properly turned on,
#a 16 digit password will be used instead of the gmail password within the program
#to get better access to variabels using the os.environ instal "pip install python-dotenv" in terminal and store the information in an environment(.env) file

def emailData():
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
    subject = 'Testing'
    body = "Hello"
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


if __name__ == "__main__":
    emailData()