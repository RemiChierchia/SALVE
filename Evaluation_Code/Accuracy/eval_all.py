import glob
import open3d as o3d
import numpy as np
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
from joblib import Parallel, delayed
from scipy.spatial import KDTree
import pandas as pd
from tqdm import tqdm

axes = [0,1]
N_JOBS = 16

def mesh_gt_alignment(sample_mesh_pcd, gt_crop):
    # Align mesh reconstruction crop with GT crop pointcloud

    source, target = o3d.geometry.PointCloud(), o3d.geometry.PointCloud()
    source.points = o3d.utility.Vector3dVector(sample_mesh_pcd.points)
    target.points = o3d.utility.Vector3dVector(gt_crop.points)
    threshold = 0.95
    trans_init = np.eye(4)
    source.transform(trans_init)

    
    reg_p2p = o3d.pipelines.registration.registration_icp(
        source,
        target,
        threshold,
        trans_init,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(),
    )    

    
    return reg_p2p

def compute_polygon_intersection_pc(pc,polygon):
    pc_points = np.array(pc.points)
    point = pc_points[:,axes]

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


def compute_metrics(prediction, gt):
    gt_pc = np.asarray(gt.points)
    gt_normals = np.asarray(gt.normals)

    
    pred_pc = np.asarray(prediction.points)
    pred_normals = np.asarray(prediction.normals)

    # compute error
    metrics = {}

    tree_p2g = KDTree(gt_pc)
    knn_p2g_dists, knn_p2g_ids = tree_p2g.query(pred_pc, k=1, workers=-1)

    tree_g2p = KDTree(pred_pc)
    knn_g2p_dists, knn_g2p_ids = tree_g2p.query(gt_pc, k=1, workers=-1)

    # Compute metrics
    
    metrics['AD'] = 0.5*(knn_p2g_dists.mean() + knn_g2p_dists.mean())
    metrics['HAUSDORFF'] = np.stack([knn_p2g_dists.max(), knn_g2p_dists.max()]).max()
    metrics['HAUSDORFF_90'] = np.stack([np.quantile(knn_p2g_dists, 0.9), np.quantile(knn_g2p_dists, 0.9)]).max()
    metrics['HAUSDORFF_95'] = np.stack([np.quantile(knn_p2g_dists, 0.95), np.quantile(knn_g2p_dists, 0.95)]).max()
    gt_noramls_near_pred = gt_normals[knn_p2g_ids]
    pred_to_gt_dot = np.abs((pred_normals * gt_noramls_near_pred).sum(axis=-1)).mean()
    pred_normals_near_gt = pred_normals[knn_g2p_ids]
    gt_to_pred_dot = np.abs((gt_normals * pred_normals_near_gt).sum(axis=-1)).mean()
    metrics['NORMAL_CONSISTENCY'] = 0.5 * (pred_to_gt_dot + gt_to_pred_dot)

    results_df = pd.DataFrame(metrics, index=[0])

    return results_df

total_metrics = pd.DataFrame()

wounds = ['PIS3','SD','PIS4']
for w in wounds:
    
    NB_POINTS_SAMPLED = 2_000_000
    gt_pc_path = f'/scratch3/chi215/sfm_metrics_evaluation/Revopoint_GT/{w}_2.ply'
    gt_pc = o3d.io.read_point_cloud(gt_pc_path)

    all_mesh_sfm = []
    
    all_mesh_sfm += glob.glob(f'{w}/*.ply')


    points = np.loadtxt(f'{w}/PolyLine_Large.txt')
    poly_large = points

    sampled_points_GT = compute_polygon_intersection_pc(gt_pc,poly_large)
    # aligned sfm to source mesh

    

    for sfm_mesh_path in tqdm(all_mesh_sfm, desc='measuring error', total=len(all_mesh_sfm)):
        mesh_recon = o3d.io.read_triangle_mesh(sfm_mesh_path)
        
        sampled_points_sfm = mesh_recon.sample_points_uniformly(number_of_points=NB_POINTS_SAMPLED, use_triangle_normal=True)
        sampled_points_sfm = compute_polygon_intersection_pc(sampled_points_sfm,poly_large)
        
        
        metrics = compute_metrics(sampled_points_sfm, sampled_points_GT)
        metrics['Method'] = sfm_mesh_path.split('/')[-1].split('.')[0].split('_')[0]
        metrics['Camera'] = sfm_mesh_path.split('/')[-1].split('.')[0].split('_')[1].lower()
        metrics['Wound'] = w

        if len(total_metrics) == 0:
            total_metrics = metrics
        else:
            total_metrics = pd.concat([total_metrics, metrics], axis=0)
        
        total_metrics.to_csv('metrics_all.csv')






