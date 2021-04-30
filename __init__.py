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
from .MyCustomNode import (MyCustomNode)
from .MyCustomTreeNode import (MyCustomTreeNode)
from .MyCustomTree import (MyCustomTree)
from .MyCustomSocket import (MyCustomSocket)
from .node_group_items import (node_group_items)
from .MyNodeCategory import (MyNodeCategory)
from .geometry_node_group_empty_new import (geometry_node_group_empty_new)
from bpy.types import NodeTree, Node, NodeSocket

### Node Categories ###
# Node categories are a python system for automatically
# extending the Add menu, toolbar panels and search operator.
# For more examples see release/scripts/startup/nodeitems_builtins.py

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem



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


geometry_node_categories = [
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