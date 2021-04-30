import bpy

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
