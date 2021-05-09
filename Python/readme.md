 # kurosc: kuramoto neighbor interaction & delay package

      /kuramoto-osc/tree/main/Python/kurosc/kurosc



            kurosc/
            ----kurosc/
            --------model_config.py
            --------main.py    <---fn main() calls run()
            --------model.py
            --------lib
            --------corticalSheet  : oscillator arrays & ics
            --------spatialKernel  : gaussian differentiate
            --------secondOrderInteraction  : nominal kuramoto model when r,beta = 0,0  



            use argparse:

            % python main.py --set local_async
            % ...

            % python main.py --set global_sync

            will import different sets from model_config.json





# spatialKernel
wavelet.py<br>
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
      w = wavelet(spatial_wavelet,x,*params.values(),True)

symbolic_calcs.py<br>
recursive sympy differentiation for gaussian<br>


# corticalSheet
oscillator.py<br>
Figure 3,5,&6<br>


# secondOrderInteraction
decouple.py<br>
Eq 13 Figure 4<br>
second order neural interrupting interactions<br>
returns a two term phase differential equation<br>
