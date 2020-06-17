"""
Processing of Point Cloud data
"""
import Kdtree
import pandas as pd

class ProcessPointCloud:
    """
    ProcessPointCloud Class
    """
    def __init__(self, pcd_file, nrows_value, display_output_flag):
        if pcd_file.endswith(".xyz"):
            self.pcd_data = pd.read_csv("point_cloud_data_sample.xyz", delimiter=" ", nrows=nrows_value)
        elif pcd_file.endswith(".pcd"):
            pass
            # TODO: Add logic for pcd data retreival
        self.kdtree_main = Kdtree()
        self.kdtree_root_node = self.kdtree_main.insert_points(self.pcd_data, display_output=display_output_flag)

    def euclidean_clustering(self, distance_threshold, cluster_parameters):
        """
        Perform Euclidean clustering
        :param distance_threshold: minimum distance between points in a cluster
        :param cluster_parameters: {min_size:value_1, max_size:value_2}
        :return: identified clusters after Euclidean Clustering
        """
        clusters_identified = dict()
        cluster_id = 0
        # Set up a boolean list with all elements set to False
        processed_flag = [False]*len(self.nrows)
        # Each row in pcd_data is a pcd point
        for point in self.pcd_data.iterrows():
            index = point[0]
            current_point = (point[0]["X"], point[0]["Y"], point[0]["Z"])
            if not processed_flag[index]:
                base_cluster = set()
                self.find_clusters(current_point, base_cluster, index, distance_threshold, cluster_parameters, processed_flag)
                # If cluster is within the parameter limits
                if base_cluster is not None:
                    if (len(base_cluster) > cluster_parameters["min_size"])\
                    and (len(base_cluster) < cluster_parameters["max_size"]):
                        clusters_identified[cluster_id] = base_cluster
                        cluster_id += 1
        return clusters_identified

    def get_point(self, index):
        """
        return point
        :param index: dataframe index
        :return: point as tuple
        """
        return (self.pcd_data.loc[index][1]["X"],
                self.pcd_data.loc[index][1]["Y"],
                self.pcd_data.loc[index][1]["Z"])

    def find_clusters(self, current_point, base_cluster, index, threshold, cluster_parameters, processed_flag):
        """
        search for clusters
        :param current_point: current point being processed.
        :param base_cluster: already known clusters.
        :param index: index of the point.
        :param threshold:  min distance for cluster identification.
        :param cluster_parameters: Cluster parameters {min_size, max_size}
        :param processed_flag: list containing status of points which have been identified as clusters.
        """
        # Considering points which have not been processed before, and are within are cluster parameter limits
        if not processed_flag[index] and len(base_cluster) < cluster_parameters["max_size"]:
            processed_flag[index] = True
            base_cluster.add(index)
            # Returns id listof the points which are near the current point,
            # id and index would be the same because of the unpacking design followed in build_kdtree method.
            nearby_points = self.kdtree_main.search_elements(node=self.kdtree_root_node, search_point=current_point,
                                                             distance_threshold=threshold, depth=0)

            if len(nearby_points):
                for index in nearby_points:
                    if not processed_flag[index]:
                        point = self.get_point(index)
                        self.find_clusters(point, self.kdtree_root_node, index,
                                           threshold, cluster_parameters, processed_flag)

if __name__ == "main":
    APPLICATION = ProcessPointCloud(pcd_file="point_cloud_data_sample.xyz", nrows_value=10, display_output_flag=True)




