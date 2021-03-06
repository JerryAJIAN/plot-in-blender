import bpy
import random

from principle_material import PrincipleMaterial

class PieMaterial():
    """
    ============
    PIE MATERIAL
    ============
    The class is used to create gradient used in pieplots.
    Imported Class:
        PrincipleMaterial           : Used to create Principle BSDF.
    Arguments:
        percent_of_x                : The percentage values of x array.
    Methods:
        create_values_and_colors    : This will form nested list of [value,color_code].
        get_random_color            : Used to create random colors.
        create_pie_material         : Used to create shader of pieplot.
        create_gradient             : This sections adds or removes elements if you update your procents_and_colors list with more / fewer elements
    """
    def __init__(self, percent_of_x, y):
        self.values_and_colors = []
        self.percent_of_x = percent_of_x
        self.y = y

    def create_values_and_colors(self):
        for i in range(len(self.percent_of_x)):
            self.values_and_colors.append([
                self.percent_of_x[i], 
                self.get_random_color(self.percent_of_x[i] ,self.y[i])])
        return self.values_and_colors

    def get_random_color(self, percent, cat):
        RAN = random.random
        r, g, b = RAN(), RAN(), RAN()
        material = PrincipleMaterial(
            str(cat) +" - "+ str(round(percent,2)),(r, g, b, 1.0))
        material.create_principle_bsdf()
        return ((r, g, b, 1.0))

    def create_gradient(self, elements, procents_and_colors):
        diff = len(elements) - len(procents_and_colors)
        if diff > 0:
            for _ in range(abs(diff)):
                elements.remove(elements[-1])
        elif diff < 0:
            for _ in range(abs(diff)):
                elements.new(position=0.0)
            
        position = 0
        for idx, section in enumerate(procents_and_colors):
            elements[idx].color = section[1]
            elements[idx].position = position
            position += (section[0] / 100.0)        
      
    def create_pie_material(self):
        material = bpy.data.materials.get("Pie Plot")
        if material is None:
            material = bpy.data.materials.new(name="Pie Plot")

        material.use_nodes = True
        mats = bpy.data.materials
        nodes = mats['Pie Plot'].node_tree.nodes
        color_ramp = nodes.get("ColorRamp")

        if color_ramp is not None:
            nodes.remove(color_ramp)
        color_ramp = material.node_tree.nodes.new("ShaderNodeValToRGB")
        elements = nodes["ColorRamp"].color_ramp.elements
        nodes["ColorRamp"].color_ramp.interpolation = "CONSTANT"
        
        procents_and_colors = self.create_values_and_colors()

        self.create_gradient(elements, procents_and_colors)
            
        principled_bsdf = nodes.get("Principled BSDF")
        material.node_tree.links.new(principled_bsdf.inputs["Base Color"], color_ramp.outputs["Color"])

        gradient = nodes.get("Gradient Texture")
        if gradient is not None:
            nodes.remove(gradient)
        gradient = material.node_tree.nodes.new("ShaderNodeTexGradient")
        gradient.gradient_type = "RADIAL"
        material.node_tree.links.new(color_ramp.inputs["Fac"], gradient.outputs["Color"])

        texture_cord = nodes.get("Texture Coordinate")
        if texture_cord is not None:
            nodes.remove(texture_cord)
        texture_cord = material.node_tree.nodes.new("ShaderNodeTexCoord")
        material.node_tree.links.new(gradient.inputs["Vector"], texture_cord.outputs["Object"])
        return material
