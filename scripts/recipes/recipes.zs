import crafttweaker.api.item.IItemStack;
import crafttweaker.api.ingredient.IIngredient;
import crafttweaker.api.data.IData;
import crafttweaker.api.util.random.Percentaged;
import crafttweaker.api.recipe.CraftingTableRecipeManager;
import crafttweaker.api.recipe.IRecipeManager;
import crafttweaker.api.item.NeoForgeItemStack;
import crafttweaker.api.item.MCItemStack;

//增加燃烧物

//增加工作台配方

craftingTable.remove(<item:croptopia:hamburger>);
craftingTable.addShapeless("farmersdelight_hamburger",<item:croptopia:hamburger>,
  [<item:minecraft:bread>,<item:farmersdelight:beef_patty>,<item:extradelight:sliced_tomato>,<item:kaleidoscope_cookery:lettuce>,<item:extradelight:sliced_onion>]);
craftingTable.remove(<item:extradelight:cheeseburger>);
craftingTable.addShapeless("extradelight_cheeseburger",<item:extradelight:cheeseburger>,
  [<item:trailandtales_delight:cheese_slice>,<item:extradelight:sliced_gherkin_item>,<item:minecraft:bread>,<item:farmersdelight:beef_patty>,<item:extradelight:sliced_tomato>,<item:kaleidoscope_cookery:lettuce>,<item:extradelight:sliced_onion>]);
craftingTable.addShapeless("extradelight_cheeseburger_1",<item:extradelight:cheeseburger>,
  [<item:trailandtales_delight:cheese_slice>,<item:extradelight:sliced_gherkin_item>,<item:croptopia:hamburger>]);
craftingTable.remove(<item:croptopia:tofuburger>);
craftingTable.addShapeless("croptopia_tofuburger",<item:croptopia:tofuburger>,
  [<item:minecraft:bread>,<item:croptopia:tofu>,<item:kaleidoscope_cookery:lettuce>,<item:extradelight:sliced_onion>]);

//增加浇注配方
<recipetype:create:filling>.addJsonRecipe("minecraft_redstone", {
  "type": "create:filling",
  "ingredients": [
    {
      "type": "neoforge:single",
      "amount": 125,
      "fluid": "kaleidoscope_grilling:premium_chili_oil"
    },
    {
      "item": "croptopia:flour"
    }
  ],
  "results": [
    {
      "amount": 1,
      "id": "minecraft:redstone"
    }
  ]}
 );


//增加烈焰人燃烧室配方
<recipetype:createaddition:liquid_burning>.addJsonRecipe("premium_chili_oil_fuel", {
  "type": "createaddition:liquid_burning",
  "burn_time": 48000,
  "superheated": true,
  "ingredients": [
    {
      "type": "neoforge:single",
      "amount": 1000,
      "fluid": "kaleidoscope_grilling:premium_chili_oil"
    }
  ],
  "results": []}
 );
<recipetype:createaddition:liquid_burning>.addJsonRecipe("secret_chili_oil_fuel", {
  "type": "createaddition:liquid_burning",
  "burn_time": 48000,
  "superheated": false,
  "ingredients": [
    {
      "type": "neoforge:single",
      "amount": 1000,
      "fluid": "kaleidoscope_grilling:secret_chili_oil"
    }
  ],
  "results": []}
 );
//增加磨粉配方(机械动力石磨、粉碎轮，森罗物语石磨配方使用kjs制作)
<recipetype:create:milling>.addJsonRecipe("dragon_dust_mill", {
  "type": "create:milling",
  "ingredients": [
    {
      "item": "ends_delight:dragon_tooth"
    }
  ],
  "results": [
    {
      "amount": 1,
      "id": "kaleidoscope_end:dragon_dust"
    }
  ]}
 );
<recipetype:create:crushing>.addJsonRecipe("dragon_dust_crush", {
  "type": "create:crushing",
  "ingredients": [
    {
      "item": "ends_delight:dragon_tooth"
    }
  ],
  "results": [
    {
      "amount": 1,
      "id": "kaleidoscope_end:dragon_dust"
    }
  ]}
 );

<recipetype:create:milling>.addJsonRecipe("star_dust_mill", {
  "type": "create:milling",
  "ingredients": [
    {
      "item": "minecraft:nether_star"
    }
  ],
  "results": [
    {
      "amount": 4,
      "id": "kaleidoscope_nether:star_dust"
    }
  ]}
 );
<recipetype:create:crushing>.addJsonRecipe("star_dust_crush", {
  "type": "create:crushing",
  "ingredients": [
    {
      "item": "minecraft:nether_star"
    }
  ],
  "results": [
    {
      "amount": 4,
      "id": "kaleidoscope_nether:star_dust"
    }
  ]}
 );


//增加砧板配方
<recipetype:farmersdelight:cutting>.addJsonRecipe("chorus_petal", {
  "type": "farmersdelight:cutting",
  "ingredients": [
    {
      "item": "minecraft:chorus_flower"
    }
  ],
  "result": [
    {
      "item": {
        "count": 4,
        "id": "kaleidoscope_end:chorus_petal"
      }
    }
  ],
  "sound": {
    "sound_id": "minecraft:item.axe.strip"
  },
  "tool": [
    {
      "type": "farmersdelight:item_ability",
      "action": "axe_strip"
    },
    {
      "tag": "c:shears"
    }
  ]
}
 );
 
//增加冲压机配方(工作盆)
<recipetype:create:compacting>.addJsonRecipe("crimson_fruit_to_lava", {
  "type": "create:compacting",
  "ingredients": [
    {
      "item": "kaleidoscope_nether:crimson_fruit"
    }
  ],
  "results": [
    {
      "amount": 50,
      "id": "minecraft:lava"
    },
    {
      "amount": 1,
      "id": "minecraft:blaze_powder"
    }
  ]}
 );
<recipetype:create:compacting>.addJsonRecipe("gold_oreberry_nugget_1", {
  "type": "create:compacting",
  "ingredients": [
    {
      "type": "neoforge:single",
      "amount": 900,
      "fluid": "oreberriesreplanted:gold_oreberry_juice"
    }
  ],
  "results": [
    {
      "amount": 1,
      "id": "minecraft:gold_ingot"
    }
  ]}
 );
<recipetype:create:compacting>.addJsonRecipe("iron_oreberry_nugget_1", {
  "type": "create:compacting",
  "ingredients": [
    {
      "type": "neoforge:single",
      "amount": 900,
      "fluid": "oreberriesreplanted:iron_oreberry_juice"
    }
  ],
  "results": [
    {
      "amount": 1,
      "id": "minecraft:iron_ingot"
    }
  ]}
 );
<recipetype:create:compacting>.addJsonRecipe("copper_oreberry_nugget_1", {
  "type": "create:compacting",
  "ingredients": [
    {
      "type": "neoforge:single",
      "amount": 900,
      "fluid": "oreberriesreplanted:copper_oreberry_juice"
    }
  ],
  "results": [
    {
      "amount": 1,
      "id": "minecraft:copper_ingot"
    }
  ]}
 );
<recipetype:create:compacting>.addJsonRecipe("zinc_oreberry_nugget_1", {
  "type": "create:compacting",
  "ingredients": [
    {
      "type": "neoforge:single",
      "amount": 900,
      "fluid": "oreberriesreplanted:zinc_oreberry_juice"
    }
  ],
  "results": [
    {
      "amount": 1,
      "id": "create:zinc_ingot"
    }
  ]}
 );
//增加搅拌机配方
<recipetype:create:mixing>.addJsonRecipe("create_human_honey", {
  "type": "create:mixing",
  "heat_requirement": "heated",
  "ingredients": [
    {"item": "rusticdelight:syrup"},
    {"item": "extradelight:yeast"},
    {"tag": "minecraft:flowers"},
    {"tag": "minecraft:flowers"},
    {"tag": "minecraft:flowers"},
    {"tag": "minecraft:flowers"},
    {"tag": "c:slime_balls"},
    {
      "type": "neoforge:single",
      "amount": 1000,
      "fluid": "minecraft:water"
    },
  ],
  "results": [
    {
      "amount": 1000,
      "id": "create:honey"
    }
  ]}
 );
