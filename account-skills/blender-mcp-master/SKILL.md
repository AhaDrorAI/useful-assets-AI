---
name: blender-mcp-master
description: >
  Comprehensive skill for controlling Blender via MCP (Model Context Protocol).
  Use this skill whenever the user asks to create 3D scenes, models, animations,
  materials, render images, or do anything in Blender. Triggers on: "blender",
  "3D model", "3D scene", "render", "mesh", "sculpt", "geometry nodes",
  "material", "shader", "texture", "HDRI", "animation", "rigging", "UV",
  "Cycles", "EEVEE", "viewport", ".blend file", "Poly Haven", "Sketchfab",
  "Hyper3D", or any reference to 3D creation. Also trigger when the user has
  Blender MCP connected and asks to "make", "build", "design", or "create"
  something visual — even if they don't say "Blender" explicitly. This skill
  is MANDATORY reading before writing ANY execute_blender_code calls.
metadata:
  last_reviewed: "2026-11-18"
  review_every_days: "90"
---

# Blender MCP Master Skill

This skill turns you into an expert Blender operator via the Blender MCP server.
It covers scene management, modeling, materials, rendering, and asset pipelines
for **Blender 5.0.1** (December 2025 release, 132 corrective fixes over 5.0.0).

## Why this skill exists

Blender's Python API is enormous and full of version-specific gotchas. Without
guidance, you'll waste tokens on deprecated APIs, trigger crashes from removed
functions, and produce renders that are black screens. This skill encodes
hard-won patterns from real MCP sessions so you can write correct code on the
first try.

---

## Available MCP Tools

You have these tools when Blender MCP is connected:

| Tool | Purpose |
|------|---------|
| `execute_blender_code` | Run arbitrary Python in Blender's context — your primary workhorse |
| `get_scene_info` | Query objects, materials, lights, cameras — always call this first |
| `get_object_info` | Deep-dive on a specific object's properties |
| `get_viewport_screenshot` | Capture what the 3D viewport currently shows |
| `search_polyhaven_assets` | Find free HDRIs, textures, and models on Poly Haven |
| `download_polyhaven_asset` | Import a Poly Haven asset into the scene |
| `set_texture` | Apply a downloaded Poly Haven texture to an object |
| `search_sketchfab_models` | Search Sketchfab's library |
| `download_sketchfab_model` | Import a Sketchfab model at a target size |
| `generate_hyper3d_model_via_text` | AI-generate a 3D model from a text prompt (uses Hyper3D credits) |
| `poll_rodin_job_status` | Check whether a Hyper3D generation has finished |
| `import_generated_asset` | Import a finished Hyper3D model into the scene |

Tool names come from the Blender MCP server and can change between versions. If a tool in this table is missing, list the tools the server actually offers and use the closest match; do not call a tool that is not offered.

---

## Golden Rules

These rules prevent the most common MCP session failures:

### 0. Safety boundaries for `execute_blender_code`
`execute_blender_code` runs arbitrary Python on the user's own machine, with the
user's file permissions. Inside it:

- Do not read, write or delete files outside Blender's temp directory and the
  folder the user named for output.
- Do not install packages (`pip`, `ensurepip`), add-ons or extensions unless the
  user asks for that specific item.
- Do not make network requests from Python. Use the MCP asset tools for downloads.
- Do not save over an existing `.blend` file. Save to a new filename, or ask first.

### 1. Always start with `get_scene_info` and the Blender version
Before touching anything, know what exists and which Blender is running:

```python
import bpy; print(bpy.app.version_string)
```

If the version is not 5.0.x, the breaking-change list in rule 3 may not apply.
Say so, and check an API call in the Python console before relying on it.

**Protect the user's scene.** Treat every existing object as the user's work.
Object names do not prove a scene is untouched: a user can reshape the default
Cube without renaming it. Do not delete, rename, move or modify existing objects
unless the user asks for it in this conversation. Add new objects alongside instead.

If the new scene needs the existing objects gone (for example, the default Cube
sits where the new subject goes), ask once: "The scene has [objects]. Delete them,
or keep them and place the new scene elsewhere?" Delete only after a yes.

### 2. Keep `execute_blender_code` calls small and incremental
Break complex work into steps of 20-40 lines each. If one step fails, you don't
lose everything. Print a confirmation message at the end of every code block so
you know it ran.

