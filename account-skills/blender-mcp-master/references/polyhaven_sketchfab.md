# Asset Integration: Poly Haven, Sketchfab, Hyper3D

Patterns for using external asset libraries via MCP tools.

## Table of Contents
1. [Poly Haven](#poly-haven)
2. [Sketchfab](#sketchfab)
3. [Hyper3D Rodin](#hyper3d-rodin)
4. [Asset Sizing Guide](#asset-sizing-guide)

---

## Poly Haven

Free CC0 assets — HDRIs, textures, and 3D models. No attribution required.

### Check availability
Always check first — the addon may not be enabled:
```
get_polyhaven_status()
```

### HDRIs (environment lighting)
```
# Browse categories
get_polyhaven_categories(asset_type="hdris")

# Search
search_polyhaven_assets(asset_type="hdris", categories="outdoor")
search_polyhaven_assets(asset_type="hdris", categories="indoor")
search_polyhaven_assets(asset_type="hdris", categories="studio")

# Download and apply (sets as world environment automatically)
download_polyhaven_asset(
    asset_id="kloofendal_48d_partly_cloudy",
    asset_type="hdris",
    resolution="2k"  # 1k, 2k, 4k available
)
```

**Resolution guide for HDRIs:**
- 1k: fast preview, low quality reflections
- 2k: good balance for most scenes (recommended)
- 4k: high quality reflections, slower to load

### Textures (PBR materials)
```
# Search by category
search_polyhaven_assets(asset_type="textures", categories="wood")
search_polyhaven_assets(asset_type="textures", categories="brick")
search_polyhaven_assets(asset_type="textures", categories="metal")
search_polyhaven_assets(asset_type="textures", categories="ground")
search_polyhaven_assets(asset_type="textures", categories="fabric")

# Download texture
download_polyhaven_asset(
    asset_id="wooden_planks",
    asset_type="textures",
    resolution="2k"
)

# Apply to an object
set_texture(object_name="Floor", texture_id="wooden_planks")
```

The `set_texture` tool creates a full PBR material with:
- Color/Albedo map
- Normal map
- Roughness map
- Displacement map (if available)

### 3D Models
```
search_polyhaven_assets(asset_type="models", categories="furniture")
download_polyhaven_asset(
    asset_id="wooden_table",
    asset_type="models",
    resolution="2k"
)
```

## Sketchfab

Huge library of user-uploaded 3D models. Some are downloadable for free.

### Check availability
```
get_sketchfab_status()
```

### Search
```
search_sketchfab_models(
    query="modern chair",
    downloadable=True,  # Only show downloadable models
    count=10
)
```

### Preview before downloading
Always preview to confirm it's what you want:
```
get_sketchfab_model_preview(uid="model_uid_here")
```

### Download and import
```
download_sketchfab_model(
    uid="model_uid_here",
    target_size=1.0  # Scale to 1 meter largest dimension
)
```

**Target size guide:**

| Object | target_size |
|--------|-------------|
| Small (cup, phone) | 0.1 - 0.3 |
| Medium (chair, lamp) | 0.7 - 1.2 |
| Large (table, desk) | 1.0 - 2.0 |
| Person | 1.7 |
| Car | 4.0 - 5.0 |
| Building | 10.0+ |

## Hyper3D Rodin

AI-powered 3D model generation from text or images.

### Check availability
```
get_hyper3d_status()
```

### Generate from text
```
generate_hyper3d_model_via_text(
    text_prompt="a wooden treasure chest with gold trim",
    bbox_condition=[1.0, 0.7, 0.6]  # Optional: L×W×H ratio
)
```

### Generate from image
```
generate_hyper3d_model_via_images(
    input_image_paths=["/path/to/reference.jpg"],
    # OR for FAL_AI mode:
    input_image_urls=["https://example.com/reference.jpg"]
)
```

### Wait for completion
Generation is async. You must poll:
```
# For MAIN_SITE mode
poll_rodin_job_status(subscription_key="key_from_generate_step")
# Wait until all statuses are "Done"

# For FAL_AI mode
poll_rodin_job_status(request_id="request_id_from_generate_step")
# Wait until status is "COMPLETED"
```

### Import the result
```
import_generated_asset(
    name="TreasureChest",
    task_uuid="uuid_from_generate"  # MAIN_SITE
    # OR request_id="id"            # FAL_AI
)
```

### Post-import steps
Generated models have normalized size. You'll usually need to:
1. Scale to desired size: `obj.scale = (2, 2, 2)`
2. Position in scene: `obj.location = (x, y, z)`
3. The model comes with built-in materials (no need to add your own)

## Asset Sizing Guide

When combining assets from different sources, everything should be in
meters (Blender's default unit). Common reference sizes:

| Object | Height/Size (meters) |
|--------|---------------------|
| Door | 2.0 |
| Dining table | 0.75 |
| Chair seat | 0.45 |
| Kitchen counter | 0.90 |
| Person standing | 1.70 |
| Car (sedan) | 1.45 tall, 4.5 long |
| Single bed | 0.5 tall, 2.0 long |
| Coffee cup | 0.10 |
| Desktop monitor | 0.40 |
| Tree (medium) | 6-10 |
