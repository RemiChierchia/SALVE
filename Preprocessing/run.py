import json
import math

import cv2
from read_write_colmap_model import read_model, write_model, qvec2rotmat, rotmat2qvec, Point3D, Image
import numpy as np
import tqdm, os

# input files
input_colmap = "/Users/chi215/Desktop/WACV_2025/precision_to_fix_for_nangelo/precision/Split_01/sparse/"
input_transform = "/Users/chi215/Desktop/wounds/transformations/Logitech/50/SD/transform4x4.txt"
undistorted_images_dir = "/Users/chi215/Desktop/WACV_2025/precision_to_fix_for_nangelo/precision/Split_01/images/"
layout = 'large' # large (SD) or small (PIS3, PIS4)
output_dir = "/Users/chi215/Desktop/WACV_2025/precision_to_fix_for_nangelo/precision/Split_01/new"

# read model and transform
cameras_CM, images_CM, points_CM = read_model(input_colmap)
trasnform_matrix = np.loadtxt(input_transform).reshape(4,4).astype(np.float64)

# transformation to center and rescale
new_transform = np.identity(4); 
new_transform[:3,:3] = 1.0*np.eye(3); 
new_transform[:3,-1] = {'large': [-(157+51)/2.0 ,-(72+51)/2.0,  -0.0],
                        'small': [-(134+51)/2.0 ,-(72+51)/2.0,  -0.0],}[layout]
# import ipdb; ipdb.set_trace()
trasnform_matrix = new_transform @ trasnform_matrix

# apply transform to poses
newImagesCM = {}
for id in tqdm.tqdm(images_CM, desc='processing images struct'):
    image_struct = images_CM[id]
    R, t = qvec2rotmat(image_struct.qvec).reshape(3,3), image_struct.tvec.reshape(3,1)
    RT = np.row_stack([np.column_stack([R,t]), [0, 0, 0, 1]])
    RT = RT @ np.linalg.inv(trasnform_matrix); RT *= np.linalg.norm(trasnform_matrix[0, :3]);
    new_qvec = rotmat2qvec(RT[:3, :3]); new_tvec = RT[:3, -1];
    newImagesCM[id] = Image(id=id, qvec=new_qvec, tvec=new_tvec, camera_id=image_struct.camera_id, name=image_struct.name, xys=image_struct.xys, point3D_ids=image_struct.point3D_ids)
    
# apply to points
# import ipdb; ipdb.set_trace()
newPointsCM = {}
for id in tqdm.tqdm(points_CM, desc='processing points struct'):
    points_struct = points_CM[id]
    new_xyz = (trasnform_matrix @ np.concatenate([points_struct.xyz, [1.0]]).reshape(-1,1)).ravel()[:-1]
    newPointsCM[id] = Point3D(id=id, xyz=new_xyz, rgb=points_struct.rgb, error=points_struct.error, 
                              image_ids=points_struct.image_ids, point2D_idxs=points_struct.point2D_idxs)
        

