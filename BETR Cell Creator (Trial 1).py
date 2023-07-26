# Assuming you have not changed the general structure of the template no modification is needed in this file.
from . import commands
from .lib import fusion360utils as futil

import adsk.core, adsk.fusion, traceback
import os.path, sys

def run(context):
    ui = None
    try: 
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = app.activeProduct
        des = adsk.fusion.Design.cast(app.activeProduct)
        rootComp = design.rootComponent

        modelParams = des.rootComponent.modelParameters
        
        #Half beam width input
        input_value1 = ui.inputBox("Please input a Half Beam Width (for ref, int was 0.75 mm): ")
        half_beam_width = float(input_value1[0])
        modelParams.itemByName('half_Beam_w').expression = str(half_beam_width)

        #Half flex width input
        input_value2 = ui.inputBox("Please input a Half Flex Width (for ref, int was 0.25 mm): ")
        half_flex_width = float(input_value2[0])
        modelParams.itemByName('half_Flex_w').expression = str(half_flex_width)

        #Half flex length input
        input_value3 = ui.inputBox("Please input a Half Flex Length (for ref, int was 1 mm): ")
        half_flex_length = float(input_value3[0])
        modelParams.itemByName('half_Flex_L').expression = str(half_flex_length)

        #B input
        input_value4 = ui.inputBox("Please input a B value (for ref, int was 8 mm *0.8): ")
        B_val = float(input_value4[0])
        modelParams.itemByName('B').expression = str(B_val) + str('*0.8')

        #Initial angle input
        input_value5 = ui.inputBox("Please input an Initial Angle (for ref, int was 150 deg): ")
        int_angle = float(input_value5[0])
        modelParams.itemByName('initial_angle').expression = str(int_angle)

        #C times2 input
        input_value6 = ui.inputBox("Please input a C Times2 value (for ref, int was 10 mm *0.8): ")
        C_times2_val = float(input_value6[0])
        modelParams.itemByName('C_times2').expression = str(C_times2_val) + str('*0.8')

        #A times 2 input
        input_value7 = ui.inputBox("Please input an A Times2 value (for ref, int was 22 mm *0.8): ")
        A_times2_val = float(input_value7[0])
        modelParams.itemByName('A_times2').expression = str(A_times2_val) + str('*0.8')

        #Angle off horizontal input
        input_value8 = ui.inputBox("Please input an Angle off of the Horizontal (for ref, int was 25 deg): ")
        angle_off_horz_val = float(input_value8[0])
        modelParams.itemByName('angle_off_horz').expression = str(angle_off_horz_val)

        #Extrusion width input
        input_value9 = ui.inputBox("Please input an Extrusion Width (for ref, int was 2 mm): ")
        ext_width = float(input_value9[0])
        modelParams.itemByName('extrude_width').expression = str(ext_width)

        #Cylinder radius input (not sure what type of param this is, commented for now)
        # input_value10 = ui.inputBox("Please input a Cylinder Radius (for ref, int was 20 mm): ")
        # cyl_rad = float(input_value10[0])
        # modelParams.itemByName('Cyl_radius').expression = str(cyl_rad)

        #Will need to eventually manipulate folder destination to project database
        endfolder = 'C:\Temp2'
        if os.path.exists(endfolder):
            pass
        elif ~os.path.exists(endfolder):
            os.makedirs(endfolder)

        name = ui.inputBox("Please enter a name for the file: ")
        filename = os.path.join(endfolder, str(name[0]) + '.stl')
        
        #Save the file as STL.
        exportMgr = adsk.fusion.ExportManager.cast(design.exportManager)
        stlOptions = exportMgr.createSTLExportOptions(rootComp)
        stlOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementMedium
        stlOptions.filename = filename
        exportMgr.execute(stlOptions)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    try:
        # Remove all of the event handlers your app has created
        futil.clear_handlers()

        # This will run the start function in each of your commands as defined in commands/__init__.py
        commands.stop()

    except:
        futil.handle_error('stop')