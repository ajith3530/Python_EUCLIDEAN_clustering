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
        :return: classified clusters
        """
        clusters_identified = dict{}
        cluster_id = 0
        # Set up a boolean list with all elements set to False
        processed_flag = [False]*len(self.nrows)

        # Each row in pcd_data is a pcd point
        for point in self.pcd_data.iterrows():
            index = point[0]
            if not processed_flag[index]:
                cluster = self.find_clusters()
                # If cluster is within the parameter limits
                if (len(cluster) > cluster_parameters["min_size"]) and (len(cluster) < cluster_parameters["max_size"]):
                    clusters_identified[cluster_id] = cluster
                    cluster_id +=1

    def find_clusters(self, clusters_identified, index, distance_threshold, cluster_parameters):
        pass




if __name__ == "main":
    APPLICATION = ProcessPointCloud(pcd_file="point_cloud_data_sample.xyz", nrows_value=10, display_output_flag=True)




