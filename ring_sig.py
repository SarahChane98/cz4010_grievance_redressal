import os, hashlib, random, Crypto.PublicKey.RSA
from functools import reduce
import json

class ring:
    def __init__(self, k, L=1024):
        self.k = k
        self.l = L
        self.n = len(k)
        self.q = 1 << (L - 1)

    def sign(self, m, z):
        self.permut(m)
        s = [None] * self.n
        u = random.randint(0, self.q)
        c = v = self.E(u) 
        for i in [*range(z+1, self.n), *range(z)]:
            s[i] = random.randint(0, self.q)
            e = self.g(s[i], self.k[i].e, self.k[i].n)
            v = self.E(v^e) 
            if (i+1) % self.n == 0:
                c = v
        s[z] = self.g(v^u, self.k[z].d, self.k[z].n)
        return [c] + s

    def verify(self, m, X):
        self.permut(m)
        def _f(i):
            return self.g(X[i+1], self.k[i].e, self.k[i].n)
        y = list(map(_f, range(len(X)-1)))
        def _g(x, i):
            return self.E(x^y[i])
        r = reduce(_g, range(self.n), X[0])
        return r == X[0]

    def permut(self, m):
        self.p = int(hashlib.sha1(bytearray('%s' % m, 'utf-8')).hexdigest(),16)

    def E(self, x): 
        msg = '%s%s' % (x, self.p)
        return int(hashlib.sha1(bytearray(msg, 'utf-8')).hexdigest(), 16)

    def g(self, x, e, n):
        q, r = divmod(x, n)
        if ((q + 1) * n) <= ((1 << self.l) - 1):
            rslt = q * n + pow(r, e, n)
        else:
            rslt = x
        return rslt


size = 4
msg1 = """
import simplejson as json # this would be just 'import json' in Python 2.7 and later
...
...

myModel = MyModel()
listIWantToStore = [1,2,3,4,5,'hello']
myModel.myList = json.dumps(listIWantToStore)
myModel.save()

"""

def _rn(_):
  return Crypto.PublicKey.RSA.generate(1024, os.urandom)


key = list(map(_rn, range(size)))
# r = ring(key)
# for i in range(1):
#     s1 = r.sign(msg1, i)
#     s2 = r.sign(msg2, i)
#     print(r.verify(msg1, s1))
#     print(r.verify(msg2, s2))
#     print(r.verify(msg1, s2))


def generate_signature(keys, my_index, message):
    r = ring(keys)
    sig = r.sign(message, my_index)
    return ','.join([str(i) for i in sig])


def verify(keys, message, signature):
    signature = [int(i) for i in signature.split(',')]
    r = ring(keys)
    return r.verify(message, signature)


# sig = generate_signature(key, 0, msg1)
# key[1] = Crypto.PublicKey.RSA.import_key(key[1].public_key().export_key())
# print(verify(key, msg1, sig))