### 3. Blender 5.0.1 API — critical breaking changes
Read `references/blender5_api.md` for the full list, but these bite hardest:

- **EEVEE engine ID**: Use `'BLENDER_EEVEE'` not `'BLENDER_EEVEE_NEXT'`
- **BGL is gone**: No `import bgl`. Use `gpu` module instead
- **Compositor**: `scene.node_tree` is removed → use `scene.compositing_node_group`
- **`scene.use_nodes`**: Deprecated, always returns True. Don't set it.
- **Brush enums**: `sculpt_tool` → `sculpt_brush_type` (all paint modes)
- **Legacy Action API**: `action.fcurves`, `action.groups`, `action.id_root` removed
- **ImageFormatSettings**: Set `media_type` before `file_format`
- **Runtime properties**: No more `scene['custom']` dict access for bpy.props

### 4. Rendering takes time — manage the MCP timeout
The MCP server has a ~60 second timeout. Renders that exceed this will error.

**Resolution budget for live renders:**

| Samples | Max safe resolution | Approx time |
|---------|-------------------|-------------|
| 16 | 1280×720 | ~15-25s |
| 32 | 960×540 | ~20-35s |
| 64 | 640×360 | ~20-40s |
| 128+ | 640×360 only | ~40-55s |

**Speed tips:**
- Hide objects you don't need (`obj.hide_render = True`)
- Reduce rain/particles/instanced objects
- Remove world Volume shaders (huge perf hit)
- Use denoising (`scene.cycles.use_denoising = True`)
- For audit renders, use 16-32 samples at 960×540

### 5. File paths — detect the OS
Blender runs on the user's machine. Detect the OS before writing files:
```python
import tempfile, os, platform
temp_dir = tempfile.gettempdir()  # Works on all platforms
# Windows: C:\Users\...\AppData\Local\Temp
# macOS:   /var/folders/...
# Linux:   /tmp
```
Never hardcode `/tmp/` — it doesn't exist on Windows.

### 6. Viewport screenshots vs renders
- `get_viewport_screenshot` → instant, shows material preview or rendered viewport
- `bpy.ops.render.render(write_still=True)` → full Cycles/EEVEE render to file
Use screenshots for quick checks, renders for final output.

---

## Workflow Patterns

### Pattern A: Scene Setup (most common)

```
1. get_scene_info → know what exists
2. execute_blender_code → clear or modify existing objects (only after the user agrees; see rule 1)
3. execute_blender_code → create new objects + materials (one step per concept)
4. execute_blender_code → set up lighting
5. execute_blender_code → position camera
6. execute_blender_code → configure render settings
7. get_viewport_screenshot → quick visual check
8. execute_blender_code → render to file (if user wants an image)
```

### Pattern B: Asset-Based Scene

```
1. get_scene_info
2. search_polyhaven_assets → find HDRI, textures, models
3. download_polyhaven_asset → import into scene
4. set_texture → apply materials
5. execute_blender_code → arrange, light, camera
6. render
```

### Pattern C: AI Model Generation

```
1. generate_hyper3d_model_via_text → start generation
2. poll_rodin_job_status → wait for completion
3. import_generated_asset → bring into scene
4. execute_blender_code → scale, position, add materials/lighting
5. render
```

---

## Materials & Shading

For detailed node setup patterns, read `references/materials_and_shaders.md`.

### Quick material creation
```python
mat = bpy.data.materials.new("MyMaterial")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (0.8, 0.2, 0.1, 1.0)
bsdf.inputs['Metallic'].default_value = 0.0
bsdf.inputs['Roughness'].default_value = 0.4
obj.data.materials.append(mat)
```

### Emission (glowing objects)
```python
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links
nodes.clear()
emit = nodes.new('ShaderNodeEmission')
emit.inputs['Color'].default_value = (1, 0.9, 0.5, 1)
emit.inputs['Strength'].default_value = 10.0
output = nodes.new('ShaderNodeOutputMaterial')
links.new(emit.outputs['Emission'], output.inputs['Surface'])
```

### Glass / transparent
```python
glass = nodes.new('ShaderNodeBsdfGlass')
glass.inputs['Color'].default_value = (0.95, 0.97, 1.0, 1.0)
glass.inputs['IOR'].default_value = 1.45  # Glass=1.45, Water=1.33, Diamond=2.42
glass.inputs['Roughness'].default_value = 0.0
```

