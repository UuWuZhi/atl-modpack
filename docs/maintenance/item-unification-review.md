# Item Unification Review

This review note summarizes the generated report from `extern/crafttweaker.log`.

Generated files:

- `docs/maintenance/item-unification-candidates.json`
- `kubejs/data/c/tags/item/food/*.json`

Summary:

- Resource groups: 75
- Candidate log lines: 609
- Unique recipe ids: 541
- Input matches: 1195
- Output matches: 230
- Container matches: 5

Manual review boundary:

- Review `candidatesByRole.container` first. These are not normal recipe
  ingredients and may need recipe-specific handling.
- Review output-side candidates before enabling `replaceOutput`, because multiple
  recipes may become duplicate recipes for the same canonical output.
- The input-side target for every member item is the generated tag
  `#c:food/<canonical_path>`, not the canonical item itself.

Known container candidates:

- `farmersdelight:beef_bulgogi`
- `farmersdelight:caramel_chicken`
- `pineapple_delight:cooking/pineapple_fried_rice`
- `farmersdelight:honey_chili_chicken`
- `farmersdelight:melon_rind_stirfry`
