#Prologue Comments
#Code Artifact: swap_hands.py
#Code Purpose: Swap piece from right hand to left hand.
# Team 19
#Created: 3/8/25
#Revised: 4/24/25
#Preconditions: Robot is in correct position in relation to the game board
#Postconditions: Piece has swapped to the left hand.
#Errors: Robot could lose power and cause an issue with connecting to joints.
#Side Effects: None
#Invariants: None
#Faults: May drop the piece too early or miss the board
import almath
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
        self.motion.setAngles(request, [3 * almath.TO_RAD, 1 * almath.TO_RAD, 100 * almath.TO_RAD, 6 * almath.TO_RAD, 104.5 * almath.TO_RAD], 0.2)
        time.sleep(3)

        # open hand
        self.motion.post.openHand("RHand")
        time.sleep(3)

        # close hand
        self.motion.post.closeHand("RHand")
        time.sleep(5)

        # Right arm in
        request = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]
        self.motion.setAngles(request, [30 * almath.TO_RAD, 10 * almath.TO_RAD, 60 * almath.TO_RAD, 88.5 * almath.TO_RAD, 0 * almath.TO_RAD], 0.2)
        time.sleep(3)

        # Left arm in
        request = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw"]
        first = ["LShoulderRoll"]
        self.motion.setAngles(first, [76 * almath.TO_RAD], 0.2)
        time.sleep(2)
        self.motion.setAngles(request, [30 * almath.TO_RAD, -10 * almath.TO_RAD, -60 * almath.TO_RAD, -88.5 * almath.TO_RAD, 0 * almath.TO_RAD], 0.2)
        time.sleep(3)

        # open hand
        self.motion.post.openHand("LHand")
        time.sleep(3)

        # close hand
        self.motion.post.closeHand("LHand")
        time.sleep(5)

        # open hand
        self.motion.post.openHand("RHand")
        time.sleep(3)

        # moving right arm out of the way
        first = ["RShoulderRoll"]
        self.motion.setAngles(first, [-6 * almath.TO_RAD], 0.2)
        time.sleep(2)
        request = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]
        angles = [86 * almath.TO_RAD, -6 * almath.TO_RAD, 76 * almath.TO_RAD, 44 * almath.TO_RAD, 0 * almath.TO_RAD]
        self.motion.setAngles(request, angles, 0.2)
        time.sleep(3)

        # reset
        self.posture.goToPosture("Stand", 0.2)

        self.onStopped() #activate the output of the box
        pass

    def onInput_onStop(self):
        self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
        self.onStopped() #activate the output of the box