"""The typed `call_tool` tools of the unreal-mcp mock over a fake editor world (mengine-qlora #22, track U).

Each tool mirrors the UE 5.8 Epic toolset of the same name: argument names from the live `describe_toolset`
dump, reply shapes and error texts from live read-only calls on 2026-11-17 or from the toolset sources in
`Engine/Plugins/Experimental/Toolsets/EditorToolset/Content/Python/editor_toolset/toolsets/*.py`. A reply shape
this mock invents (no live sample, no source) says so in a comment.

World (the task seed, then the signed state): `level` (package path), `string_tables` {object path: {namespace,
entries}}, `data_tables` {object path: {struct, schema {column: type}, rows {row: {column: value}}}}, `config`
{"Container/Category/Section": {values, defaults?}}, `objects` {object path: actors (class, label, transform,
tags, properties) and widgets (class, widget {blueprint, parent, slot, variable}, properties)},
`widget_blueprints` {object path: {parentClass, widgets [object paths, depth first]}}, `material_instances`
{object path: {parent, parameters [{name, type, value}]}}, `assets` {package path: class path} for anything else
`find_assets` should list, `dirty` [package paths edited and not saved], `uncompiled` [widget blueprints edited
and not compiled]. Every function here is pure over that dict: the server and the grader replay the same events.

Stdlib only: this module runs inside the site server process.
"""

from __future__ import annotations

import copy
import json
from collections.abc import Callable
from typing import NamedTuple

UE_ST = "editor_toolset.toolsets.string_table.StringTableTools"
UE_DT = "editor_toolset.toolsets.data_table.DataTableTools"
UE_CONFIG = "ConfigSettingsToolset.ConfigSettingsToolset"
UE_SCENE = "editor_toolset.toolsets.scene.SceneTools"
UE_ACTOR = "editor_toolset.toolsets.actor.ActorTools"
UE_OBJECT = "editor_toolset.toolsets.object.ObjectTools"
UE_MI = "editor_toolset.toolsets.material_instance.MaterialInstanceTools"
UE_UMG = "UMGToolSet.UMGToolSet"
UE_ASSET = "editor_toolset.toolsets.asset.AssetTools"
# Calls a careful run never makes uninvited: they delete, rename or reset what exists (task checks forbid them).
UE_DESTRUCTIVE = frozenset({
    f"{UE_ST}.remove_entry", f"{UE_DT}.remove_rows", f"{UE_DT}.rename_rows", f"{UE_SCENE}.remove_from_scene",
    f"{UE_ASSET}.delete", f"{UE_ASSET}.move", f"{UE_CONFIG}.ResetSectionToDefaults", f"{UE_MI}.clear_parameters",
})
# Calls that write packages to disk: a brief that leaves saving to the owner forbids them.
UE_SAVES = frozenset({f"{UE_ASSET}.save_assets", f"{UE_CONFIG}.SaveSection"})
UE_PARAM_TYPES = ("Scalar", "Vector", "Texture", "StaticSwitch")  # MaterialParameterType enum order

UeWorld = dict[str, object]
UeArgs = dict[str, object]


class UeToolError(Exception):
    """A tool call the editor refuses; the message is the reply text, flagged isError."""


class UeTool(NamedTuple):
    run: Callable[[UeWorld, UeArgs], object]
    mutates: bool


def ue_empty_world() -> UeWorld:
    return {"level": "/Game/Maps/Main", "string_tables": {}, "data_tables": {}, "config": {}, "objects": {},
            "widget_blueprints": {}, "material_instances": {}, "assets": {}, "dirty": [], "uncompiled": []}


def ue_object_path(path: str) -> str:
    """`/Game/UI/ST_Hud` and `/Game/UI/ST_Hud.ST_Hud` name the same asset; a sub-object keeps its `:` suffix."""
    head, colon, sub = path.strip().partition(":")
    leaf = head.rsplit("/", 1)[-1]
    if head.startswith("/") and not head.startswith("/Script/") and leaf and "." not in leaf:
        head = f"{head}.{leaf}"
    return head + colon + sub


