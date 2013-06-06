IDL=idl

.PHONY: all display clean

all: cpu-vs-gpu.png cpu-vs-gpu-thumbnail.png

cpu-vs-gpu.png: intel-sp.csv intel-dp.csv nvidia-sp.csv nvidia-dp.csv mg_cpu_vs_gpu.pro
	$(IDL) -quiet -e mg_cpu_vs_gpu
	@open cpu-vs-gpu.png

cpu-vs-gpu-thumbnail.png: intel-sp.csv intel-dp.csv nvidia-sp.csv nvidia-dp.csv mg_cpu_vs_gpu.pro
	$(IDL) -quiet -e "mg_cpu_vs_gpu, /thumbnail"
	@open cpu-vs-gpu-thumbnail.png

display:
	@open cpu-vs-gpu.png
	@open cpu-vs-gpu-thumbnail.png

clean:
	rm -f cpu-vs-gpu.{ps,png} cpu-vs-gpu-thumbnail.{ps,png}


