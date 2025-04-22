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
from board import Board # Used for board data structure

RED = '1' #classifications for play markers
YELLOW = '2' #other color for play markers

def determine_move(board, difficulty) -> (int, int):
    # Check for a win
    board.print() # Print board for debugging
    game_state = board.win_exists() # Use board to check for win

    if game_state != 0: # Game done
        return game_state, -1 # Return game end and no column to play (-1)

    url_move = "https://kevinalbs.com/connect4/back-end/index.php/getMoves?board_data=" + board.board + "&player=" + RED #URL for API
    response_move = requests.get(url_move).json() #send request and receive response
    print(response_move) # Print response for debugging
    vals = [0]*7 # Create empty list for vals
    curr_col = 0 # Start at 0th column
    while curr_col < 7: # Loop through columns
        if str(curr_col) in response_move: # Check for column in response
            vals[curr_col] = response_move[str(curr_col)] # Use value if it is given
        else:
            vals[curr_col] = -9999 # Use dummy value if not given
        curr_col += 1 # Go to next column

    print(vals) # Print vals of columns for debugging
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
            print(t) # Print the column for debugging
            board.make_move(i) # Use the board object to make a move
            game_state = board.win_exists() # Check if win exists within the board
            board.print() # Print the board for debugging 

            return game_state, i #return which column

    return -2, -2 #error, did not find t

def send_Information( file, difficulty ):
    # Define confidence threshold
    config = InferenceConfiguration(confidence_threshold=0.7)
    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="qhTLMqBcrKlEz4riDUpI" #REMOVE, replace with API key when used in production.
    ) #define requirements for connecting with API, website and key
    CLIENT.configure(config) #configure connection
    result = CLIENT.infer( file, model_id="connect4-ampe5/3") #get result from API

    detections = sv.Detections.from_inference(result) #get inference from the API
    detections = detections[detections.class_id != 0] #filter out bad results

    pieces = [p for p in result['predictions'] if p['class'] in ['red','yellow','empty']] #sort pieces from result and current picture
    print(f"len {len(pieces)}")
    print(f"pieces {pieces}")
    board = Board(pieces) # Construct board object from pieces
    board.print() # DEBUG - print board

    move = determine_move( board, difficulty ) #call determine move function with my correct board and given difficulty
    return move #return what column to place game piece in.
