from Data.turret_types import turret_data
from Data.block_types import block_data
from Data.ally_types import ally_data

build_data = {}
troop_data = {}


def add_items(data, dictionary):
    for item in data:
        dictionary[item] = {"text": data[item]["name"],
                            "function": item,
                            "price": data[item]["price"]}


add_items(block_data, build_data)
add_items(turret_data, build_data)
build_data[1] = {"text": "Delete",
                 "function": 1,
                 "price": 0}
add_items(ally_data, troop_data)

# build_data = {
#     1: {"text": "Tower",
#         "function": 6,
#         "price": turret_data[6]["price"]

#         },

#     2: {"text": "Rapid",
#         "function": 7,
#         "price": turret_data[7]["price"]

#         },

#     3: {"text": "Cannon",
#         "function": 8,
#         "price": turret_data[8]["price"]

#         },

#     4: {"text": "Sniper",
#         "function": 9,
#         "price": turret_data[9]["price"]

#         },

#     5: {"text": "Path",
#         "function": 3,
#         "price": 100

#         },

#     6: {"text": "Barrier",
#         "function": 2,
#         "price": 250

#         },

#     7: {"text": "Delete",
#         "function": 1,
#         "price": 0

#         },
# }


# troop_data = {
#     10: {
#         "text": "Baby PinkGuy",
#         "function": 10,
#         "price": ally_data[10]["price"],
#     },
#     11: {
#         "text": "PinkGuy",
#         "function": 11,
#         "price": ally_data[11]["price"],
#     },
#     12: {
#         "text": "Baby MaskDude",
#         "function": 12,
#         "price": ally_data[12]["price"],
#     },
#     13: {
#         "text": "MaskDude",
#         "function": 13,
#         "price": ally_data[13]["price"],
#     },
#     14: {
#         "text": "Baby NinjaFrog",
#         "function": 14,
#         "price": ally_data[14]["price"],
#     },
#     15: {
#         "text": "NinjaFrog",
#         "function": 15,
#         "price": ally_data[15]["price"],
#     },
# }
