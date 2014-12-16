## 4.4 1D DFT & IDFT

### 4.4.1 Sample from Continuous Transform

For any finite set of discrete samples taken uniformly, there exists a DFT pair.

#### 1D DFT
* Eq. 4.4-6 
	$F(u) = \sum_{x=0}^{M-1} f(x) e^{\frac{-j2\pi ux}{M}}$

With Euler's formula

$e^{j\theta} = \cos\theta + j\sin\theta$

$F(u) = \sum_{x=0}^{M-1} f(x) [\cos\frac{-2\pi ux}{M} + j\sin\frac{-2\pi ux}{M}]$

$F(u) = \sum_{x=0}^{M-1} f(x) [\cos\frac{2\pi ux}{M} - j\sin\frac{2\pi ux}{M}]$

####  1D IDFT
* Eq. 4.4-7
	$f(x) = \frac{1}{M} \sum_{u=0}^{M-1} F(u) e^{\frac{j2\pi ux}{M}}$

#### Periodic

$F(u) = F(u+kM)$

$f(x) = f(x+kM)$

#### Convolution

$f(x) \star h(x) = \sum_{m=0}^{M-1} f(m) h (x-m)$

**Circular convolution**:
Since both functions are periodic, there convolution is periodic, too.

### 4.4.2 Sampling interval v.s. frequency interval

If f(x) is taken from the continuous f(t) with interval

$\Delta T$

(i.e. M samples), in the spatial domain, the range is:

$T = M \Delta T$

In the frequency domain, the interval is:

$\Delta u = \frac{1}{M \Delta T} = \frac{1}{T}$

Then frequency range is:

$\Omega = M \Delta u = \frac{1}{\Delta T}$

## 4.5 2D FT

### 4.5.1 2D Impulse and sifiting property

### 4.5.2 2D CFT

### 4.5.3 2D Sampling

### 4.5.4 Aliasing

#### 1D to 2D aliasing

#### Interpolation & resampling

#### Moire patterns

### 4.5.5 2D DFT & IDFT

#### 2D DFT
* Eq. 4.5-15
	$F(u,v) = \sum_{x=0}^{M-1} \sum_{y=0}^{N-1} f(x,y) e^{-j2\pi(\frac{ux}{M} + \frac{vy}{N})}$

####  2D IDFT
* Eq. 4.5-16
	$f(x,y) = \frac{1}{MN} \sum_{u=0}^{M-1} \sum_{v=0}^{N-1} F(u,v) e^{j2\pi(\frac{ux}{M} + \frac{vy}{N})}$

## 4.6 Properties of 2D DFT

### 4.6.1 Spatial interval v.s. Frequency interval

If f(x, y) is taken from the continuous f(t,z) with interval

$\Delta T, \Delta Z$

(i.e. M x N samples), in the spatial domain, the range is:

$T = M \Delta T, Z = N \Delta Z$

In the frequency domain, the interval is:

$\Delta u = \frac{1}{M \Delta T} = \frac{1}{T}$
$\Delta v = \frac{1}{N \Delta Z} = \frac{1}{Z}$

### 4.6.2 Translation and Rotation

#### Translation property

$f(x,y) e^{j2\pi (\frac{u_0 x}{M} + \frac{v_0 y}{N})} \Leftrightarrow F(u-u_0, v-v_0)$

$f(x-x_0, y-y_0) \Leftrightarrow F(u,v) e^{-j2\pi (\frac{ux_0}{M} + \frac{v y_0}{N})}$

#### Rotation property

Using polar coordinates

$x = rcos\theta, \ y = r\sin\theta, \ u = \omega \cos \phi, \ v = \omega \sin \phi $

Rotate one of them, the other will be rotated with the same angle.

$f(r, \theta + \theta_0) \Leftrightarrow F(\omega, \phi + \theta_0)$

### 4.6.3 Periodicity

Both DFT and IDFT is infinitely periodic in the u and v directions.

$F(u, v) = F(u + k_1 M, v) = F(u, v + k_2 N) = F(u + k_1 M, v + k_2 N)$

$f(x, y) = f(x + k_1 M, y) = f(x, y + k_2 N) = f(x + k_1 M, y + k_2 N)$

Combining with the translation property, let:

$u_0 = \frac{M}{2}, v_0 = \frac{N}{2}$

$e^{-j2\pi (\frac{u_0 x}{M} + \frac{u_0 x}{M})} = e^{-j \pi (x+y)} = \cos(-\pi (x+y)) + j\sin(-\pi (x+y)) = \cos(\pi (x+y)) = (-1)^{x+y}$

$f(x,y)(-1)^{x+y} \Leftrightarrow F(u-\frac{M}{2}, v-\frac{N}{2})$

F(0,0) is at (M/2, N/2), F is shifted to the center.

### 4.6.4 Symmetry



### 4.6.5 Spectrum and Phase Angle

### 4.6.6 2D Convolution Theorem

### 4.6.7 Properties of 2D DFT

## 4.7 Filtering in Frequency Domain

### 4.7.1 Characteristics

### 4.7.2 Fundamentals

### 4.7.3 Steps

### 4.7.4 Spatial filtering v.s. Frequency filtering

## 4.8 Smoothing(Lowpass)

### 4.8.1 Ideal Lowpass Filters

### 4.8.2 Butterworth Lowpass Filters

### 4.8.3 Gaussian Lowpass Filters

### 4.8.4 Examples

## 4.9 Sharpening(Highpass)

### 4.9.1 Ideal Highpas Filters

### 4.9.2 Butterworth Highpass Filters

### 4.9.3 Gaussian Highpass Filters

### 4.9.4 The Laplacian in the frequency domain

### 4.9.5 Unsharp Masking, Highboost Filtering, High-Frequency-Emphasis Filtering

### 4.9.6 Homomorphic Filtering

#$$
\sum_{x=0}^{M}\sum_{y=0}^{N}f(x,y)e^{-2j\pi(\frac{ux}{M}+\frac{vy}{N})}
$$