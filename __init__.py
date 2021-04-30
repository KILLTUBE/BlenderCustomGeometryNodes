bl_info = {
    "name": "KILLTUBE",
    "blender": (2, 92, 0),
    "category": "Object",
}

import bpy
import nodeitems_utils
from nodeitems_utils import (
    NodeCategory,
    NodeItem,
    NodeItemCustom,
)

from .MyCustomNode import (
    MyCustomNode
)
from bpy.types import NodeTree, Node, NodeSocket

#####


# Implementation of custom nodes from Python


# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
class MyCustomTree(NodeTree):
    # Description string
    '''A custom node tree type that will show up in the editor type list'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'CustomTreeType'
    # Label for nice name display
    bl_label = "Custom Node Tree"
    # Icon identifier
    bl_icon = 'NODETREE'


# Custom socket type
class MyCustomSocket(NodeSocket):
    # Description string
    '''Custom node socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'CustomSocketType'
    # Label for nice name display
    bl_label = "Custom Node Socket"

    # Enum items list
    my_items = (
        ('DOWN', "Down", "Where your feet are"),
        ('UP', "Up", "Where your head should be"),
        ('LEFT', "Left", "Not right"),
        ('RIGHT', "Right", "Not left"),
    )

    my_enum_prop: bpy.props.EnumProperty(
        name="Direction",
        description="Just an example",
        items=my_items,
        default='UP',
    )

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "my_enum_prop", text=text)

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)


# Mix-in class for all custom nodes in this tree type.
# Defines a poll function to enable instantiation.
class MyCustomTreeNode:
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'CustomTreeType'




#####


### Node Categories ###
# Node categories are a python system for automatically
# extending the Add menu, toolbar panels and search operator.
# For more examples see release/scripts/startup/nodeitems_builtins.py

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

# our own base class with an appropriate poll function,
# so the categories only show up in our own tree type


class MyNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'CustomTreeType'


# all categories in a list
node_categories = [
    # identifier, label, items list
    MyNodeCategory('SOMENODES', "Some Nodes", items=[
        # our basic node
        NodeItem("CustomNodeType"),
    ]),
    MyNodeCategory('OTHERNODES', "Other Nodes", items=[
        # the node item can have additional settings,
        # which are applied to new nodes
        # NB: settings values are stored as string expressions,
        # for this reason they should be converted to strings using repr()
        NodeItem("CustomNodeType", label="Node A", settings={
            "my_string_prop": repr("Lorem ipsum dolor sit amet"),
            "my_float_prop": repr(1.0),
        }),
        NodeItem("CustomNodeType", label="Node B", settings={
            "my_string_prop": repr("consectetur adipisicing elit"),
            "my_float_prop": repr(2.0),
        }),
    ]),
]



#####

# Subclasses for standard node types

class SortedNodeCategory(NodeCategory):
    def __init__(self, identifier, name, description="", items=None):
        # for builtin nodes the convention is to sort by name
        if isinstance(items, list):
            items = sorted(items, key=lambda item: item.label.lower())

        super().__init__(identifier, name, description, items)


class CompositorNodeCategory(SortedNodeCategory):
    @classmethod
    def poll(cls, context):
        return (context.space_data.type == 'NODE_EDITOR' and
                context.space_data.tree_type == 'CompositorNodeTree')


class ShaderNodeCategory(SortedNodeCategory):
    @classmethod
    def poll(cls, context):
        return (context.space_data.type == 'NODE_EDITOR' and
                context.space_data.tree_type == 'ShaderNodeTree')


class TextureNodeCategory(SortedNodeCategory):
    @classmethod
    def poll(cls, context):
        return (context.space_data.type == 'NODE_EDITOR' and
                context.space_data.tree_type == 'TextureNodeTree')


class GeometryNodeCategory(SortedNodeCategory):
    @classmethod
    def poll(cls, context):
        return (context.space_data.type == 'NODE_EDITOR' and
                context.space_data.tree_type == 'GeometryNodeTree')



# generic node group items generator for shader, compositor, geometry and texture node groups
def node_group_items(context):
    if context is None:
        return
    space = context.space_data
    if not space:
        return
    ntree = space.edit_tree
    if not ntree:
        return

    yield NodeItemCustom(draw=group_tools_draw)

    def contains_group(nodetree, group):
        if nodetree == group:
            return True
        else:
            for node in nodetree.nodes:
                if node.bl_idname in node_tree_group_type.values() and node.node_tree is not None:
                    if contains_group(node.node_tree, group):
                        return True
        return False

    for group in context.blend_data.node_groups:
        if group.bl_idname != ntree.bl_idname:
            continue
        # filter out recursive groups
        if contains_group(group, ntree):
            continue
        # filter out hidden nodetrees
        if group.name.startswith('.'):
            continue
        yield NodeItem(node_tree_group_type[group.bl_idname],
                       group.name,
                       {"node_tree": "bpy.data.node_groups[%r]" % group.name})