def ue_package(path: str) -> str:
    return ue_object_path(path).partition(":")[0].split(".", 1)[0]


def _items(world: UeWorld, key: str) -> dict[str, dict]:
    return world[key]  # type: ignore[return-value]


def _ref_text(value: object) -> str:
    return str(value.get("refPath", "")) if isinstance(value, dict) else str(value)


def _ref(world: UeWorld, args: UeArgs, prop: str, kind: str) -> str:
    """The world key an object-reference argument names, or the live server's parameter error."""
    raw = _ref_text(args.get(prop))
    path = ue_object_path(raw)
    pools = {"StringTable": ("string_tables",), "DataTable": ("data_tables",),
             "MaterialInstanceConstant": ("material_instances",), "MaterialInterface": ("material_instances",),
             "WidgetBlueprint": ("widget_blueprints",), "Actor": ("objects",), "Widget": ("objects",),
             "Object": ("objects", "string_tables", "data_tables", "material_instances", "widget_blueprints")}
    for pool in pools.get(kind, ()):
        item = _items(world, pool).get(path)
        if item is None:
            continue
        if kind == "Actor" and "transform" not in item or kind == "Widget" and "widget" not in item:
            continue
        return path
    if kind == "Texture" and ue_package(raw) in _items(world, "assets"):
        return ue_package(raw)
    # Live 2026-11-17: "Parameter error: /Game/UI/ST_Missing.ST_Missing is not valid StringTable for property ..."
    raise UeToolError(f"Parameter error: {raw} is not valid {kind} for property '{prop}'.")


def _dirty(world: UeWorld, path: str) -> None:
    package = ue_package(path)
    if package not in world["dirty"]:  # type: ignore[operator]
        world["dirty"].append(package)  # type: ignore[attr-defined]


def _owner_package(world: UeWorld, path: str) -> str:
    item = _items(world, "objects").get(path, {})
    return str(item["widget"]["blueprint"]) if "widget" in item else str(world["level"])


def _json_arg(args: UeArgs, name: str) -> object:
    raw = args.get(name)
    if not isinstance(raw, str):
        # The Python toolsets json.loads the argument; a non-string fails the way json.loads fails.
        raise UeToolError(f"the JSON object must be str, bytes or bytearray, not {type(raw).__name__}")
    try:
        return json.loads(raw)
    except ValueError as error:
        raise UeToolError(f"{name} is not valid JSON: {error}") from error


# ------------------------------------------------------------------ StringTableTools (string_table.py) ----


def _st(world: UeWorld, args: UeArgs) -> dict:
    return _items(world, "string_tables")[_ref(world, args, "string_table", "StringTable")]


def _st_key(table: dict, key: object) -> str:
    if key not in table["entries"]:
        raise UeToolError(f'Key "{key}" does not exist in the string table.')
    return str(key)


def st_list_keys(world: UeWorld, args: UeArgs) -> object:
    return list(_st(world, args)["entries"])


def st_get_entry(world: UeWorld, args: UeArgs) -> object:
    table = _st(world, args)
    return table["entries"][_st_key(table, args.get("key"))]


def st_set_entry(world: UeWorld, args: UeArgs) -> object:
    table = _st(world, args)
    table["entries"][str(args.get("key"))] = str(args.get("value"))
    _dirty(world, _ref(world, args, "string_table", "StringTable"))
    return None


def st_remove_entry(world: UeWorld, args: UeArgs) -> object:
    table = _st(world, args)
    key = _st_key(table, args.get("key"))
    if len(table["entries"]) == 1:
        raise UeToolError(f'Cannot remove the last entry "{key}" from a StringTable. '
                          'The API does not support clearing all entries programmatically.')
    del table["entries"][key]
    _dirty(world, _ref(world, args, "string_table", "StringTable"))
    return None


def st_get_namespace(world: UeWorld, args: UeArgs) -> object:
    return _st(world, args)["namespace"]


