import sys
import os
import multiprocessing

# ----------------------------------------------------------------------
def environ(value, default=None):
    """"""
    return os.getenv(value, default)


# ----------------------------------------------------------------------
def run_script(script, port):
    """"""
    def worker(script, port):
        os.system(f"python {script} {port}")
    p = multiprocessing.Process(target=worker, args=(script, port))
    p.start()
