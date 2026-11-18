# Blender 5.0 / 5.0.1 Python API Changes

This reference documents every breaking change and deprecation relevant to
MCP-based Blender scripting. Read this when your code throws unexpected
errors or when migrating scripts from Blender 4.x.

## Table of Contents
1. [Rendering Engine IDs](#rendering-engine-ids)
2. [BGL Removal](#bgl-removal)
3. [Compositor Changes](#compositor-changes)
4. [Paint System Reorganization](#paint-system-reorganization)
5. [Asset System Changes](#asset-system-changes)
6. [Image & Media Changes](#image--media-changes)
7. [Node System Changes](#node-system-changes)
8. [Runtime Properties](#runtime-properties)
9. [Private Modules](#private-modules)
10. [Other Removals](#other-removals)
11. [New Additions](#new-additions)
12. [Hardware Requirements](#hardware-requirements)

---

## Rendering Engine IDs

**Breaking:** The EEVEE render engine identifier changed.

```python
# Blender 4.x (OLD - BROKEN in 5.0)
scene.render.engine = 'BLENDER_EEVEE_NEXT'

# Blender 5.0+ (CORRECT)
scene.render.engine = 'BLENDER_EEVEE'
```

Also changed:
- Render pass names simplified (abbreviations removed)
- `scene.eevee.gtao_distance` → `view_layer.eevee.ambient_occlusion_distance`
- Obsolete EEVEE properties removed entirely

## BGL Removal

**Breaking:** The entire `bgl` module is removed. Any script with `import bgl`
will crash.

```python
# OLD (CRASHES in 5.0)
import bgl
bgl.glEnable(bgl.GL_BLEND)

# NEW
import gpu
from gpu_extras.batch import batch_for_shader
# Use gpu.state module for GL state changes
gpu.state.blend_set('ALPHA')
```

Also:
- `Image.bindcode` removed → use `gpu.texture.from_image()`
- Direct GLSL shader creation from source files removed

## Compositor Changes

**Breaking:** The compositor node tree access changed fundamentally.

```python
# OLD (BROKEN in 5.0)
scene.use_nodes = True  # Deprecated, always True now
tree = scene.node_tree  # REMOVED

# NEW
tree = scene.compositing_node_group
# If None, create one:
if tree is None:
    tree = bpy.data.node_groups.new("Compositing", 'CompositorNodeTree')
    scene.compositing_node_group = tree
```

- `scene.use_nodes` is deprecated — always returns `True`
- Deprecated compositor nodes have been removed entirely
- Combine/Separate RGBA/HSVA nodes removed
- Point density texture node removed
- File Output node restructured: separate `directory` and `file_name` properties

## Paint System Reorganization

**Breaking:** Brush type enum properties renamed across all paint modes.

```python
# OLD (BROKEN in 5.0)
brush.sculpt_tool
brush.vertex_tool
brush.weight_tool
brush.image_tool
brush.gpencil_tool

# NEW
brush.sculpt_brush_type
brush.vertex_brush_type
brush.weight_brush_type
brush.image_brush_type
brush.gpencil_brush_type
```

Also:
- `unified_paint_settings` moved from `tool_settings` to mode-specific `Paint` structs
- Radial symmetry transferred from scene to mesh properties
- Brush curve properties renamed to `curve_distance_falloff`
- Custom brush icon properties removed

## Asset System Changes

```python
# OLD (REMOVED)
context.active_file       # In asset shelf
asset_handle = ...        # AssetHandle type
asset_catalog_path = ...  # AssetCatalogPath type
UILayout.template_asset_view()

# NEW
context.asset  # Use this instead of context.active_file
```

## Image & Media Changes

**Breaking:** `ImageFormatSettings` now requires setting `media_type` before
setting `file_format`.

```python
# OLD (may silently fail or error in 5.0)
settings.file_format = 'PNG'

# NEW (correct order)
settings.media_type = 'IMAGE'  # Set this FIRST
settings.file_format = 'PNG'   # Then this
```

## Node System Changes

- Sky Texture node: several inputs removed
- File Output node: `base_path` split into `directory` + `file_name`
- Deprecated nodes have been fully removed (they were marked deprecated in 4.x)
- The Combine/Separate nodes are gone

## Runtime Properties

**Breaking:** Properties defined via `bpy.props` can no longer be accessed
through dict-like syntax.

```python
# OLD (BROKEN in 5.0)
value = bpy.context.scene['my_custom_prop']

# This change affects addon developers primarily.
# For MCP scripting, avoid relying on dict-style property access.
```

New additions:
- `get_transform` / `set_transform` callbacks (faster than get/set)
- `READ_ONLY` flag for property definitions

## Private Modules

13 bundled Python modules became private (prefixed with underscore).
If you import any of these, your script will break:

- `animsys_refactor`
- `bl_console_utils`
- `bl_i18n_utils`
- `bl_keymap_utils`
- `bl_math`
- `bl_previews_utils`
- `bl_rna_utils`
- `bl_ui_utils`
- `bpy_extras` (some submodules)
- `freestyle` (some submodules)
- `gpu_extras` (still public, but check specific imports)
- `nodeitems_builtins`
- `nodeitems_utils`

## Other Removals

- Legacy Action API: `action.fcurves`, `action.groups`, `action.id_root` — all removed
- `PointCache.compression` property removed (caches always compressed now)
- Pre-2.50 animation compatibility dropped
- Big endian platform support discontinued
- LZMA/LZO point cache compression formats removed
- Image texture filtering properties eliminated
- Theme API completely rewritten (custom themes from 4.x won't load)

## New Additions

- **Max data-block name length**: Increased to 255 bytes (was shorter)
- **Blendfile compression**: Defaults to enabled on save
- **Transform callbacks**: `get_transform`/`set_transform` for faster property access
- **mathutils enhancements**: Extended mathematical utilities
- **Context logging**: Improved logging capabilities
- **Working color space API**: Enhanced color management

## Hardware Requirements

Increased minimums for GPU rendering:
- **NVIDIA Cycles**: Minimum compute capability sm_50 (GeForce 900 series or newer)
- **AMD HIP**: Windows driver minimums increased
- **Intel Mac**: Builds removed entirely

## 5.0.1 Corrective Release (Dec 16, 2025)

132 bug fixes including:
- Crash on selecting extrude tool
- Hair sculpting deletion crash
- Grease Pencil crash opening 4.5 files
- `bpy.app.is_job_running` crash in background mode
- EEVEE animation rendering material/light inconsistencies
- Texture painting pressure crash
- Mesh validation fixes
- Geometry Nodes fixes
- Python API compatibility patches

**Always use 5.0.1 over 5.0.0** — it resolves several crashes.
