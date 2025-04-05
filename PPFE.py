from hashlib import sha256

from timeit import default_timer as timer
from charm.core.math import pairing
from charm.toolbox.pairinggroup import PairingGroup,G1,G2,GT,pair,ZR
from gmpy2 import iroot


class PPFE():
    def __init__(self):
        global group
        group = PairingGroup('a128bit')
        global p
        p = 2 ** 22
    def setup(self,l):
        g = group.random(G1)
        h = group.random(G2)
        g0 = group.random(G1)
        h0 = group.random(G2)
        s = []
        t = []
        k = []
        for i in range(l):
            si = group.random(ZR)
            ti = group.random(ZR)
            s.append(si)
            t.append(ti)
            ki = (g ** si) * (g0 ** ti)
            k.append(ki)
        egh = pair(g,h)
        mpk= {'g':g,'h':h,'g0':g0,'h0':h0,'k':k,'l':l,'egh':egh}
        msk = {'s':s,'t':t}
        return mpk,msk
    def BSGSinitlist(self, g):
        n = iroot(p, 2)[0] + 1
        L1 = []
        L2 = []
        L1.append(group.init(GT, 0))
        L2.append(group.init(GT, 0))
        for i in range(1, n):
            L1.append(g ** i)
            L2.append(g ** (group.init(ZR, int(n * i))))
        return L1, L2, n

    def BSGScompute(self, h, L1, L2, n):
        for i in range(len(L2)):
            L2[i] = h / L2[i]
            for j in range(len(L1)):
                if L1[j] == L2[i]:
                    return j + i * n
        return None

    def UKGen(self,mpk):
        usk1 = group.random(ZR)
        usk2 = group.random(ZR)
        usk3 = group.random(ZR)
        upk1 = mpk['h']**usk1
        upk2 = mpk['g'] ** usk2
        upk3 = mpk['g'] ** usk3
        upk4 = mpk['h0'] ** usk1
        usk = {'usk1':usk1,'usk2':usk2,'usk3':usk3}
        upk = {'upk1': upk1, 'upk2': upk2, 'upk3': upk3,'upk4': upk4}
        return usk,upk


    def IDKGen(self,mpk,f):
        idk = []
        aux = []
        for i in range(len(f)):
            ui = group.random(ZR)
            idki = (mpk['h'] ** f[i]) * (mpk['h0'] ** ui)
            aux.append(ui)
            idk.append(idki)
        return idk,aux

    def DKGen(self,msk,idk):
        dk1 = group.init(G2,1)
        dk2 = group.init(G2,1)
        for i in range(len(idk)):
            dk1 = dk1 * idk[i]**msk['s'][i]
            dk2 = dk2 * idk[i]**msk['t'][i]
        dk = {'dk1':dk1,'dk2':dk2}
        return dk

    def DKVer(self,mpk,dk,aux,f):
        A = group.init(G1,1)
        B = group.init(G1,1)
        for i in range(len(f)):
            A = A * mpk['k'][i]**f[i]
            B = B * mpk['k'][i]**aux[i]
        left = pair(mpk['g'],dk['dk1']) * pair(mpk['g0'],dk['dk2'])
        right = pair(A,mpk['h']) * pair(B,mpk['h0'])

        if left == right:
            return 1
        return 0

    def Enc(self,mpk,x,upk):
        c1 = []
        c2 = []
        r = group.random(ZR)
        r1 = group.random(ZR)
        upk1r = upk['upk1']**r
        upk4r = upk['upk4'] ** r
        for i in range(len(x)):
            c1i = (mpk['egh'] ** x[i]) * pair(mpk['k'][i],upk1r)
            c1.append(c1i)
            c2i = pair(mpk['k'][i], upk4r)
            c2.append(c2i)
        c3 = mpk['g'] ** r1
        c4 = (mpk['g'] ** r) * (upk['upk2'] ** r1)
        c5 = (mpk['g0'] ** r) * (upk['upk3'] ** r1)
        C = {'c1':c1,'c2':c2,'c3':c3,'c4':c4,'c5':c5}
        return C

    def Dec(self,mpk,dk,aux,usk,C,f):
        num = group.init(GT,1)
        for i in range(len(f)):
            num = num * (C['c1'][i]**f[i]) * (C['c2'][i]**aux[i])
        den = pair(C['c4']/(C['c3']**usk['usk2']),dk['dk1']) * pair(C['c5']/(C['c3']**usk['usk3']),dk['dk2'])
        y = num/(den**usk['usk1'])
        return y
    def DecwithBSGS(self,mpk,dk,aux,usk,C,f,L1,L2,n):
        num = group.init(GT,1)
        for i in range(len(f)):
            num = num * (C['c1'][i]**f[i]) * (C['c2'][i]**aux[i])
        den = pair(C['c4']/(C['c3']**usk['usk2']),dk['dk1']) * pair(C['c5']/(C['c3']**usk['usk3']),dk['dk2'])
        c = num/(den**usk['usk1'])
        y = self.BSGScompute(c, L1, L2, n)
        return y