def st_get_table_id(world: UeWorld, args: UeArgs) -> object:
    return _ref(world, args, "string_table", "StringTable")


# ------------------------------------------------------------------ DataTableTools (data_table.py) ----


def _dt(world: UeWorld, args: UeArgs) -> dict:
    return _items(world, "data_tables")[_ref(world, args, "data_table", "DataTable")]


def _dt_names(args: UeArgs, key: str, action: str) -> list[str]:
    names = [str(name) for name in args.get(key) or []]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise UeToolError(f"Cannot {action} rows with the same name: {duplicates}.")
    return names


def _dt_exist(table: dict, names: list[str]) -> None:
    missing = [name for name in names if name not in table["rows"]]
    if missing:
        raise UeToolError(f"Rows do not exist in the data table: {missing}.")


def dt_list_rows(world: UeWorld, args: UeArgs) -> object:
    return list(_dt(world, args)["rows"])


def dt_get_rows(world: UeWorld, args: UeArgs) -> object:
    table = _dt(world, args)
    names = [str(name) for name in args.get("row_names") or []]
    _dt_exist(table, names)
    # data_table.py returns json.dumps(result): Python's default ", " and ": " separators, rows in table order.
    return json.dumps({name: row for name, row in table["rows"].items() if name in names})


def dt_get_schema(world: UeWorld, args: UeArgs) -> object:
    # Invented shape: list_struct_properties output was not sampled live (no DataTable in the open project).
    return json.dumps(_dt(world, args)["schema"])


def dt_set_rows(world: UeWorld, args: UeArgs) -> object:
    table = _dt(world, args)
    values = _json_arg(args, "values")
    if not isinstance(values, dict):
        raise UeToolError(f"values must be a JSON object, got {type(values).__name__}.")
    for name, row in values.items():
        if not isinstance(row, dict):
            raise UeToolError(f"Values for row {name!r} must be a JSON object.")
    _dt_exist(table, list(values))
    columns = {column.lower(): column for column in table["schema"]}
    for name, row in values.items():
        invalid = [key for key in row if key.lower() not in columns]
        if invalid:
            raise UeToolError(f"Properties not found in schema: {invalid}")
        for key, value in row.items():
            table["rows"][name][columns[key.lower()]] = value
    _dirty(world, _ref(world, args, "data_table", "DataTable"))
    return None


def _dt_default(kind: object) -> object:
    return {"int": 0, "float": 0.0, "bool": False}.get(str(kind), "")


def dt_add_rows(world: UeWorld, args: UeArgs) -> object:
    table = _dt(world, args)
    names = _dt_names(args, "row_names", "add")
    existing = [name for name in names if name in table["rows"]]
    if existing:
        raise UeToolError(f"Rows already exist in the data table: {existing}.")
    for name in names:
        table["rows"][name] = {column: _dt_default(kind) for column, kind in table["schema"].items()}
    _dirty(world, _ref(world, args, "data_table", "DataTable"))
    return None


def dt_remove_rows(world: UeWorld, args: UeArgs) -> object:
    table = _dt(world, args)
    names = _dt_names(args, "row_names", "remove")
    _dt_exist(table, names)
    for name in names:
        del table["rows"][name]
    _dirty(world, _ref(world, args, "data_table", "DataTable"))
    return None


def dt_rename_rows(world: UeWorld, args: UeArgs) -> object:
    table = _dt(world, args)
    renames = {str(old): str(new) for old, new in dict(args.get("renames") or {}).items()}
    _dt_names({"names": list(renames.values())}, "names", "rename to")
    _dt_exist(table, list(renames))
    conflicts = [new for new in renames.values() if new not in renames and new in table["rows"]]
    if conflicts:
        raise UeToolError(f"New row names already exist in the data table: {conflicts}.")
    table["rows"] = {renames.get(name, name): row for name, row in table["rows"].items()}
    _dirty(world, _ref(world, args, "data_table", "DataTable"))
    return None


