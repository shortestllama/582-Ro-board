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
        self.posture.goToPosture("Stand", 1)

        # request piece
        request = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw"]
        first = ["LShoulderRoll"]
        self.motion.setAngles(first, [76 * almath.TO_RAD], 0.2)
        time.sleep(2)
        self.motion.setAngles(request, [3 * almath.TO_RAD, 8 * almath.TO_RAD, -100 * almath.TO_RAD, 6 * almath.TO_RAD, -104.5 * almath.TO_RAD], 0.2)
        time.sleep(3)
        
        # open hand
        self.motion.post.openHand("LHand")
        time.sleep(3)
        
        # close hand
        self.motion.post.closeHand("LHand")
        time.sleep(5)
        
        # turn to place the piece
        rotate = ["LWristYaw"]
        self.motion.setAngles(rotate, [100 * almath.TO_RAD], 0.2)
        time.sleep(1)
        
        # bend over
        bend = ["LHipPitch", "RHipPitch", "LKneePitch", "RKneePitch", "LAnklePitch", "RAnklePitch"]
        self.motion.angleInterpolationWithSpeed(bend, [-42 * almath.TO_RAD, -42 * almath.TO_RAD, 40 * almath.TO_RAD, 40 * almath.TO_RAD, -10 * almath.TO_RAD, -10 * almath.TO_RAD], 0.07)
        time.sleep(2)  
        
        # drop piece
        self.motion.post.openHand("LHand")
        time.sleep(2)
        
        # lift hand
        lift = ["LElbowRoll"]
        self.motion.setAngles(lift, [40 * almath.TO_RAD], 0.2)
        time.sleep(2)
        
        # move arm out of the way
        last = ["LShoulderRoll"]
        self.motion.setAngles(last, [76 * almath.TO_RAD], 0.2)
        time.sleep(2)

        # reset
        self.posture.goToPosture("Stand", 1)

        self.onStopped() #activate the output of the box
        pass

    def onInput_onStop(self):
        self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
        self.onStopped() #activate the output of the box