<recipetype:create:mixing>.addJsonRecipe("non_hatchable_dragon_egg", {
  "type": "create:mixing",
  "heat_requirement": "superheated",
  "ingredients": [
    {"item": "extradelight:boiled_egg"},{"item": "kaleidoscope_end:dragon_dust"},{"item": "minecraft:dragon_breath"}
  ],
  "results": [
    {
      "amount": 1,
      "id": "ends_delight:non_hatchable_dragon_egg"
    }
  ]}
 );
<recipetype:create:mixing>.addJsonRecipe("dragon_egg_liquid", {
  "type": "create:mixing",
  "heat_requirement": "superheated",
  "ingredients": [
    {"item": "ends_delight:liquid_dragon_egg"},
    {
      "type": "neoforge:single",
      "amount": 1000,
      "fluid": "extradelight:egg_white_fluid"
    },
  ],
  "results": [
    {
      "amount": 1,
      "id": "kaleidoscope_end:dragon_egg_liquid"
    }
  ]}
 );
<recipetype:create:mixing>.addJsonRecipe("gold_oreberry_juice", {
  "type": "create:mixing",
  "heat_requirement": "heated",
  "ingredients": [
    {"item": "oreberriesreplanted:gold_oreberry"}
  ],
  "results": [
    {
      "amount": 175,
      "id": "oreberriesreplanted:gold_oreberry_juice"
    }
  ]}
 );
<recipetype:create:mixing>.addJsonRecipe("iron_oreberry_juice", {
  "type": "create:mixing",
  "heat_requirement": "heated",
  "ingredients": [
    {"item": "oreberriesreplanted:iron_oreberry"}
  ],
  "results": [
    {
      "amount": 175,
      "id": "oreberriesreplanted:iron_oreberry_juice"
    }
  ]}
 );
<recipetype:create:mixing>.addJsonRecipe("zinc_oreberry_juice", {
  "type": "create:mixing",
  "heat_requirement": "heated",
  "ingredients": [
    {"item": "oreberriesreplanted:zinc_oreberry"}
  ],
  "results": [
    {
      "amount": 175,
      "id": "oreberriesreplanted:zinc_oreberry_juice"
    }
  ]}
 );
<recipetype:create:mixing>.addJsonRecipe("copper_oreberry_juice", {
  "type": "create:mixing",
  "heat_requirement": "heated",
  "ingredients": [
    {"item": "oreberriesreplanted:copper_oreberry"}
  ],
  "results": [
    {
      "amount": 175,
      "id": "oreberriesreplanted:copper_oreberry_juice"
    }
  ]}
 );

<recipetype:create:mixing>.addJsonRecipe("gold_oreberry_juice_2", {
  "type": "create:mixing",
  "heat_requirement": "heated",
  "ingredients": [
    {"item": "oreberriesreplanted:gold_oreberry_bush"}
  ],
  "results": [
    {
      "amount": 900,
      "id": "oreberriesreplanted:gold_oreberry_juice"
    }
  ]}
 );
<recipetype:create:mixing>.addJsonRecipe("iron_oreberry_juice_2", {
  "type": "create:mixing",
  "heat_requirement": "heated",
  "ingredients": [
    {"item": "oreberriesreplanted:iron_oreberry_bush"}
  ],
  "results": [
    {
      "amount": 900,
      "id": "oreberriesreplanted:iron_oreberry_juice"
    }
  ]}
 );
<recipetype:create:mixing>.addJsonRecipe("zinc_oreberry_juice_2", {
  "type": "create:mixing",
  "heat_requirement": "heated",
  "ingredients": [
    {"item": "oreberriesreplanted:zinc_oreberry_bush"}
  ],
  "results": [
    {
      "amount": 900,
      "id": "oreberriesreplanted:zinc_oreberry_juice"
    }
  ]}
 );
<recipetype:create:mixing>.addJsonRecipe("copper_oreberry_juice_2", {
  "type": "create:mixing",
  "heat_requirement": "heated",
  "ingredients": [
    {"item": "oreberriesreplanted:copper_oreberry_bush"}
  ],
  "results": [
    {
      "amount": 900,
      "id": "oreberriesreplanted:copper_oreberry_juice"
    }
  ]}
 );



<recipetype:create:mixing>.addJsonRecipe("whipped_cream_fluid", {
  "type": "create:mixing",
  "ingredients": [
    {
      "type": "neoforge:tag",
      "amount": 250,
      "tag": "c:milk"
    }
  ],
  "results": [
    {
      "amount": 250,
      "id": "extradelight:whipped_cream_fluid"
    }
  ]}
 );
<recipetype:create:mixing>.addJsonRecipe("oil_fluid", {
  "type": "create:mixing",
  "heat_requirement": "heated",
  "ingredients": [
    {"item": "kaleidoscope_cookery:oil"}
  ],
  "results": [
    {
      "amount": 250,
      "id": "extradelight:oil_fluid"
    }
  ]}
 );
<recipetype:create:mixing>.addJsonRecipe("secret_chili_oil", {
  "type": "create:mixing",
  "heat_requirement": "heated",
  "ingredients": [
    {
      "type": "neoforge:single",
      "amount": 1000,
      "fluid": "kaleidoscope_grilling:canola_oil"
    },
    {"item": "kaleidoscope_grilling:red_chili_powder"},{"item": "kaleidoscope_grilling:red_chili_powder"},{"item": "kaleidoscope_grilling:red_chili_powder"}
  ],
  "results": [
    {
      "amount": 1000,
      "id": "kaleidoscope_grilling:secret_chili_oil"
    }
  ]}
 );
<recipetype:create:mixing>.addJsonRecipe("canola_oil_1", {
  "type": "create:mixing",
  "heat_requirement": "heated",
  "ingredients": [
    {"item": "kaleidoscope_grilling:oil_cake"},
    {"item": "kaleidoscope_grilling:oil_cake"},
    {"item": "kaleidoscope_grilling:oil_cake"}
  ],
  "results": [
    {
      "amount": 1250,
      "id": "kaleidoscope_grilling:canola_oil"
    }
  ]}
 );
<recipetype:create:mixing>.addJsonRecipe("canola_oil_2", {
  "type": "create:mixing",
  "heat_requirement": "heated",
  "ingredients": [
    {
      "type": "neoforge:single",
      "amount": 100,
      "fluid": "minecraft:water"
    },
    {"item": "kaleidoscope_grilling:oil_residue"},
    {"item": "kaleidoscope_grilling:oil_residue"},
    {"item": "kaleidoscope_grilling:oil_residue"}
  ],
  "results": [
    {
      "amount": 250,
      "id": "kaleidoscope_grilling:canola_oil"
    }
  ]}
 );
<recipetype:create:mixing>.addJsonRecipe("premium_chili_oil", {
  "type": "create:mixing",
  "heat_requirement": "superheated",
  "ingredients": [
    {
      "type": "neoforge:single",
      "amount": 1000,
      "fluid": "kaleidoscope_grilling:secret_chili_oil"
    },
    {
      "type": "neoforge:single",
      "amount": 1000,
      "fluid": "minecraft:lava"
    },
    {"item": "kaleidoscope_grilling:houttuynia_powder"},{"item": "kaleidoscope_nether:soul_pepper"}
  ],
  "results": [
    {
      "amount": 1000,
      "id": "kaleidoscope_grilling:premium_chili_oil"
    }
  ]}
 );

//增加厨锅配方
//食物使用meals 饮品使用drinks
//作物盛景重写
<recipetype:farmersdelight:cooking>.addJsonRecipe("croptopia_tamales", {
  "type": "farmersdelight:cooking",
  "experience": 1.0,
  "ingredients": [
      {"tag": "c:foods/raw_chicken"}, {"item": "farmersdelight:onion"}, {"item": "croptopia:corn_husk"},
      {"tag": "c:flour"}, {"item": "croptopia:salt"}, {"item": "kaleidoscope_cookery:red_chili"}
  ],
  "recipe_book_tab": "meals",
  "result": {
    "count": 2,
    "id": "croptopia:tamales"
  }
 }
 );
