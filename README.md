# GraphiX

Scientific visualization tools are essential for the understanding of physical simulation, as it gives a visualization aspect of the simulated phenomena. In
the past years, data produced by simulations join the big-data trend. In order to
maintain a reasonable reaction time of the user’s commands many scientific tools
tend to introduce parallelism schemes to their software. As the number of cores in
any given architecture increase, the need for software to utilize the archutecture is
inevitable. Thus, GraphiX - a scientific visualization tool parallelized in a sharedmemory fashion via OpenMP version 4.5 was created. We chose Gnuplot as the
graphical utility for GraphiX due to its speed as it is written in C. GraphiX parallelism scheme’s work-balance is nearly perfect, and scales well both in terms of
memory and amount of cores. 

For more reading please refer to [this](https://galoren.github.io/files/parco19_Graphix.pdf) paper.

## Prerequisites
1. Python Version 2
2. Pyqt4
3. GCC - tested for 4.9.1 and 5.1.0

## Installement
If you have GCC version 4.9.1 or 5.1.0 you can use the precompiled gnuplot parallel source code and skip this step
1.
```
sh setup_gnuplot.sh
```
Which extracts the parallel gnuplot source code, configures it and compiles it (assuming you have a correct version of GCC)

2. Setup Cython & Designer
```
sh setup_graphix.sh
```
Which runs the cython part of GraphiX and the GUI part.

## Execution
To run GraphiX simply change to the Gui directory and run for example the exisiting sedeov-taylor test
```
python graphix.py -f ../sedov_taylor_xy_plane_test/plot.1
```

![pic1](https://user-images.githubusercontent.com/27349725/78580562-3d980d00-783b-11ea-957a-3070b63cdfd4.PNG)

