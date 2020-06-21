"""
Processing of Point Cloud data
"""
from Kdtree import KdTree_class
import pandas as pd
import copy
import plotly.graph_objects as go
import open3d as o3d



class ProcessPointCloud:
    """
    ProcessPointCloud Class
    """
    def __init__(self, pcd_file, nrows_value, display_output_flag):
        self.nrows = nrows_value
        if pcd_file.endswith(".pcd"):
            pcd = o3d.io.read_point_cloud(r"point_cloud_data_sample_2.pcd")
            self.pcd_data = pd.DataFrame(pcd.points, columns={"X" ,"Y" ,"Z"})
            self.pcd_data = self.pcd_data[0:self.nrows]
        elif pcd_file.endswith(".xyz"):
            self.pcd_data = pd.read_csv("point_cloud_data_sample.xyz", delimiter=" ", nrows=nrows_value)
        else:
            raise Exception(f"Unsupported datatype of pcd file.")
        self.kdtree_main = KdTree_class()
        self.kdtree_root_node = self.kdtree_main.insert_points(self.pcd_data, display_output=display_output_flag)

    def euclidean_clustering(self, distance_threshold, cluster_parameters):
        """
        Perform Euclidean clustering
        :param distance_threshold: minimum distance between points in a cluster
        :param cluster_parameters: {min_size:value_1}
        :return: identified clusters after Euclidean Clustering
        """
        clusters_identified = dict()
        cluster_id = 0
        # Set up a boolean list with all elements set to False
        processed_flag = [False]*self.nrows
        # Each row in pcd_data is a pcd point
        for point in self.pcd_data.iterrows():
            index = point[0]
            current_point = (point[1]["X"], point[1]["Y"], point[1]["Z"])
            if not processed_flag[index]:
                base_cluster = set()
                self.find_clusters(current_point, base_cluster, index, distance_threshold, cluster_parameters, processed_flag)
                # If cluster is within the parameter limits
                if base_cluster is not None:
                    if (len(base_cluster) > cluster_parameters["min_size"]):
                        clusters_identified[cluster_id] = base_cluster
                        cluster_id += 1
        return clusters_identified

    def get_point(self, index):
        """
        return point
        :param index: dataframe index
        :return: point as tuple
        """
        return (self.pcd_data.loc[index]["X"],
                self.pcd_data.loc[index]["Y"],
                self.pcd_data.loc[index]["Z"])

    def find_clusters(self, current_point_, base_cluster_, index_, threshold_, cluster_parameters_, processed_flag_):
        """
        search for clusters
        :param current_point_: current point being processed.
        :param base_cluster_: already known clusters.
        :param index_: index of the point.
        :param threshold_:  min distance for cluster identification.
        :param cluster_parameters_: Cluster parameters {min_size}
        :param processed_flag_: list containing status of points which have been identified as clusters.
        """
        # Considering points which have not been processed before, and are within are cluster parameter limits
        if not processed_flag_[index_]:
            processed_flag_[index_] = True
            base_cluster_.add(index_)
            # Returns id listof the points which are near the current point,
            # id and index would be the same because of the unpacking design followed in build_kdtree method.
            nearby_points = self.kdtree_main.search_elements(node=self.kdtree_root_node ,search_point=current_point_ ,
                                                             distance_threshold=threshold_ ,depth=0)
            # This line was added to retain the orginal variable during the process of recursion
            # Using the same variable resulted in changing the contents during iteration
            # which raised an exception.
            nearby_points_ = copy.copy(nearby_points)
            # If points are present search for more clusters
            if len(nearby_points_):
                for index_ in nearby_points_:
                    if not processed_flag_[index_]:
                        # Get the point in (x,y,z) for as required by the method
                        point = self.get_point(index_)
                        # Recursively iterate through all the points
                        self.find_clusters(point, base_cluster_, index_,
                                           threshold_, cluster_parameters_, processed_flag_)

    def visualize_clusters(self, clusters):
        """
        Visualization of point cloud data
        :param clusters: identified clusters
        :return:
        """
        trace_1 = go.Scatter3d(x=self.pcd_data.X,
                             y=self.pcd_data.Y,
                             z=self.pcd_data.Z,
                             mode='markers')
        # extract points from clusters
        cluster_points = pd.DataFrame(columns={"Cluster_id", "X", "Y", "Z"})
        for key in clusters:
            # Get all the indexes related to the cluster id = key
            cluster_point_indexes = clusters[key]
            for point_index in cluster_point_indexes:
                point = self.get_point(point_index)
                cluster_points = cluster_points.append({"Cluster_id": key,
                                                         "X": point[0],
                                                         "Y": point[1],
                                                         "Z": point[2]}, ignore_index=True)
        unique_clusters = []
        for cluster_id in cluster_points.Cluster_id.unique():
            cluster_traces = [go.Scatter3d(x=cluster_points[cluster_points["Cluster_id"] == cluster_id].X ,
                                   y=cluster_points[cluster_points["Cluster_id"] == cluster_id].Y ,
                                   z=cluster_points[cluster_points["Cluster_id"] == cluster_id].Z ,
                                   mode='markers')]
            unique_clusters.extend(cluster_traces)
        data = [trace_1]
        data.extend(unique_clusters)
        fig = go.Figure(data)
        fig.show()


if __name__ == "__main__":
    # APPLICATION = ProcessPointCloud(pcd_file="point_cloud_data_sample.xyz", nrows_value=100, display_output_flag=True)
    APPLICATION = ProcessPointCloud(pcd_file="point_cloud_data_sample_2.pcd" ,nrows_value=1000, display_output_flag=True)
    clusters = APPLICATION.euclidean_clustering(distance_threshold=5, cluster_parameters={"min_size":2})
    # print(clusters)
    APPLICATION.visualize_clusters(clusters)




