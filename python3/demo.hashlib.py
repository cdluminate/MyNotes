'''
import hashlib as hl
ipython3>>> hl?
'''
import hashlib
m = hashlib.md5()
m.update(b"Nobody inspects")
m.update(b" the spammish repetition")
print(m.digest())
print(hashlib.sha224(b"Nobody inspects the spammish repetition").hexdigest())
