#!/usr/bin/python

# import guacamole libraries
import avango
import avango.gua


class ArmSegment:

    ### class variables ###

    # Number of ArmSegment instances that have already been created.
    number_of_instances = 0
    
  
    # constructor
    def __init__( self
                , PARENT_NODE = None
                , DIAMETER = 0.1
                , LENGTH = 0.1
                , ROT_OFFSET_MAT = avango.gua.make_identity_mat() # the rotation offset relative to the parent coordinate system
                ):

        ## get unique id for this instance
        self.id = ArmSegment.number_of_instances
        ArmSegment.number_of_instances += 1

        #Initialize variables
        self.length = LENGTH

        ### resources ###
        _loader = avango.gua.nodes.TriMeshLoader() # get trimesh loader to load external tri-meshes
        
        ## ToDo: init arm node(s)
        self.arm_geometry = _loader.create_geometry_from_file("arm_geometry", "data/objects/cylinder.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.arm_geometry.Transform.value = avango.gua.make_scale_mat(DIAMETER, LENGTH, DIAMETER)
        self.arm_geometry.Material.value.set_uniform("Color", avango.gua.Vec4(0.0,1.0,0.0,1.0))

        #Transformation
        self.arm_transform = avango.gua.nodes.TransformNode(Name = "arm_node")
        #self.arm_transform.Children.value = [self.arm_geometry]

        # Translation
        self.arm_yshift = avango.gua.nodes.TransformNode(Name = "arm_yshift")
        
        self.arm_yshift.Transform.value = avango.gua.make_trans_mat(0.0, LENGTH/2 , 0.0)
        self.arm_transform.Children.value = [self.arm_geometry, self.arm_yshift]

        #Translation
       # self.arm_transform.Transform.value = avango.gua.make_trans_mat(0.0,TRANSLATEY,0.0)

        if PARENT_NODE is not None:
            PARENT_NODE.Children.value.append(self.arm_transform)

    def get_node(self):
        return self.arm_transform

    def get_attached_node(self):
        return self.arm_yshift
    
    def get_height(self):
        return self.length
                
        
