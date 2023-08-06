import sys
sys.path.append('../segment_lidar')

import samlidar

model = samlidar.SamLidar(ckpt_path="sam_vit_h_4b8939.pth", algorithm="segment-anything", device="cpu")
points = model.read("pointcloud.las")
labels, *_ = model.segment(points=points, image_path="raster.tif", labels_path="labeled.tif")
model.write(points=points, segment_ids=labels, save_path="segmented.las")