### Mixing shaders (e.g., partial transparency)
```python
mix = nodes.new('ShaderNodeMixShader')
mix.inputs['Fac'].default_value = 0.5  # 0=first shader, 1=second
links.new(shader_a.outputs[0], mix.inputs[1])
links.new(shader_b.outputs[0], mix.inputs[2])
links.new(mix.outputs['Shader'], output.inputs['Surface'])
```

---

## Rendering

For full rendering reference, read `references/rendering.md`.

### Cycles setup (physically accurate)
```python
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 32
scene.cycles.use_denoising = True
scene.cycles.max_bounces = 12
scene.cycles.transmission_bounces = 8  # Important for glass/water
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
```

### EEVEE setup (fast preview)
```python
scene.render.engine = 'BLENDER_EEVEE'  # NOT 'BLENDER_EEVEE_NEXT' in 5.0!
```

### Camera setup
```python
import math
bpy.ops.object.camera_add(location=(7, -6, 5))
cam = bpy.context.active_object
cam.rotation_euler = (math.radians(63), 0, math.radians(47))
cam.data.lens = 35  # mm focal length (50=normal, 24=wide, 85=portrait)
bpy.context.scene.camera = cam  # Set as active camera
```

### Safe render-to-file pattern
```python
import os, tempfile
temp_dir = tempfile.gettempdir()
path = os.path.join(temp_dir, "my_render.png")
scene.render.filepath = path
scene.render.image_settings.file_format = 'PNG'
bpy.ops.render.render(write_still=True)
print(f"Rendered to: {path} ({os.path.getsize(path)} bytes)")
```

---

## Object Creation Cheatsheet

```python
# Primitives
bpy.ops.mesh.primitive_cube_add(size=2, location=(0,0,0))
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, segments=32, ring_count=16, location=(0,0,0))
bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, location=(0,0,0))
bpy.ops.mesh.primitive_plane_add(size=10, location=(0,0,0))
bpy.ops.mesh.primitive_cone_add(radius1=1, depth=2, location=(0,0,0))
bpy.ops.mesh.primitive_torus_add(major_radius=1, minor_radius=0.3, location=(0,0,0))

# After creation, the new object is bpy.context.active_object
obj = bpy.context.active_object
obj.name = "MyObject"
bpy.ops.object.shade_smooth()  # Smooth shading

# Transforms
obj.location = (x, y, z)
obj.rotation_euler = (rx, ry, rz)  # Radians!
obj.scale = (sx, sy, sz)
```

---

## Lights

```python
# Sun (parallel rays, good for outdoor scenes)
bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
sun = bpy.context.active_object
sun.data.energy = 5.0
sun.data.color = (1.0, 0.98, 0.95)
sun.data.angle = math.radians(0.53)  # Angular size of sun disc

# Point light
bpy.ops.object.light_add(type='POINT', location=(2, -2, 3))
point = bpy.context.active_object
point.data.energy = 100  # Watts
point.data.shadow_soft_size = 0.5  # Soft shadow radius

# Area light (best for studio/product shots)
bpy.ops.object.light_add(type='AREA', location=(3, -3, 4))
area = bpy.context.active_object
area.data.energy = 200
area.data.size = 2  # Larger = softer shadows
```

---

## World / Environment

```python
world = bpy.context.scene.world
if not world:
    world = bpy.data.worlds.new("World")
    bpy.context.scene.world = world
world.use_nodes = True
nodes = world.node_tree.nodes
links = world.node_tree.links

# Solid color background
bg = nodes['Background']
bg.inputs['Color'].default_value = (0.05, 0.05, 0.1, 1)
bg.inputs['Strength'].default_value = 1.0

# HDRI environment (use Poly Haven!)
# search_polyhaven_assets(asset_type="hdris", categories="outdoor")
# download_polyhaven_asset(asset_id="...", asset_type="hdris", resolution="2k")
```

**Performance warning:** World Volume shaders (like `ShaderNodeVolumeScatter`)
dramatically slow rendering. Use only when atmospheric effects are essential,
and keep density below 0.005.

---

## Geometry Nodes (Blender 5.0)

