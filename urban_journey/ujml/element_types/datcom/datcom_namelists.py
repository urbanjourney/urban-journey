import numpy as np

class Namelist:
    namelist = {"CASEID": {"type": str,   "parent": "DATCOM", "tags": []},
                "DIM":    {"type": str,   "parent": "DATCOM", "tags": ["IN", "FT", "CM", "M"]},
                "DERIV":  {"type": str,   "parent": "DATCOM", "tags": ["DEG", "RAD"]},
                "SREF":   {"type": float, "parent": "REFQ"},
                "LREF":   {"type": float, "parent": "REFQ"},
                "LATREF": {"type": float, "parent": "REFQ"},
                "XCG":    {"type": float, "parent": "REFQ"},
                "ZCG":    {"type": float, "parent": "REFQ"},
                "BLAYER": {"type": str,   "parent": "REFQ",   "tags": ["TURB", "NATURAL"]},
                "ROUGH":  {"type": float, "parent": "REFQ"},
                "RHR":    {"type": float, "parent": "REFQ"},
                "SCALE":  {"type": float, "parent": "REFQ"},
                "ALPHA":  {"type": list,  "parent": "FLTCON", "limit_size": 100, "splits_in_cases": "just a flag"},
                "BETA":   {"type": list,  "parent": "FLTCON", "limit_size": 1,   "splits_in_cases": "just a flag"},
                "PHI":    {"type": list,  "parent": "FLTCON", "limit_size": 1,   "splits_in_cases": "just a flag"},
                "MACH":   {"type": list,  "parent": "FLTCON", "limit_size": 20,  "splits_in_cases": "just a flag"},
                "ALT":    {"type": list,  "parent": "FLTCON", "limit_size": 20,  "splits_in_cases": "just a flag"},
                "REN":    {"type": list,  "parent": "FLTCON"},
                "VINF":   {"type": list,  "parent": "FLTCON"},
                "TINF":   {"type": list,  "parent": "FLTCON"},
                "PINF":   {"type": list,  "parent": "FLTCON"},
                "X0":     {"type": float, "parent": "AXIBOD"},
                "TNOSE":  {"type": str,   "parent": "AXIBOD", "tags": ["CONE", "OGIVE", "POWER", "HAACK", "KARMAN"]},
                "POWER":  {"type": float, "parent": "AXIBOD"},
                "LNOSE":  {"type": float, "parent": "AXIBOD"},
                "DNOSE":  {"type": float, "parent": "AXIBOD"},
                "BNOSE":  {"type": float, "parent": "AXIBOD"},
                "TRUNC":  {"type": bool,  "parent": "AXIBOD"},
                "LCENTR": {"type": float, "parent": "AXIBOD"},
                "DCENTR": {"type": float, "parent": "AXIBOD"},
                "TAFT":   {"type": str,   "parent": "AXIBOD", "tags": ["CONE", "OGIVE"]},
                "LAFT":   {"type": float, "parent": "AXIBOD"},
                "DAFT":   {"type": float, "parent": "AXIBOD"},
                "DEXIT":  {"type": float, "parent": "AXIBOD"},
                "NPROT":  {"type": int,   "parent": "PROTUB", "driving_size": ""},
                "PTYPE":  {"type": list,  "parent": "PROTUB", "limit_size": 20,  "size_as": "NPROT",
                           "tags": ["VCYL", "HCYL", "LUG", "SHOE", "BLOCK", "FAIRING"]},
                "XPROT":  {"type": list,  "parent": "PROTUB", "limit_size": 20,  "size_as": "NPROT"},
                "NLOC":   {"type": list,  "parent": "PROTUB", "limit_size": 20,  "size_as": "NPROT"},
                "PHIPRO": {"type": list,  "parent": "PROTUB", "limit_size": 400, "size_as": "NPROT*NLOC"},
                "LPROT":  {"type": list,  "parent": "PROTUB", "limit_size": 100, "size_as": ""},
                "WPROT":  {"type": list,  "parent": "PROTUB", "limit_size": 100, "size_as": ""},
                "HPROT":  {"type": list,  "parent": "PROTUB", "limit_size": 100, "size_as": ""},
                "OPROT":  {"type": list,  "parent": "PROTUB", "limit_size": 100, "size_as": ""},
                "SECTYP": {"type": str,   "parent": "FINSET", "tags": ["HEX", "NACA", "ARC", "USER"]},
                "SSPAN":  {"type": list,  "parent": "FINSET", "limit_size": 10, "driving_size": ""},
                "CHORD":  {"type": list,  "parent": "FINSET", "limit_size": 10, "size_as": "SSPAN"},
                "XLE":    {"type": list,  "parent": "FINSET", "limit_size": 10, "size_as": "SSPAN"},
                "SWEEP":  {"type": list,  "parent": "FINSET", "limit_size": 9,  "size_as": ""},
                "STA":    {"type": list,  "parent": "FINSET", "limit_size": 9,  "size_as": ""},
                "LER":    {"type": list,  "parent": "FINSET", "limit_size": 10, "size_as": "SSPAN"},
                "NPANEL": {"type": int,   "parent": "FINSET", "min": 1,        "max": 8},
                "PHIF":   {"type": list,  "parent": "FINSET", "limit_size": 8,  "size_as": ""},
                "GAM":    {"type": list,  "parent": "FINSET", "limit_size": 8,  "size_as": ""},
                "NVOR":   {"type": int,   "parent": "FINSET", "min": 1,        "max": 20},
                "ZUPPER": {"type": list,  "parent": "FINSET", "limit_size": 10, "size_as": "SSPAN"},
                "ZLOWER": {"type": list,  "parent": "FINSET", "limit_size": 10, "size_as": "SSPAN"},
                "LMAXU":  {"type": list,  "parent": "FINSET", "limit_size": 10, "size_as": "SSPAN"},
                "LMAXL":  {"type": list,  "parent": "FINSET", "limit_size": 10, "size_as": "SSPAN"},
                "LFLATU": {"type": list,  "parent": "FINSET", "limit_size": 10, "size_as": "SSPAN"},
                "LFLATL": {"type": list,  "parent": "FINSET", "limit_size": 10, "size_as": "SSPAN"},
                "XCORD":  {"type": list,  "parent": "FINSET", "limit_size": 50, "size_as": ""},
                "MEAN":   {"type": list,  "parent": "FINSET", "limit_size": 50, "size_as": "XCORD"},
                "THICK":  {"type": list,  "parent": "FINSET", "limit_size": 50, "size_as": "XCORD"},
                "YUPPER": {"type": list,  "parent": "FINSET", "limit_size": 50, "size_as": "XCORD"},
                "YLOWER": {"type": list,  "parent": "FINSET", "limit_size": 50, "size_as": "XCORD"},
                "DELTA1": {"type": list,  "parent": "DEFLCT", "limit_size": 8,  "size_as": "NPANEL"},
                "DELTA2": {"type": list,  "parent": "DEFLCT", "limit_size": 8,  "size_as": "NPANEL"},
                "DELTA3": {"type": list,  "parent": "DEFLCT", "limit_size": 8,  "size_as": "NPANEL"},
                "DELTA4": {"type": list,  "parent": "DEFLCT", "limit_size": 8,  "size_as": "NPANEL"},
                "DELTA5": {"type": list,  "parent": "DEFLCT", "limit_size": 8,  "size_as": "NPANEL"},
                "DELTA6": {"type": list,  "parent": "DEFLCT", "limit_size": 8,  "size_as": "NPANEL"},
                "DELTA7": {"type": list,  "parent": "DEFLCT", "limit_size": 8,  "size_as": "NPANEL"},
                "DELTA8": {"type": list,  "parent": "DEFLCT", "limit_size": 8,  "size_as": "NPANEL"},
                "DELTA9": {"type": list,  "parent": "DEFLCT", "limit_size": 8,  "size_as": "NPANEL"},
                "XHINGE": {"type": list,  "parent": "DEFLCT", "limit_size": 4,  "size_as": ""},
                "SKEW":   {"type": list,  "parent": "DEFLCT", "limit_size": 4,  "size_as": ""},
                "SET":    {"type": int,   "parent": "TRIM"},
                "PANL1":  {"type": bool,  "parent": "TRIM"},
                "PANL2":  {"type": bool,  "parent": "TRIM"},
                "PANL3":  {"type": bool,  "parent": "TRIM"},
                "PANL4":  {"type": bool,  "parent": "TRIM"},
                "PANL5":  {"type": bool,  "parent": "TRIM"},
                "PANL6":  {"type": bool,  "parent": "TRIM"},
                "PANL7":  {"type": bool,  "parent": "TRIM"},
                "PANL8":  {"type": bool,  "parent": "TRIM"},
                "DELMIN": {"type": float, "parent": "TRIM"},
                "DELMAX": {"type": float, "parent": "TRIM"},
                "NINCR":  {"type": int,   "parent": "TRIM"}}

    def __init__(self):
        """
            Each case is a dictionary of keys and values to parse to DATCOM input format
            mainCase| contains all the main data whereas the others contain values that do not fit in a single case.
            Values from |mainCase| are carried on to the other cases with the SAVE command.
            This is because DATCOM limits some parameters to a certain amount per case (i.e. 20 Mach numbers per case).
            |secondaryCases| contains all possible combinations of the parameters that had to be split into different
            cases. For instance, if 2 sideslip angles and 30 altitudes are set, this will generate 4 cases since only
            one sideslip angle and up to 20 altitudes can be present in a case.

            FINSET parameters have the fin set number appended (i.e.: SSPAN1, SSPAN2, ...)
        """
        self.mainCase = {}
        self.secondaryCases = [{}]
        self.cases = []

    @staticmethod
    def type_for_name(name):
        if name in Namelist.namelist.keys():
            return Namelist.namelist[name]["type"]
        else:
            pass    # TODO: handle name not recognised

    @staticmethod
    def name_in_namelist(name):
        return name in Namelist.namelist

    @staticmethod
    def get_parent(name):
        #   Remove trailing number for names of set FINSET
        if name[-1].isnumeric():
            name = name[0: -1]
        if Namelist.name_in_namelist(name):
            return Namelist.namelist[name]["parent"]
        else:
            return False

    def is_input_correct(self, name, value, parent):
        input_type = Namelist.type_for_name(name)

        if not Namelist.name_in_namelist(name):
            return False

        # Check type correctness
        if type(value) is not input_type:
            return False

        # Create temporary parent without number for the fin set parameters
        temp_parent = parent
        if "FINSET" in parent:
            temp_parent = "FINSET"

        # Check if fin set number is provided
        if "FINSET" in parent and parent is "FINSET":
            return False

        # Check if value has already been set. Handle special case FINSET parent first
        if "FINSET" in parent:
            finset_num = parent[-1]
            if name + finset_num in self.mainCase:
                return False
        if name in self.mainCase:
            return False

        # Check for parent correctness. First correct the special numbered case FINSET
        if temp_parent != Namelist.get_parent(name):
            return False

        # Check value correctness
        if input_type is list:
            if "limit_size" in Namelist.namelist[name]:
                if len(value) > Namelist.namelist[name]["limit_size"]:
                    if "splits_in_cases" not in Namelist.namelist[name]:
                        return False

            # Check if items need to be strings and then if these are correct
            if "tags" in Namelist.namelist[name]:
                for val in value:
                    if type(val) is not str:
                        return False
                    else:
                        if val not in Namelist.namelist[name]["tags"]:
                            return False

            if "size_as" in Namelist.namelist[name]:
                size_model = Namelist.namelist[name]["size_as"]
                if size_model in self.mainCase:   # Check if driving size model is set
                    size = self.mainCase[size_model] if Namelist.namelist[size_model]["type"] is int else len(self.mainCase[size_model])
                    if len(value) is not size:
                        # Size does not correspond to driving size model
                        return False

            elif "driving_size" in Namelist.namelist[name]:
                # The driving model is being set, check of the dependent items that where set before are the right size.
                for itemName in Namelist.namelist.keys():
                    if itemName is name:
                        continue
                    # Check if an item is dependent to the current
                    if "size_as" in Namelist.namelist[itemName]:
                        if Namelist.namelist[itemName]["size_as"] == name:
                            # If the dependent item has been already assigned a list, check that the size is correct
                            # Append fin set number to parameters of fin set
                            if "FINSET" in parent:
                                itemName += parent[-1]
                            if itemName in self.mainCase:
                                if len(self.mainCase[itemName]) is not len(value):
                                    # Error, an item size that depended on this has a different size
                                    return False

        elif input_type is str:
            if value in Namelist.namelist[name]["tags"] or len(Namelist.namelist[name]["tags"]) is 0:
                return True
            else:
                return False

        elif input_type is int or input_type is float:
            if "min" in Namelist.namelist[name]:
                if value < Namelist.namelist[name]["min"]:
                    return False
            if "max" in Namelist.namelist[name]:
                if value > Namelist.namelist[name]["max"]:
                    return False
            if "driving_size" in Namelist.namelist[name]:
                # The driving model is being set, check of the dependent items that where set before are the right size.
                for itemName in Namelist.namelist.keys():
                    if itemName is name:
                        continue
                    # Check if an item is dependent to the current
                    if "size_as" in Namelist.namelist[itemName]:
                        if Namelist.namelist[itemName]["size_as"] == name:
                            # If the dependent item has been already assigned a list, check that the size is correct
                            # Append fin set number to parameters of fin set
                            if "FINSET" in parent:
                                itemName += parent[-1]
                            if itemName in self.mainCase:
                                if len(self.mainCase[itemName]) is not value:
                                    # Error, an item size that depended on this has a different size
                                    return False
        return True

    def set_value(self, name, value, parent):
        if self.is_input_correct(name, value, parent):
            if "FINSET" in parent:
                name += parent[-1]  # If name is part of a fin set, append the fin set number
            self.mainCase[name] = value
            return True
        else:
            return False

    def list_of_namesets(self):
        return_list = []
        for item in self.mainCase.keys():
            parent = Namelist.get_parent(item)
            # Check if parent has already been added to the return list
            if parent not in return_list:
                return_list.append(parent)
        return return_list

    def generate_cases(self):
        # This function generates different cases and distribute the
        # parameters in self.mainCase according to datcom requirements
        # (will generate ;)
        name_sets = self.list_of_namesets()
        names_to_split_in_cases = {}
        for key, value in self.mainCase.items():
            if "splits_in_cases" in Namelist.namelist[key]:
                names_to_split_in_cases[key] = value

        for name, value in names_to_split_in_cases.items():
            slice_count = int(np.ceil((len(value)/Namelist.namelist[name]["limit_size"])))
            secondary_cases_temp = self.secondaryCases[:]
            self.secondaryCases = []
            i0, i1 = 0, Namelist.namelist[name]["limit_size"]
            for i in range(slice_count):
                this_slice = value[i0:i1]
                for case in secondary_cases_temp:
                    # Add name to case
                    new_case = case.copy()
                    new_case[name] = this_slice
                    self.secondaryCases.append(new_case)
                i0, i1 = i1, i1 + Namelist.namelist[name]["limit_size"]

    def parse_case(self, case):
        pass
