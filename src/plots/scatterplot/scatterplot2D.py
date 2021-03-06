import bpy
import math
import sys
import json

sys.path.append("src/classes/common_tools")
sys.path.append("src/classes/materials")

from common_tools import CommonTools
from principle_material import PrincipleMaterial

class ScatterPlot2D(CommonTools):
    """
    ==============
    SCATTERPLOT 2D
    ==============
    A scatterplot in two dimenshion is used to display the relationship between two quantitative variables.
    Inheritted Class:
        CommonTools         : It consists of basic operations needed for plotting.
    Imported Class:
        PrincipleMaterial   : Used to create principle material.
    Arguments :
        x                   : The array of quantitative values passed by user. It must be of number data type.
        y                   : The array of quantitative values passed by user. It must be of number data type.
        cat                 : The array of categorical values respected to each value in (x, y).  
        grid_material       : The material color for grid in plot. Default color is White.
        number_material     : The material color for numbers in plot. Default color is White.
    Methods:
        scatterplot2D       : The main function to plot.
    """
    def __init__(
            self, x, y, cat, 
            grid_material, number_material):
        self.x = x
        self.y = y
        self.cat =cat
        self.grid_material = grid_material
        self.number_material = number_material
        self.scatter_material = [
            ("red",(1,0,0,1)),("yellow",(1,1,0,1)),("blue",(0,0,1,1)),
            ("green",(0,1,0,1)),("cyan",(0,1,1,1)),("purple",(1,0,1,1)),
            ("magenda",(1,0,0.25,1),("orange",(1,0.25,0,1)))
        ]

    def scatterplot2D(self):
        # Delete everything on the screen.
        self.clear_screen()

        # Switching to material mode.
        self.change_viewport(shading="MATERIAL")
        
        # Variables used in the function.
        x_y_cat = []
        x_y_cat.extend([list(a) for a in zip(self.x, self.y, self.cat)])
        y_max_val = max(self.y)
        x_max_val = max(self.x)
        x_scale = math.ceil(x_max_val/10)
        y_scale = math.ceil(y_max_val/10)
        total = len(self.x)
        categories = list(set(self.cat))

        # Adding 2D grid
        self.create_2D_grid(
            grid_name="X_Y",grid_size=10,grid_pos=(0, 0, 0), 
            grid_rot=(math.radians(0), math.radians(-90), math.radians(0)), 
            x_sub=11, y_sub=11, grid_material=self.grid_material)
        
        # Numbering x-axis and y-axis 
        for num in range(11):    
            self.text_obj(
                text=int(num*y_scale), text_type="y_plot", text_pos=(0, -1, num), 
                text_rot=(math.radians(90),math.radians(0) ,math.radians(90)),
                text_scale=(0.4,0.4,0.4), number_material=self.number_material)
            self.text_obj(
                text=int(num*x_scale), text_type="X_plot", text_pos=(0, num, -1),
                text_rot=(math.radians(90),math.radians(0),math.radians(90)),
                text_scale=(0.4,0.4,0.4), number_material=self.number_material) 

        # Adding a sphere in the corresponding cartesian position.
        for i in range(len(categories)):
            for itr in range(total):
                if categories[i] == x_y_cat[itr][-1]:
                    # Creating a sphere.
                    bpy.ops.mesh.primitive_uv_sphere_add(
                        segments=6, ring_count=6, radius=0.12, 
                        enter_editmode=False, align='WORLD', 
                        location=(0,self.x[itr]/x_scale,self.y[itr]/y_scale))
                    
                    # The Name will be in the format : "Scatter No: 0, Cat: Male"
                    bpy.context.active_object.name = "Scatter No:" + str(itr) + ", Cat :" + str(categories[i]) 
                    
                    # The material will be created and applied.
                    activeObject = bpy.context.active_object
                    material = PrincipleMaterial("ScatterMaterial :" + str(categories[i]), self.scatter_material[i][1]) 
                    activeObject.data.materials.append(material.create_principle_bsdf())
                    
                    mesh = bpy.context.object.data
                    for f in mesh.polygons:
                        f.use_smooth = True
            
        bpy.ops.object.select_all(action = 'DESELECT')
        return

if __name__ == "__main__":
    # Json parsing.
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    argv = json.loads(argv[0])

    plot = ScatterPlot2D(
        x=argv["x"], y=argv["y"], cat=argv["cat"],
        grid_material=argv["grid_material"], number_material=argv["number_material"])
    plot.scatterplot2D()