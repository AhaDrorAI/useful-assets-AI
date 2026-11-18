# Geometry Nodes Reference (Blender 5.0)

Guide to using Geometry Nodes via Python, including the 27+ new volume
nodes added in Blender 5.0.

## Table of Contents
1. [Creating Geometry Node Groups](#creating-geometry-node-groups)
2. [Common Nodes via Python](#common-nodes-via-python)
3. [New in Blender 5.0](#new-in-blender-50)
4. [Instancing Patterns](#instancing-patterns)
5. [Particle Distribution](#particle-distribution)

---

## Creating Geometry Node Groups

```python
# Add Geometry Nodes modifier to an object
obj = bpy.data.objects["MyObject"]
mod = obj.modifiers.new("GeoNodes", 'NODES')

# Create a new node group
group = bpy.data.node_groups.new("MyNodeGroup", 'GeometryNodeTree')
mod.node_group = group

# Access the group's nodes
nodes = group.nodes
links = group.links

# Every group needs Group Input and Group Output
input_node = nodes.new('NodeGroupInput')
input_node.location = (-400, 0)

output_node = nodes.new('NodeGroupOutput')
output_node.location = (400, 0)

# Create a socket on the group input/output
group.interface.new_socket('Geometry', in_out='INPUT', socket_type='NodeSocketGeometry')
group.interface.new_socket('Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
```

## Common Nodes via Python

### Mesh primitives
```python
cube = nodes.new('GeometryNodeMeshCube')
cube.inputs['Size'].default_value = (2, 2, 2)

sphere = nodes.new('GeometryNodeMeshUVSphere')
sphere.inputs['Segments'].default_value = 32
sphere.inputs['Rings'].default_value = 16
sphere.inputs['Radius'].default_value = 1.0

cylinder = nodes.new('GeometryNodeMeshCylinder')
grid = nodes.new('GeometryNodeMeshGrid')
cone = nodes.new('GeometryNodeMeshCone')
```

### Transforms
```python
transform = nodes.new('GeometryNodeTransform')
# Inputs: Translation, Rotation, Scale

set_position = nodes.new('GeometryNodeSetPosition')
# For per-vertex displacement
```

### Instancing
```python
instance_on_points = nodes.new('GeometryNodeInstanceOnPoints')
# Connect points geometry to 'Points'
# Connect instance geometry to 'Instance'
# Optionally connect scale, rotation per-instance

realize = nodes.new('GeometryNodeRealizeInstances')
# Converts instances to real geometry (heavier but editable)
```

### Math & utilities
```python
math_node = nodes.new('ShaderNodeMath')  # Same as shader math
math_node.operation = 'ADD'  # MULTIPLY, DIVIDE, POWER, SQRT, etc.

vector_math = nodes.new('ShaderNodeVectorMath')
vector_math.operation = 'NORMALIZE'  # DOT_PRODUCT, CROSS_PRODUCT, etc.

random = nodes.new('FunctionNodeRandomValue')
# Outputs random float/vector/int per element
```

### Attribute operations
```python
# Capture attribute
capture = nodes.new('GeometryNodeCaptureAttribute')

# Named attribute
store = nodes.new('GeometryNodeStoreNamedAttribute')
store.inputs['Name'].default_value = "my_attr"

# Position
position = nodes.new('GeometryNodeInputPosition')

# Normal
normal = nodes.new('GeometryNodeInputNormal')

# Index
index = nodes.new('GeometryNodeInputIndex')
```

## New in Blender 5.0

### Combine Bundle / Separate Bundle
Group multiple data connections into a single "bundle" socket to keep
complex graphs tidy:

```python
combine = nodes.new('GeometryNodeCombineBundle')
# Connect multiple outputs into the bundle
separate = nodes.new('GeometryNodeSeparateBundle')
# Extract individual connections from a bundle
```

### Volume Grid Nodes (27 new)
Blender 5.0 introduces a new **Volume Grid** socket type and nodes for
working with volumetric data (SDF modeling, fluid sim data, smoke):

```python
# New volume grid socket type in interfaces
group.interface.new_socket('Volume', in_out='INPUT',
                           socket_type='NodeSocketVolumeGrid')

# Volume creation
grid_to_mesh = nodes.new('GeometryNodeVolumeToMesh')
mesh_to_volume = nodes.new('GeometryNodeMeshToVolume')

# Volume grid operations are primarily useful for:
# - SDF-based modeling (Boolean-like operations via distance fields)
# - Accessing fluid/smoke simulation data
# - Creating procedural volumetric effects
# - Voxel-based modeling workflows
```

### Other new nodes
- Improved curve handling nodes
- Enhanced point cloud operations
- Better simulation zone performance

## Instancing Patterns

### Scatter objects on a surface
```python
# Create the base surface (e.g., a grid)
grid = nodes.new('GeometryNodeMeshGrid')
grid.inputs['Size X'].default_value = 10
grid.inputs['Size Y'].default_value = 10
grid.inputs['Vertices X'].default_value = 50
grid.inputs['Vertices Y'].default_value = 50

# Distribute points
distribute = nodes.new('GeometryNodeDistributePointsOnFaces')
distribute.distribute_method = 'RANDOM'
distribute.inputs['Density'].default_value = 5.0

# Instance an object on the points
instance = nodes.new('GeometryNodeInstanceOnPoints')

# Connect: grid → distribute → instance.Points
# Also need: object reference for what to instance

# Object info node to reference an existing object
obj_info = nodes.new('GeometryNodeObjectInfo')
# Set obj_info.inputs['Object'] via Python:
# This requires setting the default value to the object
```

### Random scale and rotation per instance
```python
random_scale = nodes.new('FunctionNodeRandomValue')
random_scale.data_type = 'FLOAT_VECTOR'
# Connect to Instance On Points > Scale

random_rot = nodes.new('FunctionNodeRandomValue')
random_rot.data_type = 'FLOAT_VECTOR'
# Connect to Instance On Points > Rotation
```

## Particle Distribution

For creating rain, snow, or scattered elements:

```python
# Method 1: Geometry Nodes (preferred in 5.0)
# Use Distribute Points on Faces + Instance on Points

# Method 2: Direct Python (quick & dirty)
import random
for i in range(100):
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.05,
        location=(random.uniform(-10,10),
                  random.uniform(-10,10),
                  random.uniform(0,10))
    )
    obj = bpy.context.active_object
    obj.name = f"Particle_{i}"

# Method 3: Shared mesh data (memory efficient)
mesh = bpy.data.meshes.new("SharedMesh")
# Create mesh data once...
for i in range(100):
    obj = bpy.data.objects.new(f"Instance_{i}", mesh)
    obj.location = (random.uniform(-10,10), ...)
    collection.objects.link(obj)
```
