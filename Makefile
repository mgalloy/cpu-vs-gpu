.PHONY: all clean

all: cpu-vs-gpu.png

cpu-vs-gpu.png: intel-sp.csv intel-dp.csv nvidia-sp.csv nvidia-dp.csv mg_cpu_vs_gpu.pro
	$(IDL) mg_cpu_vs_gpu

clean:
	rm -f cpu-vs-gpu.png


