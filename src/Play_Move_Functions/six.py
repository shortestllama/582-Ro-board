#Prologue Comments
#Code Artifact: six.py
#Code Purpose: Puts the game piece in column 0.
# Team 19
#Created: 3/8/25
#Revised: 3/13/25
#Preconditions: Robot is in correct position in relation to the game board
#Postconditions: Robot dropped piece in column six.
#Errors: Robot could lose power and cause an issue with connecting to joints.
#Side Effects: None
#Invariants: None
#Faults: May drop the piece too early or miss the board
class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onLoad(self):
        #put initialization code here
        self.motion = ALProxy("ALMotion")
        self.posture = ALProxy("ALRobotPosture")
        pass

    def onUnload(self):
        #put clean-up code here
        pass

    def onInput_onStart(self):
        # stand
        self.posture.goToPosture("Stand", 0.2)

        # request piece
        request = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]
        first = ["RShoulderRoll"]
        self.motion.setAngles(first, [-76 * almath.TO_RAD], 0.2)
        time.sleep(2)
        self.motion.setAngles(request, [0 * almath.TO_RAD, -10 * almath.TO_RAD, 100 * almath.TO_RAD, -5 * almath.TO_RAD, 104.5 * almath.TO_RAD], 0.2)
        time.sleep(3)

        # open hand
        self.motion.post.openHand("RHand")
        time.sleep(3)

        # close hand
        self.motion.post.closeHand("RHand")
        time.sleep(5)

        # turn to place the piece
        rotate = ["RWristYaw"]
        self.motion.setAngles(rotate, [-100 * almath.TO_RAD], 0.2)
        time.sleep(1)

        # bend over
        bend = ["LHipPitch", "RHipPitch", "LKneePitch", "RKneePitch", "LAnklePitch", "RAnklePitch"]
        self.motion.angleInterpolationWithSpeed(bend, [-45 * almath.TO_RAD, -45 * almath.TO_RAD, 40 * almath.TO_RAD, 40 * almath.TO_RAD, -10 * almath.TO_RAD, -10 * almath.TO_RAD], 0.07)
        time.sleep(2)

        # drop piece
        self.motion.post.openHand("RHand")
        time.sleep(2)

        # lift hand
        lift = ["RElbowRoll"]
        self.motion.setAngles(lift, [40 * almath.TO_RAD], 0.2)
        time.sleep(2)

        # move arm out of the way
        last = ["RShoulderRoll"]
        self.motion.setAngles(last, [-76 * almath.TO_RAD], 0.2)
        time.sleep(2)

        # reset
        self.posture.goToPosture("Stand", 0.2)

        self.onStopped() #activate the output of the box
        pass

    def onInput_onStop(self):
        self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
        self.onStopped() #activate the output of the box
