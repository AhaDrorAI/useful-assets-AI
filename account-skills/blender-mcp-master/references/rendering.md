# Rendering Reference

Complete guide to Cycles and EEVEE rendering via MCP, optimized for the
60-second MCP timeout constraint.

## Table of Contents
1. [Engine Selection](#engine-selection)
2. [Cycles Configuration](#cycles-configuration)
3. [EEVEE Configuration](#eevee-configuration)
4. [MCP Timeout Management](#mcp-timeout-management)
5. [Camera Setup](#camera-setup)
6. [Lighting Strategies](#lighting-strategies)
7. [Output & File Formats](#output--file-formats)
8. [Render Optimization](#render-optimization)

---

## Engine Selection

```python
# Cycles - physically accurate ray tracing
scene.render.engine = 'CYCLES'

# EEVEE - fast rasterization (Blender 5.0 name!)
scene.render.engine = 'BLENDER_EEVEE'  # NOT 'BLENDER_EEVEE_NEXT'

# Workbench - solid/wireframe preview
scene.render.engine = 'BLENDER_WORKBENCH'
```

**When to use which:**
- Cycles: final renders, glass/caustics, accurate lighting, physics sims
- EEVEE: fast previews, stylized looks, large scenes, quick iteration
- Workbench: technical/wireframe views, modeling reference shots

## Cycles Configuration

```python
scene = bpy.context.scene
scene.render.engine = 'CYCLES'

# Samples (quality vs speed)
scene.cycles.samples = 32           # Final render samples
scene.cycles.preview_samples = 16   # Viewport preview samples
scene.cycles.use_denoising = True   # AI denoiser (huge quality boost)

# Light bounces
scene.cycles.max_bounces = 12       # Total maximum
scene.cycles.diffuse_bounces = 4    # Matte surfaces
scene.cycles.glossy_bounces = 4     # Reflective surfaces
scene.cycles.transmission_bounces = 8  # Glass/water refraction
scene.cycles.transparent_max_bounces = 8  # Alpha transparency
scene.cycles.volume_bounces = 2     # Fog/volumetrics

# Caustics (light patterns through glass)
scene.cycles.caustics_reflective = True
scene.cycles.caustics_refractive = True

# GPU rendering (if available)
prefs = bpy.context.preferences.addons.get('cycles')
if prefs:
    # Try OPTIX first (fastest), then CUDA, then HIP
    for device_type in ['OPTIX', 'CUDA', 'HIP', 'METAL']:
        try:
            prefs.preferences.compute_device_type = device_type
            break
        except:
            continue
```

### Cycles feature flags
```python
# Adaptive sampling (smart sample distribution)
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.01

# Clamping (reduces fireflies)
scene.cycles.sample_clamp_direct = 10.0
scene.cycles.sample_clamp_indirect = 10.0
```

## EEVEE Configuration

```python
scene.render.engine = 'BLENDER_EEVEE'

# Quality settings
scene.eevee.taa_render_samples = 64
scene.eevee.use_gtao = True  # Ambient occlusion

# Screen space reflections
scene.eevee.use_ssr = True
scene.eevee.use_ssr_refraction = True

# Shadows
scene.eevee.shadow_cube_size = '1024'
scene.eevee.shadow_cascade_size = '2048'
```

## MCP Timeout Management

The MCP server typically has a ~60 second timeout for `execute_blender_code`.
Renders must complete within this window.

### Safe resolution/sample matrix

| Engine | Samples | Resolution | Typical Time | Safe? |
|--------|---------|-----------|-------------|-------|
| Cycles | 16 | 1280×720 | 15-25s | Yes |
| Cycles | 32 | 960×540 | 20-35s | Yes |
| Cycles | 32 | 1280×720 | 30-50s | Risky |
| Cycles | 64 | 640×360 | 25-40s | Yes |
| Cycles | 128 | 640×360 | 40-55s | Risky |
| Cycles | 128 | 1280×720 | 60-120s | NO |
| EEVEE | 64 | 1920×1080 | 5-15s | Yes |
| EEVEE | 128 | 1920×1080 | 10-25s | Yes |

### If render times out
1. Reduce samples (32 → 16)
2. Reduce resolution (1280×720 → 960×540)
3. Hide unneeded objects: `obj.hide_render = True`
4. Remove world Volume shaders (biggest perf killer)
5. Disable caustics if not needed
6. Use denoiser to compensate for lower samples

### Batch rendering strategy
For multiple renders, keep settings minimal and only change what's needed:
```python
# Render 4 views at safe settings
scene.cycles.samples = 16
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.cycles.use_denoising = True

for cam_name in ["Cam_A", "Cam_B", "Cam_C", "Cam_D"]:
    scene.camera = bpy.data.objects[cam_name]
    scene.render.filepath = os.path.join(temp_dir, f"{cam_name}.png")
    bpy.ops.render.render(write_still=True)
```

## Camera Setup

```python
import math

# Add camera
bpy.ops.object.camera_add(location=(7, -6, 5))
cam = bpy.context.active_object
cam.name = "MainCamera"
cam.data.lens = 35  # Focal length in mm

# Common focal lengths
# 10-18mm: ultra-wide (architecture, landscapes, full rainbow arcs)
# 24-35mm: wide (environments, interiors)
# 50mm:    normal (matches human eye)
# 85mm:    portrait (product shots, detail)
# 135mm+:  telephoto (distant subjects)

# Set as active camera
bpy.context.scene.camera = cam

# Clipping
cam.data.clip_start = 0.1
cam.data.clip_end = 1000

# Depth of field
cam.data.dof.use_dof = True
cam.data.dof.focus_distance = 5.0  # meters
cam.data.dof.aperture_fstop = 2.8  # Lower = more blur

# Point camera at a target
direction = target_location - cam.location
rot_quat = direction.to_track_quat('-Z', 'Y')
cam.rotation_euler = rot_quat.to_euler()
```

## Lighting Strategies

### Three-point lighting (product/portrait)
```python
# Key light (main, strongest)
bpy.ops.object.light_add(type='AREA', location=(3, -3, 4))
key = bpy.context.active_object
key.data.energy = 200
key.data.size = 2

# Fill light (softer, opposite side)
bpy.ops.object.light_add(type='AREA', location=(-3, -2, 3))
fill = bpy.context.active_object
fill.data.energy = 80
fill.data.size = 3

# Rim/back light (edge highlight)
bpy.ops.object.light_add(type='AREA', location=(0, 3, 4))
rim = bpy.context.active_object
rim.data.energy = 150
rim.data.size = 1
```

### Outdoor lighting
```python
# Sun lamp for directional light
bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
sun = bpy.context.active_object
sun.data.energy = 5.0
sun.data.color = (1.0, 0.98, 0.95)  # Warm daylight
sun.data.angle = math.radians(0.53)  # Sun disc size
sun.rotation_euler = (math.radians(45), 0, math.radians(30))

# Combine with HDRI for realistic fill
# Use Poly Haven: search_polyhaven_assets(asset_type="hdris")
```

### Studio lighting (clean white background)
```python
# White backdrop
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 5, 0))
backdrop = bpy.context.active_object
backdrop.rotation_euler = (math.radians(90), 0, 0)
mat_white = bpy.data.materials.new("White")
mat_white.use_nodes = True
bsdf = mat_white.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (1, 1, 1, 1)
backdrop.data.materials.append(mat_white)

# Soft area lights
for loc in [(3,-3,4), (-3,-3,4), (0,-3,6)]:
    bpy.ops.object.light_add(type='AREA', location=loc)
    light = bpy.context.active_object
    light.data.energy = 150
    light.data.size = 3
```

## Output & File Formats

```python
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100  # Scale factor

# Image format
scene.render.image_settings.file_format = 'PNG'  # or 'JPEG', 'OPEN_EXR'
scene.render.image_settings.color_mode = 'RGB'    # or 'RGBA' for transparency
scene.render.image_settings.compression = 15      # PNG compression 0-100

# For transparent background (product shots)
scene.render.film_transparent = True
scene.render.image_settings.color_mode = 'RGBA'

# Output path (OS-safe)
import os, tempfile
temp_dir = tempfile.gettempdir()
scene.render.filepath = os.path.join(temp_dir, "render.png")

# Execute render
bpy.ops.render.render(write_still=True)
```

## Render Optimization

### Reducing render time
1. **Denoiser**: Always enable — saves 4-8x samples for equivalent quality
2. **Adaptive sampling**: Focuses samples on noisy areas
3. **Hide objects**: `obj.hide_render = True` for anything out of frame
4. **Collection visibility**: `collection.hide_render = True` for groups
5. **Remove volumes**: World volumetric scatter is the #1 performance killer
6. **Reduce bounces**: Default 12 is generous; 8 is usually fine
7. **Clamp indirect**: `scene.cycles.sample_clamp_indirect = 10.0` kills fireflies
8. **Lower mesh detail**: Reduce `segments`/`ring_count` on off-screen objects

### Checking render time before committing
Do a test render at 1/4 resolution first:
```python
scene.render.resolution_percentage = 25
# render... check time
scene.render.resolution_percentage = 100  # restore for final
```
