#Prologue Comments
#Code Artifact: trash_talk.py
#Code Purpose: Adds functionality for ro-board gestures during the gameplay loop.
# Team 19
#Created: 4/27/25
#Revised: 4/27/25
#Preconditions: Ro-board is playing a game with the user.
#Postconditions: Ro-board has intereracted with the user throughout the game.
#Errors: None
#Side Effects: None
#Invariants: None
#Faults: None
import random

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
 
    def onLoad(self):
        # Set up proxies
        self.memory = ALProxy("ALMemory") # For previous moves
        self.anim_speak = ALProxy("ALAnimatedSpeech") # For gestures
        self.tts = ALProxy("ALTextToSpeech") # Fallback in case gestures move feet
        self.PREV_MOVES_VAR = "prev_moves" # The name of the variable that stores the previous gestures
        self.NUM_GESTURES = 10 # Constant for the num gestures to avoid magic numbers
        self.GESTURE_DICT = { # Const dictionary of function pointers to call the gesture
            1: self.gesture_one,
            2: self.gesture_two,
            3: self.gesture_three,
            4: self.gesture_four,
            5: self.gesture_five,
            6: self.gesture_six,
            7: self.gesture_seven,
            8: self.gesture_eight,
            9: self.gesture_nine,
            10: self.gesture_ten
        }
        pass
 
    def onUnload(self):
        #put clean-up code here
        pass

    # Gesture one
    def gesture_one(self):
        self.anim_speak.say("^start(you) You are terrible at this game! ^wait(you)") # Talk trash with an animation

    # Gesture two
    def gesture_two(self):
        self.anim_speak.say("^start(not know) Are you sure about that move? ^wait(not know)") # Talk trash in a different way

    # Gesture three
    def gesture_three(self):
        self.anim_speak.say("^start(not know) Was that really the best move there? ^wait(not know)") # Talk trash in a different way

    # Gesture four
    def gesture_four(self):
        self.anim_speak.say("^start(you) Good idea! ^wait(you)") # Congratulate the user, could be sarcasm

    # Gesture five
    def gesture_five(self):
        self.anim_speak.say("^start(happy) Nice move! ^wait(happy)") # Congratulate the user

    # Gesture six 
    def gesture_six(self):
        self.anim_speak.say("^start(you) I'm not sure about that one! ^wait(you)") # More trash talk 

    # Gesture seven 
    def gesture_seven(self):
        self.anim_speak.say("^start(oppose) Awful move! ^wait(oppose)") # More trash talk 
        
    # Gesture eight 
    def gesture_eight(self):
        self.anim_speak.say("^start(you) Did you even think? ^wait(you)") # More trash talk 
        
    # Gesture nine 
    def gesture_nine(self):
        self.anim_speak.say("^start(you) You got me there! ^wait(you)") # More trash talk 
        
    # Gesture ten 
    def gesture_ten(self):
        self.anim_speak.say("^start(oppose) You might want to reconsider! ^wait(oppose)") # More trash talk 

    # This function grabs the two previously done gestures from ALMemory
    def get_two_prev_moves(self):
        # I wasn't sure if it would throw an error or return None if it wasnt initialized yet so I did both
        prev_two_moves = [0, 0]
        try: 
            prev_two_moves = self.memory.getData(self.PREV_MOVES_VAR)
            # If there are no previous moves, make a list of two placeholder values
            if prev_two_moves is None:
                prev_two_moves = [0, 0] # 0 is the placeholder
        except:
            prev_two_moves = [0, 0] # 0 is the placeholder
        
        return prev_two_moves # Actually return the previous moves

    # Function that performs a gesture and returns the gesture that was done
    def perform_gesture(self, prev_two_moves):
        random_gesture = random.randint(1, self.NUM_GESTURES) # Generate a random int
        while random_gesture in prev_two_moves: # If the gesture is in the two previous gestures, keep generating random ints
            random_gesture = random.randint(1, self.NUM_GESTURES) # Generate a random int

        self.GESTURE_DICT[random_gesture]() # Perform the gesture
        return random_gesture # Return the gesture

    # I cannot use cheographe on my mac so if these move the feet just change anim_speak to tts
    # Or change to a different animation
    def onInput_onStart(self):
        prev_two_moves = self.get_two_prev_moves() # Get the previous moves

        gesture = self.perform_gesture(prev_two_moves) # Perform a gesture and get the return value

        # Update the previously done moves by moving index 0 over to 1, and then making 0 the gesture we did
        prev_two_moves[1] = prev_two_moves[0]
        prev_two_moves[0] = gesture 
        self.memory.insertData(self.PREV_MOVES_VAR, prev_two_moves) # Update the previous moves in memory

    def onInput_onStop(self):
         self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
         self.onStopped() #activate the output of the box
