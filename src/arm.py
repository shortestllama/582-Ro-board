#Prologue Comments
#Code Artifact: arm.py
#Code Purpose:
# Team 19
#Created: 
#Revised:
#Preconditions:
#Postconditions: 
#Errors:
#Side Effects:
#Invariants:
#Faults:
import time
import almath
import argparse
from naoqi import ALProxy

class MyClass(GeneratedClass):
  def init(self):
    GeneratedClass.init(self)

  def onLoad(self):
    #put initialization code here
    pass

  def onUnload(self):
    #put clean-up code here
    pass

  def onInput_onStart(self):
    motion = ALProxy("ALMotion")
    names = "RElbowYaw"
    names2 = "RElbowRoll"
    names3 = "RShoulderPitch"
    names4 = "RShoulderRoll"
    angles1 = 60.0*almath.TO_RAD
    angles2 = 30.0*almath.TO_RAD
    fractionMaxSpeed = 0.1
    motion.setAngles(names,angles1,fractionMaxSpeed)
    time.sleep(2.0)
    motion.setAngles(names,angles2,fractionMaxSpeed)
    time.sleep(2.0)
    motion.setAngles(names2,angles1,fractionMaxSpeed)
    time.sleep(2.0)
    motion.setAngles(names2,angles2,fractionMaxSpeed)
    time.sleep(2.0)
    motion.setAngles(names3,angles1,fractionMaxSpeed)
    time.sleep(2.0)
    motion.setAngles(names3,angles2,fractionMaxSpeed)
    time.sleep(2.0)
    motion.setAngles(names4,angles1,fractionMaxSpeed)
    time.sleep(2.0)
    motion.setAngles(names4,angles2,fractionMaxSpeed)
    time.sleep(2.0)
    #print(motion.getBodyNames("Body"))
    self.onStopped() #activate the output of the box

  def onInput_onStop(self):
    self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
    self.onStopped() #activate the output of the box