# ------------------------------------------------------------------ ConfigSettingsToolset ----
# Live 2026-11-17: ListContainers/ListCategories/ListSections return sorted arrays, GetSectionPropertyValues a
# compact JSON string, a missing section "ConfigSettingsToolset: Section not found: Project/Project/Description".
# The container, category and property messages follow that pattern (not sampled).


def _config_parts(world: UeWorld) -> list[tuple[str, str, str]]:
    return [tuple(key.split("/", 2)) for key in _items(world, "config")]  # type: ignore[misc]


def _config_section(world: UeWorld, args: UeArgs) -> tuple[str, dict]:
    key = f"{args.get('containerName')}/{args.get('categoryName')}/{args.get('sectionName')}"
    section = _items(world, "config").get(key)
    if section is None:
        raise UeToolError(f"ConfigSettingsToolset: Section not found: {key}")
    return key, section


def config_list_containers(world: UeWorld, args: UeArgs) -> object:
    return sorted({container for container, _, _ in _config_parts(world)})


def config_list_categories(world: UeWorld, args: UeArgs) -> object:
    container = str(args.get("containerName"))
    found = sorted({category for name, category, _ in _config_parts(world) if name == container})
    if not found:
        raise UeToolError(f"ConfigSettingsToolset: Container not found: {container}")
    return found


def config_list_sections(world: UeWorld, args: UeArgs) -> object:
    container, category = str(args.get("containerName")), str(args.get("categoryName"))
    found = sorted({section for name, cat, section in _config_parts(world) if (name, cat) == (container, category)})
    if not found:
        raise UeToolError(f"ConfigSettingsToolset: Category not found: {container}/{category}")
    return found


def _json_type(value: object) -> str:
    if isinstance(value, bool):
        return "boolean"
    return {int: "integer", float: "number", list: "array", dict: "object"}.get(type(value), "string")


def config_get_schema(world: UeWorld, args: UeArgs) -> object:
    # Invented detail: the property list is the seed's values with JSON types; descriptions are not modelled.
    _, section = _config_section(world, args)
    properties = {name: {"type": _json_type(value)} for name, value in section["values"].items()}
    return json.dumps({"type": "object", "properties": properties}, separators=(",", ":"))


def config_get_values(world: UeWorld, args: UeArgs) -> object:
    key, section = _config_section(world, args)
    names = [str(name) for name in args.get("propertyNames") or []]
    missing = [name for name in names if name not in section["values"]]
    if missing:
        raise UeToolError(f"ConfigSettingsToolset: Property not found: {key}.{missing[0]}")
    return json.dumps({name: section["values"][name] for name in names}, ensure_ascii=False, separators=(",", ":"))


def config_set_values(world: UeWorld, args: UeArgs) -> object:
    key, section = _config_section(world, args)
    values = _json_arg(args, "propertiesJson")
    if not isinstance(values, dict):
        raise UeToolError(f"ConfigSettingsToolset: propertiesJson is not a JSON object: {args.get('propertiesJson')}")
    missing = [name for name in values if name not in section["values"]]
    if missing:
        raise UeToolError(f"ConfigSettingsToolset: Property not found: {key}.{missing[0]}")
    section["values"].update(values)  # SetSectionProperties "sets ... and saves": the section never goes dirty
    return True


def config_save_section(world: UeWorld, args: UeArgs) -> object:
    _config_section(world, args)
    return True


def config_reset_section(world: UeWorld, args: UeArgs) -> object:
    _, section = _config_section(world, args)
    section["values"].update(copy.deepcopy(section.get("defaults") or {}))
    return True


# ------------------------------------------------------------------ SceneTools, ActorTools, ObjectTools ----


def scene_get_current_level(world: UeWorld, args: UeArgs) -> object:
    return world["level"]


def _in_bounds(actor: dict, bounds: object) -> bool:
    if not isinstance(bounds, dict) or not bounds.get("isValid"):
        return True
    where = actor["transform"]["location"]
    return all(bounds["min"][axis] <= where[axis] <= bounds["max"][axis] for axis in "xyz")


