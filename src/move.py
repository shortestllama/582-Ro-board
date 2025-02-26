from inference_sdk import InferenceConfiguration, InferenceHTTPClient
import cv2
import supervision as sv
import requests
import statistics as stats

RED = '1'
YELLOW = '2'

# These are currently some hard-coded values but eventually they would
# be pulled from the image taken from the robot and the chosen difficulty
FILE = "file.jpg"
DIFFICULTY = 'hard'

def determine_move(board, difficulty):
    # Make HTTP request to API with board and let robot be yellow
    #TODO: Check for win and return magic value if game end
    # url_won = "https://kevinalbs.com/connect4/back-end/index.php/getMoves?board_data=" + board + "&player=" + YELLOW

    url_move = "https://kevinalbs.com/connect4/back-end/index.php/getMoves?board_data=" + board + "&player=" + YELLOW
    response_move = requests.get(url_move).json()

    vals = [int(response_move[i]) for i in '0123456']

    if difficulty == 'easy':
        t = min(vals) 
    elif difficulty == 'med':
        t = stats.median(vals)
    else: # difficulty == 'hard':
        t = max(vals)

    for i in '0123456':
        if int(response_move[i]) == t:
            return i

    return -1

image = cv2.imread(FILE)

# Define confidence threshold
config = InferenceConfiguration(confidence_threshold=0.2)


CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="API_KEY"
)

CLIENT.configure(config)
result = CLIENT.infer(image, model_id="connect4-ampe5/2")

detections = sv.Detections.from_inference(result)
detections = detections[detections.class_id != 0]

pieces = [p for p in result['predictions'] if p['class'] in ['red','yellow','empty']]
sorted_pieces = sorted(pieces, key=lambda d: d['y'], reverse=False)
grouped_data = [sorted_pieces[i:i + 7] for i in range(0, len(sorted_pieces), 7)]

fully_sorted = []
for group in grouped_data:
    sorted_group = sorted(group, key=lambda d: d['x'], reverse=False)
    fully_sorted.append(sorted_group)

board = ""
for row in fully_sorted:
    for column in row:
        piece = column['class']
        if piece == 'red':
            board += RED
        elif piece == 'yellow':
            board += YELLOW
        else: # piece == 'empty':
            board += '0'

move = determine_move(board, DIFFICULTY)
print(move)
