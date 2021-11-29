from joblib import Parallel, delayed
import multiprocessing
import time
num_cores = multiprocessing.cpu_count()

'''
https://pythonhosted.org/joblib/parallel.html
http://scikit-image.org/docs/dev/user_guide/tutorial_parallelization.html
'''

def crunch(i):
    time.sleep(0.01)
    return i*i

results = Parallel(n_jobs=num_cores)(
        delayed(crunch)(i) for i in range(10)
        )
print(results)

results = Parallel(n_jobs=2, backend='threading')(
        delayed(crunch)(i) for i in range(10)
        )
print(results)

with Parallel(n_jobs=2) as parallel:
    results = parallel(
            delayed(crunch)(i) for i in range(10)
            )
    print(results)

with Parallel(n_jobs=-1, verbose=50) as parallel:
    results = parallel(
            delayed(crunch)(i) for i in range(1000)
            )
