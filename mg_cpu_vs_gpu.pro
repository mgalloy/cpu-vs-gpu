; docformat = 'rst'

function mg_cpu_vs_gpu_julday, dates
  compile_opt strictarr, hidden

  juldays = dblarr(n_elements(dates))
  tokens = strsplit(dates, '-', /extract)
  foreach t, tokens, i do juldays[i] = julday(long(t[1]), long(t[2]), long(t[0]))

  return, juldays
end


pro mg_cpu_vs_gpu_series, dates, flops, names, $
                          color=color, name=name, psym=psym, $
                          y_name_correction=y_name_correction
  compile_opt strictarr, hidden

  name_charsize = 0.6
  y_name_gap = 100.0
  x_name_gap = 20.0
  x_annotation_gap = 75.0
  symsize = 0.75

  _color = n_elements(color) eq 0L ? !color.black : color
  _name = n_elements(name) eq 0L ? '' : name
  _psym = n_elements(psym) eq 0L ? -1L : psym
  _y_name_correction = n_elements(y_name_correction) eq 0L $
                         ? (fltarr(n_elements(dates))) $
                         : y_name_correction
  oplot, dates, flops, $
         color=mg_rgb2index(_color), thick=6., psym=psym, symsize=symsize
  foreach n, names, i do begin
    xyouts, dates[i] - x_name_gap, $
            flops[i] + y_name_gap + _y_name_correction[i], $
            names[i], $
            charsize=name_charsize, alignment=1.0, color=mg_rgb2index(_color)
  endforeach
  xyouts, dates[-1] + x_annotation_gap, flops[-1], _name, $
          charsize=0.75, color=mg_rgb2index(_color)
end


pro mg_cpu_vs_gpu, thumbnail=thumbnail
  compile_opt strictarr, hidden

  !quiet = 1

  root = mg_src_root()
  intel_sp = read_csv(filepath('intel-sp.csv', root=root))
  intel_dp = read_csv(filepath('intel-dp.csv', root=root))

  intel_sp_names = intel_sp.field1
  intel_sp_flops = float(intel_sp.field2)
  intel_sp_dates = mg_cpu_vs_gpu_julday(intel_sp.field3)

  intel_dp_names = intel_dp.field1
  intel_dp_flops = float(intel_dp.field2)
  intel_dp_dates = mg_cpu_vs_gpu_julday(intel_dp.field3)

  nvidia_sp = read_csv(filepath('nvidia-sp.csv', root=root))
  nvidia_dp = read_csv(filepath('nvidia-dp.csv', root=root))

  nvidia_sp_names = nvidia_sp.field1
  nvidia_sp_flops = float(nvidia_sp.field2)
  nvidia_sp_dates = mg_cpu_vs_gpu_julday(nvidia_sp.field3)

  nvidia_dp_names = nvidia_dp.field1
  nvidia_dp_flops = float(nvidia_dp.field2)
  nvidia_dp_dates = mg_cpu_vs_gpu_julday(nvidia_dp.field3)

  basename = 'cpu-vs-gpu' + (keyword_set(thumbnail) ? '-thumbnail' : '')
  mg_psbegin, filename=basename + '.ps', xsize=7, ysize=5, /inches
  !p.font = 0

  psym = mg_usersym(/circle, /fill, /with_line)
  dummy = label_date(date_format='%Y')

  plot, intel_sp_dates, intel_sp_flops, xstyle=8, ystyle=8, /nodata, /noerase, $
        xtitle='!CRelease date', xtickformat='label_date', xtickunits='Time', xminor=4, $
        xmargin=[10, 12], $
        ytitle='Theoretical peak (GFLOP/s)', ymargin=[6, 2], yticks=10, yrange=[0, 5000], $
        charsize=0.8, $
        ticklen=-0.01

  mg_decomposed, 1

  y_name_correction = fltarr(n_elements(nvidia_sp_dates))
  y_name_correction[1] = 120.0
  y_name_correction[2] = 160.0
  mg_cpu_vs_gpu_series, nvidia_sp_dates, nvidia_sp_flops, nvidia_sp_names, $
                        color=!color.sea_green, name='NVIDIA GPU SP', psym=psym, $
                        y_name_correction=y_name_correction

  mg_cpu_vs_gpu_series, nvidia_dp_dates, nvidia_dp_flops, nvidia_dp_names, $
                        color=!color.dark_green, name='NVIDIA GPU DP', psym=psym

  mg_cpu_vs_gpu_series, intel_sp_dates, intel_sp_flops, strarr(n_elements(intel_sp_dates)), $
                        color=!color.sky_blue, name='Intel SP', psym=psym

  y_name_correction = fltarr(n_elements(intel_dp_dates))
  y_name_correction[0] = -70.0
  y_name_correction[1] = 0.0
  y_name_correction[2] = 0.0
  y_name_correction[3] = -50.0
  y_name_correction[4] = 100.0
  y_name_correction[5] = -60.0
  mg_cpu_vs_gpu_series, intel_dp_dates, intel_dp_flops, intel_dp_names, $
                        color=!color.dark_blue, name='Intel DP', psym=psym, $
                        y_name_correction=y_name_correction

  mg_psend
  mg_convert, basename, $
              max_dimensions=keyword_set(thumbnail) ? [600, 500] : [800, 600]
end