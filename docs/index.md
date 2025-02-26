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

<br>Chronic wounds<br/> represent a significant <br>health<br/> and <br>economic<br/> <br>burden<br/> worldwide. Effective treatments <br>require<br/> wound clinical <br>measurements<br/>, typically <br>performed manually<br/> by specialized healthcare professionals.

Wound surface area is typically measured by performing <br>planimetry<br/> of the wound bed. These procedures are not only <br>invasive<br/> and cause patient <br>discomfort<br/> but are also prone to errors due to <br>ambiguous<br/> definitions of metrics and variations in professionals’ skill levels.
<!-- Put image -->

Most <br>existing<br/> automatic commercial <br>approaches<br/> compute wound measurements solely from <br>2D images<br/>, which are perspective-dependent.
<!-- put image -->

<br>3D analysis<br/> of wounds allows for the computation of <br>richer wound biomarkers<br/>. However, studies in this direction only considered previous generation 3D reconstruction frameworks, which have recently been surpassed by highly optimized photogrammetric toolboxes and recent neural rendering alternatives, we are talking about <br>NeRF<br/> and <br>Gaussian Splatting<br/>!
<!-- put image? -->

<br>We introduce<br/> a new dataset <br>SALVE<br/>, designed to capture common challenges encountered in clinical settings. 
<!-- put image -->

<br>We evaluate<br/> robust <br>photogrammetry pipelines<br/> such as COLMAP and Meshroom and <br>modern neural rendering approaches for 3D reconstruction<br/> such as <br>NeRF<br/> and <br>Gaussian Splatting<br/>. 
<!-- put image -->

We follow a <br>rigorous evaluation protocol<br/> that defines metrics and procedures to assess the <br>geometric accuracy and precision<br/> of the evaluated reconstruction algorithms.
<!-- put image -->


<!-- Page under developmet! -->




## Evaluation


commented below>

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
