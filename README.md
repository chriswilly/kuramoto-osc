# kuramoto-osc
AMATH 575 group project on

"Generative models of cortical oscillations: neurobiological implications of the Kuramoto model” Breakspear, Heitmann, & Daffertshofer
https://www.frontiersin.org/articles/10.3389/fnhum.2010.00190/full<br>
https://doi.org/10.3389/fnhum.2010.00190


# Matlab
may eventually contain original paper source code

# Python
contains modification to distance Kuramoto model for next steps in project<br>

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


# Plot Arbitrary Size Node Array Random Initial Conditions

      corticalSheet.oscillator.oscillatorArray.plot_phase


32x32 nodes with 0 ics LSODA solve<br>
<img width="1039" alt="ode test" src="https://github.com/chriswilly/kuramoto-osc/blob/main/Python/animation/R%3D0.00%20beta%3D0.00%20K-N%3D1.0%20%26%20c%3D4%20for%20theta_tin0pi_210517_014918455647.gif">




72x72 nodes with 0 ics & bifurfaction conditions LSODA solve<br>
<img width="1039" alt="ode test" src="https://github.com/chriswilly/kuramoto-osc/blob/main/Python/animation/_keep/R%3D%20beta%3D%20K-N%3D%20%26%20c%3D%20for%20theta_tinpi_210514_063828153355.gif">
