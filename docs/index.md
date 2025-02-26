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

## Introduction & Motivation
<b>Chronic wounds</b> represent a significant <b>health</b> and <b>economic</b> <b>burden</b> worldwide. Effective treatments <b>require</b> wound clinical <b>measurements</b>, typically <b>performed manually</b> by specialized healthcare professionals.

Wound surface area is typically measured by performing <b>planimetry</b> of the wound bed. These procedures are not only <b>invasive</b> and cause patient <b>discomfort</b> but are also prone to errors due to <b>ambiguous</b> definitions of metrics and variations in professionals’ skill levels.
<!-- Put image -->

Most <b>existing</b> automatic commercial <b>approaches</b> compute wound measurements solely from <b>2D images</b>, which are perspective-dependent.
<!-- put image -->

<b>3D analysis</b> of wounds allows for the computation of <b>richer wound biomarkers</b>. However, studies in this direction only considered previous generation 3D reconstruction frameworks, which have recently been surpassed by highly optimized photogrammetric toolboxes and recent neural rendering alternatives, we are talking about <b>NeRF</b> and <b>Gaussian Splatting</b>!
<!-- put image? -->

<b>We introduce</b> a new dataset <b>SALVE</b>, designed to capture common challenges encountered in clinical settings. 
<!-- put image -->

## Evaluation
<b>We evaluate</b> robust <b>photogrammetry pipelines</b> such as COLMAP and Meshroom and <b>modern neural rendering approaches for 3D reconstruction</b> such as <b>NeRF</b> and <b>Gaussian Splatting</b>. 
<!-- put image -->

We follow a <b>rigorous evaluation protocol</b> that defines metrics and procedures to assess the <b>geometric accuracy and precision</b> of the evaluated reconstruction algorithms.
<!-- put image -->


<!-- Page under developmet! -->






<!-- commented below> -->

<!-- <br/>

If you find this work useful, please cite
```
@article{leb at2023syn3dwound,
  title={Syn3DWound: A Synthetic Dataset for 3D Wound Bed Analysis},
  author={Lebrat, L{\'e}o and Cruz, Rodrigo Santa and Chierchia, Remi and Arzhaeva, Yulia and Armin, Mohammad Ali and Goldsmith, Joshua and Oorloff, Jeremy and Reddy, Prithvi and Nguyen, Chuong and Petersson, Lars and others},
  journal={arXiv preprint arXiv:2311.15836},
  year={2023}
}
``` -->


## Acknowledgment 
This work was supported by
the MRFF Rapid Applied Research Translation grant
(RARUR000158), CSIRO [AI 4 Missions](https://research.csiro.au/ai4m/ai-is-helping-to-transform-wound-care/) Minimising Antimicrobial Resistance Mission, and Australian Government
Training Research Program (AGRTP) Scholarship.
