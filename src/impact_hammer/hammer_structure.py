import json

class HammerStructure:
    def __init__(self, json_path):
        with open(json_path) as json_file:
            struct_dict = json.load(json_file)
        self.L_arm = struct_dict["length_arm_m"]
        self.m_hammer = struct_dict["mass_head_kg"]
        self.m_arm = struct_dict["arm_extrusion_kg"]

    def get_moment_of_inertia(self):
        # https://en.wikipedia.org/wiki/List_of_moments_of_inertia
        return self.m_hammer * self.L_arm**2 + 1/3 * self.m_arm * self.L_arm**2