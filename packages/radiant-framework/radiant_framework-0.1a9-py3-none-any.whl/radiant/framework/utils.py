import sys
import os
import multiprocessing



########################################################################
class Environ_:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """"""
        self.environ = json.load(open('/environ.json'))

    # ----------------------------------------------------------------------
    def __call__(self, value, default=None):
        """"""
        return os.getenv(value, default)


    # ----------------------------------------------------------------------
    def __getattr__(self, value):
        """"""
        return os.getenv(value, None)


environ = Environ_()





# ----------------------------------------------------------------------
def run_script(script, port):
    """"""
    def worker(script, port):
        os.system(f"python {script} {port}")
    p = multiprocessing.Process(target=worker, args=(script, port))
    p.start()