# convert to sdfstudio
print("Converting colmap camera intrinsics to transforms.json")
transforms_dict = None; single_camera_id = None;
for camera_id in cameras_CM:
    if transforms_dict is None:
        single_camera_id = camera_id		 
        camera_model, width, height, params = cameras_CM[camera_id].model, cameras_CM[camera_id].width, cameras_CM[camera_id].height, cameras_CM[camera_id].params

        if  camera_model == 'SIMPLE_PINHOLE':
            transforms_dict = {
                "w": float(width), "h": float(height), "fl_x": float(params[0]), "fl_y": float(params[0]), "cx": float(params[1]), "cy": float(params[2]),
                "camera_angle_x": math.atan(float(width) / (float(params[0]) * 2)) * 2, "camera_angle_y": math.atan(float(height) / (float(params[0]) * 2)) * 2,
                "aabb_scale": 1, "k1": 0.0, "k2": 0.0, "p1": 0.0, "p2": 0.0, "frames": []
            }
        elif camera_model == 'PINHOLE':					
            transforms_dict = {
                "w": float(width), "h": float(height), "fl_x": float(params[0]), "fl_y": float(params[1]), "cx": float(params[2]), "cy": float(params[3]),
                "camera_angle_x": math.atan(float(width) / (float(params[0]) * 2)) * 2, "camera_angle_y": math.atan(float(height) / (float(params[1]) * 2)) * 2, 
                "aabb_scale": 1, "k1": 0.0, "k2": 0.0, "p1": 0.0, "p2": 0.0, "frames": []
            }		
        elif camera_model == 'OPENCV':	
            transforms_dict = {
                "w": float(width), "h": float(height), "fl_x": float(params[0]), "fl_y": float(params[1]), "cx": float(params[2]), "cy": float(params[3]),
                "camera_angle_x": math.atan(float(width) / (float(params[0]) * 2)) * 2, "camera_angle_y": math.atan(float(height) / (float(params[1]) * 2)) * 2, 
                "aabb_scale": 1, "k1": float(params[4]), "k2": float(params[5]), "p1": float(params[6]), "p2": float(params[7]), "frames": []
            }				
        else:
            raise ValueError(f"camera model {camera_model} is not implemented")
    else:
        raise ValueError("Just support single camera reconstruction")			
print(f"camera: {transforms_dict}")	

print("Converting colmap camera poses to transforms.json")
sfm_points = []
for image_id in tqdm.tqdm(newImagesCM, desc='Reading image poses'):

    qvec = newImagesCM[image_id].qvec; tvec = newImagesCM[image_id].tvec
    R = qvec2rotmat(-qvec); t = tvec.reshape([3,1]);
    image_file_path = os.path.join(undistorted_images_dir, newImagesCM[image_id].name);
    assert newImagesCM[image_id].camera_id == single_camera_id				

    # compute sharpness
    image = cv2.imread(image_file_path); 
    sharpness = cv2.Laplacian(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()
    
    # compose pose
    c2w = np.linalg.inv(np.row_stack([np.column_stack([R, t]), [.0, .0, .0, 1.]]))		
    c2w[0:3,2] *= -1; c2w[0:3,1] *= -1; # flip the y and z axis
    # c2w = c2w[[1,0,2,3],:] # swap y and z
    #c2w[2,:] *= -1 # flip whole world upside down
    
    transforms_dict['frames'].append({"file_path": os.path.join('images', os.path.basename(image_file_path)), "sharpness": sharpness, "transform_matrix": c2w.tolist()})
    
    pcl = []
    for point3D_id in newImagesCM[image_id].point3D_ids:
        if point3D_id >= 0:
            pcl.append(newPointsCM[point3D_id].xyz)
    pcl = np.stack(pcl).reshape(-1, 3).astype(np.float32); #pcl = pcl[:, [1,0,2]]; #pcl[:, 2] *= -1;	
    sfm_points.append(pcl)

# saving results
print(f"saving output to {output_dir}")
os.makedirs(output_dir, exist_ok=True)
# saving colmap
os.makedirs(os.path.join(output_dir, 'colmap_aligned'), exist_ok=True)
write_model(cameras_CM, newImagesCM, newPointsCM, path=os.path.join(output_dir, 'colmap_aligned'), ext='.txt')
# saving transform json
transforms_file = os.path.join(output_dir, 'transforms.json')
with open(transforms_file, "w") as jsonFile:
		json.dump(transforms_dict, jsonFile, indent=2)

# save saprse points
sfm_out_dir = os.path.join(output_dir, 'sfm_points')
os.makedirs(sfm_out_dir, exist_ok=True)
for pcl_idx, pcl in enumerate(sfm_points):
	file_name = os.path.basename(transforms_dict['frames'][pcl_idx]['file_path'])
	file_name = file_name.split('.')[0] + '.txt'
	np.savetxt(os.path.join(sfm_out_dir,file_name), pcl)

print("DONE")