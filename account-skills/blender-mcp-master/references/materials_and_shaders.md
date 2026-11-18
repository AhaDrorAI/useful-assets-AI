# Materials & Shader Node Patterns

Comprehensive reference for building materials via Python in Blender 5.0+.

## Table of Contents
1. [Material Basics](#material-basics)
2. [Principled BSDF Presets](#principled-bsdf-presets)
3. [Custom Node Setups](#custom-node-setups)
4. [Procedural Textures](#procedural-textures)
5. [Glass & Transparency](#glass--transparency)
6. [Emission & Volumetrics](#emission--volumetrics)
7. [World / Environment Shaders](#world--environment-shaders)

---

## Material Basics

Every material operation follows this pattern:

```python
# Create material
mat = bpy.data.materials.new("MaterialName")
mat.use_nodes = True

# Access nodes
nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Clear all nodes for custom setup (optional)
nodes.clear()

# Assign to object
obj.data.materials.append(mat)
# Or replace existing: obj.data.materials[0] = mat
```

When you DON'T clear nodes, the default setup includes a Principled BSDF
connected to a Material Output. Access it via:
```python
bsdf = nodes["Principled BSDF"]  # or nodes.get("Principled BSDF")
```

## Principled BSDF Presets

The Principled BSDF is the workhorse shader. Key inputs:

| Input | Range | Description |
|-------|-------|-------------|
| Base Color | (R,G,B,A) | Surface color |
| Metallic | 0.0-1.0 | 0=dielectric, 1=metal |
| Roughness | 0.0-1.0 | 0=mirror, 1=matte |
| IOR | 1.0-3.0 | Index of refraction (glass=1.45) |
| Transmission Weight | 0.0-1.0 | 0=opaque, 1=transparent (Blender 5.0 name) |
| Emission Color | (R,G,B,A) | Glow color |
| Emission Strength | 0.0+ | Glow intensity |
| Alpha | 0.0-1.0 | Transparency (needs blend mode) |

### Common material presets

```python
# Polished metal
bsdf.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1)
bsdf.inputs['Metallic'].default_value = 1.0
bsdf.inputs['Roughness'].default_value = 0.1

# Rough plastic
bsdf.inputs['Base Color'].default_value = (0.8, 0.1, 0.1, 1)
bsdf.inputs['Metallic'].default_value = 0.0
bsdf.inputs['Roughness'].default_value = 0.4

# Wood-like
bsdf.inputs['Base Color'].default_value = (0.4, 0.2, 0.08, 1)
bsdf.inputs['Metallic'].default_value = 0.0
bsdf.inputs['Roughness'].default_value = 0.6

# Rubber
bsdf.inputs['Base Color'].default_value = (0.02, 0.02, 0.02, 1)
bsdf.inputs['Metallic'].default_value = 0.0
bsdf.inputs['Roughness'].default_value = 0.9

# Gold
bsdf.inputs['Base Color'].default_value = (1.0, 0.77, 0.34, 1)
bsdf.inputs['Metallic'].default_value = 1.0
bsdf.inputs['Roughness'].default_value = 0.2

# Chrome mirror
bsdf.inputs['Base Color'].default_value = (0.95, 0.95, 0.95, 1)
bsdf.inputs['Metallic'].default_value = 1.0
bsdf.inputs['Roughness'].default_value = 0.02
```

## Custom Node Setups

### Full custom material pattern
```python
mat = bpy.data.materials.new("Custom")
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links
nodes.clear()

# Build from scratch
output = nodes.new('ShaderNodeOutputMaterial')
output.location = (400, 0)

shader = nodes.new('ShaderNodeBsdfPrincipled')
shader.location = (0, 0)

links.new(shader.outputs['BSDF'], output.inputs['Surface'])
```

### Node positioning
Position nodes on a grid for clean layout. Use increments of ~200:
```python
node.location = (x, y)  # x=left-to-right, y=top-to-bottom
# Typical flow: inputs at -600, processing at -300, shaders at 0, output at 300
```

### Color Ramp
```python
ramp = nodes.new('ShaderNodeValToRGB')
ramp.color_ramp.elements[0].position = 0.0
ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
ramp.color_ramp.elements[1].position = 1.0
ramp.color_ramp.elements[1].color = (1, 1, 1, 1)
# Add intermediate stops:
new_elem = ramp.color_ramp.elements.new(0.5)
new_elem.color = (1, 0, 0, 1)
```

### Map Range
```python
map_range = nodes.new('ShaderNodeMapRange')
map_range.inputs['From Min'].default_value = 0.0
map_range.inputs['From Max'].default_value = 1.0
map_range.inputs['To Min'].default_value = 0.3
map_range.inputs['To Max'].default_value = 0.8
map_range.clamp = True
```

## Procedural Textures

### Noise texture
```python
noise = nodes.new('ShaderNodeTexNoise')
noise.inputs['Scale'].default_value = 5.0
noise.inputs['Detail'].default_value = 8.0
noise.inputs['Roughness'].default_value = 0.5
# Connect Fac output to a Color Ramp for control
```

### Voronoi (cells, organic patterns)
```python
voronoi = nodes.new('ShaderNodeTexVoronoi')
voronoi.feature = 'F1'  # 'F1', 'F2', 'SMOOTH_F1', 'DISTANCE_TO_EDGE'
voronoi.inputs['Scale'].default_value = 10.0
```

### Wave (stripes, rings)
```python
wave = nodes.new('ShaderNodeTexWave')
wave.wave_type = 'BANDS'  # or 'RINGS'
wave.inputs['Scale'].default_value = 3.0
wave.inputs['Distortion'].default_value = 2.0
```

### Texture coordinates
Always add a Texture Coordinate node for proper mapping:
```python
tex_coord = nodes.new('ShaderNodeTexCoord')
# Use 'Object' output for object-space mapping
# Use 'UV' for UV-mapped textures
# Use 'Generated' for auto-generated coordinates
```

## Glass & Transparency

### Simple glass
```python
nodes.clear()
glass = nodes.new('ShaderNodeBsdfGlass')
glass.inputs['Color'].default_value = (0.95, 0.97, 1.0, 1)
glass.inputs['IOR'].default_value = 1.45
glass.inputs['Roughness'].default_value = 0.0
output = nodes.new('ShaderNodeOutputMaterial')
links.new(glass.outputs['BSDF'], output.inputs['Surface'])
```

### IOR reference values
| Material | IOR |
|----------|-----|
| Air | 1.000 |
| Water | 1.333 |
| Glass (crown) | 1.52 |
| Glass (flint) | 1.62 |
| Diamond | 2.42 |
| Ice | 1.31 |
| Amber | 1.55 |
| Crystal | 2.00 |

### Dispersion simulation
Blender doesn't have native spectral rendering, but you can fake dispersion
by mixing 3 Glass BSDFs with different IOR per color channel:

```python
glass_r = nodes.new('ShaderNodeBsdfGlass')
glass_r.inputs['Color'].default_value = (1, 0, 0, 1)
glass_r.inputs['IOR'].default_value = 1.330  # Red bends least

glass_g = nodes.new('ShaderNodeBsdfGlass')
glass_g.inputs['Color'].default_value = (0, 1, 0, 1)
glass_g.inputs['IOR'].default_value = 1.335

glass_b = nodes.new('ShaderNodeBsdfGlass')
glass_b.inputs['Color'].default_value = (0, 0, 1, 1)
glass_b.inputs['IOR'].default_value = 1.343  # Violet bends most

mix1 = nodes.new('ShaderNodeMixShader')
mix1.inputs['Fac'].default_value = 0.5
links.new(glass_r.outputs['BSDF'], mix1.inputs[1])
links.new(glass_g.outputs['BSDF'], mix1.inputs[2])

mix2 = nodes.new('ShaderNodeMixShader')
mix2.inputs['Fac'].default_value = 0.33
links.new(mix1.outputs['Shader'], mix2.inputs[1])
links.new(glass_b.outputs['BSDF'], mix2.inputs[2])
```

### Transparent BSDF (for overlays, holograms)
```python
transparent = nodes.new('ShaderNodeBsdfTransparent')
# Mix with another shader for partial transparency
mix = nodes.new('ShaderNodeMixShader')
mix.inputs['Fac'].default_value = 0.3  # 0.3 = 70% transparent
```

## Emission & Volumetrics

### Emission shader
```python
emit = nodes.new('ShaderNodeEmission')
emit.inputs['Color'].default_value = (1, 0.9, 0.5, 1)
emit.inputs['Strength'].default_value = 10.0
```

### Volume scatter (fog/atmosphere)
WARNING: Expensive to render. Keep density low.
```python
# On world shader:
vol = nodes.new('ShaderNodeVolumeScatter')
vol.inputs['Color'].default_value = (0.5, 0.55, 0.7, 1)
vol.inputs['Density'].default_value = 0.003  # Keep below 0.01
links.new(vol.outputs['Volume'], output.inputs['Volume'])
```

### Volume absorption (colored glass, underwater)
```python
vol_abs = nodes.new('ShaderNodeVolumeAbsorption')
vol_abs.inputs['Color'].default_value = (0.1, 0.4, 0.8, 1)
vol_abs.inputs['Density'].default_value = 0.5
```

## World / Environment Shaders

### Gradient sky
```python
world = bpy.context.scene.world
world.use_nodes = True
nodes = world.node_tree.nodes
links = world.node_tree.links
nodes.clear()

tex_coord = nodes.new('ShaderNodeTexCoord')
separate = nodes.new('ShaderNodeSeparateXYZ')
links.new(tex_coord.outputs['Generated'], separate.inputs['Vector'])

ramp = nodes.new('ShaderNodeValToRGB')
links.new(separate.outputs['Z'], ramp.inputs['Fac'])
ramp.color_ramp.elements[0].color = (0.2, 0.3, 0.5, 1)  # Horizon
ramp.color_ramp.elements[1].color = (0.05, 0.08, 0.2, 1)  # Zenith

bg = nodes.new('ShaderNodeBackground')
bg.inputs['Strength'].default_value = 1.0
links.new(ramp.outputs['Color'], bg.inputs['Color'])

output = nodes.new('ShaderNodeOutputWorld')
links.new(bg.outputs['Background'], output.inputs['Surface'])
```

### Angular/position-based shader
Useful for physics simulations (e.g., rainbow projection):
```python
geom = nodes.new('ShaderNodeNewGeometry')
# Use geom.outputs['Position'] for world-space position
# Use geom.outputs['Normal'] for surface normal direction
# Use geom.outputs['Incoming'] for camera ray direction

# Compute angle from a reference direction:
dot = nodes.new('ShaderNodeVectorMath')
dot.operation = 'DOT_PRODUCT'
links.new(geom.outputs['Normal'], dot.inputs[0])
# Connect reference direction to dot.inputs[1]

acos = nodes.new('ShaderNodeMath')
acos.operation = 'ARCCOSINE'
links.new(dot.outputs['Value'], acos.inputs[0])
# Result is angle in radians
```
