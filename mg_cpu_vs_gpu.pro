; docformat = 'rst'

pro mg_cpu_vs_gpu
  compile_opt strictarr

  root = mg_src_root()
  intel_sp = read_csv(filepath('intel-sp.csv', root=root))
  intel_dp = read_csv(filepath('intel-dp.csv', root=root))

  nvidia_sp = read_csv(filepath('nvidia-sp.csv', root=root))
  nvidia_dp = read_csv(filepath('nvidia-dp.csv', root=root))

end