For the full reference including all 27 new volume nodes, read
`references/geometry_nodes.md`.

Key Blender 5.0 additions:
- **Combine Bundle / Separate Bundle** — group multiple socket connections
- **27 new Volume Grid nodes** — SDF modeling, fluid/smoke data access
- **New volume grid socket type**

---

## Asset Integration

For Poly Haven, Sketchfab, and Hyper3D patterns, read
`references/polyhaven_sketchfab.md`.

**Licences and credits.** Poly Haven assets are CC0. Sketchfab models carry
per-model licences (some forbid commercial use or need attribution): report the
model's licence and author to the user when you import it. Hyper3D generation
spends the user's credits: ask before each generation.

Quick reference:
```python
# Check if integrations are available
get_polyhaven_status()
get_sketchfab_status()
get_hyper3d_status()

# Search and download
search_polyhaven_assets(asset_type="textures", categories="wood")
download_polyhaven_asset(asset_id="wooden_planks", asset_type="textures", resolution="2k")
set_texture(object_name="Floor", texture_id="wooden_planks")
```

---

## Common Pitfalls & Fixes

| Problem | Cause | Fix |
|---------|-------|-----|
| Render is completely black | Camera not set, or pointing wrong way | `scene.camera = cam_object` + check rotation |
| Render times out (~60s) | Too many samples or objects | Reduce samples, hide unneeded objects, remove volumes |
| Glass/water doesn't refract | Transmission bounces too low | `scene.cycles.transmission_bounces = 12` |
| Smooth shading looks faceted | Not enough geometry | Add subdivision or increase mesh segments |
| Material not visible | Not assigned to object | `obj.data.materials.append(mat)` |
| Viewport is black | Wrong shading mode | Set `space.shading.type = 'MATERIAL'` or `'RENDERED'` |
| File save fails with `/tmp/` | Windows system | Use `tempfile.gettempdir()` instead |
| `BLENDER_EEVEE_NEXT` error | Blender 5.0+ renamed it | Use `'BLENDER_EEVEE'` |
| `scene.node_tree` error | Removed in 5.0 | Use `scene.compositing_node_group` |
| `bgl` import error | BGL removed in 5.0 | Use `gpu` module |
| Objects from inside sphere invisible | Backface culling / normals | Flip normals or disable backface culling |
| Emission not visible in viewport | Using Material Preview (EEVEE) | Switch to Rendered mode for proper glow |

---

## Cleanup & Organization

```python
# Delete specific objects
bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.ops.object.delete()

# Clean orphan data. Orphans can include the user's own unused meshes and
# materials (kept with a fake user or awaiting reuse). Run this only on a scene
# you built in this session, or after the user agrees.
for block in bpy.data.meshes:
    if block.users == 0:
        bpy.data.meshes.remove(block)
for block in bpy.data.materials:
    if block.users == 0:
        bpy.data.materials.remove(block)

# Use collections for organization
col = bpy.data.collections.new("MyGroup")
bpy.context.scene.collection.children.link(col)
col.objects.link(obj)

# Hide/show collections
col.hide_viewport = True
col.hide_render = True
```

---

## Multi-Camera Workflow

For complex scenes, create multiple cameras for different views:
```python
cameras = {
    "Main": {"loc": (7,-6,5), "rot": (63,0,47), "lens": 35},
    "Closeup": {"loc": (2,-2,1.5), "rot": (80,0,30), "lens": 50},
    "Top": {"loc": (0,0,20), "rot": (0,0,0), "lens": 24},
}
for name, cfg in cameras.items():
    bpy.ops.object.camera_add(location=cfg["loc"])
    cam = bpy.context.active_object
    cam.name = f"Camera_{name}"
    cam.rotation_euler = tuple(math.radians(a) for a in cfg["rot"])
    cam.data.lens = cfg["lens"]
```
Then switch between them: `scene.camera = bpy.data.objects["Camera_Main"]`

---

## Render Batch Pattern

When the user wants multiple images, render in a loop with minimal settings
and only swap what changes between shots:
```python
for cam_name in ["Camera_Main", "Camera_Closeup", "Camera_Top"]:
    scene.camera = bpy.data.objects[cam_name]
    scene.render.filepath = os.path.join(temp_dir, f"render_{cam_name}.png")
    bpy.ops.render.render(write_still=True)
```
