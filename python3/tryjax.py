import rich
console = rich.get_console()
import time
import jax
import jax.numpy as np

rk = jax.random.PRNGKey(0)
x = jax.random.normal(rk, (10,))
console.print(x)

size=(3000,3000)
x = jax.random.normal(rk, size, dtype=np.float32)
x = jax.device_put(x)
t_start = time.time()
y = np.dot(x, x.T).block_until_ready()
t_end = time.time()
console.print(t_end - t_start)
