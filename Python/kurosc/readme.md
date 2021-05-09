jump to <br>

      kuramoto-osc/Python/kurosc/kurosc/main.py




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


      corticalSheet.oscillator import oscillatorArray
      secondOrderInteraction.decouple import interaction
      spatialKernel.wavelet import kernel


kurosc package structure based on this
https://python-packaging.readthedocs.io/en/latest/minimal.html