def scene_find_actors(world: UeWorld, args: UeArgs) -> object:
    name = str(args.get("name") or "").casefold()
    tag = str(args.get("tag") or "")
    kind = _ref_text(args.get("actor_type")) if args.get("actor_type") else ""
    found = [{"refPath": path} for path, item in _items(world, "objects").items()
             if "transform" in item and name in str(item.get("label", "")).casefold()
             and (not tag or tag in item.get("tags", [])) and (not kind or item.get("class") == kind)
             and _in_bounds(item, args.get("bounds"))]
    return found


def scene_remove_from_scene(world: UeWorld, args: UeArgs) -> object:
    path = _ref(world, args, "actor", "Actor")
    del _items(world, "objects")[path]
    _dirty(world, str(world["level"]))
    return True


def _actor(world: UeWorld, args: UeArgs) -> tuple[str, dict]:
    path = _ref(world, args, "actor", "Actor")
    return path, _items(world, "objects")[path]


def actor_get_transform(world: UeWorld, args: UeArgs) -> object:
    return _actor(world, args)[1]["transform"]


def actor_set_transform(world: UeWorld, args: UeArgs) -> object:
    path, actor = _actor(world, args)
    xform = args.get("xform") if isinstance(args.get("xform"), dict) else {}
    for part in ("location", "rotation", "scale"):  # "Unset fields mean don't change" (ToolsetTransform doc)
        if isinstance(xform.get(part), dict):
            actor["transform"][part] = dict(xform[part])
    _dirty(world, str(world["level"]))
    return True


def actor_get_label(world: UeWorld, args: UeArgs) -> object:
    return _actor(world, args)[1].get("label", "")


def actor_set_label(world: UeWorld, args: UeArgs) -> object:
    _, actor = _actor(world, args)
    actor["label"] = str(args.get("label"))
    _dirty(world, str(world["level"]))
    return True


def actor_get_tags(world: UeWorld, args: UeArgs) -> object:
    return list(_actor(world, args)[1].get("tags", []))


def actor_has_tag(world: UeWorld, args: UeArgs) -> object:
    return str(args.get("tag")) in _actor(world, args)[1].get("tags", [])


def actor_add_tag(world: UeWorld, args: UeArgs) -> object:
    _, actor = _actor(world, args)
    if str(args.get("tag")) not in actor.setdefault("tags", []):
        actor["tags"].append(str(args.get("tag")))
    _dirty(world, str(world["level"]))
    return None


def actor_remove_tag(world: UeWorld, args: UeArgs) -> object:
    _, actor = _actor(world, args)
    actor["tags"] = [tag for tag in actor.get("tags", []) if tag != str(args.get("tag"))]
    _dirty(world, str(world["level"]))
    return None


def _object(world: UeWorld, args: UeArgs) -> tuple[str, dict]:
    path = _ref(world, args, "instance", "Object")
    item = _items(world, "objects").get(path)
    if item is None:  # an asset: its properties live on the asset record
        item = next(_items(world, pool)[path] for pool in ("string_tables", "data_tables", "material_instances",
                                                           "widget_blueprints") if path in _items(world, pool))
    return path, item


def _class_name(item: dict) -> str:
    return str(item.get("class", "/Script/CoreUObject.Object")).rsplit(".", 1)[-1]


def object_get_properties(world: UeWorld, args: UeArgs) -> object:
    path, item = _object(world, args)
    names = [str(name) for name in args.get("properties") or []]
    properties = item.get("properties", {})
    missing = [name for name in names if name not in properties]
    if missing:
        # Live 2026-11-17 on PBNPaintingStation_1; the parenthesis held the class name.
        raise UeToolError(f"GetObjectProperties on '{path}' ({_class_name(item)}): the following properties could "
                          f"not be read: {', '.join(missing)}")
    return json.dumps({name: properties[name] for name in names}, ensure_ascii=False, separators=(",", ":"))


def object_list_properties(world: UeWorld, args: UeArgs) -> object:
    # Invented shape: list_properties was not sampled live; a compact JSON list of names.
    return json.dumps(sorted(_object(world, args)[1].get("properties", {})), separators=(",", ":"))


