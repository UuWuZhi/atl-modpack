from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


RESOURCE_FILES = (
    Path("extern/resources_0.json"),
    Path("extern/resources_1.json"),
    Path("extern/resources_2.json"),
)
DEFAULT_LOG = Path("extern/crafttweaker.log")
DEFAULT_REPORT = Path("docs/maintenance/item-unification-candidates.json")
DEFAULT_TAG_ROOT = Path("kubejs/data/c/tags/item/food")
DEFAULT_RULES = Path("kubejs/server_scripts/generated/item_unification_rules.json")

ITEM_IN_ANGLE = re.compile(r"<item:([^>]+)>")
ITEM_IN_JSON_ITEM = re.compile(r'(?:"item"\s*:\s*"([^"]+)")')
ITEM_IN_JSON_ID = re.compile(r'(?:"id"\s*:\s*"([^"]+)")')
RECIPE_ID_PATTERNS = (
    re.compile(r'Recipe name:\s*([^,]+),'),
    re.compile(r'with name:\s*\'([^\']+)\''),
    re.compile(r'add(?:Json)?Recipe\("([^"]+)"'),
    re.compile(r'craftingTable\.add(?:Shaped|Shapeless)\("([^"]+)"'),
)
RECIPE_TYPE_PATTERNS = (
    re.compile(r"<recipetype:([^>]+)>"),
    re.compile(r"Adding '([^']+)' recipe"),
    re.compile(r"Recipe Serializer:\s*([^~]+?)\s*~~"),
)


def load_groups(resource_files: tuple[Path, ...]) -> list[dict]:
    groups: list[dict] = []
    seen_group_keys: set[tuple[tuple[str, ...], str]] = set()
    item_targets: dict[str, tuple[str, str]] = {}

    for resource_file in resource_files:
        data = json.loads(resource_file.read_text(encoding="utf-8"))
        for index, entry in enumerate(data, start=1):
            members = list(entry["matchItems"])
            target = entry["resultItems"]
            key = (tuple(sorted(members)), target)
            if key in seen_group_keys:
                continue
            seen_group_keys.add(key)

            source = f"{resource_file.as_posix()}#{index}"
            for member in members:
                previous = item_targets.get(member)
                if previous and previous[0] != target:
                    raise ValueError(
                        f"conflicting target for {member}: "
                        f"{previous[0]} from {previous[1]} vs {target} from {source}"
                    )
                item_targets[member] = (target, source)

            groups.append(
                {
                    "source": source,
                    "target": target,
                    "tag": f"c:food/{target.split(':', 1)[1]}",
                    "members": members,
                }
            )

    return groups


def write_tags(groups: list[dict], tag_root: Path) -> list[Path]:
    written: list[Path] = []
    tag_root.mkdir(parents=True, exist_ok=True)

    for group in groups:
        tag_path = tag_root / f"{group['tag'].split('/', 1)[1]}.json"
        payload = {
            "replace": False,
            "values": group["members"],
        }
        tag_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        written.append(tag_path)

    return written


def write_kubejs_rules(groups: list[dict], rules_file: Path) -> None:
    rules_file.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "groups": groups,
        "containerRecipeIds": [
            "farmersdelight:beef_bulgogi",
            "farmersdelight:caramel_chicken",
            "pineapple_delight:cooking/pineapple_fried_rice",
            "farmersdelight:honey_chili_chicken",
            "farmersdelight:melon_rind_stirfry",
        ],
    }
    rules_file.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def extract_recipe_id(line: str) -> str | None:
    for pattern in RECIPE_ID_PATTERNS:
        match = pattern.search(line)
        if match:
            return match.group(1).strip()
    return None


def extract_recipe_type(line: str) -> str | None:
    if "craftingTable.addShaped" in line or "craftingTable.addShapeless" in line:
        return "minecraft:crafting"
    if "campfire.addRecipe" in line:
        return "minecraft:campfire_cooking"
    if "smoker.addRecipe" in line:
        return "minecraft:smoking"
    if "furnace.addRecipe" in line:
        return "minecraft:smelting"

    for pattern in RECIPE_TYPE_PATTERNS:
        match = pattern.search(line)
        if match:
            return match.group(1).strip().strip('"')
    return None


def classify_role(line: str, item: str, match_start: int) -> str:
    lowered = line.lower()

    if "~~ recipe name:" in lowered and "inputs:" in lowered:
        inputs_index = lowered.find("inputs:")
        outputs_index = lowered.find("outputs:")
        if outputs_index != -1 and match_start < inputs_index:
            return "output"
        if match_start >= inputs_index:
            return "input"

    prefix = lowered[max(0, match_start - 80) : match_start]
    suffix = lowered[match_start : min(len(lowered), match_start + len(item) + 80)]
    window = prefix + suffix

    if "with output" in lowered or "outputs:" in lowered:
        output_index = min(
            [idx for idx in (lowered.find("with output"), lowered.find("outputs:")) if idx != -1],
            default=-1,
        )
        if output_index != -1 and match_start > output_index:
            return "output"

    for key in ("ingredients", "ingredient", "inputs"):
        if key in window:
            return "input"

    for key in ("result", "results", "output", "outputs", "out"):
        if key in window:
            return "output"

    for key in ("container", "carrier", "useditem", "utensil"):
        if key in window:
            return key

    return "unknown"


