##Dependencies
1. pillow
2. Numpy
3. Scipy >= 0.14.0

##How to generate the results
Enter the `src` directory, run `python main.py`. It will use the `02.png` under `img` directory as default to produce the results.

To use another source image, put the image under `img` directory, then run `python main.py -s [filename]`. For example, to use a `03.png`, put it under `img`, then run `python main.py -s 03.png`.

The results will show up in `result` directory.

##Directory structure
    .
	├─ README.md
	├─ requirements.txt
	├─ doc
	│   └─ report.pdf
	├─ img (source image)
	│   └─ 02.png
	├─ result (the results)
    │   ├── average-11-11.png (image smoothed with 11x11 averaging filter)
    │   ├── dft-double.png (IDFT of DFT of the original image)
    │   ├── dft-spectrum.png (spectrum of the DFT)
    │   ├── fft-double.png (IFFT of FFT of the original image)
    │   ├── fft-spectrum.png (spectrum of the FFT)
    │   └── laplacian.png (image filtered with laplacian filter)
	└─ src (the python source code)
        ├── filter.py (filter function)
        ├── fourier.py (DFT/IDFT/FFT/IFFT)
        └── main.py (generate the results for the report)

##About
* [Github repository](https://github.com/joyeecheung/SE-343-Digital-Image-Processing/tree/master/hw3)
* Author: Qiuyi Zhang
* Time: Dec. 2014