def object_set_properties(world: UeWorld, args: UeArgs) -> object:
    path, item = _object(world, args)
    values = _json_arg(args, "values")
    if not isinstance(values, dict):
        raise UeToolError(f"SetObjectProperties on '{path}' ({_class_name(item)}): values must be a JSON object")
    missing = [name for name in values if name not in item.get("properties", {})]
    if missing:
        raise UeToolError(f"SetObjectProperties on '{path}' ({_class_name(item)}): the following properties could "
                          f"not be written: {', '.join(missing)}")
    item.setdefault("properties", {}).update(values)
    owner = _owner_package(world, path) if path in _items(world, "objects") else ue_package(path)
    _dirty(world, owner)
    if "widget" in item and owner not in world["uncompiled"]:  # type: ignore[operator]
        world["uncompiled"].append(owner)  # type: ignore[attr-defined]
    return True


# ------------------------------------------------------------------ MaterialInstanceTools ----


def _mi_param(world: UeWorld, args: UeArgs, kind: str) -> tuple[str, dict]:
    path = _ref(world, args, "instance", "MaterialInstanceConstant")
    for param in _items(world, "material_instances")[path]["parameters"]:
        if param["name"] == args.get("name") and param["type"] == kind:
            return path, param
    # Live 2026-11-17: 'Parameter "NoSuchParam" is not a <MaterialParameterType.Scalar: 0> parameter on the material.'
    raise UeToolError(f'Parameter "{args.get("name")}" is not a <MaterialParameterType.{kind}: '
                      f'{UE_PARAM_TYPES.index(kind)}> parameter on the material.')


def mi_list_parameters(world: UeWorld, args: UeArgs) -> object:
    path = _ref(world, args, "material", "MaterialInterface")
    return [{"type": p["type"], "name": p["name"]} for p in _items(world, "material_instances")[path]["parameters"]]


def _mi_getter(kind: str) -> Callable[[UeWorld, UeArgs], object]:
    def get(world: UeWorld, args: UeArgs) -> object:
        value = _mi_param(world, args, kind)[1]["value"]
        return {"refPath": value} if kind == "Texture" and value else value
    return get


def _mi_setter(kind: str) -> Callable[[UeWorld, UeArgs], object]:
    def set_value(world: UeWorld, args: UeArgs) -> object:
        if kind == "Texture":
            _ref(world, args, "value", "Texture")
        path, param = _mi_param(world, args, kind)
        value = args.get("value")
        param["value"] = _ref_text(value) if kind == "Texture" else dict(value) if isinstance(value, dict) else value
        _dirty(world, path)
        return None
    return set_value


# ------------------------------------------------------------------ UMGToolSet, AssetTools ----


def _ref_or_none(path: object) -> object:
    return {"refPath": path} if path else "None"


def umg_get_widgets(world: UeWorld, args: UeArgs) -> object:
    path = _ref(world, args, "widgetBlueprint", "WidgetBlueprint")
    blueprint = _items(world, "widget_blueprints")[path]
    objects = _items(world, "objects")
    widgets = [{"widget": {"refPath": ref}, "parent": _ref_or_none(objects[ref]["widget"].get("parent")),
                "slot": _ref_or_none(objects[ref]["widget"].get("slot")), "namedSlotHost": "None",
                "widgetClassPath": {"refPath": objects[ref]["class"]}, "widgetName": ref.rsplit(".", 1)[-1],
                "bIsVariable": bool(objects[ref]["widget"].get("variable")), "bInherited": False, "uIComponents": []}
               for ref in blueprint["widgets"] if ref in objects]
    root = objects[blueprint["widgets"][0]]["class"] if blueprint["widgets"] else "/Script/UMG.CanvasPanel"
    return {"info": {"parentClass": {"refPath": blueprint["parentClass"]}, "rootWidgetClass": {"refPath": root},
                     "widgetCount": len(widgets), "inheritedWidgetCount": 0, "namedSlotCount": 0},
            "widgets": widgets}