def classify_crafttweaker_call_roles(line: str) -> dict[int, str]:
    if "addJsonRecipe" in line:
        return {}

    roles: dict[int, str] = {}
    angle_matches = list(ITEM_IN_ANGLE.finditer(line))
    if not angle_matches:
        return roles

    if "craftingTable.addShaped" in line or "craftingTable.addShapeless" in line:
        roles[angle_matches[0].start(1)] = "output"
        for match in angle_matches[1:]:
            roles[match.start(1)] = "input"
        return roles

    if (
        "campfire.addRecipe" in line
        or "smoker.addRecipe" in line
        or "furnace.addRecipe" in line
    ):
        roles[angle_matches[0].start(1)] = "output"
        if len(angle_matches) > 1:
            roles[angle_matches[1].start(1)] = "input"
        for match in angle_matches[2:]:
            roles[match.start(1)] = "unknown"
        return roles

    if ".addRecipe(" in line:
        roles[angle_matches[0].start(1)] = "output"
        input_list_start = line.find("[", angle_matches[0].end())
        input_list_end = line.find("]", input_list_start) if input_list_start != -1 else -1
        for match in angle_matches[1:]:
            start = match.start(1)
            if input_list_start != -1 and input_list_start < start < input_list_end:
                roles[start] = "input"
            elif ".mutable()" in line[start : start + 120]:
                roles[start] = "container"
            else:
                roles[start] = "unknown"
        return roles

    return roles


def extract_items_with_positions(line: str) -> list[tuple[str, int]]:
    found: list[tuple[str, int]] = []
    for pattern in (ITEM_IN_ANGLE, ITEM_IN_JSON_ITEM, ITEM_IN_JSON_ID):
        for match in pattern.finditer(line):
            found.append((match.group(1), match.start(1)))
    return found


def analyze_log(log_file: Path, groups: list[dict]) -> dict:
    item_to_group = {}
    for group in groups:
        for member in group["members"]:
            item_to_group[member] = group

    match_items = set(item_to_group)
    candidates = []
    role_counts: Counter[str] = Counter()
    type_counts: Counter[str] = Counter()
    item_counts: Counter[str] = Counter()
    recipe_ids: set[str] = set()

    with log_file.open("r", encoding="utf-8", errors="replace") as log:
        for line_number, line in enumerate(log, start=1):
            if not any(item in line for item in match_items):
                continue

            role_overrides = classify_crafttweaker_call_roles(line)
            matches = []
            for item, start in extract_items_with_positions(line):
                if item not in match_items:
                    continue
                group = item_to_group[item]
                role = role_overrides.get(start) or classify_role(line, item, start)
                matches.append(
                    {
                        "item": item,
                        "target": group["target"],
                        "inputTag": group["tag"],
                        "role": role,
                    }
                )
                role_counts[role] += 1
                item_counts[item] += 1

            if not matches:
                continue

            recipe_id = extract_recipe_id(line)
            recipe_type = extract_recipe_type(line)
            if recipe_id:
                recipe_ids.add(recipe_id)
            if recipe_type:
                type_counts[recipe_type] += 1

            candidates.append(
                {
                    "line": line_number,
                    "recipeId": recipe_id,
                    "recipeType": recipe_type,
                    "matches": matches,
                    "raw": line.rstrip("\n"),
                }
            )

    grouped_by_role: dict[str, list[dict]] = defaultdict(list)
    for candidate in candidates:
        roles = sorted({match["role"] for match in candidate["matches"]})
        for role in roles:
            grouped_by_role[role].append(candidate)

    return {
        "summary": {
            "candidateLines": len(candidates),
            "uniqueRecipeIds": len(recipe_ids),
            "roleCounts": dict(sorted(role_counts.items())),
            "recipeTypeCounts": dict(type_counts.most_common()),
            "itemCounts": dict(item_counts.most_common()),
        },
        "groups": groups,
        "candidates": candidates,
        "candidatesByRole": {
            role: entries for role, entries in sorted(grouped_by_role.items())
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate item-unification tags and filter CraftTweaker recipe logs."
    )
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--tag-root", type=Path, default=DEFAULT_TAG_ROOT)
    parser.add_argument("--rules", type=Path, default=DEFAULT_RULES)
    parser.add_argument("--no-tags", action="store_true")
    args = parser.parse_args()

    groups = load_groups(RESOURCE_FILES)
    written_tags = [] if args.no_tags else write_tags(groups, args.tag_root)
    write_kubejs_rules(groups, args.rules)
    report = analyze_log(args.log, groups)
    report["summary"]["groups"] = len(groups)
    report["summary"]["tagFilesWritten"] = len(written_tags)
    report["summary"]["tagRoot"] = args.tag_root.as_posix()
    report["summary"]["rulesFile"] = args.rules.as_posix()

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
