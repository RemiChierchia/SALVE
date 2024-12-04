import subprocess, glob, sys, os



config_files = sorted(glob.glob(sys.argv[1]))
print(f"{len(config_files)} configuration files found")

gpu_id = int(sys.argv[2])
print(f"using GPU {gpu_id}")

for i, config_file in enumerate(config_files):
	dirname = os.path.dirname(config_file)
	cmd = f"CUDA_VISIBLE_DEVICES={gpu_id} ns-extract-mesh --load-config {dirname}/config.yml --output-path {dirname}/mesh_1024_vm.ply --create_visibility_mask True"
	subprocess.run(cmd, shell=True)
#	cmd = f"CUDA_VISIBLE_DEVICES={gpu_id} ns-extract-mesh --load-config {dirname}/config.yml --output-path {dirname}/mesh_1024.ply --create_visibility_mask False"
#	subprocess.run(cmd, shell=True)
