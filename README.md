# GraphiX
<img align="right" width="96" src="https://user-images.githubusercontent.com/27349725/78643293-b8553c80-78bc-11ea-8cc2-5599c8a2fdf2.png">

Scientific visualization tools are essential for the understanding of physical simulation, as it gives a visualization aspect of the simulated phenomena. In
the past years, data produced by simulations join the big-data trend. In order to
maintain a reasonable reaction time of the user’s commands many scientific tools
tend to introduce parallelism schemes to their software. As the number of cores in
any given architecture increase, the need for software to utilize the archutecture is
inevitable. Thus, GraphiX - a scientific visualization tool parallelized in a shared-memory fashion via OpenMP version 4.5 was created. We chose Gnuplot as the
graphical utility for GraphiX due to its speed as it is written in C. GraphiX parallelism scheme’s work-balance is nearly perfect, and scales well both in terms of
memory and amount of cores. 

For more reading please refer to [this](http://ebooks.iospress.nl/volumearticle/53958) paper.

## Prerequisites
1. Python Version 2
2. Pyqt4
3. GCC - tested for 4.9.1 and 5.1.0

## Installement
If you have GCC version 4.9.1 or 5.1.0 you can use the precompiled gnuplot parallel source code and skip this step
1. Run the following command to extract the parallel gnuplot source code, configure it and compiles it
```
sh setup_gnuplot.sh
```
2. Setup Cython & Designer
```
sh setup_graphix.sh
```
Which runs the cython part of GraphiX and the GUI part.

## Execution
To run GraphiX simply change to the Gui directory and run for example the exisiting sedeov-taylor test
```
python graphix.py ../sedov_taylor_xy_plane_test/plot.1
```
![pic2](https://user-images.githubusercontent.com/27349725/78646490-c9ed1300-78c1-11ea-9cef-8a3e0a2c88b2.PNG)

## Options
### Heatmap & Contours

As shown above, GraphiX is capable producing heatmaps in high response time thanks to the parallelism scheme.
In addition, one can disable the heatmap option and generate a contour of the same parameters

![pic3](https://user-images.githubusercontent.com/27349725/78662053-6de1b900-78d8-11ea-92d2-8e6281da9e31.PNG)

### Next & Previous plot
You can also skip to the next or previous plot, in which graphix will search for the file with the same prefix but a suffix that is the first larger number than the current one. While maintaining the last command selected

![image](https://user-images.githubusercontent.com/27349725/78661676-dc724700-78d7-11ea-8a26-68752422581e.png)


## Citation
If you use one of these source codes please cite
```
@inproceedings{DBLP:conf/parco/HarelParco19,
  author    = {Re'em Harel and
               Gal Oren},
  editor    = {Ian Foster and
               Gerhard R. Joubert and
               Luděk Kučera and
               Wolfgang E. Nagel and
               Frans Peters},
  title     = {GraphiX: {A} Fast Human-Computer Interaction Symmetric Multiprocessing Parallel Scientific Visualization Tool},
  booktitle = {Parallel Computing: Technology Trends, Proceedings of the International
               Conference on Parallel Computing, Prague, Czech Republic, 10-13 September 2019},
  series    = {Advances in Parallel Computing},
  volume    = {36},
  pages     = {509--520},
  publisher = {{IOS} Press},
  year      = {2020},
  doi       = {10.3233/APC200079},
  biburl    = {https://dblp.org/rec/conf/parco/HarelParco19.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```
