"""
kDTree Implementation
"""
import math
class Node:
    """
    data: list of [x,y,z] coordinates
    """
    def __init__(self, data, point_id):
        self.point = {"X": data[0], "Y": data[1], "Z": data[2]}
        self.point_id = point_id
        self.left_node = None
        self.right_node = None


class KdTree_class:
    """
    Implementation of KDtree
    """
    def __init__(self):
        self.root = None
        self.kdtree_display_dict = dict()


    def insert_points(self, pcd_dataframe, display_output=False):
        """
        :param pcd_dataframe: dataframe containing (x,y,z) coordinates data
        :return:
        """
        for row in pcd_dataframe.iterrows():
            x, y, z, point_id = row[1]["X"], row[1]["Y"], row[1]["Z"], row[0]
            point = (x, y, z)
            level = 0
            self.root = self.build_kdtree(self.root, level, point, point_id)
        # If display_output is enabled, then display the contents of Kdtree
        if display_output:
            print("Kdtree Build Complete")
            self.display_kdtree(self.root)
            for pair in self.kdtree_display_dict.items():
                print(f"Depth = {pair[0]}, Points = {pair[1]} ")
        return self.root

    def build_kdtree(self, node, depth, point,point_id):
        """
        :param node: Node class object
        :param depth: level0 -x, level1-y, Level2-z
        :return: root node
        """
        if node is None:
            node = Node(point, point_id)
            return node

        # If current node is empty, then assign the point as root
        current_node = Node(point, point_id)
        # Level should always be within 0-2 range
        depth %= 3
        # levels correspond to (X,Y,Z), check at each level before assigning left/right to the root node
        # self.__dict_key returns X,Y,Z based on the level value. Check function for detailed description
        if node.point[self.__dict_key(depth)] < current_node.point[self.__dict_key(depth)]:
            # If value at level less than current node point, add it as a right node
            node.right_node = self.build_kdtree(node.right_node, depth + 1, point, point_id)
        else:
            # If value at level is more than current node point, add it as a left node
            node.left_node = self.build_kdtree(node.left_node, depth + 1, point, point_id)
        return node

    def search_elements(self, node, search_point, distance_threshold, depth=0, kdtree_search_results=set()):
        """
        :param node: node of kdtree
        :param search_point: (x,y,z) point
        :param distance_threshold: pcd elements near point
        :param depth: level of the kdtree depth
        :param kdtree_search_results: level of the kdtree depth
        :return: ids which can be considered as near points
        """
        depth %= 3
        current_node = node
        if current_node is not None:
            # If current node is within the distance threshold of search_point
            if(((current_node.point["X"] < search_point[0] + distance_threshold) and (current_node.point["X"] > search_point[0] - distance_threshold)) and
               ((current_node.point["Y"] < search_point[1] + distance_threshold) and (current_node.point["Y"] > search_point[1] - distance_threshold)) and
               ((current_node.point["Z"] < search_point[2] + distance_threshold) and (current_node.point["Z"] > search_point[2] - distance_threshold))):
                # Calculate the distance of search point from current node
                point_distance = math.sqrt(math.pow((current_node.point["X"] - search_point[0]), 2) +
                                           math.pow((current_node.point["Y"] - search_point[1]), 2) +
                                           math.pow((current_node.point["Z"] - search_point[2]), 2))
                if point_distance <= distance_threshold:
                    kdtree_search_results.add(current_node.point_id)
                else:
                    pass
            # Iterate recursively
            # if current_node.point[self.__dict_key(depth)] < search_point[depth]:
            if current_node.point[self.__dict_key(depth)] < search_point[depth] + distance_threshold:
                self.search_elements(current_node.right_node, search_point, distance_threshold,
                                     depth+1, kdtree_search_results)

            # else:
            if current_node.point[self.__dict_key(depth)] > search_point[depth] - distance_threshold:
                self.search_elements(current_node.left_node, search_point, distance_threshold,
                                     depth+1, kdtree_search_results)
            return kdtree_search_results

    def display_kdtree(self, node, depth=0):
        """
        updates the self.kdtree_dict with the points are corresponding depth
        :param node: root node
        :param depth: indicates the depth of Kdtree

        """
        current_node = node
        try:
            # If there are values already present, append the list with the point.
            self.kdtree_display_dict[depth].extend([(current_node.point["X"],
                                                    current_node.point["Y"],
                                                    current_node.point["Z"])])
        except KeyError:
            # If there are no values at the level, add value as first point
            self.kdtree_display_dict[depth] = [(current_node.point["X"],
                                                current_node.point["Y"],
                                                current_node.point["Z"])]
        # Run the recursion until a function hits the empty node
        if current_node is not None:
            # Check
            if current_node.left_node is not None:
                left_node = current_node.left_node
                # increment the value of depth
                depth += 1
                # at every node, call the recursive function
                self.display_kdtree(left_node ,depth)

            if current_node.right_node is not None:
                right_node = current_node.right_node
                # increment the value of depth
                depth += 1
                # at every node, call the recursive function
                self.display_kdtree(right_node ,depth)

    @staticmethod
    def __dict_key(number):
        """
        returns XYZ based on number
        :param number: 0,1,2
        :return: X,Y,Z
        """
        try:
            key_dict = {0: "X", 1: "Y", 2: "Z"}
            return str(key_dict[number])
        except KeyError:
            raise Exception(f"Incorrect Level({number}) Assignment.")


if __name__ == "__main__":
    pass