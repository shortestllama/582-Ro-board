#Prologue Comments
#Code Artifact: pick_up_piece.py
#Code Purpose: Code for the robot to pick up the piece.
# Team 19
#Created: 4/08/25
#Revised: 4/08/25
#Preconditions: Piece is within the piece holder and a game has been initiated.
#Postconditions: Ro-board has picked up the piece, holding in hand correctly, and ready to place piece next.
#Errors: May have a bad grab if the piece is not properly socketed within the piece holder.
#Side Effects: None
#Invariants: None
#Faults: Dropping the piece is possible if there are outside objects hitting the hands.
import almath

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self) #pick up piece generated class

    def onLoad(self):
        self.motion = ALProxy("ALMotion")
        #put initialization code here
        pass

    def onUnload(self):
        #put clean-up code here
        pass

    def onInput_onStart(self):
        # initialize arm movements
        arm = ["RElbowRoll", "RElbowYaw", "RShoulderRoll", "RWristYaw"]
        # arm out to avoid piece holder
        self.motion.setAngles(["RShoulderRoll"], [-76 * almath.TO_RAD], 0.2)
        time.sleep(1.5)
        # position arm
        self.motion.setAngles(["RElbowRoll", "RElbowYaw"], [88.5 * almath.TO_RAD, 90 * almath.TO_RAD], 0.2)
        time.sleep(1)
        # rotate hand
        self.motion.setAngles(arm, [88.5 * almath.TO_RAD, 90 * almath.TO_RAD, -43 * almath.TO_RAD, -45 * almath.TO_RAD], 0.2)
        # open hand
        self.motion.openHand("RHand")
        # drop hand
        self.motion.setAngles(["RElbowRoll", "RElbowYaw"], [73 * almath.TO_RAD, 85 * almath.TO_RAD], 0.2)
        # close hand
        self.motion.closeHand("RHand")
        self.onStopped() #activate the output of the box
        pass

    def onInput_onStop(self):
        self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
        self.onStopped() #activate the output of the box
