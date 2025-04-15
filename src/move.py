#Prologue Comments
#Code Artifact: move.py
#Code Purpose: choose which column to place the next piece.  This code is defunct and has been moved to APIs.py
# Team 19
#Created: 2/25/25
#Revised: 3/12/25
#Preconditions: Ro-board is set up to have taken a picture from the board
#Postconditions: Ro-board knows what column to place next piece in
#Errors: If the Ro-board is not connected to the internet, socket timeouts
#Side Effects: None
#Invariants: None
#Faults: If there is a timeout may cause a bad return value
from inference_sdk import InferenceConfiguration, InferenceHTTPClient
import cv2
import supervision as sv
import requests
import statistics as stats

RED = '1' #classifications for play markers
YELLOW = '2' #other color for play markers

# These are currently some hard-coded values but eventually they would
# be pulled from the image taken from the robot and the chosen difficulty
FILE = "received_image.jpg"
DIFFICULTY = 'hard'

def determine_move(board, difficulty):
    # Make HTTP request to API with board and let robot be yellow
    #TODO: Check for win and return magic value if game end
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

image = cv2.imread(FILE) #read image from file

# Define confidence threshold
config = InferenceConfiguration(confidence_threshold=0.5)


CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="temp" #REMOVE, replace with API key when used in production.
) #define requirements for connecting with API, website and key

CLIENT.configure(config) #configure connection
result = CLIENT.infer(image, model_id="connect4-ampe5/3") #get result from API

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
print(move) #output which move the Ro-board should make
