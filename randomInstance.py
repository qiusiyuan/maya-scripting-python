#randomInstances.py
import maya.cmds as cmds
import random


random.seed(1234)

result = cmds.ls(orderedSelection=True)

print 'result: %s' %(result)

transformName = result[0]

#create an empty group
instanceGroupName = cmds.group(empty = True, name = transformName + '_instance_grp#')

#create another 50 random polycube
for i in  range(0,50):
    
    instanceResult =  cmds.instance(transformName,name = transformName +'_instance#')

    #add instance to the group
    cmds.parent( instanceResult, instanceGroupName)
    
    #random position
    x =  random.uniform(-10,10)
    y = random.uniform(0,20)
    z =  random.uniform(-10,10)
    cmds.move(x,y,z,instanceResult)
    
    #random rotation
    xRot = random.uniform(0,360)
    yRot = random.uniform(0,360)
    zRot = random.uniform(0,360)
    cmds.rotate(xRot,yRot,zRot,instanceResult)
    
    #random size
    scalingFactor = random.uniform(0.3,1.5)
    cmds.scale(scalingFactor, scalingFactor, scalingFactor,instanceResult)

#hide the original cube
cmds.hide(transformName)

#center pivot
cmds.xform(instanceGroupName, centerPivots = True)