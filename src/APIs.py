#Prologue Comments
#Code Artifact: APIs.py
#Code Purpose: Contains all the methods needed to take a file image and difficulty and send them to the APIs.  Then it returns which column to put the piece inside.
# Team 19
#Created: 3/13/25
#Revised: 3/25/25
#Preconditions: Ro-board is set up to have taken a picture from the board and is ready to send the picture.
#Postconditions: Ro-board knows what column to place next piece in
#Errors: If the computer does not have the packages or a connection to the internet, then it will timeout.
#Side Effects: None
#Invariants: None
#Faults: If there is a timeout it may cause a bad return value
from inference_sdk import InferenceConfiguration, InferenceHTTPClient #used for RoboFlow
import supervision as sv #Used for RoboFlow
import requests #used for connections
import http.server #sets up HTTP server
from PIL import Image #creates image file to send to Connect4 API
from board import Board
import numpy as np

RED = '1' #classifications for play markers
YELLOW = '2' #other color for play markers

def determine_move(board, difficulty) -> (int, int):
    # Check for a win
    board = board[len(board)-42:] # Trim board down to 42 pieces to correct hallucinations
    while len(board) < 42:
        board = '0' + board
    print(len(board))
    b = Board(board)
    game_state = b.win_exists()

    if game_state != 0: # Game done
        return game_state, -1
    print(board)
    print(len(board))
    url_move = "https://kevinalbs.com/connect4/back-end/index.php/getMoves?board_data=" + board + "&player=" + RED #URL for API
    response_move = requests.get(url_move).json() #send request and receive response
    print(response_move)
    vals = [0]*7
    curr_col = 0
    while curr_col < 7:
        if str(curr_col) in response_move:
            vals[curr_col] = response_move[str(curr_col)]
        else:
            vals[curr_col] = -9999
        curr_col += 1

    print(vals)
    if difficulty == "1": #if gameplay is on easy, get the smallest column response
        print("easy")
        t = min(vals) #min value is worst
    elif difficulty == "2": #get medium response, which is medium correct column to choose.
        print("medium")
        t = sorted( list( set( vals ) ), reverse=True )[1] #Second greatest is the second best, hence medium difficulty
        #sorting it gets the greatest value, and the one next to it is the second greatest.
    else: # difficulty == 'hard': #get the greatest column response
        print("hard")
        t = max(vals) #max value is best

    for i in range(len(vals)): #check each colomn number
        if int(vals[i]) == t: #check if equal to my column from difficulty choice
            print(t)
            b.make_move(i)
            game_state = b.win_exists()
            print(b.board)

            return game_state, i #return which column

    return -2, -2 #error, did not find t

def send_Information( file, difficulty ):
    # Define confidence threshold
    config = InferenceConfiguration(confidence_threshold=0.7)
    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="TEMP" #REMOVE, replace with API key when used in production.
    ) #define requirements for connecting with API, website and key
    CLIENT.configure(config) #configure connection
    result = CLIENT.infer( file, model_id="connect4-ampe5/3") #get result from API

    detections = sv.Detections.from_inference(result) #get inference from the API
    detections = detections[detections.class_id != 0] #filter out bad results

    pieces = [p for p in result['predictions'] if p['class'] in ['red','yellow','empty']] #sort pieces from result and current picture
    sorted_pieces = sorted(pieces, key=lambda d: d['y'] + d['height'] / 2, reverse=False) #sort pieces by color
    print(sorted_pieces)
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

    print(board)

    move = determine_move( board, difficulty ) #call determine move function with my correct board and given difficulty
    return move #return what column to place game piece in.