# menu entry for node group tools
def group_tools_draw(self, layout, context):
    layout.operator("node.group_make")
    layout.operator("node.group_ungroup")
    layout.separator()

class KungsNodeItem:
    def __init__(self, nodetype, label=None, settings=None, poll=None):

        if settings is None:
            settings = {}

        self.nodetype = nodetype
        self._label = label
        self.settings = settings
        self.poll = poll

    @property
    def label(self):
        if self._label:
            return self._label
        else:
            # if no custom label is defined, fall back to the node type UI name
            bl_rna = bpy.types.Node.bl_rna_get_subclass(self.nodetype)
            if bl_rna is not None:
                return bl_rna.name
            else:
                return "kungs label"

    @property
    def translation_context(self):
        if self._label:
            return bpy.app.translations.contexts.default
        else:
            # if no custom label is defined, fall back to the node type UI name
            bl_rna = bpy.types.Node.bl_rna_get_subclass(self.nodetype)
            if bl_rna is not None:
                return bl_rna.translation_context
            else:
                return bpy.app.translations.contexts.default

    # NB: is a staticmethod because called with an explicit self argument
    # NodeItemCustom sets this as a variable attribute in __init__
    @staticmethod
    def draw(self, layout, _context):
        props = layout.operator("node.add_node", text=self.label, text_ctxt=self.translation_context)
        props.type = self.nodetype
        props.use_transform = True

        for setting in self.settings.items():
            ops = props.settings.add()
            ops.name = setting[0]
            ops.value = setting[1]

