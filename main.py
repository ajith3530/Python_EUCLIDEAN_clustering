from Kdtree import KdTree
import pandas as pd

point_cloud = pd.read_csv("point_cloud_data_sample.xyz", delimiter=" ", nrows=10)

tree = KdTree()
tree.insert_points(point_cloud, display_output=True)