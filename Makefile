IDL=idl
IDL_PRESENT=0


.PHONY: all display clean

all: main

ifeq ($(IDL_PRESENT), 1)
  results=cpu_vs_gpu.pdf cpu-vs-gpu.png
else
  results=cpu_vs_gpu.pdf
endif

main: $(results)

thumbnail: cpu-vs-gpu-thumbnail.png

cpu-vs-gpu.png: intel-sp.csv intel-dp.csv nvidia-sp.csv nvidia-dp.csv mg_cpu_vs_gpu.pro
	$(IDL) -quiet -e mg_cpu_vs_gpu
	@echo "Wrote cpu-vs-gpu.png"

cpu_vs_gpu.pdf: intel-sp.csv intel-dp.csv nvidia-sp.csv nvidia-dp.csv nvidia-boost-sp.csv nvidia-boost-dp.csv cpu_vs_gpu_plot.py
	./cpu_vs_gpu_plot.py
	@echo "Wrote cpu_vs_gpu.png"

cpu-vs-gpu-thumbnail.png: intel-sp.csv intel-dp.csv nvidia-sp.csv nvidia-dp.csv mg_cpu_vs_gpu.pro
	$(IDL) -quiet -e "mg_cpu_vs_gpu, /thumbnail"
	echo "Wrote cpu-vs-gpu-thumbnail.png"

display:
	@if [ -f cpu-vs-gpu.png ] ; then open cpu-vs-gpu.png; fi
	@if [ -f cpu-vs-gpu-thumbnail.png ] ; then open cpu-vs-gpu-thumbnail.png; fi
	@if [ -f cpu_vs_gpu.pdf ] ; then open cpu_vs_gpu.pdf; fi

clean:
	rm -f cpu-vs-gpu.{ps,png} cpu-vs-gpu-thumbnail.{ps,png}
	rm -f cpu_vs_gpu.pdf


