import maya.cmds as cmds
import functools
import maya.mel as mel
import sys
import re
import pymel.core as pm

project_name = "my_pro"#default new project name,should be modified
chosen_dir = ""
dirID = "project_choose"
new_name =""

#folder list to add into new project
add_on_list = ["cache/nCache/fluid","data","images","scenes/edits","renderData/fur/furShadowMap","scripts",
"renderData/shaders","renderData/fur/furFiles","renderData/fur/furEqualMap","movies","autosave","sound",
"Time Editor","renderData/iprImages","sourceimages/3dPaintTextures","cache/particles","sourceimages","clips",
"renderData/fur/furImages","renderData/depth","sceneAssembly","Time Editor/Clip Exports","cache/bifrost",
"renderData/fur/furAttrMap","assets"]
#browse to show new project
def create_new(*pargs):
        global new_name
        name = str(cmds.textField(new_name,query = True,text = True))
        def condition(name):#specify the new project name restriction
            if len(name)<8:
                return True
            return False
        if condition(name):
            cmds.sysFile("/Users/ntdstaff/Library/Preferences/Autodesk/maya/2017/projects/"+name, md=True)
            pm.mel.setProject("/Users/ntdstaff/Library/Preferences/Autodesk/maya/2017/projects/"+name)
            for newfolder in add_on_list:
                cmds.sysFile("/Users/ntdstaff/Library/Preferences/Autodesk/maya/2017/projects/"+name+"/"+newfolder, md=True)
        #file dialog
            cmds.fileDialog2(dir = "/Users/ntdstaff/Library/Preferences/Autodesk/maya/2017/projects/"+name,ds = 1,fm=2)
        
        #block for create good
            while cmds.window("good",exists = True):
                cmds.deleteUI("good")
            cmds.window("good",h=100,w=200)
            cmds.rowColumnLayout(numberOfRows=2)
            cmds.text(label = "your project %s has been chosen as working directory" %(name))
            def deleteWi(*pargs):
                cmds.deleteUI("new")
                cmds.deleteUI("good")
                cmds.deleteUI(dirID)
            cmds.button(label ="Ok",command = deleteWi)
            cmds.showWindow("good")
        
#create a new project
def newPro(*parg):
    global chosen_dir,new_name
    if cmds.window("new",exists = True):
        cmds.deleteUI("new")       
    window = cmds.window("new",h=100,w=200)
    cmds.rowColumnLayout(numberOfColumns =3, columnWidth= [(1,155),(2,60),(3,60)], columnOffset = [(1,'right',3)])
    cmds.text(label = "your new project name: ")
    new_name = cmds.textField(text = project_name)
    
    cmds.button(label = "OK",command = create_new)
    cmds.showWindow(window)
    
#browse a file dialog to choose working project (for existPro())  
def wkSpace(*pargs):
    chosen_lst = cmds.fileDialog2(ds = 1,fm = 2,dir = "/Users/ntdstaff/Library/Preferences/Autodesk/maya/2017/projects/")
    try:     
        while chosen_lst[0].split('/')[:-1] != "/Users/ntdstaff/Library/Preferences/Autodesk/maya/2017/projects".split('/'):

            chosen_lst = cmds.fileDialog2(ds = 1,fm = 2,dir = "/Users/ntdstaff/Library/Preferences/Autodesk/maya/2017/projects/")
        pm.mel.setProject(chosen_lst[0])
            
        if cmds.window("prompt", exists = True):
            cmds.deleteUI("prompt")
        cmds.window("prompt")
        cmds.rowColumnLayout( numberOfRows=4 )
        cmds.text(label = "You choose :", al = "left")
        cmds.text(label = chosen_lst[0],al = "center")
        cmds.text(label = "as your working project",al = "right")
        cmds.rowColumnLayout(numberOfColumns =3, columnWidth= [(1,75),(2,60),(3,60)], columnOffset = [(1,'right',3)])
        cmds.separator(h= 10)
        def exit(*parg):
            if cmds.window("exist", exists = True):
                cmds.deleteUI("exist")
            if cmds.window("prompt", exists = True):
                cmds.deleteUI("prompt")
            if cmds.window(dirID, exists = True):
                cmds.deleteUI(dirID)
        cmds.button(label = "Ok",command = exit)
        cmds.showWindow("prompt")  
    except TypeError:
        print "no folder is chosen"
###choose an existing project
def existPro(*pargs):
    global chosen_dir
    
        
    if cmds.window("exist", exists = True):
        cmds.deleteUI("exist")
    cmds.window("exist")
    cmds.rowColumnLayout( numberOfRows=2 )
    cmds.text(label = "Choose your working project")
    cmds.rowColumnLayout(numberOfColumns =3, columnWidth= [(1,75),(2,60),(3,60)], columnOffset = [(1,'right',3)])
    cmds.separator(h= 10)
    cmds.button(label = "choose",command = wkSpace)
    cmds.showWindow("exist")

    
        
        
        
### choose a working project, (This is the first and main step)

def browseDir():
    while cmds.window(dirID,exists = True):
                cmds.deleteUI(dirID)
    
    window = cmds.window(dirID, h = 100, w =200)
    cmds.rowColumnLayout( numberOfRows=2 )
    cmds.text(label= "Choose your working project or create a new one")
    cmds.rowColumnLayout(numberOfColumns =3, columnWidth= [(1,75),(2,60),(3,60)], columnOffset = [(1,'right',3)])
    cmds.separator(h= 10)
    cmds.button(label = "choose",command = existPro)
    cmds.button(label = "create",command = newPro)
    

    cmds.showWindow( window)
    
       
#    Create a window with a some fields for entering text.
windowID = 'save'
def saveScene( fileName):
    cmds.file(rename = fileName)
    cmds.file(save=True )
    return 1
###
def myFileBrowser(*pargs):
    global windowID
    multipleFilters = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb)"
    val = cmds.fileDialog2( ff=multipleFilters,ds =2,fm = 0)
    if val:
         print val
         saveScene(val[-1])
         if cmds.window(windowID, exists =True):
            cmds.deleteUI(windowID)



###
browseDir()
