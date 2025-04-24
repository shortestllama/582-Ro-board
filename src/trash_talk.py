import random

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
 
    def onLoad(self):
        #put initialization code here
        self.anim_speak = ALProxy("ALAnimatedSpeech")
        self.tts = ALProxy("ALTextToSpeech")
        pass
 
    def onUnload(self):
        #put clean-up code here
        pass

        # I cannot use cheographe on my mac so if these move the feet just change anim_speak to tts
        # Or change to a different animation
    def onInput_onStart(self):
        random_integer = random.randint(0, 12) # Generate a random int
        if random_integer > 6 and random_integer < 10: # If the number is 7, 8, or 9 
            self.anim_speak.say("^start(you) You are terrible at this game! ^wait(you)") # Talk trash with an animation
        elif  random_integer == 10 or random_integer == 11: # If the number is 10 or 11
            self.anim_speak.say("^start(not know) Are you sure about that move? ^wait(not know)") # Talk trash in a different way
        elif  random_integer == 12: # If the number is 12 
            self.anim_speak.say("^start(not know) Was that really the best move there? ^wait(not know)") # Talk trash in a different way
        elif random_integer > 3 and random_integer < 7 : # If the number is 4, 5, or 6
            self.anim_speak.say("^start(you) Good idea! ^wait(you)") # Congratulate the user
        else: # If the number is 0-3
            self.anim_speak.say("^start(happy) Nice move! ^wait(happy)") # Congratulate the user

    def onInput_onStop(self):
         self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
         self.onStopped() #activate the output of the box
