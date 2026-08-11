
//蒸笼配方
ServerEvents.recipes(event => {
    event.remove({output: 'youkaishomecoming:bun' });
    event.remove({output: 'kaleidoscope_cookery:baozi' });
    event.remove({output: 'farmersdelight:dumplings' });
    event.remove({output: 'youkaishomecoming:scholar_ginkgo' });
    event.remove({output: 'youkaishomecoming:oyaki' });
    event.remove({output: 'youkaishomecoming:imitation_bear_paw' });
    event.remove({output: 'youkaishomecoming:bowl_of_cream' });
    event.remove({output: 'twilightdelight:thorn_rose_tea' });
    event.remove({output: 'trailandtales_delight:pitcher_plant_tea' });
    event.remove({output: 'trailandtales_delight:torchflower_tea' });
    event.remove({output: 'extradelight:tea' });
    event.remove({output: 'rusticdelight:coffee' });
    event.remove({output: 'trailandtales_delight:ancient_coffee' });
    event.remove({output: 'rusticdelight:milk_coffee' });
    event.remove({output: 'rusticdelight:chocolate_coffee' });
    event.remove({output: 'rusticdelight:honey_coffee' });
    event.remove({output: 'rusticdelight:syrup_coffee' });
    event.remove({output: 'extradelight:whipped_cream' });
    event.remove({output: 'kaleidoscope_tavern:miners_star' });
    event.custom({
  "type": "kaleidoscope_cookery:stockpot",
  "carrier": {
    "item": "minecraft:paper"
  },
  "ingredients": [
    {
      "item": "kaleidoscope_end:void_conch"
    },
    {
      "item": "kaleidoscope_end:void_conch"
    },
    {
      "item": "kaleidoscope_end:dream_berry"
    },
    {
      "item": "kaleidoscope_end:dragon_dust"
    }
  ],
  "result": {
    "count": 5,
    "id": "kaleidoscope_end:void_conch"
  },
  "soup_base": "minecraft:water"
    });



    event.custom({
  "type": "kaleidoscope_tavern:barrel",
  "carrier": {
    "item": "kaleidoscope_tavern:empty_bottle"
  },
  "fluid": "kaleidoscope_tavern:gold_grape_juice",
  "ingredients": [
    {
      "item": "oreberriesreplanted:gold_oreberry"
    }
  ],
  "result": {
    "count": 1,
    "id": "kaleidoscope_tavern:miners_star"
  }
    });
    event.custom({
  "type": "kaleidoscope_cookery:steamer",
  "ingredient": {
    "item": "kaleidoscope_cookery:stuffed_dough_food"
  },
  "result": {
    "count": 1,
    "id": "farmersdelight:dumplings"
  }
    });
    event.custom({
  "type": "kaleidoscope_cookery:steamer",
  "ingredient": {
    "item": "youkaishomecoming:raw_bun"
  },
  "result": {
    "count": 1,
    "id": "youkaishomecoming:bun"
  }
    });
    event.custom({
  "type": "kaleidoscope_cookery:steamer",
  "ingredient": {
    "item": "youkaishomecoming:raw_scholar_ginkgo"
  },
  "result": {
    "count": 1,
    "id": "youkaishomecoming:scholar_ginkgo"
  }
    });
    event.custom({
  "type": "kaleidoscope_cookery:steamer",
  "ingredient": {
    "item": "youkaishomecoming:raw_oyaki"
  },
  "result": {
    "count": 1,
    "id": "youkaishomecoming:oyaki"
  }
    });
    event.custom({
  "type": "kaleidoscope_cookery:steamer",
  "ingredient": {
    "item": "youkaishomecoming:raw_imitation_bear_paw"
  },
  "result": {
    "count": 1,
    "id": "youkaishomecoming:imitation_bear_paw"
  }
    });
    event.custom({
  "type": "kaleidoscope_cookery:steamer",
  "ingredient": {
    "item": "crabbersdelight:crab"
  },
  "result": {
    "count": 1,
    "id": "croptopia:steamed_crab"
  }
    });
    event.recipes.kaleidoscope_cookery.pot(
        "minecraft:blaze_rod",
        [
        "minecraft:blaze_powder","minecraft:blaze_powder","minecraft:blaze_powder","minecraft:blaze_powder","minecraft:blaze_powder"
        ],
        "minecraft:stick",
        100,
        0
    );
    event.recipes.kaleidoscope_cookery.pot(
        "croptopia:grilled_cheese",
        [
            "trailandtales_delight:cheese_slice"
        ],
        "minecraft:bread",
        300,
        8
    );
    event.recipes.kaleidoscope_cookery.pot(
        "croptopia:croque_madame",
        [
            "minecraft:egg","minecraft:porkchop","trailandtales_delight:cheese_slice",
            "youkaishomecoming:butter","croptopia:flour"
        ],
        "minecraft:bread",
        300,
        8
    );
    event.recipes.kaleidoscope_cookery.pot(
        "croptopia:croque_monsieur",
        [
            "minecraft:porkchop","trailandtales_delight:cheese_slice",
            "youkaishomecoming:butter","croptopia:flour"
        ],
        "minecraft:bread",
        300,
        8
    );
    event.recipes.kaleidoscope_cookery.pot(
        "croptopia:baked_crepes",
        [
        "trailandtales_delight:cheese_slice","croptopia:flour","minecraft:egg","minecraft:egg",
        "trailandtales_delight:cheese_slice","croptopia:spinach"
        ],
        "minecraft:paper",
        300,
        5
    );
    event.recipes.kaleidoscope_cookery.pot(
        "croptopia:scrambled_eggs",
        [
        "trailandtales_delight:cheese_slice","minecraft:egg"
        ],
        "minecraft:paper",
        300,
        3
    );
    event.recipes.kaleidoscope_cookery.pot(
        "croptopia:roasted_radishes",
        [
     "croptopia:salt","croptopia:radish","croptopia:olive_oil",
     "croptopia:garlic","croptopia:pepper"
        ],
        "minecraft:stick",
        200,
        3
    );
    event.recipes.kaleidoscope_cookery.pot(
        "croptopia:grilled_oysters",
        [
     "croptopia:salt","extradelight:lemon","croptopia:oyster",
     "croptopia:garlic","trailandtales_delight:cheese_slice"
        ],
        "minecraft:paper",
        200,
        3
    );
    event.recipes.kaleidoscope_cookery.pot(
        "croptopia:roasted_squash",
        [
     "croptopia:salt","croptopia:squash","croptopia:olive_oil",
     "croptopia:garlic","croptopia:pepper"
        ],
        "minecraft:stick",
        200,
        3
    );
    event.recipes.kaleidoscope_cookery.pot(
        "croptopia:roasted_asparagus",
        [
     "croptopia:salt","croptopia:asparagus","croptopia:olive_oil",
     "croptopia:garlic","croptopia:pepper"
        ],
        "minecraft:stick",
        200,
        3
    );
    event.recipes.kaleidoscope_cookery.pot(
        "croptopia:roasted_turnips",
        [
     "croptopia:salt","croptopia:turnip","croptopia:olive_oil",
     "croptopia:garlic","croptopia:pepper"
        ],
        "minecraft:stick",
        200,
        3
    );
    event.recipes.kaleidoscope_cookery.pot(
        "croptopia:fish_and_chips",
        [
     "croptopia:salt","croptopia:french_fries","croptopia:flour",
     "croptopia:garlic","croptopia:pepper", "aquaculture:fish_fillet_raw"
        ],
        "minecraft:paper",
        200,
        3
    );
    event.recipes.kaleidoscope_cookery.pot(
        "croptopia:crab_legs",
        [
     "croptopia:salt","youkaishomecoming:butter","croptopia:flour",
     "croptopia:garlic","croptopia:pepper", "crabbersdelight:crab"
        ],
        "minecraft:paper",
        200,
        3
    );
    event.recipes.kaleidoscope_cookery.pot(
        "croptopia:dauphine_potatoes",
        [
     "minecraft:potato","extradelight:whipped_cream","croptopia:flour",
     "youkaishomecoming:butter"
        ],
        "minecraft:paper",
        200,
        3
    );
    event.recipes.kaleidoscope_cookery.pot(
        "croptopia:roasted_sunflower_seeds",
        [
     "minecraft:sunflower","croptopia:salt","croptopia:pepper"
        ],
        "minecraft:paper",
        200,
        8
    );
    event.recipes.kaleidoscope_cookery.pot(
        "croptopia:roasted_pumpkin_seeds",
        [
     "minecraft:pumpkin_seeds","croptopia:salt","croptopia:pepper"
        ],
        "minecraft:paper",
        200,
        8
    );
    event.recipes.kaleidoscope_cookery.pot(
        "croptopia:kale_chips",
        [
     "croptopia:kale","croptopia:salt","croptopia:pepper"
        ],
        "minecraft:paper",
        200,
        3
    );
    event.recipes.kaleidoscope_cookery.pot(
        "croptopia:quesadilla",
        [
     "croptopia:avocado","croptopia:salt","minecraft:chicken","trailandtales_delight:cheese_slice"
        ],
        "croptopia:tortilla",
        200,
        3
    );
    event.recipes.kaleidoscope_cookery.pot(
        "croptopia:fajitas",
        [
     "farmersdelight:onion","croptopia:salt","rusticdelight:bell_pepper_yellow","butchercraft:ground_beef",
     "trailandtales_delight:cheese_slice","farmersdelight:tomato"
        ],
        "croptopia:tortilla",
        200,
        3
    );
    event.recipes.kaleidoscope_cookery.pot(
        "croptopia:hashed_brown",
        [
     "minecraft:potato","croptopia:salt","croptopia:flour"
        ],
        "minecraft:paper",
        200,
        5
    );
    event.recipes.kaleidoscope_cookery.pot(
        "croptopia:deep_fried_shrimp",
        [
     "croptopia:shrimp",
     "croptopia:salt","extradelight:breadcrumbs"
        ],
        "minecraft:paper",
        100,
        1
    );
    event.recipes.kaleidoscope_cookery.pot(
        "croptopia:ratatouille",
        [
     "croptopia:basil","croptopia:eggplant",
     "croptopia:squash","farmersdelight:tomato",
     "croptopia:zucchini","farmersdelight:onion",
     "croptopia:salt","rusticdelight:bell_pepper_yellow"
        ],
        "minecraft:bowl",
        200,
        1
    );
    event.recipes.kaleidoscope_cookery.pot(
        "croptopia:sweet_crepes",
        [
     "croptopia:strawberry_jam","minecraft:sugar",
     "croptopia:flour","minecraft:egg",
     "croptopia:milk_bottle"
        ],
        "minecraft:paper",
        200,
        3
    );
    event.recipes.kaleidoscope_cookery.pot(
        "croptopia:carnitas",
        [
     "butchercraft:cubed_pork","farmersdelight:onion",
     "farmersdelight:cabbage_leaf","croptopia:tortilla"
        ],
        "minecraft:bowl",
        200,
        3
    );
    event.recipes.kaleidoscope_cookery.pot(
        "croptopia:stuffed_artichoke",
        [
     "extradelight:lemon","croptopia:salt",
     "kaleidoscope_cookery:raw_dough","croptopia:olive_oil",
     "trailandtales_delight:cheese_slice","croptopia:pepper"
        ],
        "croptopia:artichoke",
        200,
        3
    );
    event.recipes.kaleidoscope_cookery.pot(
        "croptopia:the_big_breakfast",
        [
     "minecraft:egg","croptopia:salt",
     "butchercraft:cooked_sausage","croptopia:cooked_bacon",
     "croptopia:hashed_brown","croptopia:pepper"
        ],
        "croptopia:toast",
        300,
        3
    );

})