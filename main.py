from Kdtree import KdTree_class
import pandas as pd

point_cloud = pd.read_csv("point_cloud_data_sample.xyz", delimiter=" ", nrows=10)

tree = KdTree_class()
root_node = tree.insert_points(point_cloud, display_output=True)
print(tree.search_elements(root_node, (3.12998489, -4.83957614, -6.24208885), 0.5))
# print(tree.kdtree_search_dict)