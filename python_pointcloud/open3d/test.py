import numpy as np

import trimesh

# points = np.random.random((100, 3))

# cloud = trimesh.PointCloud(points)
cloudXYZ = np.loadtxt("../data/pz.txt")
cloud = trimesh.PointCloud(cloudXYZ)

# print(cloud.convex_hull)
scene = trimesh.Scene([cloud.convex_hull])
scene.show()
