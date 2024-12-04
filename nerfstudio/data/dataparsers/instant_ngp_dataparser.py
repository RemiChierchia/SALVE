# Copyright 2022 The Nerfstudio Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Data parser for instant ngp data"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Tuple, Type

import numpy as np
import torch
from rich.console import Console
from PIL import Image

from nerfstudio.cameras import camera_utils
from nerfstudio.cameras.cameras import Cameras, CameraType
from nerfstudio.data.dataparsers.base_dataparser import (
    DataParser,
    DataParserConfig,
    DataparserOutputs,
)
from nerfstudio.data.scene_box import SceneBox
from nerfstudio.utils.images import BasicImages
from nerfstudio.utils.io import load_from_json

CONSOLE = Console(width=120)

def get_sampling_masks(image_idx: int, sampling_masks):
    """function to process additional foreground_masks

    Args:
        image_idx: specific image index to work with
        fg_masks: foreground_masks
    """

    # sensor depth
    sampling_masks = sampling_masks[image_idx]

    return {"sampling_masks": sampling_masks}


def get_foreground_masks(image_idx: int, fg_masks):
    """function to process additional foreground_masks

    Args:
        image_idx: specific image index to work with
        fg_masks: foreground_masks
    """

    # sensor depth
    fg_mask = fg_masks[image_idx]

    return {"fg_mask": fg_mask}


def get_sparse_sfm_points(image_idx: int, sfm_points):
    """function to process additional sparse sfm points

    Args:
        image_idx: specific image index to work with
        sfm_points: sparse sfm points
    """

    # sfm points
    sparse_sfm_points = sfm_points[image_idx]
    sparse_sfm_points = BasicImages([sparse_sfm_points])
    return {"sparse_sfm_points": sparse_sfm_points}


@dataclass
class InstantNGPDataParserConfig(DataParserConfig):
    """Instant-NGP dataset parser config"""

    _target: Type = field(default_factory=lambda: InstantNGP)
    """target class to instantiate"""
    data: Path = Path("data/ours/posterv2")
    """Directory specifying location of data."""
    scale_factor: float = 1.0
    """How much to scale the camera origins by."""
    scene_scale: float = 0.33
    """How much to scale the scene."""
    include_foreground_mask: bool = False
    """whether or not to load foreground mask""" 
    include_sampling_mask: bool = False
    """whether or not to load pixel sampling mask"""        
    include_sfm_points: bool = False
    """whether or not to load sfm points"""


