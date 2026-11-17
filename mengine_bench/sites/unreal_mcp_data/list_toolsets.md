- ToolsetRegistry.AgentSkillToolset: Provides tools for listing, reading, and creating/updating skills.
- VibeUE.ActorService: Actor service exposed directly to Python.

Trimmed to the operations Epic's native toolsets (ActorTools, SceneTools,
EditorAppToolset) do NOT provide: transform lock/constraints, absolute-transform
flags, preserve-scale-ratio, viewport camera framing, and full property dumps.

Python Usage:
  import unreal
  actor_service = unreal.ActorService

  # Transform Locking
  actor_service.set_actor_lock_location("MyActor", True)   # Lock location in viewport
  actor_service.set_preserve_scale_ratio(True)   # Lock uniform scale (padlock icon)
  actor_service.set_absolute_transform("MyActor", False, True, False)  # Absolute rotation

  # Camera framing
  view = actor_service.get_actor_view_camera("MyActor", unreal.EViewDirection.TOP)

  # Properties
  props = actor_service.get_all_properties("MyActor")
- VibeUE.AnimGraphService: Animation Graph service exposed directly to Python.

This service provides AnimBlueprint introspection and navigation functionality,
including the ability to open specific state machines and states in the editor.

Python Usage:
  import unreal

  # List all state machines in an AnimBP
  machines = unreal.AnimGraphService.list_state_machines("/Game/ABP_Character")
  for m in machines:
      print(f"Machine: {m.machine_name}, States: {m.state_count}")

  # List states in a state machine
  states = unreal.AnimGraphService.list_states_in_machine("/Game/ABP_Character", "Locomotion")
  for s in states:
      print(f"State: {s.state_name} ({s.state_type})")

  # Open a specific state in the editor
  unreal.AnimGraphService.open_anim_state("/Game/ABP_Character", "Locomotion", "IdleLoop")

@note All methods are static and thread-safe
@note C++ out parameters become Python return values

**C++ Source:**

- **Plugin**: VibeUE
- **Module**: VibeUE
- **File**: UAnimGraphService.h
- VibeUE.AnimMontageService: Animation Montage service exposed directly to Python.

This service provides comprehensive CRUD operations for Animation Montage assets
including section management, slot tracks, animation segments, branching points,
and blend settings. These operations require C++ because Python's set_editor_property()
returns read-only copies of internal TArrays like CompositeSections and SlotAnimTracks.

IMPORTANT: All montage_path parameters require the FULL asset path (package_name from AssetData),
NOT the folder path (package_path). For example:
  - CORRECT: "/Game/Characters/Mannequin/Montages/AM_Attack"
  - WRONG:   "/Game/Characters/Mannequin/Montages" (this is a folder, not an asset)

Python Usage:
  import unreal

  # List all montages for a skeleton
  montages = unreal.AnimMontageService.find_montages_for_skeleton("/Game/SK_Mannequin")
  for m in montages:
      print(f"{m.montage_name}: {m.duration}s, {m.section_count} sections")

  # Create a montage from an animation
  path = unreal.AnimMontageService.create_montage_from_animation(
      "/Game/Animations/Attack", "/Game/Montages", "AM_Attack")

  # Add sections for combo system
  unreal.AnimMontageService.add_section(path, "WindUp", 0.0)
  unreal.AnimMontageService.add_section(path, "Attack", 0.3)
  unreal.AnimMontageService.add_section(path, "Recovery", 0.8)

  # Link sections for combo flow
  unreal.AnimMontageService.set_next_section(path, "WindUp", "Attack")
  unreal.AnimMontageService.set_next_section(path, "Attack", "Recovery")

  # Add branching point for combo input window
  unreal.AnimMontageService.add_branching_point(path, "ComboWindow", 0.6)

@note All methods are static and thread-safe
@note For notifies on montages, you can use AnimSequenceService methods (inherited)

**C++ Source:**

- **Plugin**: VibeUE
- **Module**: VibeUE
- **File**: UAnimMontageService.h
- VibeUE.AnimSequenceService: Animation Sequence service exposed directly to Python.

This service provides comprehensive CRUD operations for Animation Sequence assets
including keyframe access, curve editing, notify management, sync markers,
root motion configuration, and animation data extraction.

IMPORTANT: All anim_path parameters require the FULL asset path (package_name from AssetData),
NOT the folder path (package_path). For example:
  - CORRECT: "/Game/Characters/Mannequin/Animations/Run/AS_Run_Forward"
  - WRONG:   "/Game/Characters/Mannequin/Animations/Run" (this is a folder, not an asset)

