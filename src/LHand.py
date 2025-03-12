#Prologue Comments
#Code Artifact: LHand.py
#Code Purpose: Moves left arm and hip joints to request piece, move hand and arm, and then place piece into a column
# Team 19
#Created: 2/25/25
#Revised: 3/12/25
#Preconditions: Robot is charged and ready to move
#Postconditions: Robot dropped piece and is now standing
#Errors: Could lose power and be unable to move joints
#Side Effects: Piece should be within the game board
#Invariants: none
#Faults: May drop piece unexpectantly if it got a bad grab, or may miss the grab on a bad handoff
class MyClass(GeneratedClass): #my class for left hand movement and crouching when moving the left hand.
    def __init__(self): #class constructor
        GeneratedClass.__init__(self) #init this class

    def onLoad(self):
        #put initialization code here
        self.motion = ALProxy("ALMotion") #set this motion to ALMotion
        self.posture = ALProxy("ALRobotPosture") #set this posture to default ALRobotPosture
        pass

    def onUnload(self):
        #put clean-up code here
        pass

    def onInput_onStart(self):
        # stand
        self.posture.goToPosture("Stand", 1)

        # request piece
        request = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw"] #various joints to move to request
        first = ["LShoulderRoll"] #first move the left shoulder
        self.motion.setAngles(first, [76 * almath.TO_RAD], 0.2) #set left shoulder to 76 degrees
        time.sleep(2) #wait
        self.motion.setAngles(request, [3 * almath.TO_RAD, 8 * almath.TO_RAD, -100 * almath.TO_RAD, 6 * almath.TO_RAD, -104.5 * almath.TO_RAD], 0.2) #set all these joints to these various angles
        time.sleep(3) #wait
        
        # open hand
        self.motion.post.openHand("LHand")
        time.sleep(3) #wait
        
        # close hand
        self.motion.post.closeHand("LHand")
        time.sleep(5) #wait
        
        # turn to place the piece
        rotate = ["LWristYaw"]
        self.motion.setAngles(rotate, [100 * almath.TO_RAD], 0.2) #rotate left wrist yaw to 100 degrees
        time.sleep(1) #wait
        
        # bend over
        bend = ["LHipPitch", "RHipPitch", "LKneePitch", "RKneePitch", "LAnklePitch", "RAnklePitch"] #joints to bend over
        self.motion.angleInterpolationWithSpeed(bend, [-42 * almath.TO_RAD, -42 * almath.TO_RAD, 40 * almath.TO_RAD, 40 * almath.TO_RAD, -10 * almath.TO_RAD, -10 * almath.TO_RAD], 0.07)
        #move all the joints in this way with various angles to bend over
        time.sleep(2) #wait
        
        # drop piece
        self.motion.post.openHand("LHand")
        time.sleep(2) #wait
        
        # lift hand
        lift = ["LElbowRoll"] #set left elbow to move
        self.motion.setAngles(lift, [40 * almath.TO_RAD], 0.2) #set left elbow roll to 40 degrees
        time.sleep(2) #wait
        
        # move arm out of the way
        last = ["LShoulderRoll"] #set left shoulder
        self.motion.setAngles(last, [76 * almath.TO_RAD], 0.2) #set left shoulder roll to 76 degrees
        time.sleep(2) #wait

        # reset
        self.posture.goToPosture("Stand", 1) #back to standard stand position

        self.onStopped() #activate the output of the box
        pass

    def onInput_onStop(self):
        self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
        self.onStopped() #activate the output of the box
