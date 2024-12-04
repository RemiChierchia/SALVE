import subprocess, sys

procs = []
with open(sys.argv[1], 'r') as file:
	for exp in file.readlines():
		exp = exp.strip()
		# import ipdb; ipdb.set_trace()
		name = exp.split(' ')[0]
		scale = exp.split(' ')[-1]
		print(f"running {exp}")
		cmd = (f"CUDA_VISIBLE_DEVICES={sys.argv[2]} ns-train neus-facto --vis tensorboard "
			f"--experiment-name {name} --output-dir /nas/home/chi215/Wounds/results_neusfacto_precision/ "
			f"--pipeline.model.sdf-field.inside-outside False --pipeline.model.sdf-field.use-grid-feature True --pipeline.model.sdf-field.encoding-type hash "
			f"--pipeline.model.sdf-field.num-layers 2 --pipeline.model.sdf-field.beta-init 0.3 --pipeline.model.sdf-field.bias 0.5 --optimizers.fields.optimizer.lr 0.01 "
			f"--pipeline.model.eikonal-loss-mult 0.2 "
			f"--trainer.save-only-latest-checkpoint False --trainer.steps-per-save 10000 --trainer.max-num-iterations 60000 --trainer.steps-per-eval-image 10000 "
			f"--pipeline.datamanager.train-num-rays-per-batch 4096 "
			f"instant-ngp-data --data /nas/home/chi215/Wounds/SDFStudioData/PrecisionExps/LigthGlue_COLMAP_scaled/{name.split('/')[0]}/SD/{name.split('/')[-2]}/ --scene_scale {scale} --include_sampling_mask False")
		print(cmd)
		procs.append(subprocess.Popen(cmd, shell=True))

		if len(procs) >= int(sys.argv[3]):
			for p in procs: p.wait()
			for p in procs: p.kill() 
			procs = []


if len(procs) > 0:
	for p in procs: p.wait()
	for p in procs: p.kill()
	procs = []
print("Done")
