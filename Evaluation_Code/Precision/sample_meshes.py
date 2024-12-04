import argparse
import numpy as np
import open3d as o3d
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from joblib import Parallel, delayed
from scipy.spatial import KDTree
import pandas as pd
import os
import logging
import time
import sys
import glob
import trimesh
import tqdm
N_JOBS = 16

os.environ['OMP_NUM_THREADS'] = str(N_JOBS)


def submesh(verts, faces, verts_sel, sel_type="any"):
    # selection type: keep a face if or if at least one vertice is selected
    verts = np.array(verts)
    faces = np.array(faces)
    verts_sel = np.array(verts_sel)
    faces_sel = verts_sel[faces]
    if sel_type == "all":
        faces_sel = np.all(faces_sel, axis=1)
    elif sel_type == "any":
        faces_sel = np.any(faces_sel, axis=1)
    else:
        print("{sel_type} is not supported")
        sys.exit(1)

    crop = o3d.geometry.TriangleMesh(o3d.utility.Vector3dVector(verts), o3d.utility.Vector3iVector(faces))
    triangles_to_remove = np.where(faces_sel==False)[0]
    crop.remove_triangles_by_index(triangles_to_remove)

    return crop

def compute_polygon_intersection_pc(pc,polygon):
    pc_points = np.array(pc.points)
    point = pc_points[:,0:2]

    pol = Polygon(polygon)
    def task(i):
        try:
            p = Point(point[i,:2])
            ret = pol.contains(p)
        except:
            ret = False
        return ret
    results = Parallel(n_jobs=N_JOBS)(delayed(task)(i) for i in range(len(point)))
    mask = np.array(results)

    pc_crop = pc.select_by_index(np.where(mask==True)[0])

    return pc_crop



def compute_polygon_intersection_mesh(mesh,polygon):
    mesh_temp_vert = np.array(mesh.vertices)
    mesh_temp_faces = np.array(mesh.triangles)
    point = mesh_temp_vert[:,0:2]

    pol = Polygon(polygon)
    def task(i):
        try:
            p = Point(point[i,:2])
            ret = pol.contains(p)
        except:
            ret = False
        return ret
    results = Parallel(n_jobs=N_JOBS)(delayed(task)(i) for i in range(len(point)))

    mask = np.array(results)
    mesh_crop = submesh(mesh_temp_vert, mesh_temp_faces, mask)

    return mesh_crop


if __name__ == '__main__':
    
    # wounds = ['PIS3','SD','PIS4']
    wounds = ['SD']
    for w in tqdm.tqdm(wounds):
        
        meshes = glob.glob(f'{w}/*_translated.ply')
        # meshes = glob.glob(f'Neusfacto/{w}/*.ply')
        poly = np.loadtxt(f'{w}/PolyLine_Large.txt')
        # poly = np.loadtxt(f'Neusfacto/{w}/PolyLine_Large.txt')
        
        save_dir = os.path.join(os.path.dirname(meshes[0]), 'sampled')
        os.makedirs(save_dir, exist_ok=True)
        
        for mesh in tqdm.tqdm(meshes):
            
            if 'pc.ply' not in os.path.basename(mesh).split('_'):
                mesh_o3d = o3d.io.read_triangle_mesh(mesh)
                # import ipdb; ipdb.set_trace()
                mesh_o3d_poly = compute_polygon_intersection_mesh(mesh_o3d, poly)
                if not mesh_o3d_poly.has_vertex_normals():
                    mesh_o3d_poly.compute_vertex_normals()
                
                # sampled = mesh_o3d_poly.sample_points_uniformly(number_of_points=30_000)
            
                mesh_tri_poly = trimesh.Trimesh(vertices=mesh_o3d_poly.vertices, faces=mesh_o3d_poly.triangles, vertex_normals=mesh_o3d_poly.vertex_normals)
                samples,indices = trimesh.sample.sample_surface_even(mesh_tri_poly, 30_000)

                sampled = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(samples))
                sampled.normals = o3d.utility.Vector3dVector(mesh_tri_poly.face_normals[indices])
                
                refined = compute_polygon_intersection_pc(sampled, poly)
                
                # o3d.visualization.draw_geometries([refined])
                save_name = os.path.basename(mesh).split('.')[0] + '_sampled.ply'
                o3d.io.write_point_cloud(os.path.join(save_dir, save_name), refined)