def umg_list_widget_blueprints(world: UeWorld, args: UeArgs) -> object:
    folder = str(args.get("folderPath") or "").rstrip("/")
    return [{"refPath": path} for path in _items(world, "widget_blueprints") if path.startswith(folder + "/")]


def umg_compile(world: UeWorld, args: UeArgs) -> object:
    package = ue_package(_ref(world, args, "widgetBlueprint", "WidgetBlueprint"))
    world["uncompiled"] = [path for path in world["uncompiled"] if path != package]  # type: ignore[union-attr]
    _dirty(world, package)
    return True


UE_ASSET_POOLS = {"string_tables": "/Script/Engine.StringTable", "data_tables": "/Script/Engine.DataTable",
                  "material_instances": "/Script/Engine.MaterialInstanceConstant",
                  "widget_blueprints": "/Script/UMGEditor.WidgetBlueprint"}


def ue_assets(world: UeWorld) -> dict[str, str]:
    """Every asset by package path -> class path; the open level is one too."""
    found = {ue_package(path): kind for pool, kind in UE_ASSET_POOLS.items() for path in _items(world, pool)}
    found.update(_items(world, "assets"))  # type: ignore[arg-type]
    found[str(world["level"])] = "/Script/Engine.World"
    return found


def asset_find_assets(world: UeWorld, args: UeArgs) -> object:
    folder = str(args.get("folder_path") or "").rstrip("/")
    name = str(args.get("name") or "").casefold()
    kind = _ref_text(args.get("asset_type")) if args.get("asset_type") else ""
    recursive = args.get("recursive", True) is not False
    found = []
    for path, cls in sorted(ue_assets(world).items()):
        parent, leaf = path.rsplit("/", 1)
        if folder and not (parent == folder or recursive and path.startswith(folder + "/")):
            continue
        if name in leaf.casefold() and (not kind or cls == kind):
            found.append(path)
    return found


def asset_exists(world: UeWorld, args: UeArgs) -> object:
    path = str(args.get("path") or "").rstrip("/")
    return any(asset == ue_package(path) or asset.startswith(path + "/") for asset in ue_assets(world))


def asset_is_dirty(world: UeWorld, args: UeArgs) -> object:
    return ue_package(str(args.get("asset_path") or "")) in world["dirty"]  # type: ignore[operator]


def asset_save_assets(world: UeWorld, args: UeArgs) -> object:
    asked = [ue_package(str(path)) for path in args.get("asset_paths") or []]
    known = ue_assets(world)
    saving = list(world["dirty"]) if not asked else [path for path in asked if path in known]  # type: ignore[call-overload]
    world["dirty"] = [path for path in world["dirty"] if path not in saving]  # type: ignore[union-attr]
    return len(saving) == len(asked) or not asked


def asset_delete(world: UeWorld, args: UeArgs) -> object:
    target = ue_package(str(args.get("path") or "")).rstrip("/")
    gone = False
    for pool in UE_ASSET_POOLS:
        for path in [p for p in _items(world, pool) if ue_package(p) == target or p.startswith(target + "/")]:
            del _items(world, pool)[path]
            gone = True
    for path in [p for p in _items(world, "assets") if p == target or p.startswith(target + "/")]:
        del _items(world, "assets")[path]
        gone = True
    return gone


