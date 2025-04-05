
from timeit import default_timer as timer
from charm.core.math.elliptic_curve import G, ZR
from charm.toolbox.ecgroup import ECGroup
from charm.toolbox.eccurve import secp256k1
from gmpy2 import iroot
from Crypto.Random import random
import PiBFE

class BFE:
    def __init__(self):
        global group
        self.group = ECGroup(secp256k1)
        global p,p1
        p = 2 ** 22
        p1 = 2 ** 10
    def setup(self,l):
        g = self.group.random(G)
        f = self.group.random(G)
        s = {}
        hi = {}
        for i in range(1,l+1):
            si = random.randint(0, p1)#self.group.random(ZR)
            s[i] = si
            hi[i] = g ** si
        pp = {'g': g, 'f': f, 'hi':hi, 'l': l}
        msk = s
        return pp,msk
    def BSGSinitlist(self, g, h):
        n = iroot(p, 2)[0] + 1
        L1 = []
        L2 = []
        L1.append(self.group.init(G, 2))
        L2.append(h)
        for i in range(1, n):
            L1.append(g ** i)
            L2.append(h/(g ** (self.group.init(ZR, int(n * i)))))
        return L1, L2, n
    def BSGScompute(self, L1, L2, n):
        for i in range(len(L2)):
            for j in range(len(L1)):
                if L1[j] == L2[i]:
                    return j + i * n
        return None
    def KDer(self,pp,y,msk):
        x = self.group.random(ZR)
        h = pp['g']**x
        ci = {}
        r = {}
        for i in range(1, pp['l'] + 1):
            ri = self.group.random(ZR)
            c1i = pp['g'] ** ri
            c2i = (pp['f'] ** y[i]) * (h ** ri)
            ci[i] = (c1i,c2i)
            r[i] = ri
        xprove = (h,ci)
        wprove = (x,y,r)
        piU = PiBFE.PiUProve(self.group,pp,xprove,wprove)
        if PiBFE.PiUVerify(self.group,pp,xprove,piU) == 0:
            return 0
        r1 = self.group.random(ZR)
        c1sky = pp['g'] ** r1
        c2sky = h ** r1
        for i in range(1, pp['l'] + 1):
            c1sky = c1sky * (ci[i][0] ** msk[i])
            c2sky = c2sky * (ci[i][1] ** msk[i])
        xprove = (c1sky, c2sky,pp['hi'],h,ci)
        wprove = (msk, r1)
        piAUT = PiBFE.PiAUTProve(self.group, pp, xprove, wprove)
        if PiBFE.PiAUTVerify(self.group, pp, xprove, piAUT) == 0:
            return 0
        fsy = c2sky / (c1sky**x)
        return fsy
    def KDerwithBSGS(self,pp,y,msk):
        x = self.group.random(ZR)
        h = pp['g']**x
        ci = {}
        r = {}
        for i in range(1, pp['l'] + 1):
            ri = self.group.random(ZR)
            c1i = pp['g'] ** ri
            c2i = (pp['f'] ** y[i]) * (h ** ri)
            ci[i] = (c1i,c2i)
            r[i] = ri
        xprove = (h,ci)
        wprove = (x,y,r)
        piU = PiBFE.PiUProve(self.group,pp,xprove,wprove)
        if PiBFE.PiUVerify(self.group,pp,xprove,piU) == 0:
            return 0
        r1 = self.group.random(ZR)
        c1sky = pp['g'] ** r1
        c2sky = h ** r1
        for i in range(1, pp['l'] + 1):
            c1sky = c1sky * (ci[i][0] ** msk[i])
            c2sky = c2sky * (ci[i][1] ** msk[i])
        xprove = (c1sky, c2sky,pp['hi'],h,ci)
        wprove = (msk, r1)
        piAUT = PiBFE.PiAUTProve(self.group, pp, xprove, wprove)
        if PiBFE.PiAUTVerify(self.group, pp, xprove, piAUT) == 0:
            return 0
        fsy = c2sky / (c1sky**x)
        L1, L2, n = self.BSGSinitlist(pp['f'],fsy)
        sy = self.BSGScompute(L1,L2,n)
        return sy
a = BFE()
# l = 3
# pp,msk = a.setup(l)
# y = {}
# for i in range(1,l+1):
#     yi = a.group.random(ZR)
#     sy = msk[i] * yi
#     y[i] = yi
# fsy = a.KGen(pp,y,msk)
number = 100
def KGentest(l):
    t = 0
    pp,msk = a.setup(l)
    y = {}
    for i in range(1, l + 1):
        yi = 2**32 - i
        y[i] = yi
    for i in range(number):
        start = timer()
        a.KDer(pp,y,msk)
        end = timer()
        t = t + (end - start)
    print(str(l) + "   " + str(t*1000/number))
if __name__ == '__main__':
    l = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    print("KGentest:")
    for i in l:
        KGentest(i)