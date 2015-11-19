#!/usr/bin/python

# import guacamole libraries
import avango
import avango.gua


### import application libraries
from lib.KeyboardInput import KeyboardInput
from lib.Hinge import Hinge
from lib.ArmSegment import ArmSegment
from lib.Hook import Hook


class Crane:
  
    # constructor
    def __init__( self
                , PARENT_NODE = None
                , TARGET_LIST = []
                ):



        ### resources ###

        ## init internal classes
        self.input = KeyboardInput()
        
        ## init base node for whole crane
        self.base_node = avango.gua.nodes.TransformNode(Name = "base_node")
        self.base_node.Transform.value = avango.gua.make_trans_mat(0.0,-0.1,0.0)
        PARENT_NODE.Children.value.append(self.base_node)
        
        print(TARGET_LIST)
        
        ## ToDo: init first hinge && connect rotation input 
        # ...
        print(self.base_node)
        self.hinge1_obj = Hinge()
        self.hinge1_obj.my_constructor( PARENT_NODE = self.base_node
                      , CASE = 0
                      , DIAMETER = 0.1
                      , HEIGHT = 0.01
                      , ROT_OFFSET_MAT = avango.gua.make_identity_mat() # the rotation offset relative to the parent coordinate system
                      , ROT_AXIS = avango.gua.Vec3(0,1,0) # the axis to rotate arround with the rotation input (default is head axis)
                      , ROT_CONSTRAINT = [-180, 180.0] # intervall with min and max rotation of this hinge
                      )
        self.hinge1_obj.sf_rot_value.connect_from(self.input.sf_rot_value0)

        ## ToDo: init first arm-segment
        self.arm1_obj = ArmSegment(PARENT_NODE = self.hinge1_obj.get_attached_node()
                      , DIAMETER = 0.005
                      , LENGTH = 0.15 
                      , ROT_OFFSET_MAT = avango.gua.make_identity_mat() # the rotation offset relative to the parent coordinate system
                      )
        
        ## ToDo: init second hinge && connect rotation input
        self.hinge2_obj = Hinge()
        self.hinge2_obj.my_constructor( PARENT_NODE = self.arm1_obj.get_attached_node()
                      , CASE = 1
                      , DIAMETER = 0.025
                      , HEIGHT = 0.015
                      , ROT_OFFSET_MAT = avango.gua.make_rot_mat(90.0, 1.0, 0.0, 0.0) # the rotation offset relative to the parent coordinate system
                      , ROT_AXIS = avango.gua.Vec3(0,0,1) # the axis to rotate arround with the rotation input (default is head axis)
                      , ROT_CONSTRAINT = [0.0, 90.0] # intervall with min and max rotation of this hinge
                      )
        self.hinge2_obj.sf_rot_value.connect_from(self.input.sf_rot_value1)

        
        ## ToDo: init second arm-segment
        self.arm2_obj = ArmSegment(PARENT_NODE = self.hinge2_obj.get_attached_node()
                      , DIAMETER = 0.005
                      , LENGTH = 0.1
                      , ROT_OFFSET_MAT = avango.gua.make_identity_mat() # the rotation offset relative to the parent coordinate system
                      )
        
        ## ToDo: init third hinge && connect rotation input 
        self.hinge3_obj = Hinge()
        self.hinge3_obj.my_constructor( PARENT_NODE = self.arm2_obj.get_attached_node()
                      , CASE = 2
                      , DIAMETER = 0.025
                      , HEIGHT = 0.015
                      , ROT_OFFSET_MAT = avango.gua.make_rot_mat(90.0, 1.0, 0.0, 0.0) # the rotation offset relative to the parent coordinate system
                      , ROT_AXIS = avango.gua.Vec3(0,0,1) # the axis to rotate arround with the rotation input (default is head axis)
                      , ROT_CONSTRAINT = [-90.0, 90.0] # intervall with min and max rotation of this hinge
                      )
        self.hinge3_obj.sf_rot_value.connect_from(self.input.sf_rot_value2)

        ## ToDo: init third arm-segment
        self.arm3_obj = ArmSegment(PARENT_NODE = self.hinge3_obj.get_attached_node()
                      , DIAMETER = 0.005
                      , LENGTH = 0.1
                      , ROT_OFFSET_MAT = avango.gua.make_identity_mat() # the rotation offset relative to the parent coordinate system
                      )        

        ## ToDo: init hook
        self.hook_obj = Hook()
        self.hook_obj = self.hook_obj.my_constructor(PARENT_NODE = self.arm3_obj.get_attached_node()
                      , SIZE = 0.02
                      , TARGET_LIST = TARGET_LIST
                      )


        #self.hook_obj.sf_mat.connect_from()