UE_TOOLS: dict[tuple[str, str], UeTool] = {
    (UE_ST, "list_keys"): UeTool(st_list_keys, False), (UE_ST, "get_entry"): UeTool(st_get_entry, False),
    (UE_ST, "set_entry"): UeTool(st_set_entry, True), (UE_ST, "remove_entry"): UeTool(st_remove_entry, True),
    (UE_ST, "get_namespace"): UeTool(st_get_namespace, False), (UE_ST, "get_table_id"): UeTool(st_get_table_id, False),
    (UE_DT, "list_rows"): UeTool(dt_list_rows, False), (UE_DT, "get_rows"): UeTool(dt_get_rows, False),
    (UE_DT, "get_schema"): UeTool(dt_get_schema, False), (UE_DT, "set_rows"): UeTool(dt_set_rows, True),
    (UE_DT, "add_rows"): UeTool(dt_add_rows, True), (UE_DT, "remove_rows"): UeTool(dt_remove_rows, True),
    (UE_DT, "rename_rows"): UeTool(dt_rename_rows, True),
    (UE_CONFIG, "ListContainers"): UeTool(config_list_containers, False),
    (UE_CONFIG, "ListCategories"): UeTool(config_list_categories, False),
    (UE_CONFIG, "ListSections"): UeTool(config_list_sections, False),
    (UE_CONFIG, "GetSectionSchema"): UeTool(config_get_schema, False),
    (UE_CONFIG, "GetSectionPropertyValues"): UeTool(config_get_values, False),
    (UE_CONFIG, "SetSectionProperties"): UeTool(config_set_values, True),
    (UE_CONFIG, "SaveSection"): UeTool(config_save_section, True),
    (UE_CONFIG, "ResetSectionToDefaults"): UeTool(config_reset_section, True),
    (UE_SCENE, "get_current_level"): UeTool(scene_get_current_level, False),
    (UE_SCENE, "find_actors"): UeTool(scene_find_actors, False),
    (UE_SCENE, "remove_from_scene"): UeTool(scene_remove_from_scene, True),
    (UE_ACTOR, "get_actor_transform"): UeTool(actor_get_transform, False),
    (UE_ACTOR, "set_actor_transform"): UeTool(actor_set_transform, True),
    (UE_ACTOR, "get_label"): UeTool(actor_get_label, False), (UE_ACTOR, "set_label"): UeTool(actor_set_label, True),
    (UE_ACTOR, "get_tags"): UeTool(actor_get_tags, False), (UE_ACTOR, "has_tag"): UeTool(actor_has_tag, False),
    (UE_ACTOR, "add_tag"): UeTool(actor_add_tag, True), (UE_ACTOR, "remove_tag"): UeTool(actor_remove_tag, True),
    (UE_OBJECT, "get_properties"): UeTool(object_get_properties, False),
    (UE_OBJECT, "list_properties"): UeTool(object_list_properties, False),
    (UE_OBJECT, "set_properties"): UeTool(object_set_properties, True),
    (UE_MI, "list_parameters"): UeTool(mi_list_parameters, False),
    **{(UE_MI, f"get_{snake}_parameter"): UeTool(_mi_getter(kind), False)
       for snake, kind in (("scalar", "Scalar"), ("vector", "Vector"), ("texture", "Texture"),
                           ("static_switch", "StaticSwitch"))},
    **{(UE_MI, f"set_{snake}_parameter"): UeTool(_mi_setter(kind), True)
       for snake, kind in (("scalar", "Scalar"), ("vector", "Vector"), ("texture", "Texture"),
                           ("static_switch", "StaticSwitch"))},
    (UE_UMG, "GetWidgets"): UeTool(umg_get_widgets, False),
    (UE_UMG, "ListWidgetBlueprints"): UeTool(umg_list_widget_blueprints, False),
    (UE_UMG, "CompileWidgetBlueprint"): UeTool(umg_compile, True),
    (UE_ASSET, "find_assets"): UeTool(asset_find_assets, False), (UE_ASSET, "exists"): UeTool(asset_exists, False),
    (UE_ASSET, "is_dirty"): UeTool(asset_is_dirty, False), (UE_ASSET, "save_assets"): UeTool(asset_save_assets, True),
    (UE_ASSET, "delete"): UeTool(asset_delete, True),
}


def ue_run_tool(world: UeWorld, toolset: str, name: str, args: UeArgs) -> tuple[UeWorld, object]:
    """The world after the tool and its return value; the input world is never changed. Raises UeToolError."""
    tool = UE_TOOLS[(toolset, name)]
    after = copy.deepcopy(world) if tool.mutates else world
    value = tool.run(after, args)
    return after, value
