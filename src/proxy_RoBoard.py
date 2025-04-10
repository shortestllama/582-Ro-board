#Prologue Comments
#Code Artifact: proxy_RoBoard.py
#Code Purpose: Creates a proxy HTTP server for the Ro-Board.  Receives an image file and difficulty from the Ro-Board, then sends it to the APIs.py methods.
# It then takes the result and sends that to the Ro-Board.
# Team 19
#Created: 3/25/25
#Revised: 3/25/25
#Preconditions: Ro-board is set up to have taken a picture from the board and is ready to send the picture.
#Postconditions: Ro-board knows what column to place next piece in
#Errors: If the computer does not have the packages or a connection to the internet, then it will timeout.
#Side Effects: None
#Invariants: None
#Faults: If there is a timeout it may cause a bad return value
import http.server #Used for server
import socketserver #Used for server
import APIs #import from my APIs file
import cgi #used to parse multipart image files.
from PIL import Image #used to create Image files
import cv2

PORT = 8000 #default port to serve on.

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self): #Only react to POST requests.
        # Parse the content type header to handle multipart form data
        content_type, pdict = cgi.parse_header(self.headers["Content-Type"])
        
        if content_type == "multipart/form-data": #if the request is correctly formatted
            # Parse the form data (this includes both text fields and file data)
            pdict["boundary"] = bytes(pdict["boundary"], "utf-8") #encode from bytes back to utf-8
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={"REQUEST_METHOD": "POST"}, keep_blank_values=True) #use cgi to put image back together.
            
            # Extract the 'difficulty' value from form fields
            difficulty = form.getvalue( "difficulty" )
            
            # Extract the file data
            file_item = form["file"]
            
            if file_item.filename:
                # Save the uploaded image to a file
                with open("received_image.jpg", "wb") as f: #overwrite if needed
                    f.write(file_item.file.read()) #write to file system as bytes.
                image = cv2.imread("received_image.jpg") #open as an Image file.
                game_state, column = APIs.send_Information( image, difficulty ) #call function to get which column
                # Send a success response
                self.send_response(200)
                self.send_header("Content-Type", "application/json") #as a json.
                self.end_headers() #let Ro-Board know I am done with headers.
                response = f'{{"message": "Received", "game_state": {game_state}, "column": {column}}}' #create response, includes column and success on message.
                print(response)
                self.wfile.write(response.encode("utf-8")) #send response
            else:
                # No file uploaded
                self.send_response(400) #bad message sent
                self.send_header("Content-Type", "application/json") #start headers
                self.end_headers() #end headers
                response = '{"message": "No file uploaded"}' #sent in json format, no file = incorrect
                self.wfile.write(response.encode("utf-8")) #send response.
        else:
            # If content type is not multipart/form-data
            self.send_response(400) #error
            self.send_header("Content-Type", "application/json") #start headers.
            self.end_headers() #end headers.
            response = '{"message": "Invalid content type"}' #let Ro-Board know to error handle.
            self.wfile.write(response.encode("utf-8")) #send message
with socketserver.TCPServer(("", PORT), MyHandler) as httpd: #start server on my port on this machine.
    print(f"Serving at port {PORT}") #print out that I am serving
    httpd.serve_forever() #listen for POST requests.