Python Usage:
  import unreal

  # Use the FULL asset path, including the asset name
  anim_path = "/Game/Characters/Mannequin/Animations/Run/AS_Run_Forward"

  # List all animations for a skeleton
  anims = unreal.AnimSequenceService.find_animations_for_skeleton("/Game/SK_Mannequin")
  for anim in anims:
      print(f"{anim.anim_name}: {anim.duration}s")

  # Get bone pose at time
  pose = unreal.AnimSequenceService.get_pose_at_time(anim_path, 0.5, True)
  for bone in pose:
      print(f"{bone.bone_name}: {bone.transform.location}")

  # Add animation notify (use full class path)
  unreal.AnimSequenceService.add_notify(
      anim_path,
      "/Script/Engine.AnimNotify",
      0.25,
      "Footstep"
- VibeUE.AssetDiscoveryService: Asset import/export and Content Browser service exposed directly to Python.

Asset search and general CRUD are provided by the engine's AssetTools toolset.
This service owns crash-safe image import, texture export, Content Browser
selection, and open-editor checks.

Python Usage:
  import unreal

  # Import an image without pumping the task graph inside an MCP call
  path, error = unreal.AssetDiscoveryService.import_asset(
      "C:/Images/rocks.jpg", "/Game/UI/Textures", "T_Rocks")

  # Inspect the current Content Browser selection
  asset_data = unreal.AssetDiscoveryService.get_primary_content_browser_selection()
  if asset_data:
      print(asset_data.package_name)

@note All methods are static.
- VibeUE.BehaviorTreeService: Read and author Behavior Tree assets.

All writes go through the editor EdGraph (UBehaviorTree::BTGraph) and are committed with
UBehaviorTreeGraph::OnSave(), which regenerates the runtime UBehaviorTree::RootNode.
Writing RootNode directly reads back correctly and is silently discarded on the next
graph update, so it is never done here.
- VibeUE.BlackboardService: Read and author Blackboard (UBlackboardData) assets.

Separate from UBehaviorTreeService because UBlackboardData is a flat UDataAsset with no
graph, and is useful (and testable) on its own.

Writes hold to the same discipline as the BT service: refused while a Play In Editor session
is running (live UBlackboardComponents hold key IDs and value offsets computed at init, and
mutating Keys under them type-confuses every later read) and while a Blackboard editor is
open on the asset (its copy would silently overwrite the change on the human's next save).
Every key mutation runs the engine's own post-edit fix-ups — the ones
UBlackboardData::PostEditChangeProperty runs for a details-panel edit — so loaded child
blackboards, synchronized-key state and editor listeners stay coherent.
- VibeUE.BlueprintService: Blueprint service exposed directly to Python.

This service provides blueprint introspection and analysis with native
Unreal Engine types.

Python Usage:
  import unreal

  # Get blueprint info (returns BlueprintDetailedInfo or None)
  info = unreal.BlueprintService.get_blueprint_info("/Game/Blueprints/BP_Player_Test")
  if info:
      print(f"Parent: {info.parent_class}")
      for var in info.variables:
          print(f"  {var.variable_name}: {var.variable_type}")

  # List variables
  variables = unreal.BlueprintService.list_variables("/Game/BP_Player_Test")

  # List components
  components = unreal.BlueprintService.list_components("/Game/BP_Player_Test")

@note All methods are static and thread-safe
@note C++ out parameters become Python return values
- VibeUE.EngineSettingsService: Engine Settings Service - Python API for Unreal Engine configuration manipulation.

Provides comprehensive access to engine configuration including:
- Rendering settings (r.* cvars, quality, features)
- Physics settings (gravity, collision profiles)
- Audio settings (sample rates, channels)
- Garbage collection settings (gc.*)
- Threading/performance settings
- Platform-specific settings
- Console variables (cvars) direct access
- All engine config file access

Python Usage:
  import unreal

  # Inspect engine config sections and values
  sections = unreal.EngineSettingsService.list_engine_sections("Engine.ini")
  value = unreal.EngineSettingsService.get_engine_ini_value(
      "/Script/Engine.Engine", "GameEngine", "Engine.ini")

  # Get/set console variables
  value = unreal.EngineSettingsService.get_console_variable("r.ReflectionMethod")
  result = unreal.EngineSettingsService.set_console_variable("r.ReflectionMethod", "1")

  # Search for settings/cvars
  matches = unreal.EngineSettingsService.search_console_variables("shadow")
  for m in matches:
      print(f"{m.name}: {m.description}")

@note Changes are written to config files and may require editor restart
- VibeUE.EnumStructService: Enum and Struct Service - Python API for UserDefinedEnum and UserDefinedStruct manipulation

Provides full CRUD operations for:
- UserDefinedEnum: Create, read, modify, delete enum assets
- UserDefinedStruct: Create, read, modify, delete struct assets

Note: Native C++ enums and structs are read-only. Modification methods will
return false/error for native types.

Python Usage:
  import unreal

  # Search for enums
  enums = unreal.EnumStructService.search_enums("Weapon")

  # Create a UserDefinedEnum
  path = unreal.EnumStructService.create_enum("/Game/Enums", "EWeaponType")
  unreal.EnumStructService.add_enum_value(path, "Sword", "A melee weapon")

  # Create a UserDefinedStruct
  path = unreal.EnumStructService.create_struct("/Game/Structs", "FWeaponData")
  unreal.EnumStructService.add_struct_property(path, "Damage", "float")
- VibeUE.EnvQueryService: Read, author, tune and run Environment Query (EQS) assets.

All writes go through the editor EdGraph (UEnvQuery::EdGraph) and commit with
UEnvironmentQueryGraph::UpdateAsset(). Writing UEnvQuery::Options directly is a trap: UpdateAsset
calls GetOptionsMutable().Reset() and regenerates the whole array from the graph, so a direct
write reads back correctly and is discarded on the next commit.

Requires the EnvironmentQueryEditor plugin. Without it every method reports the feature as
unavailable rather than failing to build.
- VibeUE.FabService: Fab asset import service (issue #517). It can discover/import the signed-in Epic account's owned
library, or search the public zero-price catalog and directly import eligible glTF/GLB listings
(including Quixel Megascans) without adding them to the account library.

Thin orchestration over Unreal 5.8's built-in Fab plugin: it reuses the Epic login the editor/launcher
already holds (via its own EOS session), calls fab.com's owned-library REST feed, and (for import)
drives the engine Fab plugin's downloader. These fab.com endpoints are unofficial/reverse-engineered
and may change without notice — see docs/design/fab-service-spec.md and the `fab` skill.

Owned flow: AuthStatus() → ListLibrary() → GetAsset() → ImportAsset() → ImportStatus().
Free flow: SearchFreeCatalog() → explicit EULA acceptance → ImportFreeAsset() → ImportStatus().
No purchasing, add-to-library, or entitlement claiming is implemented.
- VibeUE.FoliageService: Foliage service exposed directly to Python.

Provides foliage placement and management for landscapes:

Discovery:
- list_foliage_types: List all foliage types in the level with instance counts
- get_instance_count: Get instance count for a specific foliage type

Foliage Type Management:
- create_foliage_type: Create a UFoliageType asset from a static mesh
- set_foliage_type_property: Set a property on a foliage type asset
- get_foliage_type_property: Get a property from a foliage type asset

Placement:
- scatter_foliage: Scatter instances in a circular region with Poisson disk sampling
- scatter_foliage_rect: Scatter instances in a rectangular region
- add_foliage_instances: Place instances at specific locations

Layer-Aware Placement:
- scatter_foliage_on_layer: Scatter only where a landscape paint layer is dominant

Removal:
- remove_foliage_in_radius: Remove instances of a type in a circular region
- remove_all_foliage_of_type: Remove all instances of a type from the level
- clear_all_foliage: Remove all foliage of all types

Query:
- get_foliage_in_radius: Get foliage instances in a circular region

Existence:
- foliage_type_exists: Check if a foliage type asset exists
- has_foliage_instances: Check if any foliage instances exist for a type

Python Usage:
  import unreal

  # Scatter 200 trees
  result = unreal.FoliageService.scatter_foliage(
      "/Game/Meshes/SM_Tree", 0.0, 0.0, 5000.0, 200)

  # List foliage types
  types = unreal.FoliageService.list_foliage_types()

  # Remove trees in area
  unreal.FoliageService.remove_foliage_in_radius("/Game/Meshes/SM_Tree", 0.0, 0.0, 1000.0)
- VibeUE.GameplayTagService: Gameplay Tag Service - Python API for querying and bulk-adding Gameplay Tags.

This service provides:
- Bulk-adding new tags (to INI config + runtime registration)
- Querying tag information and direct children
- Checking tag existence

Python Usage:
  import unreal

  # Add multiple tags at once
  result = unreal.GameplayTagService.add_tags(["Cube.StartChasing", "Cube.StopChasing"], "Chase events")

  # Check if a tag exists
  exists = unreal.GameplayTagService.has_tag("Cube.StartChasing")

  # Get detailed tag info
  info = unreal.GameplayTagService.get_tag_info("Cube.StartChasing")  # info struct or None (NOT a tuple)

  # Get direct children of a tag
  children = unreal.GameplayTagService.get_children("Cube")

@note This service owns: has_tag, get_tag_info, get_children, add_tags (bulk).
      Single-tag create / rename / remove are the engine's GameplayTagsToolset —
      reach them with call_tool (run describe_toolset on the GameplayTags toolset for
      the exact action names). There is no rename_tag / remove_tag on this service.
@note Tags are written to DefaultGameplayTags.ini by default and registered at runtime.
- VibeUE.InputService: Input service exposed directly to Python (Enhanced Input System).

Python method names (use THESE with discover_python_class method_filter —
the snake_case names below are the real Python API):

Reflection:
- discover_types: Discover available value types, modifier types, and trigger types

Action Management:
- create_action: Create a new Input Action asset
- list_input_actions: List all Input Action assets
- get_input_action_info: Get properties of an Input Action
- configure_action: Configure Input Action properties (consume input, description, ...)
- input_action_exists: Check whether an Input Action asset exists

Mapping Context Management:
- create_mapping_context: Create a new Input Mapping Context
- list_mapping_contexts: List all Mapping Contexts
- get_mapping_context_info: Get properties of a Mapping Context
- get_mappings: Get all key mappings in a context
- add_key_mapping: Add a key mapping to a context
- remove_mapping: Remove a key mapping from a context
- get_available_keys: Get list of available input keys
- mapping_context_exists / key_mapping_exists: Existence checks

Modifier Management:
- add_modifier: Add a modifier to a key mapping
- remove_modifier: Remove a modifier from a key mapping
- get_modifiers: Get modifiers on a key mapping
- get_available_modifier_types: Get available modifier types

Trigger Management:
- add_trigger: Add a trigger to a key mapping
- remove_trigger: Remove a trigger from a key mapping
- get_triggers: Get triggers on a key mapping
- get_available_trigger_types: Get available trigger types

PIE Input Injection (issue #550):
- inject_action: Inject an Enhanced Input action value into the running PIE session
- inject_key: Send a key press to the PIE game viewport via Slate (no OS focus needed)

Python Usage:
  import unreal

  # Discover available types
  types = unreal.InputService.discover_types()

  # Create an input action
  result = unreal.InputService.create_action("IA_Jump", "/Game/Input", "Axis1D")

  # Create a mapping context
  result = unreal.InputService.create_mapping_context("IMC_Default", "/Game/Input")

  # Add key mapping
  unreal.InputService.add_key_mapping("/Game/Input/IMC_Default", "/Game/Input/IA_Jump", "SpaceBar")

@note This replaces the JSON-based manage_enhanced_input MCP tool
- VibeUE.LandscapeMaterialService: Landscape material service exposed directly to Python.

Provides 20 landscape material management actions:

Material Creation:
- create_landscape_material: Create a material configured for landscape use

Layer Blend Node:
- create_layer_blend_node: Create a LandscapeLayerBlend expression
- create_layer_blend_node_with_layers: Create blend node with all layers in one call
- add_layer_to_blend_node: Add a layer to an existing blend node
- remove_layer_from_blend_node: Remove a layer from a blend node
- get_layer_blend_info: Get info about a blend node's layers
- connect_to_layer_input: Connect an expression to a layer's input on blend node

Coordinates:
- create_layer_coords_node: Create landscape UV coordinate expression

Layer Sample:
- create_layer_sample_node: Create a LandscapeLayerSample expression for sampling layer weight

Grass Output:
- create_grass_output: Create a LandscapeGrassOutput expression with grass type mappings

Layer Info Objects:
- create_layer_info_object: Create a ULandscapeLayerInfoObject asset
- get_layer_info_details: Get details about a layer info object

Assignment:
- assign_material_to_landscape: Assign material to landscape with layer mapping

Convenience:
- setup_layer_textures: Set up complete layer with diffuse/normal/roughness

Weight Node:
- create_layer_weight_node: Create a LandscapeLayerWeight expression

Height/Slope-Driven Blending:
- create_height_mask_node: Build a world-height → 0-1 mask node network (no weight maps)
- create_slope_mask_node: Build a slope-angle → 0-1 mask node network (no weight maps)
- setup_height_slope_blend: Wire height/slope masks into a blend node (full auto-blend setup)

Existence:
- landscape_material_exists: Check if a material exists
- layer_info_exists: Check if a layer info object exists

Python Usage:
  import unreal

  # Create landscape material
  mat = unreal.LandscapeMaterialService.create_landscape_material("M_Terrain", "/Game/Materials")

  # Add layer blend
  blend = unreal.LandscapeMaterialService.create_layer_blend_node(mat.asset_path)
  unreal.LandscapeMaterialService.add_layer_to_blend_node(mat.asset_path, blend.node_id, "Grass")

  # Create layer info objects
  info = unreal.LandscapeMaterialService.create_layer_info_object("Grass", "/Game/Landscape")
- VibeUE.LandscapeService: Landscape Service
- VibeUE.MapBlockoutService: UMapBlockoutService — procedural FPS-map blockout from a VibeUE landscape.

Workflow (matches docs/design/map-designer-spec.md):
  0. ExportLandcoverGrid        — pulls weight layers off the source landscape
  1. GenerateRoads              — Main + Dirt network, gated on connectivity
  2. PlacePOIs                  — towns/farms/villages on the road network
  3. PlaceFields                — agricultural fields, 50–60% coverage band
  4. PlaceFoliage               — forest + treelines + scrub, 30–40% trees
  5. PlaceRailway               — railway + water-crossing bridges
  6. RunFinalPass               — re-validate everything + write 8 deliverable files

RunFullPipeline runs the whole sequence and writes the deliverables.
Each stage can also be called individually; consumers may inspect/repair the
intermediate state before advancing.

After the plan is built, the Materialize* methods turn it into real engine
geometry: landscape splines, paint layers, spawned actors, foliage instances.

Python usage:
  cfg = unreal.MapBlockoutConfig()
  cfg.level_name = "Verkhova"
  cfg.layers.crop, cfg.layers.forest = "Crop", "Forest"
  result = unreal.MapBlockoutService.run_full_pipeline_for_landscape("Landscape1", cfg)
  if result.success:
      unreal.MapBlockoutService.materialize_roads_as_splines(
          result.final_state.stage1_roads, "Landscape1")
- VibeUE.MaterialNodeService: Material Node Service
- VibeUE.MaterialService: Material service exposed directly to Python.

Provides material management actions NOT covered by Epic's native
MaterialTools / MaterialInstanceTools:

Lifecycle:
- save_material: Save material to disk
- compile_material: Compile/rebuild material shaders
- refresh_editor: Refresh open Material Editor
- open_in_editor: Open material in editor

Information:
- get_material_info: Get comprehensive material information
- summarize: Get AI-friendly material summary
- list_parameters: List all material parameters
- get_property_info: Get detailed property metadata

Property Management:
- set_property: Set a single property value
- set_properties: Set multiple properties at once

Bulk Instance Parameters:
- set_instance_parameters_bulk: Set many instance params in one call

Existence Checks:
- material_exists / material_instance_exists / parameter_exists

@note This replaces the JSON-based manage_material MCP tool
- VibeUE.MetaSoundService: Python-accessible MetaSound source authoring service.

Quick reference (all methods are static — call on the class):
  r = unreal.MetaSoundService.create_meta_sound("/Game/Audio", "MS_Sine", "Mono")
  nodes = unreal.MetaSoundService.list_available_nodes("Sine")    # discover node class
  r2 = unreal.MetaSoundService.add_node(r.asset_path, "Metasound.Standard", "Sine", "Audio")
  # r2.node_id = GUID of the Sine node
  # connect Sine output to the built-in graph output node
  unreal.MetaSoundService.connect_nodes(r.asset_path, r2.node_id, "Out", graph_out_id, "Audio:0")
  unreal.MetaSoundService.save_meta_sound(r.asset_path)

Use list_nodes() to retrieve NodeIds of the built-in interface nodes
(OnPlay output, OnFinished input, AudioOut inputs) created at asset creation.
- VibeUE.NiagaraEmitterService: Niagara Emitter Service - Python API for emitter color and parameter authoring.

Methods this service actually exposes (issue #462 — the docstring previously listed
renderer/module-input/script-discovery actions that are not bound):

Color authoring:
- set_color_tint(system_path, emitter_name, color[, hue_shift]) — handles ColorFromCurve
- get_color_curve_keys(system_path, emitter_name)
- set_color_curve_keys(system_path, emitter_name, keys)
- shift_color_hue(system_path, emitter_name, degrees)

Parameters:
- get_rapid_iteration_parameters(system_path, emitter_name, stage)

For emitter add/copy/duplicate/remove/move and renderer CRUD, use the engine
NiagaraToolsets via call_tool (see UNiagaraService notes). Scratch-pad / Custom-HLSL
graph authoring is on NiagaraScratchPadService.

Python Usage:
  import unreal

  # Inspect rapid-iteration parameters for an emitter stage
  params = unreal.NiagaraEmitterService.get_rapid_iteration_parameters(
      "/Game/VFX/NS_Fire", "Sparks", "Update")

  # Set color tint (works even with ColorFromCurve)
  unreal.NiagaraEmitterService.set_color_tint("/Game/VFX/NS_Fire", "Flames", "(0.0, 3.0, 0.0)")
- VibeUE.NiagaraScratchPadService: Niagara Scratch Pad Service - Python API for authoring scratch-pad module graphs.

The existing NiagaraEmitterService can add/list/configure stack *modules*, but it cannot
reach inside a scratch-pad module to build node-based logic or set Custom HLSL. This service
fills that gap: it resolves a stack module to its underlying scratch UNiagaraScript, then
lets you create nodes, set Custom HLSL, add typed pins, and wire pins together - the same
operations MaterialNodeService provides for material graphs.

Typical workflow (build a Custom-HLSL splat module):
  import unreal
  S = "/Game/VFX/NS_TrackPainter"
  E = "CompletelyEmpty"
  # 1. Create an empty scratch module on the Particle Update stage
  r = unreal.NiagaraScratchPadService.create_scratch_module(S, E, "ParticleUpdate", "SplatLine")
  mod = r.module_name
  # 2. Drop a Custom HLSL node and set the splat code
  hlsl = unreal.NiagaraScratchPadService.add_custom_hlsl_node(S, E, mod, CODE, 300, 0)
  # 3. Declare typed inputs/outputs on the Custom HLSL node
  unreal.NiagaraScratchPadService.add_pin(S, E, mod, hlsl.node_id, "Input", "Vector", "StartPos")
  unreal.NiagaraScratchPadService.add_pin(S, E, mod, hlsl.node_id, "Output", "float", "Result")
  # 4. Expose stack inputs and wire them in
  unreal.NiagaraScratchPadService.add_module_input(S, E, mod, "TireRadius", "float")
  unreal.NiagaraScratchPadService.connect_pins(S, E, mod, mapget_id, "Module.TireRadius", hlsl.node_id, "TireRadius")
  # 5. Apply + compile
  unreal.NiagaraScratchPadService.apply_changes(S)

All graph mutations operate on the scratch script asset directly (no open editor required).
Call apply_changes() once at the end to refresh signatures, rebuild emitter nodes, recompile,
and save. Discover method signatures with discover_python_class('unreal.NiagaraScratchPadService').
- VibeUE.NiagaraService: Niagara Service - Python API for Niagara rapid-iteration tuning + diagnostics.

This service was TRIMMED (issue #462): system / emitter / user-parameter
create / add / copy / duplicate / remove / move / compile are now owned by the
engine NiagaraToolsets (NiagaraToolset_System / _Assets / _Component / _Info) and
are reached with call_tool — they are NOT methods on this service. Scratch-pad /
Custom-HLSL graph authoring lives on NiagaraScratchPadService.

Methods this service actually exposes:

Rapid-iteration parameters (per-emitter script settings):
- list_rapid_iteration_params(system_path, emitter_name)
- set_rapid_iteration_param(system_path, emitter_name, param_name, value)
- set_rapid_iteration_param_by_stage(system_path, emitter_name, stage, param_name, value)

Diagnostics:
- compare_systems(source_path, target_path)
- get_emitter_lifecycle(system_path, emitter_name)  # info struct or None
- debug_activation(system_path)

For system/emitter/parameter CRUD + compile, discover the engine tools with
list_toolsets() / describe_toolset("NiagaraToolsets.NiagaraToolset_System") and
invoke via call_tool.

Python Usage:
  import unreal

  # Discover and tune an emitter's rapid-iteration parameters:
  params = unreal.NiagaraService.list_rapid_iteration_params("/Game/VFX/NS_Fire", "Flames")
  unreal.NiagaraService.set_rapid_iteration_param(
      "/Game/VFX/NS_Fire", "Flames", "Constants.flames.Color.Scale Color", "(0.0, 3.0, 0.0)")

  # Diagnose:
  print(unreal.NiagaraService.debug_activation("/Game/VFX/NS_Fire"))
- VibeUE.PerformanceService: Performance & tracing service — frame-timing triage, Unreal Insights trace capture, trace+log
analysis, and trace-attached standalone play.

Unreal 5.8's native toolsets have NO performance or tracing tools, so this is VibeUE's net-new
capability: it answers "are we CPU- or GPU-bound?" and drives Insights captures the engine's
EditorAppToolset (which can start PIE/Simulate) cannot measure.

Recommended flow: FrameTiming() FIRST (CPU vs GPU bound verdict) → StartTrace → reproduce the
workload → StopTrace → Analyse. For a representative reading, profile under PIE or a standalone
session, not the bare editor viewport. Methods return a JSON string.
- VibeUE.PIEActorService: Spawn and destroy transient actors inside a running Play-In-Editor (PIE) world.

Native Python (unreal.World / unreal.GameplayStatics) exposes NO actor spawn — the
deferred-spawn entry points are BlueprintInternalUseOnly — and every editor-side spawn path
(EditorActorSubsystem.spawn_actor_from_class, the engine SceneTools toolset) either targets the
editor world or refuses outright while PIE is active. This service resolves the LIVE PIE world by
role and spawns into it, so a gate/harness can drop a blocker, a test dummy, or a trigger volume
into the actual game session without a Blueprint.

Every method returns an FString JSON document. On success it carries success:true plus the
documented fields; on failure it carries success:false, an UPPER_SNAKE error_code, and a
human-readable message. Nothing here ever touches the editor world, opens a transaction, saves a
package, or writes config.

Python method names (snake_case — the real bound API):
- resolve_world: Resolve a PIE world by selector and report its net role and actor count
- spawn_actor: Spawn a transient actor into a resolved PIE world; returns a handle
- destroy_actor: Destroy one actor this service spawned, by handle (idempotent)
- destroy_all: Destroy every actor this service spawned this session (idempotent)
- list_spawned: List the actors this service spawned this session

Selector grammar (strict — anything else is INVALID_SELECTOR):
  "server"      -> PIE instance 0: the standalone world, the listen host, or the dedicated server.
  "client"      -> the single client world (instance >= 1). AMBIGUOUS_WORLD if more than one
                   client exists; WORLD_NOT_FOUND if there is none.
  "client:N"    -> client instance N, where N >= 1.
  "instance:N"  -> the exact PIE instance N, where N >= 0.
Worlds are resolved from GEditor->GetWorldContexts() (EWorldType::PIE only); the editor world,
GEditor->PlayWorld, and stale /Memory/UEDPIE_* shells are never used. No PIE -> PIE_NOT_RUNNING.

Authority: a spawn into a client world (GetNetMode() == NM_Client) is refused with
CLIENT_REQUIRES_OPT_IN unless allow_client_local is passed — a client-local actor is cosmetic and
never replicates. Spawn on "server" for anything that must exist for all players.

Handles are "<session_serial>:<guid>". They live only for the PIE session that produced them:
FEditorDelegates::EndPIE bumps the session serial and clears the registry, so a handle from an
earlier session reports STALE_HANDLE. Only actors THIS service registered are ever destroyed —
never by name, tag, or class search.

Python usage:
  import unreal, json
  info = json.loads(unreal.PIEActorService.resolve_world("server"))
  res  = json.loads(unreal.PIEActorService.spawn_actor(
             "server", "/Script/Engine.StaticMeshActor", unreal.Transform()))
  handle = res["handle"]
  # ... run a check against the spawned actor ...
  unreal.PIEActorService.destroy_all()
- VibeUE.ProjectSettingsService: Project Settings Service - Python API for Unreal Engine project settings manipulation.

Provides comprehensive access to project configuration including:
- General project settings (name, company, legal)
- Map settings (default maps, game modes)
- Rendering settings (quality, features)
- Physics settings (gravity, collision)
- Input settings
- Audio settings
- All UDeveloperSettings subclasses (dynamically discovered)
- Direct INI file access for custom sections

Python Usage:
  import unreal

  # Direct INI access
  value = unreal.ProjectSettingsService.get_ini_value(
      "/Script/Engine.Engine", "GameEngine", "DefaultEngine.ini")
  result = unreal.ProjectSettingsService.set_ini_value(
      "/Script/EngineSettings.GeneralProjectSettings", "ProjectName", "My Game", "DefaultGame.ini")

  # Discover all settings classes
  classes = unreal.ProjectSettingsService.discover_settings_classes()
  for c in classes:
      print(f"{c.class_name}: {c.property_count} properties")

@note Changes are written to config files and may require editor restart
- VibeUE.RuntimeVirtualTextureService: Service for managing Runtime Virtual Textures (RVT).

Runtime Virtual Textures enable efficient rendering of large landscapes by
caching material results into virtual texture pages. This service provides
tools to create RVT assets, place RVT volumes in levels, and assign RVTs
to landscape actors.

Python usage:
  import unreal

  # Create an RVT asset
  result = unreal.RuntimeVirtualTextureService.create_runtime_virtual_texture(
      "RVT_MyLandscape", "/Game/RVT",
      material_type="BaseColor_Normal_Roughness"
- VibeUE.SkeletonService: Skeleton and Skeletal Mesh service exposed directly to Python.

This service provides comprehensive CRUD operations for Skeleton and SkeletalMesh assets
including bone hierarchy management, retargeting configuration,
curve metadata, and blend profile management.

Python Usage:
  import unreal

  # Discover skeleton assets
  skeletons = unreal.SkeletonService.list_skeletons("/Game", True)

  # Get skeleton info
  info = unreal.SkeletonService.get_skeleton_info("/Game/Characters/SK_Mannequin")
  print(f"Bones: {info.bone_count}, Blend Profiles: {info.blend_profile_count}")

@note All methods are static and thread-safe
@note C++ out parameters become Python return values

**C++ Source:**

- **Plugin**: VibeUE
- **Module**: VibeUE
- **File**: USkeletonService.h
- VibeUE.SoundCueService: SoundCue authoring service exposed directly to Python.

Provides creation, inspection, and editing of SoundCue assets including
their node graphs, attenuation settings, and SoundWave references.

Node indexing: list_nodes() returns nodes in graph order (0-based). Indices
are valid until the next structural mutation, so always re-call list_nodes()
after add/connect/remove operations before referencing indices again.

Audio flow in SoundCue graphs: audio travels FROM leaf nodes TOWARD the root.
WavePlayer nodes produce audio, which feeds UP into Mixer/Random/etc., which
feeds into the cue's root (FirstNode). connect_nodes(parent, child, slot)
means "child provides audio TO parent at input slot".

Python Usage:
  import unreal

  # Create a simple cue with a single wave
  result = unreal.SoundCueService.create_sound_cue(
      "/Game/Audio/SC_Footstep",
      "/Game/Audio/SW_Step_Stone"
- VibeUE.StateTreeService: VibeUE service for creating, inspecting, and editing StateTree assets.
Exposed to Python as unreal.StateTreeService

State paths use "/" separator starting from the subtree root name,
e.g. "Root", "Root/Walking", "Root/Walking/Idle"
- VibeUE.TransactionService: Transaction Service - Python API for the editor undo/redo system (issue #469).

Wraps GEditor's transaction buffer (GEditor->Trans) so agents can drive undo/redo,
group edits into a single named transaction, inspect history, and reset the buffer —
the analogue of pressing Ctrl+Z / Ctrl+Y or using the Edit menu.

IMPORTANT: Most VibeUE service edits already wrap themselves in their own transactions,
so undo() typically reverts the last whole operation. To group MULTIPLE edits into one
undo step, call begin_transaction("My change"), perform the edits, then end_transaction().

Python Usage:
  import unreal
  svc = unreal.TransactionService

  # Group several edits into one undo step
  svc.begin_transaction("Build wall")
  # ... spawn/modify actors ...
  svc.end_transaction()

  svc.undo()                 # revert it
  svc.redo()                 # re-apply it

  state = svc.get_state()    # can_undo/can_redo, undo/redo counts + next titles
  print(state.undo_count, state.next_undo_title)
  for h in svc.get_history(20):
      print(h.title, "(undone)" if h.is_undone else "")

  svc.reset("Test cleanup")  # clears the undo buffer (does NOT touch the world)
- VibeUE.UVMappingService: UV mapping service exposed directly to Python.

Provides automation-grade UV channel manipulation for StaticMesh and SkeletalMesh
assets. All mesh-mutating actions automatically mark the package dirty and rebuild
render data; callers should follow with a save (manage_asset save) once a batch of
edits is complete.

Action groups:

Inspect:
- list_uv_channels           : Per-LOD channel inventory and stats
- get_uv_channel_info        : Stats for one (LOD, channel) pair
- get_uv_health              : Aggregate health report across all LODs

Channel lifecycle:
- add_uv_channel             : Append a new empty UV channel to a LOD
- remove_uv_channel          : Drop a channel and shift remaining channels down
- copy_uv_channel            : Duplicate one channel's UVs into another
- set_uv_channel_count       : Resize the channel array exactly

Generation:
- generate_lightmap_uvs      : Build a packed lightmap UV channel from a source channel
- auto_unwrap_uvs            : Box / planar / cylindrical projection unwrap into a channel
- pack_uvs                   : Repack islands in an existing channel with padding

Transform:
- transform_uvs              : Scale, rotate, translate UVs in a channel
- flip_uvs                   : Mirror U and/or V in a channel

Lightmap settings:
- get_lightmap_settings      : Read source/dest indices, resolution, generate flag
- set_lightmap_settings      : Configure all lightmap-related fields in one call

Visualize:
- export_uv_layout_image     : Render a UV layout PNG for AI / human inspection

Existence:
- mesh_has_uv_channel        : Quick check before reading or writing

Python usage:
  import unreal

  # Quick health check before edits
  ok, health = unreal.UVMappingService.get_uv_health("/Game/Meshes/SM_Wall")

  # Generate lightmap UVs into channel 1 from channel 0
  result = unreal.UVMappingService.generate_lightmap_uvs(
      "/Game/Meshes/SM_Wall", 0, 1, 1.0)

  # Configure lightmap settings (resolution + indices) in one call
  unreal.UVMappingService.set_lightmap_settings(
      "/Game/Meshes/SM_Wall", 1, 0, 128, True)

  # Auto-unwrap a custom UV channel using box projection
  unreal.UVMappingService.auto_unwrap_uvs(
      "/Game/Meshes/SM_Wall", 0, 2, "Box", 66.0)

  # Export the lightmap channel for visual review
  unreal.UVMappingService.export_uv_layout_image(
      "/Game/Meshes/SM_Wall", 0, 1, "D:/uv_wall_lm.png", 1024)
- VibeUE.ViewportService: Viewport Service - Python API for controlling the Unreal Editor level viewport.

Provides access to all viewport camera options from the perspective dropdown menu:
- View type switching (Perspective, Top, Bottom, Left, Right, Front, Back)
- Field of View, Near/Far Clip Plane configuration
- Exposure settings (Game Settings / fixed EV100)
- Game View toggle, Cinematic Control, Camera Shakes
- Viewport layout switching (single pane, quad view 2x2, etc.)
- Camera location/rotation control
- Realtime rendering toggle

Python Usage:
  import unreal

  # Get current viewport state
  info = unreal.ViewportService.get_viewport_info()
  print(f"Type: {info.viewport_type}, FOV: {info.fov}")

  # Switch to orthographic views
  unreal.ViewportService.set_viewport_type("top")
  unreal.ViewportService.set_viewport_type("perspective")

  # Adjust camera properties
  unreal.ViewportService.set_fov(75.0)
  unreal.ViewportService.set_near_clip_plane(10.0)
  unreal.ViewportService.set_far_clip_plane(50000.0)

  # Exposure control
  unreal.ViewportService.set_exposure(True, 1.0)
  unreal.ViewportService.set_exposure_game_settings()

  # Game View and cinematic
  unreal.ViewportService.set_game_view(True)
  unreal.ViewportService.set_allow_cinematic_control(True)

  # Viewport layout (single vs quad)
  unreal.ViewportService.set_viewport_layout("FourPanes2x2")
  unreal.ViewportService.set_viewport_layout("OnePane")

  # Camera position/rotation is engine-side (this service is read-only for pose):
  #   read:  ViewportService.get_viewport_info().location / .rotation
  #   write: EditorAppToolset.SetCameraTransform via call_tool, or
  #          unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
  #              .set_level_viewport_camera_info(location, rotation)

@note ViewportService owns view type, view mode, FOV, clip planes, exposure, game view,
      cinematic control, realtime, camera speed, and layout. It does NOT set camera
      position/rotation (no set_camera_location / set_camera_rotation) — use the engine
      path above. (issue #471)
- VibeUE.WidgetService: Widget service exposed directly to Python.

Provides 41 widget management actions:
- list_widget_blueprints: List all Widget Blueprints in the project
- get_hierarchy: Get widget hierarchy tree
- get_root_widget: Get the root widget of a Widget Blueprint
- list_components: List all widget components in a Widget Blueprint
- search_types: Get available widget types (native types + discovered WBPs for reference)
- get_component_properties: Get properties for a specific component
- add_component: Add a widget component to a Widget Blueprint (native types or custom WBPs by name)
- remove_component: Remove a widget component from a Widget Blueprint
- rename_widget: Rename a widget component in a Widget Blueprint
- validate: Validate widget hierarchy for errors
- get_property: Get a specific property value
- set_property: Set a specific property value
- list_properties: List all editable properties of a component
- get_available_events: Get available events for a widget type
- bind_event: Bind an event to a function
- list_view_models: List all ViewModels registered on a Widget Blueprint
- add_view_model: Add a ViewModel to a Widget Blueprint
- remove_view_model: Remove a ViewModel from a Widget Blueprint
- list_view_model_bindings: List all MVVM bindings on a Widget Blueprint
- add_view_model_binding: Create a binding between a ViewModel property and a widget property
- remove_view_model_binding: Remove an MVVM binding by index
- set_font: Apply a full font configuration to a text widget
- get_font: Read a full font configuration from a text widget
- set_brush: Apply a brush to a widget brush slot
- get_brush: Read a brush from a widget brush slot
- list_animations: List all widget animations on a Widget Blueprint
- create_animation: Create a new widget animation
- remove_animation: Remove a widget animation
- add_animation_track: Add a property track to a widget animation
- add_keyframe: Add a keyframe to a widget animation track
- capture_preview: Render a widget preview to a PNG file
- start_pie: Start Play-In-Editor
- stop_pie: Stop Play-In-Editor
- is_pie_running: Check whether PIE is active
- spawn_widget_in_pie: Spawn a widget instance into the PIE viewport
- get_live_property: Read a property from a live PIE widget instance
- remove_widget_from_pie: Remove a spawned PIE widget instance from the viewport
- widget_blueprint_exists: Check if a Widget Blueprint exists
- widget_exists: Check if a widget component exists in a Widget Blueprint

Python Usage:
  import unreal

  # List all Widget Blueprints
  widgets = unreal.WidgetService.list_widget_blueprints()

  # Get widget hierarchy
  hierarchy = unreal.WidgetService.get_hierarchy("/Game/UI/WBP_MainMenu")

  # List components in a widget
  components = unreal.WidgetService.list_components("/Game/UI/WBP_MainMenu")

  # Add a button component
  result = unreal.WidgetService.add_component("/Game/UI/WBP_MainMenu", "Button", "MyButton", "CanvasPanel_0", True)

  # Get available widget types
  types = unreal.WidgetService.search_types()

  # Get property value
  value = unreal.WidgetService.get_property("/Game/UI/WBP_MainMenu", "MyButton", "Visibility")

  # Set property value
  unreal.WidgetService.set_property("/Game/UI/WBP_MainMenu", "MyButton", "Visibility", "Visible")

  # List ViewModels
  vms = unreal.WidgetService.list_view_models("/Game/UI/WBP_MainMenu")

  # Add a ViewModel
  unreal.WidgetService.add_view_model("/Game/UI/WBP_MainMenu", "MyHealthViewModel", "HealthVM")

  # Add a ViewModel binding
  unreal.WidgetService.add_view_model_binding("/Game/UI/WBP_MainMenu", "HealthVM", "CurrentHealth", "HealthBar", "Percent", "OneWayToDestination")

@note This replaces the JSON-based manage_umg_widget MCP tool
- VibeUE.WorkflowService: High-level, evidence-producing workflows built from VibeUE's lower-level editor primitives.
- AutomationTestToolset.AutomationTestToolset: Automation test discovery and execution toolset.

Wraps the IAutomationControllerManager API (the same backend the Session
Frontend uses) to let MCP clients list available tests, run them, and
retrieve results.

Typical workflow:
  1. DiscoverTests() once per session to initialize workers and load the test list.
  2. ListTests() to find tests by name or tag.
  3. RunTests() with the desired test names.
  4. GetTestStatus() / GetTestResults() to monitor and retrieve results.
  5. StopTests() to abort if needed.
- DataflowAgent.DataflowAgentToolset: Dataflow Agent Toolset - exposes Dataflow graph editing operations as AI agent tools.
- ConfigSettingsToolset.ConfigSettingsToolset: Tools for listing, inspecting, and editing Config Settings sections
- DataRegistryToolset.DataRegistryTools: Provides tools for querying and inspecting Data Registries.
- EditorToolset.EditorAppToolset: Tools for querying and modifying Unreal Editor state: console variables, asset imaging,
actor and asset selection, viewport camera, content browser navigation, and Play-In-Editor
session control.
- EditorToolset.LogsToolset: Provides tools for reading the Unreal Engine output log and controlling
log category verbosity.
- GameFeaturesToolset.GameFeaturesToolset: Provides tools for listing, activating, and deactivating Game Feature Plugins.
- GASToolsets.GameplayCueToolset: Provides tools for inspecting, executing, and managing gameplay cues and their notify assets.
- GASToolsets.AttributeSetToolset: Provides tools for discovering AttributeSet classes and their gameplay attributes.
- GASToolsets.AbilitySystemInspectorToolset: Provides tools for inspecting the runtime state of an AbilitySystemComponent.
Each function takes a direct actor pointer and raises a script error if the
actor is null or has no AbilitySystemComponent.
- GameplayTagsToolset.GameplayTagsToolset: Provides tools for reading and managing gameplay tags in the project's GameplayTagsManager.
- NiagaraToolsets.NiagaraToolset_Info: Niagara Toolset for general Niagara information and guidance.

Provides:
- Enum value lookups
- General usage information

Call these functions when you need context about Niagara types.
- NiagaraToolsets.NiagaraToolset_Component: Niagara Toolset for Niagara Component operations.

Use this toolset when working with:
- Niagara Components on actors
- Runtime Niagara system manipulation
- User variable overrides on component instances
- FX-related operations in levels or blueprints

This is the primary toolset for runtime Niagara operations.
- NiagaraToolsets.NiagaraToolset_Blueprint: Niagara Toolset for Niagara and Blueprint integration.

Provides utilities for creating Blueprint wrappers around Niagara Systems,
making it easier to expose Niagara effects as reusable Blueprint actors.

Use this toolset when you need to create Blueprint-based FX actors from Niagara systems.
- NiagaraToolsets.NiagaraToolset_System: Niagara Toolset for Niagara System operations.

Provides comprehensive access to Niagara System editing, including:
- System, emitter, and module creation and modification
- Schema discovery for understanding structure
- Topology and Summary inspection for viewing current configuration
- Data access for reading and writing properties
- Dependency rollups via GetSystemDependencies
- Dynamic-input chain traversal via GetDynamicInputChain

This is the primary toolset for working with Niagara Systems in the editor.
- NiagaraToolsets.NiagaraToolset_Assets: Niagara Toolset for discovery of Niagara script assets.

Provides:
- GetAssetDiscoveryInfo: project-configured asset discovery groups
- FindNiagaraScripts: asset registry search filtered by usage, visibility, name, and module usage bitmask
- GetNiagaraScriptDigest: decoded asset-registry tags for a single script

All functions read from the asset registry without LoadObject. Pair with
NiagaraToolset_System.AddModule to drop discovered modules into a stack.

Note: FAssetData JSON serialization does not include the TagsAndValues map (it
is not a UPROPERTY), so callers wanting decoded metadata for a result row from
FindNiagaraScripts must round-trip through GetNiagaraScriptDigest.
- PluginToolset.PluginToolset: Tools for creating, editing, enabling, and querying Unreal plugins
- PCGToolset.PCGToolset: Toolset for building and modifying PCG graphs
- PCGToolset.PCGSpatialToolset: PCGSpatial Toolset
- PhysicsToolsets.PhysicsAssetToolset: Provides tools for creating and managing Physics Assets.
- SemanticSearchToolset.SemanticSearchToolset: Toolset exposing the SemanticSearch plugin's hybrid vector + BM25 asset search
to the AI Toolset Registry.
- SlateInspectorToolset.SlateInspectorToolset: Playwright-style Slate UI automation toolset.

Exposes snapshot, screenshot, and interaction tools for driving the
Unreal Editor UI programmatically.  Registered via UToolsetRegistry
so the ModelContextProtocol plugin picks them up automatically.

A shallow root observer (depth 0) continuously tracks top-level
windows.  Before working with a specific window or panel, call
Observe() on it to get deep widget coverage, then Unobserve() when
done.  Observers walk their subtree every ~100ms, assigning refs to
newly appeared widgets and keeping the ref cache current.

Input simulation uses direct Slate event APIs (ProcessKeyCharEvent,
ProcessMouseButtonDownEvent, etc.) rather than the AutomationDriver,
because AutomationDriver's synchronous API deadlocks when called from
the game thread (which is where MCP tool calls execute).
- WorldConditionsToolset.WorldConditionTools: Inspect WorldCondition (FWorldConditionQueryDefinition, FWorldConditionBase) structs.
- UMGToolSet.UMGToolSet: UMG widget toolset for AI-driven widget creation and tree manipulation.

IMPORTANT WORKFLOW - for every widget and slot returned by this toolset:
  1. Call ObjectTools.list_properties(widget) to discover exact property names.
  2. Call ObjectTools.get_properties(widget, [...]) with those exact names.
  3. Call ObjectTools.set_properties(widget, {...}) with those exact names.
Property names vary per widget class and CANNOT be guessed - list_properties is required.
Skipping step 1 causes set_properties to silently fail or set wrong properties.

Returns UObject pointers - ToolsetRegistry serializes them as {"refPath": "..."} automatically.
Pass returned Widget, Slot, and Parent pointers directly to ObjectTools or back to this toolset.
- state_tree_toolset.toolsets.state_tree.StateTreeTools: Inspect StateTree (ST) assets.
- editor_toolset.toolsets.actor.ActorTools: Provides tools for inspecting and modifying actors, including
    their transforms, labels, parent-child relationships, and components.
- editor_toolset.toolsets.asset.AssetTools: Provides tools for interacting with assets in the Unreal project and files on disk.
- editor_toolset.toolsets.blueprint.BlueprintTools: Provides tools for working with Blueprints.
- editor_toolset.toolsets.curve_table.CurveTableTools: Provides tools for creating and editing CurveTable assets.
- editor_toolset.toolsets.data_asset.DataAssetTools: Provides tools for working with Data Assets.
- editor_toolset.toolsets.data_table.DataTableTools: Provides tools for creating and editing DataTable assets.
- editor_toolset.toolsets.material.MaterialTools: Provides tools for creating and editing Material and MaterialFunction assets.
- editor_toolset.toolsets.material_instance.MaterialInstanceTools: Provides tools for creating and modifying MaterialInstanceConstant assets.
- editor_toolset.toolsets.object.ObjectTools: Provides tools for inspecting and modifying the properties of
    Unreal Objects and Unreal Classes, including those in Blueprints.
    Also use this toolset to discover available classes and subclasses.
- editor_toolset.toolsets.primitive.PrimitiveTools: Provides tools for adding primitive geometry components to actors.
- editor_toolset.toolsets.scene.SceneTools: Provides tools for working with the currently loaded level, including
    loading levels, placing and removing actors, controlling the level camera,
    and organizing actors in the outliner.
- editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools: Provides tools for inspecting and modifying skeletal mesh assets, including
    the mesh/materials, bone hierarchies, and sockets.
- editor_toolset.toolsets.static_mesh.StaticMeshTools: Provides tools for inspecting and modifying static mesh assets.
- editor_toolset.toolsets.string_table.StringTableTools: Provides tools for creating and editing StringTable assets.
- editor_toolset.toolsets.programmatic.ProgrammaticToolset: Batches calls to other registered tools through a small sandboxed Python
    script that glues them together with custom logic. The script's purpose is
    tool orchestration, not general Python execution.
- editor_toolset.toolsets.texture.TextureTools: Provides tools for working with Texture assets.
- conversation_toolset.toolsets.conversation.ConversationTools: Inspect Conversation Graph (UConversationDatabase) dialogue assets.
- animation_toolset.toolsets.controlrig.ControlRigTools: Tools for creating and editing Control Rig assets, including hierarchy
    management, graph operations, and node/pin manipulation.
- animation_toolset.toolsets.sequencer.SequencerTools: Core tools for creating and editing Level Sequences in Sequencer. Use
    whenever working with Sequencer - covers sequence lifecycle (create, open,
    close), playback control (play, pause, scrub, speed, loop), sequence
    properties (display rate, frame ranges, marked frames, tick resolution),
    actor bindings (add actors, spawnables, cameras, find and manage bindings),
    tracks (add, find, remove any track type), sections (range, easing, blend
    type, completion mode), selection state, folder organization, sub-sequence
    navigation, event tracks, track filters, and sequence locking. For
    keyframing use SequencerKeyframingTools. For Control Rig use
    SequencerControlRigTools. For outliner inspection use
    SequencerOutlinerTools.
- animation_toolset.toolsets.keyframing.SequencerKeyframingTools: Tools for keyframing and animating properties on the Sequencer
    timeline. Use when adding, querying, or removing keyframes on channels,
    setting default values, evaluating channels at specific times, working
    with the Curve Editor, or managing channel selection. Covers float, bool,
    integer, and string key types with configurable interpolation.
- animation_toolset.toolsets.controlrig_sequencer.SequencerControlRigTools: Tools for animating with Control Rig inside Sequencer. Use when adding
    Control Rig tracks to bindings, getting or setting control values (bool,
    float, int, position, rotator, scale, euler transform, transform), keying
    controls, baking animation to Control Rig, managing layered rigs and
    priority, masking controls per section, space switching (world, parent,
    control, bone), tweening and blending between keys, snapping controls to
    actors, mirroring poses, zeroing transforms, or managing animation layers
    (add, delete, duplicate, reorder, merge, collapse).
- animation_toolset.toolsets.outliner.SequencerOutlinerTools: Tools for inspecting and managing the Sequencer outliner tree. Use when
    getting a snapshot of the outliner hierarchy, querying node children,
    managing outliner selection, expanding or collapsing nodes, or toggling
    node states like mute, solo, deactivate, lock, and pin. Also useful for
    test verification of Sequencer UI state.
- animation_toolset.toolsets.conditions.SequencerConditionTools: Tools for managing runtime conditions on Sequencer tracks, sections, and
    track rows. Use when setting up dynamic conditions that control whether
    tracks or sections evaluate at runtime based on platform, gameplay state,
    or custom logic. Supports MovieScenePlatformCondition,
    MovieSceneDirectorBlueprintCondition, and MovieSceneGroupCondition types.
- animation_toolset.toolsets.custom_bindings.SequencerCustomBindingTools: Tools for converting and managing custom binding types in Sequencer. Use
    when converting between possessable, spawnable, and custom/replaceable
    bindings, querying what custom binding type a binding uses, accessing
    custom binding objects for property inspection, or changing the actor
    template class on spawnables/replaceables.
- animation_toolset.toolsets.import_export.SequencerImportExportTools: Tools for importing and exporting animation data to and from Sequencer.
    Use when exporting bindings or Control Rig animation to FBX files,
    importing FBX animation onto bindings or Control Rig tracks, exporting
    animation to AnimSequence assets, or linking AnimSequences for
    auto-updates.
- aimodule_toolset.toolsets.behavior_tree.BehaviorTreeTools: Inspect BehaviorTree (BT) assets.
