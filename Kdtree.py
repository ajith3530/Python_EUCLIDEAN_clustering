"""
kDTree Implementation
"""

class Node:
    """
    data: list of [x,y,z] coordinates
    """
    def __init__(self, data, point_id):
        self.point = {"X": data[0], "Y": data[1], "Z": data[2]}
        self.id = point_id
        self.left_node = None
        self.right_node = None

class KdTree:
    """
    Implementation of KDtree
    """
    def __init__(self):
        self.root = None

    def insert_points(self, pcd_dataframe):
        """
        :param pcd_dataframe: dataframe containing (x,y,z) coordinates data
        :return:
        """
        for row in pcd_dataframe.iterrows():
            x, y, z, point_id = row[1]["X"], row[1]["Y"], row[1]["Z"], row[0]
            point = [x, y, z]

            level = 0
            # Adding None as
            self.root = self.build_kdtree(self.root, level, point, point_id)
        print("Kdtree Build Complete")

    def build_kdtree(self, node, level, point, point_id):
        """
        :param node: Node class object
        :param level: level0 -x, level1-y, Level2-z
        :return:
        """
        # # This is for the very first point being added to the KdTREE
        # if self.root == None:
        #     self.root = Node(point, point_id)
        # After the first point is added - For recursion cases
        if node == None:
            node = Node(point, point_id)
            return node
        else:
            # For the subsequent cases
            # self.current_node = node
            # If current node is empty, then assign the point as root
            current_node = Node(point, point_id)
            # Level should always be within 0-2 range
            level %= 3
            if node.point[self.__dict_key(level)] > current_node.point[self.__dict_key(level)]:
                node.right_node = self.build_kdtree(node.right_node, level + 1, point, point_id)
            else:
                node.left_node = self.build_kdtree(node.left_node, level + 1, point, point_id)
            return node

    def remove_elements(self):
        pass

    def search_elements(self):
        pass

    def display_Kdtree(self):
        current_node = self.root
        if not current_node == None:
            print(f"Root Node = {current_node.point}")
            print(f"Left Section")




    @staticmethod
    def __dict_key(number):
        try:
            key_dict={0:"X", 1:"Y", 2:"Z"}
            return str(key_dict[number])
        except KeyError:
            raise Exception(f"Incorrect Level({number}) Assignment.")


if __name__ == "__main__":
    pass