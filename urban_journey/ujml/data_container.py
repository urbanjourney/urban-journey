from urban_journey.ujml.exceptions import RequiredAttributeError, UJMLError, UJMLTypeError


class DataContainer(object):
    def __init__(self):
        self.__data_nodes = {}

    def add_data_node(self, node):
        if node.id is None:
            return

        if node.id == "add_data_node":
            node.raise_exception(UJMLError, "Data element cannot have id='add_data_node'")

        if not hasattr(node, "data"):
            raise TypeError("Not a valid data element.")

        self.__data_nodes[node.id] = node

    def __getitem__(self, member_name):
        return self.__data_nodes[member_name].data

    # def __setitem__(self, member_name, v):
    #     self.__data_nodes[member_name] = v
