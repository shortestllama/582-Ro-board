#Prologue Comments
#Code Artifact: client.py
#Code Purpose: Test script that emulates the robot.  The robot code should copy this one to send messages to the proxy server.
# Team 19
#Created: 3/25/25
#Revised: 3/25/25
#Preconditions: Http-server is running
#Postconditions: Information was sent to the server and the column response was received
#Errors: If the Http-server is not running, it may timeout.
#Side Effects: None
#Invariants: None
#Faults: If there is a timeout it may cause a crash.
import requests #Robot has this.
# Creating Client Socket 
if __name__ == '__main__': 
    host = '127.0.0.1' #CHANGE to where the proxy servers is existing.
    port = 8000 #CHANGE to port served on the http server
    url = "http://" + host + ":" + str( port ) #creates url from host and port
    difficulty = 3 #Get from Ro-Board difficulty.
    data = { #send in JSON format.
        "difficulty" : difficulty #set difficulty here
    }
    files = { #send picture of the board to the http server
        "file" : open( "Ro-board.jpg", "rb" ) #CHANGE to image file name.
    }
    try: #try to send the request
        x = requests.post(url, data=data, files=files ) #post request with both difficulty and picture of the board.
        print( "Response: " + str( x.text ) ) #CHANGE to parse the responding column.
    except Exception as e: #timeout error catch
        print( e ) #Put Ro-Board's timeout logic here.
        