<recipetype:farmersdelight:cooking>.addJsonRecipe("olive_oil", {
  "type": "farmersdelight:cooking",
  "experience": 1.0,
  "ingredients": [
      {"item": "croptopia:olive"}, {"item": "croptopia:olive"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 1,
    "id": "croptopia:olive_oil"
  }
 }
 );
<recipetype:farmersdelight:cooking>.addJsonRecipe("onion_rings", {
  "type": "farmersdelight:cooking",
  "experience": 1.0,
  "ingredients": [
      {"item": "farmersdelight:onion"}, {"item": "croptopia:flour"}, {"item": "croptopia:salt"},
      {"item": "croptopia:olive_oil"}
  ],
  "recipe_book_tab": "meals",
  "result": {
    "count": 1,
    "id": "croptopia:onion_rings"
  }
 }
 );
<recipetype:farmersdelight:cooking>.addJsonRecipe("french_fries", {
  "type": "farmersdelight:cooking",
  "experience": 1.0,
  "ingredients": [
      {"item": "minecraft:potato"}, {"item": "croptopia:salt"}, {"item": "croptopia:olive_oil"}
  ],
  "recipe_book_tab": "meals",
  "result": {
    "count": 1,
    "id": "croptopia:french_fries"
  }
 }
 );
<recipetype:farmersdelight:cooking>.addJsonRecipe("chicken_and_noodles", {
  "type": "farmersdelight:cooking",
  "experience": 1.0,
  "ingredients": [
      {"tag": "c:foods/raw_chicken"}, {"item": "kaleidoscope_cookery:red_chili"}, {"item": "kaleidoscope_cookery:raw_noodles"}, {"item": "croptopia:olive_oil"}
  ],
  "recipe_book_tab": "meals",
  "result": {
    "count": 1,
    "id": "croptopia:chicken_and_noodles"
  }
 }
 );
<recipetype:farmersdelight:cooking>.addJsonRecipe("borscht", {
  "type": "farmersdelight:cooking",
  "experience": 1.0,
  "ingredients": [
      {"item": "farmersdelight:onion"}, {"item": "minecraft:carrot"}, {"item": "minecraft:potato"},
      {"item": "croptopia:garlic"}, {"item": "farmersdelight:tomato"}, {"item": "minecraft:beetroot"},
  ],
  "result": {
    "count": 1,
    "id": "croptopia:borscht"
  }
 }
 );
<recipetype:farmersdelight:cooking>.addJsonRecipe("tofu_and_dumplings", {
  "type": "farmersdelight:cooking",
  "experience": 1.0,
  "ingredients": [
      {"tag": "c:tofu"}, {"item": "kaleidoscope_cookery:raw_dough"}, {"item": "kaleidoscope_cookery:red_chili"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:tofu_and_dumplings"
  }
 }
 );
<recipetype:farmersdelight:cooking>.addJsonRecipe("chicken_and_dumplings", {
  "type": "farmersdelight:cooking",
  "experience": 1.0,
  "ingredients": [
      {"tag": "c:foods/raw_chicken"}, {"item": "kaleidoscope_cookery:raw_dough"}, {"item": "kaleidoscope_cookery:red_chili"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:chicken_and_dumplings"
  }
 }
 );
<recipetype:farmersdelight:cooking>.addJsonRecipe("pumpkin_soup", {
  "type": "farmersdelight:cooking",
  "experience": 1.0,
  "ingredients": [
      {"item": "croptopia:pepper"}, {"item": "croptopia:salt"}, {"item": "farmersdelight:onion"},
      {"item": "croptopia:garlic"}, {"item": "minecraft:pumpkin"}, {"item": "minecraft:pumpkin"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:pumpkin_soup"
  }
 }
 );
<recipetype:farmersdelight:cooking>.addJsonRecipe("chimichanga", {
  "type": "farmersdelight:cooking",
  "experience": 1.0,
  "ingredients": [
      {"item": "croptopia:burrito"}, {"item": "croptopia:flour"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:chimichanga"
  }
 }
 );
<recipetype:farmersdelight:cooking>.addJsonRecipe("sweet_potato_fries", {
  "type": "farmersdelight:cooking",
  "experience": 1.0,
  "ingredients": [
      {"item": "expandeddelight:sweet_potato"}, {"item": "croptopia:olive_oil"}, {"item": "croptopia:salt"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:sweet_potato_fries"
  }
 }
 );
<recipetype:farmersdelight:cooking>.addJsonRecipe("stuffed_poblanos", {
  "type": "farmersdelight:cooking",
  "experience": 1.0,
  "ingredients": [
      {"item": "extradelight:corn_seeds"}, {"item": "trailandtales_delight:cheese_slice"}, {"item": "farmersdelight:rice"},
      {"item": "croptopia:blackbean"}, {"item": "kaleidoscope_cookery:red_chili"}, {"item": "minecraft:beef"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:stuffed_poblanos"
  }
 }
 );
<recipetype:farmersdelight:cooking>.addJsonRecipe("chili_relleno", {
  "type": "farmersdelight:cooking",
  "experience": 1.0,
  "ingredients": [
      {"item": "minecraft:egg"}, {"item": "croptopia:flour"}, {"item": "croptopia:salt"},
      {"item": "kaleidoscope_cookery:red_chili"}, {"item": "croptopia:olive_oil"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:chili_relleno"
  }
 }
 );
<recipetype:farmersdelight:cooking>.addJsonRecipe("lemon_chicken", {
  "type": "farmersdelight:cooking",
  "experience": 1.0,
  "ingredients": [
      {"item": "minecraft:chicken"}, {"item": "extradelight:lemon"}, 
      {"item": "kaleidoscope_cookery:red_chili"}, {"item": "farmersdelight:tomato"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:lemon_chicken"
  }
 }
 );
<recipetype:farmersdelight:cooking>.addJsonRecipe("ketchup_jar_item", {
  "type": "farmersdelight:cooking",
  "experience": 1.0,
  "ingredients": [
      {"item": "croptopia:tomato_juice"}, {"item": "extradelight:vinegar"}, 
      {"item": "minecraft:sugar"}
  ],
  "result": {
    "count": 1,
    "id": "extradelight:ketchup_jar_item"
  }
 }
 );
<recipetype:farmersdelight:cooking>.addJsonRecipe("macaron", {
  "type": "farmersdelight:cooking",
  "experience": 1.0,
  "ingredients": [
      {"item": "minecraft:sugar"}, {"item": "minecraft:sugar"}, {"item": "minecraft:egg"}, 
      {"item": "croptopia:almond"}, {"item": "croptopia:almond"}
  ],
  "result": {
    "count": 2,
    "id": "croptopia:macaron"
  }
 }
 );
<recipetype:farmersdelight:cooking>.addJsonRecipe("croptopia_beer", {
  "type": "farmersdelight:cooking",
  "container": {
    "count": 1,
    "id": "minecraft:glass_bottle"
  },
  "experience": 1.0,
  "ingredients": [
      {"item": "croptopia:hops"}, {"item": "croptopia:barley"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:beer"
  }
 }
 );
//非常多的配方
<recipetype:farmersdelight:cooking>.addJsonRecipe("fried_calamari", {
  "experience": 1.0,
  "ingredients": [
      {"item": "croptopia:calamari"}, {"item": "extradelight:lemon"}, {"item": "croptopia:olive_oil"},
      {"item": "croptopia:sea_lettuce"}, {"item": "croptopia:flour"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:fried_calamari"
  }
 }
 );
<recipetype:farmersdelight:cooking>.addJsonRecipe("refried_beans", {
  "experience": 1.0,
  "ingredients": [
      {"item": "croptopia:blackbean"}, {"item": "croptopia:blackbean"}, {"item": "kaleidoscope_cookery:red_chili"},
      {"item": "trailandtales_delight:cheese_slice"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:refried_beans"
  }
 }
 );
<recipetype:farmersdelight:cooking>.addJsonRecipe("cabbage_roll", {
  "experience": 1.0,
  "ingredients": [
      {"item": "butchercraft:ground_beef"}, {"item": "farmersdelight:cabbage_leaf"}, {"item": "farmersdelight:cabbage_leaf"},
      {"item": "farmersdelight:rice"}, {"item": "croptopia:salt"}, {"item": "farmersdelight:onion"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:cabbage_roll"
  }
 }
 );
<recipetype:farmersdelight:cooking>.addJsonRecipe("goulash", {
  "experience": 1.0,
  "ingredients": [
      {"item": "butchercraft:ground_beef"}, {"item": "croptopia:tomato_juice"}, {"item": "farmersdelight:cabbage_leaf"},
      {"item": "butchercraft:ground_beef"}, {"item": "croptopia:salt"}, {"item": "farmersdelight:onion"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:goulash"
  }
 }
 );
<recipetype:farmersdelight:cooking>.addJsonRecipe("spaghetti_squash", {
  "experience": 1.0,
  "ingredients": [
      {"item": "croptopia:squash"}, {"item": "kaleidoscope_cookery:red_chili"},
      {"item": "croptopia:salt"}, {"item": "farmersdelight:onion"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:spaghetti_squash"
  }
 }
 );

<recipetype:farmersdelight:cooking>.addJsonRecipe("croptopia_scones", {
  "experience": 1.0,
  "ingredients": [
      {"item": "biomeswevegone:blueberries"}, {"item": "minecraft:egg"}, {"item": "minecraft:sugar"},
      {"item": "neapolitan:dried_vanilla_pods"}, {"item": "croptopia:salt"}, {"item": "croptopia:flour"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:scones"
  }
 }
 );
<recipetype:farmersdelight:cooking>.addJsonRecipe("steamed_clams", {
  "experience": 1.0,
  "ingredients": [
      {"item": "croptopia:clam"}, {"item": "croptopia:clam"}, {"item": "youkaishomecoming:butter"},
      {"item": "croptopia:garlic"}, {"item": "croptopia:salt"}, {"item": "croptopia:pepper"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:steamed_clams"
  }
 }
 );
<recipetype:farmersdelight:cooking>.addJsonRecipe("tortilla", {
  "experience": 1.0,
  "ingredients": [
      {"item": "extradelight:corn_meal"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:tortilla"
  }
 }
 );
<recipetype:farmersdelight:cooking>.addJsonRecipe("fried_chicken", {
  "experience": 1.0,
  "ingredients": [
      {"item": "croptopia:olive_oil"},{"item": "minecraft:chicken"},
      {"item": "extradelight:breadcrumbs"},{"item": "kaleidoscope_cookery:red_chili"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:fried_chicken"
  }
 }
 );






//增加搅拌碗配方

<recipetype:extradelight:mixing_bowl>.addJsonRecipe("beetroot_salad", {
  "type": "extradelight:mixing_bowl",
  "experience": 1.0,
  "fluids": [
    {
      "amount": 250,
      "fluid": "extradelight:mayo_fluid"
    }
  ],
  "ingredients": [
      {"item": "minecraft:beetroot"}, {"item": "minecraft:beetroot"}, {"item": "minecraft:beetroot"},
      {"item": "kaleidoscope_cookery:lettuce"}, {"item": "trailandtales_delight:cheese_slice"}, {"item": "extradelight:lemon"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:beetroot_salad"
  },
  "stirs": 4,
  "utensil": {
    "tag": "c:spoons"
  }
 }
 );
<recipetype:extradelight:mixing_bowl>.addJsonRecipe("apricot_jam", {
  "type": "extradelight:mixing_bowl",
  "experience": 1.0,
  "fluids": [
  ],
  "ingredients": [
      {"item": "croptopia:apricot"}, {"item": "minecraft:sugar"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:apricot_jam"
  },
  "stirs": 2,
  "utensil": {
    "tag": "c:spoons"
  }
 }
 );
<recipetype:extradelight:mixing_bowl>.addJsonRecipe("blackberry_jam", {
  "type": "extradelight:mixing_bowl",
  "experience": 1.0,
  "fluids": [
  ],
  "ingredients": [
      {"item": "croptopia:blackberry"}, {"item": "minecraft:sugar"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:blackberry_jam"
  },
  "stirs": 2,
  "utensil": {
    "tag": "c:spoons"
  }
 }
 );
<recipetype:extradelight:mixing_bowl>.addJsonRecipe("blueberry_jam", {
  "type": "extradelight:mixing_bowl",
  "experience": 1.0,
  "fluids": [
  ],
  "ingredients": [
      {"item": "croptopia:blueberry"}, {"item": "minecraft:sugar"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:blueberry_jam"
  },
  "stirs": 2,
  "utensil": {
    "tag": "c:spoons"
  }
 }
 );
<recipetype:extradelight:mixing_bowl>.addJsonRecipe("cherry_jam", {
  "type": "extradelight:mixing_bowl",
  "experience": 1.0,
  "fluids": [
  ],
  "ingredients": [
      {"item": "croptopia:cherry"}, {"item": "minecraft:sugar"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:cherry_jam"
  },
  "stirs": 2,
  "utensil": {
    "tag": "c:spoons"
  }
 }
 );
<recipetype:extradelight:mixing_bowl>.addJsonRecipe("elderberry_jam", {
  "type": "extradelight:mixing_bowl",
  "experience": 1.0,
  "fluids": [
  ],
  "ingredients": [
      {"item": "croptopia:elderberry"}, {"item": "minecraft:sugar"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:elderberry_jam"
  },
  "stirs": 2,
  "utensil": {
    "tag": "c:spoons"
  }
 }
 );
<recipetype:extradelight:mixing_bowl>.addJsonRecipe("grape_jam", {
  "type": "extradelight:mixing_bowl",
  "experience": 1.0,
  "fluids": [
  ],
  "ingredients": [
      {"item": "croptopia:grape"}, {"item": "minecraft:sugar"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:grape_jam"
  },
  "stirs": 2,
  "utensil": {
    "tag": "c:spoons"
  }
 }
 );
<recipetype:extradelight:mixing_bowl>.addJsonRecipe("peach_jam", {
  "type": "extradelight:mixing_bowl",
  "experience": 1.0,
  "fluids": [
  ],
  "ingredients": [
      {"item": "croptopia:peach"}, {"item": "minecraft:sugar"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:peach_jam"
  },
  "stirs": 2,
  "utensil": {
    "tag": "c:spoons"
  }
 }
 );
<recipetype:extradelight:mixing_bowl>.addJsonRecipe("raspberry_jam", {
  "type": "extradelight:mixing_bowl",
  "experience": 1.0,
  "fluids": [
  ],
  "ingredients": [
      {"item": "croptopia:raspberry"}, {"item": "minecraft:sugar"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:raspberry_jam"
  },
  "stirs": 2,
  "utensil": {
    "tag": "c:spoons"
  }
 }
 );
<recipetype:extradelight:mixing_bowl>.addJsonRecipe("strawberry_jam", {
  "type": "extradelight:mixing_bowl",
  "experience": 1.0,
  "fluids": [
  ],
  "ingredients": [
      {"item": "croptopia:strawberry"}, {"item": "minecraft:sugar"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:strawberry_jam"
  },
  "stirs": 2,
  "utensil": {
    "tag": "c:spoons"
  }
 }
 );
<recipetype:extradelight:mixing_bowl>.addJsonRecipe("mango_ice_cream", {
  "type": "extradelight:mixing_bowl",
  "experience": 1.0,
  "fluids": [
    {
      "amount": 250,
      "fluid": "minecraft:milk"
    }
  ],
  "ingredients": [
      {"item": "minecraft:egg"}, {"item": "minecraft:sugar"}, {"item": "croptopia:mango"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:mango_ice_cream"
  },
  "stirs": 4,
  "utensil": {
    "tag": "c:spoons"
  }
 }
 );
<recipetype:extradelight:mixing_bowl>.addJsonRecipe("strawberry_ice_cream", {
  "type": "extradelight:mixing_bowl",
  "experience": 1.0,
  "fluids": [
    {
      "amount": 250,
      "fluid": "minecraft:milk"
    }
  ],
  "ingredients": [
      {"item": "minecraft:egg"}, {"item": "minecraft:sugar"}, {"item": "neapolitan:strawberries"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:strawberry_ice_cream"
  },
  "stirs": 4,
  "utensil": {
    "tag": "c:spoons"
  }
 }
 );
<recipetype:extradelight:mixing_bowl>.addJsonRecipe("chocolate_ice_cream", {
  "type": "extradelight:mixing_bowl",
  "experience": 1.0,
  "fluids": [
    {
      "amount": 250,
      "fluid": "minecraft:milk"
    }
  ],
  "ingredients": [
      {"item": "minecraft:egg"}, {"item": "minecraft:sugar"}, {"item": "create:bar_of_chocolate"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:chocolate_ice_cream"
  },
  "stirs": 4,
  "utensil": {
    "tag": "c:spoons"
  }
 }
 );
<recipetype:extradelight:mixing_bowl>.addJsonRecipe("rum_raisin_ice_cream", {
  "type": "extradelight:mixing_bowl",
  "experience": 1.0,
  "fluids": [
    {
      "amount": 250,
      "fluid": "minecraft:milk"
    }
  ],
  "ingredients": [
      {"item": "minecraft:egg"}, {"item": "minecraft:sugar"}, {"item": "croptopia:rum"}, {"item": "croptopia:raisins"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:rum_raisin_ice_cream"
  },
  "stirs": 4,
  "utensil": {
    "tag": "c:spoons"
  }
 }
 );
<recipetype:extradelight:mixing_bowl>.addJsonRecipe("vanilla_ice_cream", {
  "type": "extradelight:mixing_bowl",
  "experience": 1.0,
  "fluids": [
    {
      "amount": 250,
      "fluid": "minecraft:milk"
    }
  ],
  "ingredients": [
      {"item": "minecraft:egg"}, {"item": "minecraft:sugar"}, {"item": "neapolitan:dried_vanilla_pods"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:vanilla_ice_cream"
  },
  "stirs": 4,
  "utensil": {
    "tag": "c:spoons"
  }
 }
 );
<recipetype:extradelight:mixing_bowl>.addJsonRecipe("pecan_ice_cream", {
  "type": "extradelight:mixing_bowl",
  "experience": 1.0,
  "fluids": [
    {
      "amount": 250,
      "fluid": "minecraft:milk"
    }
  ],
  "ingredients": [
      {"item": "minecraft:egg"}, {"item": "minecraft:sugar"}, {"item": "croptopia:pecan"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:pecan_ice_cream"
  },
  "stirs": 4,
  "utensil": {
    "tag": "c:spoons"
  }
 }
 );
<recipetype:extradelight:mixing_bowl>.addJsonRecipe("whipped_cream", {
  "type": "extradelight:mixing_bowl",
  "container": {
    "count": 4,
    "id": "minecraft:bowl"
  },
  "experience": 1.0,
  "fluids": [
    {
      "amount": 250,
      "fluid": "minecraft:milk"
    }
  ],
  "ingredients": [
  ],
  "result": {
    "count": 4,
    "id": "extradelight:whipped_cream"
  },
  "stirs": 12,
  "utensil": {
    "tag": "c:spoons"
  }
 }
 );

//添加茶壶配方(森罗→妖怪)
<recipetype:youkaishomecoming:kettle>.addJsonRecipe("barley_tea", {
  "type": "youkaishomecoming:kettle",
  "container": {
    "count": 4,
    "id": "kaleidoscope_cookery:empty_cup"
  },
  "experience": 1.0,
  "ingredients": [
      {"item": "minecraft:wheat_seeds"}, {"item": "minecraft:wheat_seeds"}, {"item": "minecraft:wheat_seeds"}, {"item": "minecraft:wheat_seeds"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 4,
    "id": "kaleidoscope_cookery:barley_tea"
  }
 }
 );
<recipetype:youkaishomecoming:kettle>.addJsonRecipe("tieguanyin", {
  "type": "youkaishomecoming:kettle",
  "container": {
    "count": 4,
    "id": "kaleidoscope_cookery:empty_cup"
  },
  "experience": 1.0,
  "ingredients": [
      {"item": "minecraft:iron_nugget"}, {"item": "minecraft:iron_nugget"}, {"item": "minecraft:iron_nugget"}, {"item": "minecraft:iron_nugget"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 4,
    "id": "kaleidoscope_cookery:tieguanyin"
  }
 }
 );
<recipetype:youkaishomecoming:kettle>.addJsonRecipe("biluochun", {
  "type": "youkaishomecoming:kettle",
  "container": {
    "count": 4,
    "id": "kaleidoscope_cookery:empty_cup"
  },
  "experience": 1.0,
  "ingredients": [
      {"item": "minecraft:nautilus_shell"}, {"item": "minecraft:nautilus_shell"}, {"item": "minecraft:nautilus_shell"}, {"item": "minecraft:nautilus_shell"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 4,
    "id": "kaleidoscope_cookery:biluochun"
  }
 }
 );
<recipetype:youkaishomecoming:kettle>.addJsonRecipe("oolong", {
  "type": "youkaishomecoming:kettle",
  "container": {
    "count": 4,
    "id": "kaleidoscope_cookery:empty_cup"
  },
  "experience": 1.0,
  "ingredients": [
      {"item": "minecraft:dragon_breath"}, {"item": "minecraft:dragon_breath"}, {"item": "minecraft:dragon_breath"}, {"item": "minecraft:dragon_breath"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 4,
    "id": "kaleidoscope_cookery:oolong"
  }
 }
 );
<recipetype:youkaishomecoming:kettle>.addJsonRecipe("ice_crystal_tea", {
  "type": "youkaishomecoming:kettle",
  "container": {
    "count": 4,
    "id": "kaleidoscope_cookery:empty_cup"
  },
  "experience": 1.0,
  "ingredients": [
      {"item": "kaleidoscope_twilight:four_leaf_ice_crystal"}, {"item": "kaleidoscope_twilight:four_leaf_ice_crystal"}, 
      {"item": "kaleidoscope_twilight:four_leaf_ice_crystal"}, {"item": "kaleidoscope_twilight:four_leaf_ice_crystal"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 4,
    "id": "kaleidoscope_twilight:ice_crystal_tea"
  }
 }
 );
<recipetype:youkaishomecoming:kettle>.addJsonRecipe("hot_tears_tea", {
  "type": "youkaishomecoming:kettle",
  "container": {
    "count": 4,
    "id": "kaleidoscope_cookery:empty_cup"
  },
  "experience": 1.0,
  "ingredients": [
      {"item": "twilightforest:fiery_tears"}, {"item": "twilightforest:fiery_tears"}, 
      {"item": "twilightforest:fiery_tears"}, {"item": "twilightforest:fiery_tears"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 4,
    "id": "kaleidoscope_twilight:hot_tears_tea"
  }
 }
 );
<recipetype:youkaishomecoming:kettle>.addJsonRecipe("phantom_tea", {
  "type": "youkaishomecoming:kettle",
  "container": {
    "count": 4,
    "id": "kaleidoscope_cookery:empty_cup"
  },
  "experience": 1.0,
  "ingredients": [
      {"item": "kaleidoscope_twilight:evil_soul"}, {"item": "kaleidoscope_twilight:evil_soul"}, 
      {"item": "kaleidoscope_twilight:evil_soul"}, {"item": "kaleidoscope_twilight:evil_soul"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 4,
    "id": "kaleidoscope_twilight:phantom_tea"
  }
 }
 );
<recipetype:youkaishomecoming:kettle>.addJsonRecipe("sakura_fubuki", {
  "type": "youkaishomecoming:kettle",
  "container": {
    "count": 4,
    "id": "kaleidoscope_cookery:empty_cup"
  },
  "experience": 1.0,
  "ingredients": [
      {"item": "minecraft:pink_petals"}, {"item": "minecraft:pink_petals"}, 
      {"item": "minecraft:pink_petals"}, {"item": "minecraft:pink_petals"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 4,
    "id": "kaleidoscope_cookery:sakura_fubuki"
  }
 }
 );
<recipetype:youkaishomecoming:kettle>.addJsonRecipe("flower_tea", {
  "type": "youkaishomecoming:kettle",
  "container": {
    "count": 4,
    "id": "kaleidoscope_cookery:empty_cup"
  },
  "experience": 1.0,
  "ingredients": [
      {"tag": "minecraft:small_flowers"}, {"tag": "minecraft:small_flowers"}, 
      {"tag": "minecraft:small_flowers"}, {"tag": "minecraft:small_flowers"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 4,
    "id": "kaleidoscope_cookery:flower_tea"
  }
 }
 );
<recipetype:youkaishomecoming:kettle>.addJsonRecipe("naga_tea", {
  "type": "youkaishomecoming:kettle",
  "container": {
    "count": 4,
    "id": "kaleidoscope_cookery:empty_cup"
  },
  "experience": 1.0,
  "ingredients": [
      {"item": "twilightforest:naga_scale"}, {"item": "twilightforest:naga_scale"}, 
      {"item": "twilightforest:naga_scale"}, {"item": "twilightforest:naga_scale"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 4,
    "id": "kaleidoscope_twilight:naga_tea"
  }
 }
 );
<recipetype:youkaishomecoming:kettle>.addJsonRecipe("witchcraft_tea", {
  "type": "youkaishomecoming:kettle",
  "container": {
    "count": 4,
    "id": "kaleidoscope_cookery:empty_cup"
  },
  "experience": 1.0,
  "ingredients": [
      {"item": "kaleidoscope_twilight:witchcraft_bone"}, {"item": "kaleidoscope_twilight:witchcraft_bone"}, 
      {"item": "kaleidoscope_twilight:witchcraft_bone"}, {"item": "kaleidoscope_twilight:witchcraft_bone"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 4,
    "id": "kaleidoscope_twilight:witchcraft_tea"
  }
 }
 );
<recipetype:youkaishomecoming:kettle>.addJsonRecipe("fire_tea", {
  "type": "youkaishomecoming:kettle",
  "container": {
    "count": 4,
    "id": "kaleidoscope_cookery:empty_cup"
  },
  "experience": 1.0,
  "ingredients": [
      {"item": "twilightforest:fiery_blood"}, {"item": "twilightforest:fiery_blood"}, 
      {"item": "twilightforest:fiery_blood"}, {"item": "twilightforest:fiery_blood"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 4,
    "id": "kaleidoscope_twilight:fire_tea"
  }
 }
 );
<recipetype:youkaishomecoming:kettle>.addJsonRecipe("minotaur_mushroom_tea", {
  "type": "youkaishomecoming:kettle",
  "container": {
    "count": 4,
    "id": "kaleidoscope_cookery:empty_cup"
  },
  "experience": 1.0,
  "ingredients": [
      {"item": "minecraft:red_mushroom"}, {"item": "minecraft:red_mushroom"}, 
      {"item": "minecraft:red_mushroom"}, {"item": "minecraft:red_mushroom"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 4,
    "id": "kaleidoscope_twilight:minotaur_mushroom_tea"
  }
 }
 );
<recipetype:youkaishomecoming:kettle>.addJsonRecipe("chorus_flower_tea", {
  "type": "youkaishomecoming:kettle",
  "container": {
    "count": 4,
    "id": "kaleidoscope_cookery:empty_cup"
  },
  "experience": 1.0,
  "ingredients": [
      {"item": "kaleidoscope_end:chorus_petal"}, {"item": "kaleidoscope_end:chorus_petal"}, 
      {"item": "kaleidoscope_end:chorus_petal"}, {"item": "kaleidoscope_end:chorus_petal"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 4,
    "id": "kaleidoscope_end:chorus_flower_tea"
  }
 }
 );
<recipetype:youkaishomecoming:kettle>.addJsonRecipe("ender_mint_tea", {
  "type": "youkaishomecoming:kettle",
  "container": {
    "count": 4,
    "id": "kaleidoscope_cookery:empty_cup"
  },
  "experience": 1.0,
  "ingredients": [
      {"item": "kaleidoscope_end:ender_mint"}, {"item": "kaleidoscope_end:ender_mint"}, 
      {"item": "kaleidoscope_end:ender_mint"}, {"item": "kaleidoscope_end:ender_mint"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 4,
    "id": "kaleidoscope_end:ender_mint_tea"
  }
 }
 );
<recipetype:youkaishomecoming:kettle>.addJsonRecipe("void_tea", {
  "type": "youkaishomecoming:kettle",
  "container": {
    "count": 4,
    "id": "kaleidoscope_cookery:empty_cup"
  },
  "experience": 1.0,
  "ingredients": [
      {"item": "kaleidoscope_end:void_conch"}, {"item": "kaleidoscope_end:void_conch"}, 
      {"item": "kaleidoscope_end:void_conch"}, {"item": "kaleidoscope_end:void_conch"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 4,
    "id": "kaleidoscope_end:void_tea"
  }
 }
 );
<recipetype:youkaishomecoming:kettle>.addJsonRecipe("ender_dragon_tea", {
  "type": "youkaishomecoming:kettle",
  "container": {
    "count": 4,
    "id": "kaleidoscope_cookery:empty_cup"
  },
  "experience": 1.0,
  "ingredients": [
      {"item": "kaleidoscope_end:dragon_dust"}, {"item": "kaleidoscope_end:dragon_dust"}, 
      {"item": "kaleidoscope_end:dragon_dust"}, {"item": "kaleidoscope_end:dragon_dust"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 4,
    "id": "kaleidoscope_end:ender_dragon_tea"
  }
 }
 );
//添加茶壶配方(乐事→妖怪)
<recipetype:youkaishomecoming:kettle>.addJsonRecipe("thorn_rose_tea", {
  "type": "youkaishomecoming:kettle",
  "container": {
    "count": 1,
    "id": "minecraft:glass_bottle"
  },
  "experience": 1.0,
  "ingredients": [
      {"item": "twilightforest:thorn_rose"}, {"item": "minecraft:sugar"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 1,
    "id": "twilightdelight:thorn_rose_tea"
  }
 }
 );
<recipetype:youkaishomecoming:kettle>.addJsonRecipe("pitcher_plant_tea", {
  "type": "youkaishomecoming:kettle",
  "container": {
    "count": 1,
    "id": "minecraft:glass_bottle"
  },
  "experience": 1.0,
  "ingredients": [
      {"item": "minecraft:pitcher_plant"}, {"item": "minecraft:sugar"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 1,
    "id": "trailandtales_delight:pitcher_plant_tea"
  }
 }
 );
<recipetype:youkaishomecoming:kettle>.addJsonRecipe("torchflower_tea", {
  "type": "youkaishomecoming:kettle",
  "container": {
    "count": 1,
    "id": "minecraft:glass_bottle"
  },
  "experience": 1.0,
  "ingredients": [
      {"item": "minecraft:torchflower"}, {"item": "minecraft:sugar"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 1,
    "id": "trailandtales_delight:torchflower_tea"
  }
 }
 );
<recipetype:youkaishomecoming:kettle>.addJsonRecipe("extradelight_tea", {
  "type": "youkaishomecoming:kettle",
  "container": {
    "count": 1,
    "id": "minecraft:glass_bottle"
  },
  "experience": 1.0,
  "ingredients": [
      {"tag": "c:tea_ingredients"}, {"tag": "c:tea_ingredients"}, {"item": "minecraft:sugar"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 1,
    "id": "extradelight:tea"
  }
 }
 );
<recipetype:youkaishomecoming:kettle>.addJsonRecipe("builders_tea", {
  "type": "youkaishomecoming:kettle",
  "container": {
    "count": 1,
    "id": "minecraft:glass_bottle"
  },
  "experience": 1.0,
  "ingredients": [
      {"tag": "oreberriesreplanted:oreberries"}, {"item": "minecraft:sugar"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 1,
    "id": "create:builders_tea"
  }
 }
 );
<recipetype:youkaishomecoming:kettle>.addJsonRecipe("cherry_petal_tea", {
  "type": "youkaishomecoming:kettle",
  "container": {
    "count": 1,
    "id": "minecraft:glass_bottle"
  },
  "experience": 1.0,
  "ingredients": [
      {"item": "trailandtales_delight:dried_cherry_petal"}, {"item": "trailandtales_delight:dried_cherry_petal"}, {"item": "minecraft:sugar"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 1,
    "id": "trailandtales_delight:cherry_petal_tea"
  }
 }
 );

//添加摩卡壶配方
<recipetype:youkaishomecoming:moka_pot>.addJsonRecipe("rusticdelight_coffee", {
  "type": "youkaishomecoming:moka_pot",
  "container": {
    "count": 1,
    "id": "minecraft:glass_bottle"
  },
  "experience": 1.0,
  "ingredients": [
      {"tag": "rusticdelight:coffee_ingredients"}, {"tag": "rusticdelight:coffee_ingredients"}, 
      {"tag": "rusticdelight:coffee_ingredients"}, {"tag": "rusticdelight:coffee_ingredients"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 1,
    "id": "rusticdelight:coffee"
  }
 }
 );
<recipetype:youkaishomecoming:moka_pot>.addJsonRecipe("chocolate_coffee", {
  "type": "youkaishomecoming:moka_pot",
  "container": {
    "count": 1,
    "id": "minecraft:glass_bottle"
  },
  "experience": 1.0,
  "ingredients": [
      {"item": "youkaishomecoming:coffee_powder"}, {"tag": "c:milks"}, 
      {"item": "minecraft:cocoa_beans"}, {"item": "minecraft:cocoa_beans"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 1,
    "id": "rusticdelight:chocolate_coffee"
  }
 }
 );
<recipetype:youkaishomecoming:moka_pot>.addJsonRecipe("ancient_coffee", {
  "type": "youkaishomecoming:moka_pot",
  "container": {
    "count": 1,
    "id": "minecraft:glass_bottle"
  },
  "experience": 1.0,
  "ingredients": [
      {"item": "trailandtales_delight:baked_torchflower_seeds"}, {"tag": "c:milks"}, 
      {"item": "trailandtales_delight:baked_pitcher_pod"}, {"item": "minecraft:sugar"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 1,
    "id": "trailandtales_delight:ancient_coffee"
  }
 }
 );
<recipetype:youkaishomecoming:moka_pot>.addJsonRecipe("milk_coffee", {
  "type": "youkaishomecoming:moka_pot",
  "container": {
    "count": 1,
    "id": "minecraft:glass_bottle"
  },
  "experience": 1.0,
  "ingredients": [
      {"item": "youkaishomecoming:coffee_powder"}, {"tag": "c:milks"}, {"tag": "c:milks"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 1,
    "id": "rusticdelight:milk_coffee"
  }
 }
 );
<recipetype:youkaishomecoming:moka_pot>.addJsonRecipe("syrup_coffee", {
  "type": "youkaishomecoming:moka_pot",
  "container": {
    "count": 1,
    "id": "minecraft:glass_bottle"
  },
  "experience": 1.0,
  "ingredients": [
      {"item": "youkaishomecoming:coffee_powder"}, {"item": "rusticdelight:syrup"}, {"tag": "c:milks"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 1,
    "id": "rusticdelight:syrup_coffee"
  }
 }
 );
<recipetype:youkaishomecoming:moka_pot>.addJsonRecipe("honey_coffee", {
  "type": "youkaishomecoming:moka_pot",
  "container": {
    "count": 1,
    "id": "minecraft:glass_bottle"
  },
  "experience": 1.0,
  "ingredients": [
      {"item": "minecraft:honey_bottle"}, {"item": "youkaishomecoming:coffee_powder"}, {"tag": "c:milks"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 1,
    "id": "rusticdelight:honey_coffee"
  }
 }
 );

//添加冷凝配方
<recipetype:extradelight:chiller>.addJsonRecipe("bar_of_chocolate", {
  "consumeContainer": false,
  "type": "extradelight:chiller",
  "container": {
    "count": 1,
    "id": "extradelight:bar_mold"
  },
  "cookingtime": 400,
  "experience": 0.35,
  "fluid": {
    "amount": 250,
    "id": "minecraft:milk"
  },
  "ingredients": [
    {"item": "minecraft:cocoa_beans"}, {"item": "minecraft:sugar"}
  ],
  "result": {
    "count": 1,
    "id": "create:bar_of_chocolate"
  }
 }
 );

//添加榨汁配方
<recipetype:expandeddelight:juicing>.addJsonRecipe("tomato_juice", {
  "type": "expandeddelight:juicing",
  "container": {
    "count": 1,
    "id": "minecraft:glass_bottle"
  },
  "experience": 1.0,
  "ingredients": [
    {"item": "farmersdelight:tomato"}, {"item": "farmersdelight:tomato"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 1,
    "id": "croptopia:tomato_juice"
  }
 }
 );
<recipetype:expandeddelight:juicing>.addJsonRecipe("limeade", {
  "type": "expandeddelight:juicing",
  "container": {
    "count": 1,
    "id": "minecraft:glass_bottle"
  },
  "experience": 1.0,
  "ingredients": [
    {"item": "extradelight:lemon"}, {"item": "croptopia:lime"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 1,
    "id": "croptopia:limeade"
  }
 }
 );
<recipetype:expandeddelight:juicing>.addJsonRecipe("saguaro_juice", {
  "type": "expandeddelight:juicing",
  "container": {
    "count": 1,
    "id": "minecraft:glass_bottle"
  },
  "experience": 1.0,
  "ingredients": [
    {"item": "croptopia:saguaro"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 1,
    "id": "croptopia:saguaro_juice"
  }
 }
 );
<recipetype:expandeddelight:juicing>.addJsonRecipe("orange_juice", {
  "type": "expandeddelight:juicing",
  "container": {
    "count": 1,
    "id": "minecraft:glass_bottle"
  },
  "experience": 1.0,
  "ingredients": [
    {"item": "extradelight:orange"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 1,
    "id": "croptopia:orange_juice"
  }
 }
 );
<recipetype:expandeddelight:juicing>.addJsonRecipe("apple_juice", {
  "type": "expandeddelight:juicing",
  "container": {
    "count": 1,
    "id": "minecraft:glass_bottle"
  },
  "experience": 1.0,
  "ingredients": [
    {"item": "minecraft:apple"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 1,
    "id": "croptopia:apple_juice"
  }
 }
 );
<recipetype:expandeddelight:juicing>.addJsonRecipe("croptopia_soy_milk", {
  "type": "expandeddelight:juicing",
  "container": {
    "count": 1,
    "id": "minecraft:glass_bottle"
  },
  "experience": 1.0,
  "ingredients": [
    {"item": "tofucraft:seeds_soybeans"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 1,
    "id": "croptopia:soy_milk"
  }
 }
 );
<recipetype:expandeddelight:juicing>.addJsonRecipe("cranberry_juice", {
  "type": "expandeddelight:juicing",
  "container": {
    "count": 1,
    "id": "minecraft:glass_bottle"
  },
  "experience": 1.0,
  "ingredients": [
    {"item": "croptopia:cranberry"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 1,
    "id": "croptopia:cranberry_juice"
  }
 }
 );
<recipetype:expandeddelight:juicing>.addJsonRecipe("pineapple_juice", {
  "type": "expandeddelight:juicing",
  "container": {
    "count": 1,
    "id": "minecraft:glass_bottle"
  },
  "experience": 1.0,
  "ingredients": [
    {"item": "pineapple_delight:pineapple_side"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 1,
    "id": "croptopia:pineapple_juice"
  }
 }
 );
<recipetype:expandeddelight:juicing>.addJsonRecipe("croptopia_wine", {
  "type": "expandeddelight:juicing",
  "container": {
    "count": 1,
    "id": "minecraft:glass_bottle"
  },
  "experience": 1.0,
  "ingredients": [
    {"item": "kaleidoscope_tavern:grape"}, {"item": "kaleidoscope_tavern:grape"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 1,
    "id": "croptopia:wine"
  }
 }
 );
<recipetype:expandeddelight:juicing>.addJsonRecipe("lemonade", {
  "type": "expandeddelight:juicing",
  "container": {
    "count": 1,
    "id": "minecraft:glass_bottle"
  },
  "experience": 1.0,
  "ingredients": [
    {"item": "extradelight:lemon"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 1,
    "id": "croptopia:lemonade"
  }
 }
 );
<recipetype:expandeddelight:juicing>.addJsonRecipe("melon_juice", {
  "type": "expandeddelight:juicing",
  "container": {
    "count": 1,
    "id": "minecraft:glass_bottle"
  },
  "experience": 1.0,
  "ingredients": [
    {"item": "minecraft:melon_slice"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 1,
    "id": "croptopia:melon_juice"
  }
 }
 );
<recipetype:expandeddelight:juicing>.addJsonRecipe("grape_juice", {
  "type": "expandeddelight:juicing",
  "container": {
    "count": 1,
    "id": "minecraft:glass_bottle"
  },
  "experience": 1.0,
  "ingredients": [
    {"item": "kaleidoscope_tavern:grape"}
  ],
  "recipe_book_tab": "drinks",
  "result": {
    "count": 1,
    "id": "croptopia:grape_juice"
  }
 }
 );

//添加烤炉配方
<recipetype:extradelight:oven>.addJsonRecipe("cheese_pizza", {
  "type": "extradelight:oven",
  "consumeContainer": false,
  "container": {
    "count": 1,
    "id": "extradelight:sheet"
  },
  "experience": 1.0,
  "ingredients": [
    {"item": "kaleidoscope_cookery:raw_dough"}, {"item": "extradelight:ketchup_jar_item"},
    {"item": "trailandtales_delight:cheese_slice"}, {"item": "trailandtales_delight:cheese_slice"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:cheese_pizza"
  }
 }
 );

<recipetype:extradelight:oven>.addJsonRecipe("supreme_pizza", {
  "type": "extradelight:oven",
  "consumeContainer": false,
  "container": {
    "count": 1,
    "id": "extradelight:sheet"
  },
  "experience": 1.0,
  "ingredients": [
    {"item": "kaleidoscope_cookery:raw_dough"}, {"item": "extradelight:sliced_tomato"}, {"item": "croptopia:olive"},
    {"item": "trailandtales_delight:cheese_slice"}, {"item": "rusticdelight:bell_pepper_yellow"}, {"item": "butchercraft:ground_beef"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:supreme_pizza"
  }
 }
 );
<recipetype:extradelight:oven>.addJsonRecipe("croptopia_pizza", {
  "type": "extradelight:oven",
  "consumeContainer": false,
  "container": {
    "count": 1,
    "id": "extradelight:sheet"
  },
  "experience": 1.0,
  "ingredients": [
    {"item": "kaleidoscope_cookery:raw_dough"}, {"item": "extradelight:sliced_tomato"},
    {"item": "trailandtales_delight:cheese_slice"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:pizza"
  }
 }
 );
<recipetype:extradelight:oven>.addJsonRecipe("pineapple_pepperoni_pizza", {
  "type": "extradelight:oven",
  "consumeContainer": false,
  "container": {
    "count": 1,
    "id": "extradelight:sheet"
  },
  "experience": 1.0,
  "ingredients": [
    {"item": "kaleidoscope_cookery:raw_dough"}, {"item": "extradelight:sliced_tomato"},{"item": "croptopia:pepperoni"},
    {"item": "trailandtales_delight:cheese_slice"},{"item": "pineapple_delight:pineapple_side"},{"item": "pineapple_delight:pineapple_side"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:pineapple_pepperoni_pizza"
  }
 }
 );
<recipetype:extradelight:oven>.addJsonRecipe("anchovy_pizza", {
  "type": "extradelight:oven",
  "consumeContainer": false,
  "container": {
    "count": 1,
    "id": "extradelight:sheet"
  },
  "experience": 1.0,
  "ingredients": [
    {"item": "kaleidoscope_cookery:raw_dough"}, {"item": "extradelight:sliced_tomato"}, {"item": "croptopia:anchovy"},
    {"item": "trailandtales_delight:cheese_slice"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:anchovy_pizza"
  }
 }
 );
<recipetype:extradelight:oven>.addJsonRecipe("banana_cream_pie", {
  "type": "extradelight:oven",
  "consumeContainer": false,
  "container": {
    "count": 1,
    "id": "extradelight:pie_dish"
  },
  "experience": 1.0,
  "ingredients": [
    {"item": "farmersdelight:pie_crust"}, {"item": "croptopia:milk_bottle"}, {"item": "minecraft:egg"},
    {"item": "minecraft:sugar"}, {"item": "neapolitan:dried_vanilla_pods"}, {"item": "croptopia:banana"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:banana_cream_pie"
  }
 }
 );

<recipetype:extradelight:oven>.addJsonRecipe("cherry_pie", {
  "type": "extradelight:oven",
  "consumeContainer": false,
  "container": {
    "count": 1,
    "id": "extradelight:pie_dish"
  },
  "experience": 1.0,
  "ingredients": [
    {"item": "farmersdelight:pie_crust"}, {"item": "croptopia:milk_bottle"}, {"item": "minecraft:egg"},
    {"item": "minecraft:sugar"}, {"item": "croptopia:cherry"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:cherry_pie"
  }
 }
 );
<recipetype:extradelight:oven>.addJsonRecipe("pecan_pie", {
  "type": "extradelight:oven",
  "consumeContainer": false,
  "container": {
    "count": 1,
    "id": "extradelight:pie_dish"
  },
  "experience": 1.0,
  "ingredients": [
    {"item": "farmersdelight:pie_crust"}, {"item": "croptopia:milk_bottle"}, {"item": "minecraft:egg"},
    {"item": "minecraft:sugar"}, {"item": "croptopia:pecan"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:pecan_pie"
  }
 }
 );
<recipetype:extradelight:oven>.addJsonRecipe("rhubarb_pie", {
  "type": "extradelight:oven",
  "consumeContainer": false,
  "container": {
    "count": 1,
    "id": "extradelight:pie_dish"
  },
  "experience": 1.0,
  "ingredients": [
    {"item": "farmersdelight:pie_crust"}, {"item": "croptopia:milk_bottle"}, {"item": "minecraft:egg"},
    {"item": "minecraft:sugar"}, {"item": "croptopia:rhubarb"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:rhubarb_pie"
  }
 }
 );
<recipetype:extradelight:oven>.addJsonRecipe("croptopia_apple_pie", {
  "type": "extradelight:oven",
  "consumeContainer": false,
  "container": {
    "count": 1,
    "id": "extradelight:pie_dish"
  },
  "experience": 1.0,
  "ingredients": [
    {"item": "farmersdelight:pie_crust"}, {"item": "croptopia:milk_bottle"}, {"item": "minecraft:egg"},
    {"item": "minecraft:sugar"}, {"item": "minecraft:apple"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:apple_pie"
  }
 }
 );
<recipetype:extradelight:oven>.addJsonRecipe("croptopia_quiche", {
  "type": "extradelight:oven",
  "consumeContainer": false,
  "container": {
    "count": 1,
    "id": "extradelight:pie_dish"
  },
  "experience": 1.0,
  "ingredients": [
    {"item": "minecraft:egg"}, {"item": "croptopia:milk_bottle"}, {"item": "minecraft:egg"},
    {"item": "extradelight:sliced_onion"}, {"item": "croptopia:flour"}, {"item": "croptopia:spinach"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:quiche"
  }
 }
 );
<recipetype:extradelight:oven>.addJsonRecipe("cornish_pasty", {
  "type": "extradelight:oven",
  "consumeContainer": false,
  "container": {
    "count": 1,
    "id": "extradelight:pie_dish"
  },
  "experience": 1.0,
  "ingredients": [
    {"item": "croptopia:rutabaga"}, {"item": "butchercraft:ground_beef"}, {"item": "minecraft:potato"},
    {"item": "croptopia:pepper"}, {"item": "farmersdelight:onion"}, {"item": "kaleidoscope_cookery:raw_dough"}
  ],
  "result": {
    "count": 1,
    "id": "croptopia:cornish_pasty"
  }
 }
 );
<recipetype:extradelight:oven>.addJsonRecipe("cinnamon_roll", {
  "type": "extradelight:oven",
  "consumeContainer": false,
  "container": {
    "count": 1,
    "id": "extradelight:loaf_pan"
  },
  "experience": 1.0,
  "ingredients": [
    {"item": "croptopia:cinnamon"}, {"item": "youkaishomecoming:butter"}, 
    {"item": "croptopia:salt"}, {"item": "minecraft:sugar"}, 
    {"item": "extradelight:whipped_cream"}, {"item": "croptopia:milk_bottle"}, 
    {"item": "minecraft:egg"}, {"item": "kaleidoscope_cookery:raw_dough"}
  ],
  "result": {
    "count": 3,
    "id": "croptopia:cinnamon_roll"
  }
 }
 );
