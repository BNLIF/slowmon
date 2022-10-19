# slowmon
Slow Control Monitor Tools


## GECOLogConverter

Convert geco log file to csv file format. Usage:
```python
from geco import GECOLogConverter
gc = GECOLogConverter()                                                                                                                                                               
gc.convert_to_csv('/path/to/your/geco/file.log')
```

## GECOPlotter

To get the trend data for a particular channels, do:
```python
from geco import GECOPlotter
file_list=['/path/to/file1.csv', '/path/to/file2.csv']
gp = GECOPlotter(file_list)
t, y = gp.get_imon_trend(204) # 204 stands for board 2, channel 4
```

To generate a large array of plots for all channels, do:
```python
from geco import GECOPlotter
file_list=['/path/to/file1.csv', '/path/to/file2.csv']
gp = GECOPlotter(file_list)
gp.plot_all_imon_trend(save_fig=True, fig_format='pdf')
```


