const ITEM_UNIFICATION_RULES = JsonIO.toObject(
  JsonIO.readJson('kubejs/server_scripts/generated/item_unification_rules.json')
);

const CONTAINER_RECIPE_REPLACEMENTS = [
  {
    id: 'farmersdelight:beef_bulgogi',
    json: {
      type: 'farmersdelight:cooking',
      ingredients: [
        { tag: 'c:beef/cubed/raw' },
        { tag: 'extradelight:processed/onion' },
        { tag: 'c:chili/powder' },
        { tag: 'c:condiments/hot_sauce' },
        { tag: 'extradelight:processed/garlic' },
        { tag: 'c:condiments/soy_sauce' }
      ],
      container: { tag: 'c:food/cooked_rice' },
      result: { id: 'extradelight:beef_bulgogi', count: 2 },
      experience: 1.0,
      cookingtime: 200,
      recipe_book_tab: 'meals'
    }
  },
  {
    id: 'farmersdelight:caramel_chicken',
    json: {
      type: 'farmersdelight:cooking',
      ingredients: [
        { tag: 'c:chicken/thigh/raw' },
        { item: 'minecraft:sugar' },
        { tag: 'extradelight:processed/onion' },
        { tag: 'extradelight:processed/garlic' },
        { tag: 'c:fish_sauce' },
        { tag: 'c:condiments/soy_sauce' }
      ],
      container: { tag: 'c:food/cooked_rice' },
      result: { id: 'extradelight:caramel_chicken', count: 2 },
      experience: 1.0,
      cookingtime: 200,
      recipe_book_tab: 'meals'
    }
  },
  {
    id: 'pineapple_delight:cooking/pineapple_fried_rice',
    json: {
      type: 'farmersdelight:cooking',
      ingredients: [
        { item: 'pineapple_delight:pineapple_side' },
        { tag: 'c:crops/rice' },
        { tag: 'c:eggs' },
        { item: 'minecraft:carrot' }
      ],
      container: { tag: 'c:food/pineapple' },
      result: { id: 'pineapple_delight:pineapple_fried_rice', count: 1 },
      experience: 1.0,
      cookingtime: 200,
      recipe_book_tab: 'meals'
    }
  },
  {
    id: 'farmersdelight:honey_chili_chicken',
    json: {
      type: 'farmersdelight:cooking',
      ingredients: [
        { tag: 'c:chicken/cubed/raw' },
        { item: 'minecraft:honey_bottle' },
        { tag: 'extradelight:processed/chili' },
        { tag: 'extradelight:processed/garlic' },
        { tag: 'extradelight:processed/ginger' },
        { tag: 'c:condiments/soy_sauce' }
      ],
      container: { tag: 'c:food/cooked_rice' },
      result: { id: 'extradelight:honey_chili_chicken', count: 2 },
      experience: 1.0,
      cookingtime: 200,
      recipe_book_tab: 'meals'
    }
  },
  {
    id: 'farmersdelight:melon_rind_stirfry',
    json: {
      type: 'farmersdelight:cooking',
      ingredients: [
        { item: 'extradelight:melon_rind' },
        { tag: 'extradelight:processed/carrot' },
        { tag: 'c:fish_sauce' },
        { tag: 'c:condiments/soy_sauce' },
        { tag: 'extradelight:processed/garlic' },
        { tag: 'extradelight:processed/ginger' }
      ],
      container: { tag: 'c:food/cooked_rice' },
      result: { id: 'extradelight:melon_rind_stirfry', count: 1 },
      experience: 1.0,
      cookingtime: 200,
      recipe_book_tab: 'meals'
    }
  }
];

ServerEvents.recipes(event => {
  ITEM_UNIFICATION_RULES.groups.forEach(group => {
    const inputTag = `#${group.tag}`;

    group.members.forEach(sourceItem => {
      event.replaceInput({ input: sourceItem }, sourceItem, inputTag);

      if (sourceItem !== group.target) {
        event.replaceOutput({ output: sourceItem }, sourceItem, group.target);
      }
    });
  });

  CONTAINER_RECIPE_REPLACEMENTS.forEach(recipe => {
    event.remove({ id: recipe.id });
    event.custom(recipe.json).id(recipe.id);
  });
});
