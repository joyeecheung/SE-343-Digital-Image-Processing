##Dependencies
1. pillow
2. Numpy, Scipy>=0.14.0

##How to generate the results
Enter the `src` directory, run `python main.py`. It will use the `02.png` under `img` directory as default to produce the results.

To use another source image, put the image under `img` directory, then run `python main.py -s [filename]`. For example, to use a `03.png`, put it under `img`, then run `python main.py -s 03.png`.

The results will show up in `result` directory.

##Directory structure
```
.
├─ README.md
├─ requirements.txt
├─ doc
│   └─ report.pdf
├─ img (source image)
│   └─ 02.png
├─ result (the results)
│   ├─  quantize-128.png
│   ├─  quantize-2.png
│   ├─  quantize-32.png
│   ├─  quantize-4.png
│   ├─  quantize-8.png
│   ├─  scale-12-8.png
│   ├─  scale-192-128.png
│   ├─  scale-24-16.png
│   ├─  scale-300-200.png
│   ├─  scale-450-300.png
│   ├─  scale-48-32.png
│   ├─  scale-500-200.png
│   └─  scale-96-64.png
└─src (the python source code)
    ├─  main.py (entry point)
    ├─  quantize.py
    ├─  scale.py
    └─  util.py
```