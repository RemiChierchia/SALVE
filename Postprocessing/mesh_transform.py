import glob
import open3d as o3d
import numpy as np
import os

# meshes = glob.glob("/Users/chi215/Desktop/for_leo/*/*.ply")
meshes = glob.glob("/Users/chi215/Desktop/wounds/PrecisionExps/Results/Logitech/PIS3/Split_03/Logitech_PIS3_scale010.ply")
# meshes = glob.glob("/Users/chi215/Desktop/wounds/results/SD/Logitech/vanilla/aabb2/scale008/Logitech_SD_50_aabb2_scale008.ply")
gt_sd = o3d.io.read_point_cloud("/Users/chi215/Desktop/Revopoint_GT/SD_2.ply")
gt_pis3 = o3d.io.read_point_cloud("/Users/chi215/Desktop/Revopoint_GT/PIS3_2.ply")
gt_pis4 = o3d.io.read_point_cloud("/Users/chi215/Desktop/Revopoint_GT/PIS4_2.ply")
for m in meshes:
# m=meshes
# print(meshes)
    file = m.split('/')[-1]
    camera = file.split('/')[0].split('_')[0]
    wound = file.split('.')[0].split('_')[1]
    scale = file.split('.')[0].split('_')[-1]
    # aabb = file.split('.')[0].split('_')[-2]

    print(file)
    if not 'aligned' in file:

        t = np.identity(4)
        t[:3,:3] = 1.0*np.eye(3)
        
        if wound == 'SD':# or wound == 'PIS4':
            t[:3,-1] = [-(157+51)/2.0 ,-(72+51)/2.0,  -0.0]
            gt = gt_sd
        elif wound == 'PIS3' or wound == 'PIS4':
            # import ipdb; ipdb.set_trace()
            t[:3,-1] = [-(134+51)/2.0 ,-(72+51)/2.0,  -0.0]
            if wound == 'PIS3':
                gt = gt_pis3
            else:
                gt = gt_pis4
        else:
            NameError("Wound Type Not Found!")
        
        scene_scale = float(str('0.'+scale[-3:]))
        print(scene_scale)
        mesh = o3d.io.read_triangle_mesh(m)
        mesh.vertices = o3d.utility.Vector3dVector(np.asarray(mesh.vertices) * (1/scene_scale))
        # mesh.vertices = o3d.utility.Vector3dVector(vertices[:,:3])
        mesh.transform(np.linalg.inv(t))
        # import ipdb; ipdb.set_trace()
        o3d.visualization.draw_geometries([gt, mesh])
        name_path = os.path.join(os.path.dirname(m), camera+'_'+wound+'_aligned.ply')
        try:
            o3d.io.write_triangle_mesh(name_path, mesh)
        except:
            print("Failed to save the transformed mesh!")
