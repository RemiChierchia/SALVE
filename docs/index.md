---
layout: single
author_profile: True
classes: wide
excerpt: "A 3D Reconstruction Benchmark of Wounds from Consumer-grade Videos<br/>WACV 2025"
header:
  overlay_image: /assets/images/main.png
  overlay_filter: 0.5
  caption: "Qualitative evaluation of six 3D surface reconstruction methods using our SALVE dataset."
  actions:
    - label: "Paper (arXiv preprint)"
      url: "https://arxiv.org/abs/2407.19652"
    # - label: "Code"
    #   url: "https://github.com/lebrat/Syn3DWound"
    # - label: "Dataset"
    #   url: "https://data.csiro.au/collection/csiro:61849"
# gallery_pipepline:
#   - url: /assets/images/explaination_pipeline.png
#     image_path: /assets/images/explaination_pipeline.png
#     alt: "From a 3D mesh avatar and segmented wound, Syn3DWound allows to generate a synthetic dataset for 3D wound bed analysis."
#     title: "From a 3D mesh avatar and segmented wound, Syn3DWound allows to generate a synthetic dataset for 3D wound bed analysis."
# gallery_airplane:
#   - url: /assets/images/avion_mongenet.png
#     image_path: /assets/images/avion_mongenet.png
#     alt: "MongeNet mesh discretization by a point cloud"
#     title: "MongeNet mesh discretization by a point cloud"
#   - url: /assets/images/avion_uniform.png
#     image_path: /assets/images/avion_uniform.png
#     alt: "Standard random uniform mesh discretization by a point cloud"
#     title: "Standard random uniform mesh discretization by a point cloud"
paginate: true 
---

Page under developmet!

Chronic wounds represent a significant health and economic burden worldwide. Effective wound treatments depend on multiple wound clinical measurements, typically performed manually by specialized healthcare professionals.
Wound surface area is typically measured by performing planimetry of the wound bed. These procedures are not only invasive and cause patient discomfort but are also prone to errors due to ambiguous definitions of metrics and variations in professionals’ skill levels.
Most existing automatic commercial approaches compute wound measurements solely from 2D images, which are perspective-dependent.
3D analysis of wounds allows for the computation of richer wound biomarkers. However, studies in this direction only considered previous generation 3D reconstruction frameworks, which have recently been surpassed by highly optimized photogrammetric toolboxes and recent neural rendering alternatives, we are talking about NeRF and Gaussian Splatting!

We introduce a new dataset SALVE, designed to capture common challenges encountered in clinical settings. We evaluate robust photogrammetry pipelines such as COLMAP and Meshroom and modern neural rendering approaches for 3D reconstruction such as NeRF and Gaussian Splatting. We follow a rigorous evaluation protocol that defines metrics and procedures to assess the geometric accuracy and precision of the evaluated reconstruction algorithms.

<!--
{% include gallery id="gallery_pipepline" caption="From a real wound and a 3D avatar Syn3DWound generate realistic synthetic images, segmentation mask and wound bed  geometry." %} -->



## Evaluation


<!-- commented below>

<!-- <br/>

If you find this work useful, please cite
```
@article{lebrat2023syn3dwound,
  title={Syn3DWound: A Synthetic Dataset for 3D Wound Bed Analysis},
  author={Lebrat, L{\'e}o and Cruz, Rodrigo Santa and Chierchia, Remi and Arzhaeva, Yulia and Armin, Mohammad Ali and Goldsmith, Joshua and Oorloff, Jeremy and Reddy, Prithvi and Nguyen, Chuong and Petersson, Lars and others},
  journal={arXiv preprint arXiv:2311.15836},
  year={2023}
}
``` -->


## Acknowledgment 
This research was supported by [AI 4 Missions](https://research.csiro.au/ai4m/ai-is-helping-to-transform-wound-care/)
