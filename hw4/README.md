##Dependencies

1. pillow
2. Numpy
3. matplotlib

##How to generate the results

Make sure that numpy accepts division by zero (warning instead of error).

Enter the `src` directory, run `python main.py`. It will use the `02.png`, `task_1.png` and `task_2.png` under `img` directory as default to produce the results.

The results will show up in `result` directory.

##Directory structure

    .
	├─ README.md
	├─ requirements.txt
	├─ doc
	│   └── report.pdf
	├─ img (source image)
    ├─  ├── 02.png
    ├─  ├── task_1.png
	│   └── task_2.png
	├─ result (the results)
    │   ├── hist (color histogram equalization)
    │   │    ├── hist-seperate.png
    │   │    └── hist-together.png
    │   ├── task1 (image filtering)
    │   │    ├── arithmetic-mean-3-3.png
    │   │    ├── arithmetic-mean-9-9.png
    │   │    ├── contraharmonic-mean-3-3.png
    │   │    ├── contraharmonic-mean-9-9.png
    │   │    ├── harmonic-mean-3-3.png
    │   │    └── harmonic-mean-9-9.png
    │   └── task2 (denoising)
    │        ├── gauss
    │        │    ├── gauss-0-40.png
    │        │    ├── gauss-arithmetic.png
    │        │    ├── gauss-contraharmonic.png
    │        │    ├── gauss-geometric.png
    │        │    ├── gauss-harmonic.png
    │        │    └── gauss-median.png
    │        ├── salt
    │        │    ├── salt-20.png
    │        │    ├── salt-contraharmonic--1-5.png
    │        │    └── salt-contraharmonic-1-5.png
    │        └── sap
    │             ├──sap-20-20.png
    │             ├──sap-arithmetic.png
    │             ├──sap-contraharmonic.png
    │             ├──sap-harmonic.png
    │             ├──sap-max.png
    │             ├──sap-median.png
    │             └──sap-min.png
    │
	└─ src (the python source code)
        ├── filter.py (filter function)
        ├── hist.py (histogram function)
        ├── main.py (generate the results for the report)
        ├── noise.py (noise generators)
        └── util.py (utilities)

##About

* [Github repository](https://github.com/joyeecheung/SE-343-Digital-Image-Processing/tree/master/hw4)
* Author: Qiuyi Zhang
* Time: Dec. 2014
