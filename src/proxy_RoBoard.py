#Prologue Comments
#Code Artifact: proxy_RoBoard.py
#Code Purpose: Sets up a proxy server for the Ro-Board.  The Ro-Board sends a picture of the board, and this code sends that picture to RoboFlow to
# analyze and return.  Once this proxy receives the response, it parses it and chooses a column for the robot.  The code then returns the column to
# the Ro-Board
# Team 19
#Created: 3/13/25
#Revised: 3/13/25
#Preconditions: Ro-board is set up to have taken a picture from the board and is ready to send the picture.
#Postconditions: Ro-board knows what column to place next piece in
#Errors: If the computer does not have the packages or a connection to the internet, then it will timeout.
#Side Effects: None
#Invariants: None
#Faults: If there is a timeout it may cause a bad return value
from inference import InferenceConfiguration, InferenceHTTPClient
import cv2
import supervision as sv
import requests
import statistics as stats
import socket

RED = '1' #classifications for play markers
YELLOW = '2' #other color for play markers

def determine_move(board, difficulty):
    # Make HTTP request to API with board and let robot be yellow
    # TODO: Check for win and return magic value if game end
    # url_won = "https://kevinalbs.com/connect4/back-end/index.php/getMoves?board_data=" + board + "&player=" + YELLOW

    url_move = "https://kevinalbs.com/connect4/back-end/index.php/getMoves?board_data=" + board + "&player=" + YELLOW #URL for API
    response_move = requests.get(url_move).json() #send request and receive response

    vals = [int(response_move[i]) for i in '0123456'] #parse response

    if difficulty == 'easy': #if gameplay is on easy, get the smallest column response
        t = min(vals) #min value is worst
    elif difficulty == 'med': #get medium response, which is medium correct column to choose.
        t = stats.median(vals) #median value is median between worst and best
    else: # difficulty == 'hard': #get the greatest column response
        t = max(vals) #max value is best

    for i in '0123456': #check each colomn number
        if int(response_move[i]) == t: #check if equal to my column from difficulty choice
            return i #return which column

    return -1 #error, did not find t
def send_Information( file, difficulty ):
    # Define confidence threshold
    config = InferenceConfiguration(confidence_threshold=0.2)
    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="API_KEY"
    ) #define requirements for connecting with API, website and key

    CLIENT.configure(config) #configure connection
    result = CLIENT.infer( file, model_id="connect4-ampe5/2") #get result from API

    detections = sv.Detections.from_inference(result) #get inference from the API
    detections = detections[detections.class_id != 0] #filter out bad results

    pieces = [p for p in result['predictions'] if p['class'] in ['red','yellow','empty']] #sort pieces from result and current picture
    sorted_pieces = sorted(pieces, key=lambda d: d['y'], reverse=False) #sort pieces by color
    grouped_data = [sorted_pieces[i:i + 7] for i in range(0, len(sorted_pieces), 7)] #group them then by class.

    fully_sorted = [] #init sorted array
    for group in grouped_data: #now put groups in sorted array
        sorted_group = sorted(group, key=lambda d: d['x'], reverse=False) #sort individual group
        fully_sorted.append(sorted_group) #add to array

    board = "" #init board
    for row in fully_sorted: #now go through sorted array and change into enums
        for column in row: #go through each column and change into enums
            piece = column['class'] #get current piece
            if piece == 'red': #if is in red class
                board += RED #add enum RED to board
            elif piece == 'yellow': #if in yellow class
                board += YELLOW #add enum YELLOW to board
            else: # piece == 'empty':
                board += '0' #add enum empty to board

    move = determine_move(board, DIFFICULTY) #call determine move function with my correct board and given difficulty
    return move #return what column to place game piece in.
if __name__ == '__main__': 
    # Defining Socket 
    host = '' #my IP, change if needed.
    port = 8080 #port for this proxy server.

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #create socket
    sock.bind((host, port))  # bind socket to me and given port
    sock.listen() # listen to the socket
    # Establishing Connections 
    conn = sock.accept() #wait for a client to connect
    print('Connected with client')  #let me know

    # Receiving File Data 
    image = conn[0].recv(1024).decode() #get the socket info, which is at [0], and set it to receive a file and decode
    #data is now my file information.  I need to then send this to RoboFlow
    print( "Received file from Ro-Board" ) #let user know
    difficulty = "hard" #TEMP
    column = send_Information( image, difficulty ) #call function to get which column
    print( result ) #TEMP.
    #Next, send the result back to the Ro-Board
    #send post request
    Robot_IP = '127.0.0.1' #TEMP: change to Ro-Board IP
    requests.post( url=Robot_IP, data=column )
	# Closing all Connections 
    conn[0].close() 
