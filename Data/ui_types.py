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
                 "price": None
                 }
add_items(ally_data, troop_data)
