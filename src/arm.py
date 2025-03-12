#Prologue Comments
#Code Artifact: arm.py
#Code Purpose: Moves the right arm into position to be ready to grab a piece
# Team 19
#Created: 2/25/25
#Revised: 3/12/25
#Preconditions: Robot is set up and ready to move
#Postconditions: Robot is ready to grab a piece
#Errors: If the robot is not charged it may be unable to move
#Side Effects: Robot moves its right arm from this code
#Invariants: None
#Faults: Physical environment may be in the way of the arm which could cause it to fall over.
import time
import almath
import argparse
from naoqi import ALProxy

class MyClass(GeneratedClass): #my class to move the arm
  def init(self): #class constructor
    GeneratedClass.init(self) #init this class

  def onLoad(self):
    #put initialization code here
    pass

  def onUnload(self):
    #put clean-up code here
    pass

  def onInput_onStart(self):
    motion = ALProxy("ALMotion") #on arm move start
    names = "RElbowYaw" #right elbow yaw
    names2 = "RElbowRoll" #right elbow roll
    names3 = "RShoulderPitch" #right shoulder pitch
    names4 = "RShoulderRoll" #right shoulder roll
    angles1 = 60.0*almath.TO_RAD #convert angle to Radian
    angles2 = 30.0*almath.TO_RAD #convert angle to Radian
    fractionMaxSpeed = 0.1 #set max speed multiplier
    motion.setAngles(names,angles1,fractionMaxSpeed) #set angle of right elbow yaw to 60
    time.sleep(2.0) #wait
    motion.setAngles(names,angles2,fractionMaxSpeed) #set angle of right elbow yaw to 30
    time.sleep(2.0) #wait
    motion.setAngles(names2,angles1,fractionMaxSpeed) #set angle of right elbow roll to 60
    time.sleep(2.0) #wait
    motion.setAngles(names2,angles2,fractionMaxSpeed) #set angle of right elbow roll to 30
    time.sleep(2.0) #wait
    motion.setAngles(names3,angles1,fractionMaxSpeed) #set angle of right shoulder pitch to 60
    time.sleep(2.0) #wait
    motion.setAngles(names3,angles2,fractionMaxSpeed) #set angle of right shoulder pitch to 30
    time.sleep(2.0) #wait
    motion.setAngles(names4,angles1,fractionMaxSpeed) #set angle of right shoulder roll to 60
    time.sleep(2.0) #wait
    motion.setAngles(names4,angles2,fractionMaxSpeed) #set angle of right shoulder roll to 30
    time.sleep(2.0) #wait
    #print(motion.getBodyNames("Body"))
    self.onStopped() #activate the output of the box

  def onInput_onStop(self):
    self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
    self.onStopped() #activate the output of the box
