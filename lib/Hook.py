#!/usr/bin/python

# import guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed


class Hook(avango.script.Script):

    ## internal fields
    sf_mat = avango.gua.SFMatrix4()
 
    # constructor
    def __init__(self):
        self.super(Hook).__init__()


    def my_constructor( self    
                      , PARENT_NODE = None
                      , SIZE = 0.1
                      , TARGET_LIST = []
                      ):


        ### external resources ###
        
        self.TARGET_LIST = TARGET_LIST


        ### resources ###
        
        _loader = avango.gua.nodes.TriMeshLoader() # get trimesh loader to load external tri-meshes

        ## ToDo: init hook node(s)
        # ...
        self.hook_geometry = _loader.create_geometry_from_file("hook_geometry", "data/objects/sphere.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.hook_geometry.Transform.value = avango.gua.make_scale_mat(SIZE, SIZE, SIZE)

        #Add color
        self.hook_geometry.Material.value.set_uniform("Color", avango.gua.Vec4(0.0,0.0,1.0,1.0))
        ## ToDo: init field connections
        # ...
        #Transformation Translation
        self.hook_transform = avango.gua.nodes.TransformNode(Name = "hinge_node")
        self.hook_transform.Children.value = [self.hook_geometry]

        #self.hook_transform.Transform.value = avango.gua.make_trans_mat(0.0,TRANSLATEY,0.0)

        #No translation for this one?

        if PARENT_NODE is not None:
            PARENT_NODE.Children.value.append(self.hook_transform)

    ### callback functions ###
    
    @field_has_changed(sf_mat)
    def sf_mat_changed(self):
        _pos = self.sf_mat.value.get_translate() # world position of hook
        
        for _node in self.TARGET_LIST: # iterate over all target nodes
            _bb = _node.BoundingBox.value # get bounding box of a node
            #print(_node.Name.value, _bb.contains(_pos))
            
            if _bb.contains(_pos) == True: # hook position inside bounding box of this node
                _node.Material.value.set_uniform("Color", avango.gua.Vec4(1.0,0.0,0.0,1.0)) # highlight color
            else:
                _node.Material.value.set_uniform("Color", avango.gua.Vec4(1.0,1.0,1.0,1.0)) # default color

       