class ObjectMoveX(bpy.types.GeometryNode):
#class ObjectMoveX(bpy.types.Operator):
    """My Object Moving Script"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.move_x"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Move X by One"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    type = 'NODE_EDITOR'
    tree_type = 'GeometryNodeTree'

    def execute(self, context):        # execute() is called when running the operator.
        #print("Hello World execute")
        # The original script
        scene = context.scene
        for obj in scene.objects:
            obj.location.x += 1.0

        return {'FINISHED'}            # Lets Blender know the operator finished successfully.
    @classmethod
    def poll(self, node_tree):
        return True

def geometry_node_group_empty_new(context):
    group = bpy.data.node_groups.new("Geometry Nodes", 'GeometryNodeTree')
    group.inputs.new('NodeSocketGeometry', "Geometry")
    group.outputs.new('NodeSocketGeometry', "Geometry")
    input_node = group.nodes.new('NodeGroupInput')
    output_node = group.nodes.new('NodeGroupOutput')
    output_node.is_active_output = True

    input_node.select = False
    output_node.select = False

    input_node.location.x = -200 - input_node.width
    output_node.location.x = 200

    group.links.new(output_node.inputs[0], input_node.outputs[0])

    return group

geometry_node_categories = [
    ## identifier, label, items list
    #GeometryNodeCategory('GEO_SOMENODES', "Some Nodes", items=[
    ##MyNodeCategory('GEO_SOMENODES', "Some Nodes", items=[
    #    # our basic node
    #    NodeItem("CustomNodeType"),
    #]),
    #GeometryNodeCategory('GEO_OTHERNODES', "Other Nodes", items=[
    ##MyNodeCategory('GEO_OTHERNODES', "Other Nodes", items=[
        # the node item can have additional settings,
        # which are applied to new nodes
        # NB: settings values are stored as string expressions,
        # for this reason they should be converted to strings using repr()

    #]),

    #node_categories,
    GeometryNodeCategory("GEO_KILLTUBE", "KILLTUBE", items=[
        #NodeItemCustom(draw=group_tools_draw),
        #geometry_node_group_empty_new(context),
        #KungsNodeItem("MyCustomNode"),
        NodeItem("CustomNodeType"),
        NodeItem("CustomNodeType", label="Node A", settings={
            "my_string_prop": repr("Lorem ipsum dolor sit amet"),
            "my_float_prop": repr(1.0),
        }),
        NodeItem("CustomNodeType", label="Node B", settings={
            "my_string_prop": repr("consectetur adipisicing elit"),
            "my_float_prop": repr(2.0),
        }),
    ]),
    # Geometry Nodes
    GeometryNodeCategory("GEO_ATTRIBUTE", "Attributezzzzz", items=[
        #NodeItemCustom(draw=group_tools_draw),
        #geometry_node_group_empty_new(context),
        #KungsNodeItem("MyCustomNode"),
        #NodeItem("CustomNodeType"),
        #NodeItem("GeometryNodeAttributeRandomize"),
        #NodeItem("GeometryNodeAttributeRandomize"),
        NodeItem("GeometryNodeAttributeRandomize"),
        NodeItem("GeometryNodeAttributeMath"),
        NodeItem("GeometryNodeAttributeCompare"),
        NodeItem("GeometryNodeAttributeFill"),
        NodeItem("GeometryNodeAttributeMix"),
        NodeItem("GeometryNodeAttributeColorRamp"),
        NodeItem("GeometryNodeAttributeVectorMath"),
    ]),
    GeometryNodeCategory("GEO_COLOR", "Color", items=[
        NodeItem("ShaderNodeValToRGB"),
        NodeItem("ShaderNodeSeparateRGB"),
        NodeItem("ShaderNodeCombineRGB"),
    ]),
    GeometryNodeCategory("GEO_GEOMETRY", "Geometry", items=[
        NodeItem("GeometryNodeTransform"),
        NodeItem("GeometryNodeJoinGeometry"),
    ]),
    GeometryNodeCategory("GEO_INPUT", "Input", items=[
        NodeItem("GeometryNodeObjectInfo"),
        NodeItem("FunctionNodeRandomFloat"),
        NodeItem("ShaderNodeValue"),
        NodeItem("FunctionNodeInputVector"),
    ]),
    GeometryNodeCategory("GEO_MESH", "Mesh", items=[
        NodeItem("GeometryNodeBoolean"),
        NodeItem("GeometryNodeTriangulate"),
        NodeItem("GeometryNodeEdgeSplit"),
        NodeItem("GeometryNodeSubdivisionSurface"),
    ]),
    GeometryNodeCategory("GEO_POINT", "Point", items=[
        NodeItem("GeometryNodePointDistribute"),
        NodeItem("GeometryNodePointInstance"),
        NodeItem("GeometryNodePointSeparate"),
        NodeItem("GeometryNodePointScale"),
        NodeItem("GeometryNodePointTranslate"),
        NodeItem("GeometryNodeRotatePoints"),
        NodeItem("GeometryNodeAlignRotationToVector"),
    ]),
    GeometryNodeCategory("GEO_UTILITIES", "Utilities", items=[
        NodeItem("ShaderNodeMapRange"),
        NodeItem("ShaderNodeClamp"),
        NodeItem("ShaderNodeMath"),
        NodeItem("FunctionNodeBooleanMath"),
        NodeItem("FunctionNodeFloatCompare"),
    ]),
    GeometryNodeCategory("GEO_VECTOR", "Vector", items=[
        NodeItem("ShaderNodeSeparateXYZ"),
        NodeItem("ShaderNodeCombineXYZ"),
        NodeItem("ShaderNodeVectorMath"),
    ]),
    GeometryNodeCategory("GEO_GROUP", "Group", items=node_group_items),
    GeometryNodeCategory("GEO_LAYOUT", "Layout", items=[
        NodeItem("NodeFrame"),
        NodeItem("NodeReroute"),
    ]),
    # NodeItem("FunctionNodeCombineStrings"),
    # NodeItem("FunctionNodeGroupInstanceID"),
]

classes = (
    #MyCustomTree,
    MyCustomSocket,
    MyCustomNode,
)

def register():
    #nodeitems_utils.register_node_categories('SHADER', shader_node_categories)
    #nodeitems_utils.register_node_categories('COMPOSITING', compositor_node_categories)
    #nodeitems_utils.register_node_categories('TEXTURE', texture_node_categories)

    #bpy.utils.register_class(KungsNodeItem)
    #bpy.utils.register_class(MyCustomNode)
    #bpy.utils.register_class(CustomNodeType)



    #nodeitems_utils.register_nodes('GEOMETRY', MyCustomNode)
    

    try:
        nodeitems_utils.unregister_node_categories('GEOMETRY')
    except:
        pass

    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    nodeitems_utils.register_node_categories('GEOMETRY', geometry_node_categories)

    # Doesn't do anything it seems:
    #try:
    #    nodeitems_utils.unregister_node_categories('CUSTOM_NODES')
    #except:
    #    pass
    #nodeitems_utils.register_node_categories('CUSTOM_NODES', node_categories)
    #bpy.utils.register_class(ObjectMoveX)


def unregister():
    #nodeitems_utils.unregister_node_categories('SHADER')
    #nodeitems_utils.unregister_node_categories('COMPOSITING')
    #nodeitems_utils.unregister_node_categories('TEXTURE')
    nodeitems_utils.unregister_node_categories('GEOMETRY')
    #bpy.utils.unregister_class(ObjectMoveX)
    #nodeitems_utils.unregister_node_categories('CUSTOM_NODES')

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()