import subprocess, glob, sys, os, shutil, yaml, tqdm
from pathlib import Path

config_file = sys.argv[1]
print(f"{config_file} configuration file")

gpu_id = int(sys.argv[2])
print(f"using GPU {gpu_id}")

out_dir=os.path.join(os.path.join(os.path.dirname(config_file), 'meshes')); os.makedirs(out_dir, exist_ok=True);
checkpoints_files = sorted(glob.glob(os.path.join(os.path.dirname(config_file), 'sdfstudio_models', '*.ckpt')))
print(f"{len(checkpoints_files)} checkpoints found")

for ckpt_file in tqdm.tqdm(checkpoints_files[:2], desc='Generating meshes'):
	ckpt_it = int(os.path.basename(ckpt_file).replace('step-', '').replace('.ckpt', ''))	
	ckpt_out_dir = os.path.join(out_dir, f"ITE_{ckpt_it:09d}"); os.makedirs(ckpt_out_dir, exist_ok=True)

	# handle config files
	tgt_config_file = os.path.join(ckpt_out_dir, "config.yaml")
	shutil.copy2(config_file, tgt_config_file)
	config = yaml.load(Path(tgt_config_file).read_text(), Loader=yaml.Loader)
	config.trainer.load_step = ckpt_it
	Path(tgt_config_file).write_text(yaml.dump(config), "utf8")

	# Generate Mesh
	# cmd = f"CUDA_VISIBLE_DEVICES={gpu_id} ns-extract-mesh --load-config {tgt_config_file} --output-path {ckpt_out_dir}/mesh_1024.ply --create_visibility_mask False"
	# subprocess.run(cmd, shell=True)
	cmd = f"CUDA_VISIBLE_DEVICES={gpu_id} ns-extract-mesh --load-config {tgt_config_file} --output-path {ckpt_out_dir}/mesh_1024_vm.ply --create_visibility_mask True"
	subprocess.run(cmd, shell=True)

	# # Generate texture
	# tex_out_dir = os.path.join(ckpt_out_dir, "texture"); os.makedirs(tex_out_dir);
	# cmd = f"CUDA_VISIBLE_DEVICES={gpu_id} python scripts/texture.py --load-config {tgt_config_file} --input-mesh-filename {ckpt_out_dir}/mesh_1024_vm.ply --output-dir {tex_out_dir} --target_num_faces 100000"
	# subprocess.run(cmd, shell=True)