@dataclass
class InstantNGP(DataParser):
    """Instant NGP Dataset"""

    config: InstantNGPDataParserConfig

    def _generate_dataparser_outputs(self, split="train"):

        # If self.config.data is queried only here, I can add here the check for split='val'
        config_data = self.config.data
        
        # import pandas as pd
        # import os
        # if os.path.exists(config_data / "split_data.txt"):
        #     split_data = pd.read_csv(config_data / "split_data.txt", sep=';')
        
        # if split==str("val"):
        #     data_ids = np.array(split_data['ImageId'][split_data['Split'] == 1])
        # elif split==str("train"):
        #     data_ids = np.array(split_data['ImageId'][split_data['Split'] == 0])
        
        meta = load_from_json(config_data / "transforms.json")
        image_filenames = []
        sfm_points, foreground_mask_images, sampling_mask_images = [], [], []
        poses = []
        num_skipped_image_filenames = 0
        for frame in meta["frames"]:
            # if frame['file_path'].split("/")[-1] in data_ids:
            fname = config_data / Path(frame["file_path"])
            if not fname:
                num_skipped_image_filenames += 1
            else:
                image_filenames.append(fname)
                poses.append(np.array(frame["transform_matrix"]))        

                mname =  config_data / Path('masks') / fname.name;
                if self.config.include_foreground_mask:                    
                    foreground_mask = np.array(Image.open(mname), dtype="uint8")
                    foreground_mask = foreground_mask[:,:,None]
                    foreground_mask_images.append(torch.from_numpy(foreground_mask).float() / 255.0)


                spname = config_data / Path('sfm_points') / (fname.name.split('.')[0] + '.txt');
                if self.config.include_sfm_points:                
                    # load sparse sfm points
                    sfm_points_view = np.loadtxt(spname)
                    sfm_points_view *= self.config.scene_scale
                    sfm_points.append(torch.from_numpy(sfm_points_view).float())

                
                mname =  config_data / Path('sampling_weights') / fname.name.replace('.jpg', '.npy');
                if self.config.include_sampling_mask:                    
                    sampling_mask = np.load(mname).astype(np.float32)
                    sampling_mask = sampling_mask[:,:,None]
                    sampling_mask_images.append(torch.from_numpy(sampling_mask).float())



        if num_skipped_image_filenames >= 0:
            CONSOLE.print(f"Skipping {num_skipped_image_filenames} files in dataset split {split}.")
        assert (
            len(image_filenames) != 0
        ), """
        No image files found. 
        You should check the file_paths in the transforms.json file to make sure they are correct.
        """
        poses = np.array(poses).astype(np.float32)
        poses[:, :3, 3] *= self.config.scene_scale        

        camera_to_world = torch.from_numpy(poses[:, :3])  # camera to world transform

        distortion_params = camera_utils.get_distortion_params(
            k1=float(meta["k1"]), k2=float(meta["k2"]), p1=float(meta["p1"]), p2=float(meta["p2"])
        )

        # in x,y,z order
        # assumes that the scene is centered at the origin
        aabb_scale = meta["aabb_scale"]
        scene_box = SceneBox(
            aabb=torch.tensor(
                [[-aabb_scale, -aabb_scale, -aabb_scale], [aabb_scale, aabb_scale, aabb_scale]], dtype=torch.float32
            )
        )

        fl_x, fl_y = InstantNGP.get_focal_lengths(meta)        

        cameras = Cameras(
            fx=float(fl_x),
            fy=float(fl_y),
            cx=float(meta["cx"]),
            cy=float(meta["cy"]),
            distortion_params=distortion_params,
            height=int(meta["h"]),
            width=int(meta["w"]),
            camera_to_worlds=camera_to_world,
            camera_type=CameraType.PERSPECTIVE,
        )

        additional_inputs_dict = {}
        if self.config.include_foreground_mask:            
            additional_inputs_dict["foreground_masks"] = {
                "func": get_foreground_masks,
                "kwargs": {"fg_masks": foreground_mask_images},
            }
            
        if self.config.include_sampling_mask:            
            additional_inputs_dict["sampling_masks"] = {
                "func": get_sampling_masks,
                "kwargs": {"sampling_masks": sampling_mask_images},
            }
            

        if self.config.include_sfm_points:
            additional_inputs_dict["sfm_points"] = {
                "func": get_sparse_sfm_points,
                "kwargs": {"sfm_points": sfm_points},
            }

        # TODO(ethan): add alpha background color
        dataparser_outputs = DataparserOutputs(
            image_filenames=image_filenames,            
            cameras=cameras,
            scene_box=scene_box,
            additional_inputs=additional_inputs_dict,
        )

        return dataparser_outputs

    @classmethod
    def get_focal_lengths(cls, meta: Dict) -> Tuple[float, float]:
        """Reads or computes the focal length from transforms dict.
        Args:
            meta: metadata from transforms.json file.
        Returns:
            Focal lengths in the x and y directions. Error is raised if these cannot be calculated.
        """
        fl_x, fl_y = 0, 0

        def fov_to_focal_length(rad, res):
            return 0.5 * res / np.tan(0.5 * rad)

        if "fl_x" in meta:
            fl_x = meta["fl_x"]
        elif "x_fov" in meta:
            fl_x = fov_to_focal_length(np.deg2rad(meta["x_fov"]), meta["w"])
        elif "camera_angle_x" in meta:
            fl_x = fov_to_focal_length(meta["camera_angle_x"], meta["w"])

        if "fl_y" in meta:
            fl_y = meta["fl_y"]
        elif "y_fov" in meta:
            fl_y = fov_to_focal_length(np.deg2rad(meta["y_fov"]), meta["h"])
        elif "camera_angle_y" in meta:
            fl_y = fov_to_focal_length(meta["camera_angle_y"], meta["h"])

        if fl_x == 0 or fl_y == 0:
            raise AttributeError("Focal length cannot be calculated from transforms.json (missing fields).")

        return (fl_x, fl_y)



