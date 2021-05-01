# spatialKernel
spatial_kernel.py<br>
Figure 2<br>
construct wavelet for distance decay spatial kernel<br>
returns a normalized gaussian nth order derivative<br>


scale 'a' nonlinearly ~10^n for magnitude<br>
'b' is center mass<br>
scale 'c' linearly for width<br>
'd' is order of derivative for arbitrary spatial_wavelet <br>
    params = {'a': 10000/3*2,
              'b': 0,
              'c': 10,
              'order': 19,
              }
    w = kernel(spatial_wavelet,x,*params.values(),True)

symbolic_calcs.py<br>
recursive sympy differentiation for gaussian<br>


# corticalSheet
oscillatorArray.py<br>


# secondOrderInteraction
neuralInteraction.py<br>
Eq 13 Figure 4<br>
second order neural interrupting interactions<br>
returns a two term phase differential equation<br>
