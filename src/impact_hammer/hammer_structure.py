import json

class HammerStructure:
    def __init__(self, json_path):
        with open(json_path) as json_file:
            struct_dict = json.load(json_file)
        self.L_hammer = struct_dict["length_arm_m"]
        self.m_hammer = struct_dict["mass_head_kg"]