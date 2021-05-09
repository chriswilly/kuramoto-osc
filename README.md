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



96x96 nodes with 0 ics LSODA solve<br>
<img width="1039" alt="ode test" src="https://github.com/chriswilly/kuramoto-osc/blob/main/Python/animation/_keep/Oscillator%20Phase%20in%20pi_210507_021946476379.gif">
