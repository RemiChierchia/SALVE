import open3d as o3d
import numpy as np
import glob
import pandas as pd
import ot
import time
import copy
import os

from tqdm import tqdm
from joblib import Parallel, delayed


N_JOBS = 32

os.environ['OMP_NUM_THREADS'] = str(N_JOBS)


def compute_metric_col(j,T,x,y,y_normals,x_normals):
    weights = T[:,j]
    weight = weights.sum()

    y_point = y[j]
    y_normal = y_normals[j]
    x_mask = T[:,j]>0
    x_points = x[x_mask]
    x_normals = x_normals[x_mask]
    x_weight = T[x_mask,j]
    dists = np.linalg.norm(x_points-y_point,axis=1)
    D_eucledian = (dists*x_weight).sum()

    normals_dot = np.dot(x_normals,y_normal)
    D_normals = (normals_dot*x_weight).sum()

    return D_eucledian, D_normals


if __name__ == '__main__':

    # import argparse
    # import copy
    # argparser = argparse.ArgumentParser(description='Select wound mesh')
    # argparser.add_argument('--method', type=str, required=True)
    # argparser.add_argument('--wound', type=str, required=True)
    # args = argparser.parse_args()
    # method_folder = args.method
    # wound = args.wound
    wounds = ['PIS3','SD','PIS4']
    for w in wounds:
    
        df_results = pd.DataFrame(columns=['Wound', 'Reconstruction', 'Reference', 'EMD', 'Normal'])
        
        all_meshes = glob.glob(f'{w}/sampled/*.ply')
        
        gt_pc_path = f'sampled_gts/{w}_2_sampled.ply'
        gt_pc = o3d.io.read_point_cloud(gt_pc_path)
        
        for pred_path in all_meshes:
        
            # reference_mesh_path = f'manually_aligned/{w}/01_MR_iphone_crop.ply'
            # gt = o3d.io.read_point_cloud(gt_path)

            # import ipdb; ipdb.set_trace()
            # all_mesh_sfm = []
            # all_mesh_sfm = copy.deepcopy(all_meshes)
            # all_mesh_sfm.remove(gt_path)
            

            # for pred_path in tqdm(all_mesh_sfm, desc='measuring error', total=len(all_mesh_sfm)):

            # all of the meshes should be downsampled to roughly 20~30k points (with normals) 
            pred = o3d.io.read_point_cloud(pred_path)

            gt_points = np.asarray(gt_pc.points)
            pred_points = np.asarray(pred.points)
            x = gt_points
            y = pred_points
            a = np.ones(x.shape[0])/x.shape[0]
            b = np.ones(y.shape[0])/y.shape[0]
            M = ot.dist(x, y)
            t = time.time()
            T = ot.emd(a, b, M,numItermax=5_000_000)#,numThreads=32)
            print('solving OT for {} points took: {} (GT {})'.format(y.shape[0]//1_000, time.time()-t,x.shape[0]//1_000))
            name_numpy = pred_path.replace('.ply','_T.npy')
            np.save(name_numpy,T)
            print('saved: {}'.format(name_numpy))


            # here we can plug directly the computation of the over code
            # if you don't want to have to run the second part
            # Saving T is was quite important as I was able to verify that the OT has ran
            # properly
            x_normals = np.asarray(gt_pc.normals)
            y_normals = np.asarray(pred.normals)
            T = np.load(name_numpy)
            
            # compute all of the EMD distances and EMD normals
            
            # import ipdb; ipdb.set_trace()
            distance, nc = zip(*Parallel(n_jobs=N_JOBS)(delayed(compute_metric_col)(j,T,x,y,y_normals,x_normals) for j in tqdm(range(T.shape[1]), desc='Computing metrics',total=T.shape[1])))
            emd = np.array(distance).sum()
            normal = np.array(nc).sum()
            

            method = name_numpy.replace('.npy','').split('/')[-1]
            ref_method = gt_pc_path.replace('.ply','').split('/')[-1]
            
            if len(df_results) > 0:
                df_results = pd.concat([df_results, pd.DataFrame([[w, method, ref_method, emd, normal]], columns=['Wound', 'Reconstruction', 'Reference', 'EMD', 'Normal'])])
            else:
                df_results = pd.DataFrame([[w, method, ref_method, emd, normal]], columns=['Wound', 'Reconstruction', 'Reference', 'EMD', 'Normal'])

        df_results.to_csv(f'{w}/sampled/EMD_normal_DS50_sugar.csv')