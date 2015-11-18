#!/usr/bin/python

# import guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed


class Hinge(avango.script.Script):

    ## input fields
    sf_rot_value = avango.SFFloat()

    ### class variables ###

    # Number of Hinge instances that have already been created.
    number_of_instances = 0
   
    # constructor
    def __init__(self):
        self.super(Hinge).__init__()

        ## get unique id for this instance
        self.id = Hinge.number_of_instances
        Hinge.number_of_instances += 1



    def my_constructor( self    
                      , PARENT_NODE = None
                      , CASE = 0
                      , DIAMETER = 0.1
                      , HEIGHT = 0.1
                      , ROT_OFFSET_MAT = avango.gua.make_identity_mat() # the rotation offset relative to the parent coordinate system
                      , ROT_AXIS = avango.gua.Vec3(0,1,0) # the axis to rotate arround with the rotation input (default is head axis)
                      , ROT_CONSTRAINT = [-45.0, 45.0] # intervall with min and max rotation of this hinge
                      ):


        ### variables ###
        self.height = HEIGHT
        self.diameter = DIAMETER

        self.case = CASE
        ### parameters ###
        
        self.rot_axis = ROT_AXIS
        
        self.rot_constraint = ROT_CONSTRAINT

        self.current_amount_hinge0 = 0
        self.current_amount_hinge1 = 90
        self.current_amount_hinge2 = 90
        ### resources ###

        _loader = avango.gua.nodes.TriMeshLoader() # get trimesh loader to load external tri-meshes

        ## ToDo: init hinge node(s)
        self.hinge_geometry = _loader.create_geometry_from_file("hinge_geometry", "data/objects/cylinder.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.hinge_geometry.Transform.value = ROT_OFFSET_MAT * avango.gua.make_scale_mat(DIAMETER, HEIGHT, DIAMETER)
        self.hinge_geometry.Material.value.set_uniform("Color", avango.gua.Vec4(1.0,0.0,0.0,1.0))
        
        # Transformation
        self.hinge_transform = avango.gua.nodes.TransformNode(Name = "hinge_node")
        
        # Translation
        self.hinge_yshift = avango.gua.nodes.TransformNode(Name = "hinge_yshift")
        self.hinge_transform.Children.value = [self.hinge_geometry, self.hinge_yshift]

        #Optimal value 0.04, replaced Height with 0.04

        self.hinge_yshift.Transform.value = avango.gua.make_trans_mat(0.0, 0.04, 0.0) #child nodes are shifted by half of the height (or diameter?)


        if PARENT_NODE is not None:
            PARENT_NODE.Children.value.append(self.hinge_transform)

        
    ### callback functions ###
    
    @field_has_changed(sf_rot_value)
    def sf_rot_value_changed(self):
        pass
        ## ToDo: accumulate input to hinge node && consider rotation contraints of this hinge
        # ...

        #print("before")
        if self.case == 0:
            if ((self.current_amount_hinge0 + self.sf_rot_value.value) >= self.rot_constraint[0]) and ((self.current_amount_hinge0 + self.sf_rot_value.value) <= self.rot_constraint[1]):
                self.hinge_yshift.Transform.value =  avango.gua.make_rot_mat(self.sf_rot_value.value, self.rot_axis) * self.hinge_yshift.Transform.value 
                self.current_amount_hinge0 = self.current_amount_hinge0 + self.sf_rot_value.value
        if self.case == 1:
            if ((self.current_amount_hinge1 + self.sf_rot_value.value) >= self.rot_constraint[0]) and ((self.current_amount_hinge1 + self.sf_rot_value.value) <= self.rot_constraint[1]):
                self.hinge_yshift.Transform.value =  avango.gua.make_rot_mat(self.sf_rot_value.value, self.rot_axis) * self.hinge_yshift.Transform.value 
                self.current_amount_hinge1 = self.current_amount_hinge1 + self.sf_rot_value.value
        elif self.case == 2:
            if ((self.current_amount_hinge2 + self.sf_rot_value.value) >= self.rot_constraint[0]) and ((self.current_amount_hinge2 + self.sf_rot_value.value) <= self.rot_constraint[1]):
                self.hinge_yshift.Transform.value =  avango.gua.make_rot_mat(self.sf_rot_value.value, self.rot_axis) * self.hinge_yshift.Transform.value 
                self.current_amount_hinge2 = self.current_amount_hinge2 + self.sf_rot_value.value

        

        

        #print(self.hinge_transform.Transform.value)
        #ROT_OFFSET_MAT = avango.gua.make_rot_mat(sf_rot_value.value, self.rot_axis)

    def get_node(self):
        return self.hinge_transform

    def get_attached_node(self):
        return self.hinge_yshift
        
    def get_height(self):
        return self.height
    def get_diameter(self):
        return self.diameter
