from hashlib import sha256
from gmpy2 import iroot
from timeit import default_timer as timer
from charm.core.math import pairing
from charm.toolbox.pairinggroup import PairingGroup,G1,G2,GT,pair,ZR

class PPFC():
    def __init__(self):
        global group
        group = PairingGroup('a128bit')
        global p
        p = 2 ** 22
    def setup(self,l):
        g = group.random(G1)
        h = group.random(G2)
        gi = {}
        hi = {}
        a = group.random(ZR)
        for i in range(1,l+1):
            gi[i] = g**(a**i)
            hi[i] = h ** (a ** i)
        for i in range(l+2,2*l+1):
            hi[i] = h ** (a ** i)
        eg1hl = pair(gi[1],hi[l])
        ck= {'g':g,'h':h,'l':l,'gi':gi,'hi':hi,'eg1hl':eg1hl}
        return ck

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

    def AKGen(self, ck):
        g = ck['g']
        h = ck['h']
        g0 = group.random(G1)
        h0 = group.random(G2)
        s = {}
        t = {}
        k = {}
        for i in range(1,ck['l']+1):
            si = group.random(ZR)
            ti = group.random(ZR)
            s[i] = si
            t[i] = ti
            ki = (g ** si) * (g0 ** ti)
            k[i] = ki
        egh = pair(g, h)
        apk = {'g': g, 'h': h, 'g0': g0, 'h0': h0, 'k': k, 'egh': egh}
        ask = {'s': s, 't': t}
        return apk, ask
    def Com(self,ck,apk,f):
        alpha = group.random(ZR)
        comf = ck['g'] ** alpha
        for i in range(1,len(f)+1):
            comf = comf * (ck['gi'][i] ** f[i])
        usk1 = group.random(ZR)
        usk2 = group.random(ZR)
        usk3 = group.random(ZR)
        upk1 = apk['h'] ** usk1
        upk2 = apk['g'] ** usk2
        upk3 = apk['g'] ** usk3
        upk4 = apk['h0'] ** usk1
        usk = {'usk1': usk1, 'usk2': usk2, 'usk3': usk3}
        upk = {'upk1': upk1, 'upk2': upk2, 'upk3': upk3, 'upk4': upk4}
        com = {'comf':comf,'upk':upk}
        d = {'alpha':alpha,'f':f,'usk':usk}
        return com,d

    def IOKGen(self,apk,f):
        iok = {}
        aux = {}
        for i in range(1,len(f)+1):
            ui = group.random(ZR)
            ioki = (apk['h'] ** f[i]) * (apk['h0'] ** ui)
            aux[i] = ui
            iok[i] = ioki
        return iok,aux

    def OKGen(self,ask,iok):
        ok1 = group.init(G2,1)
        ok2 = group.init(G2,1)
        for i in range(1,len(iok)+1):
            ok1 = ok1 * iok[i]**ask['s'][i]
            ok2 = ok2 * iok[i]**ask['t'][i]
        ok = {'ok1':ok1,'ok2':ok2}
        return ok

    def OKVer(self,apk,ok,aux,f):
        A = group.init(G1,1)
        B = group.init(G1,1)
        for i in range(1,len(f)+1):
            A = A * apk['k'][i]**f[i]
            B = B * apk['k'][i]**aux[i]
        left = pair(apk['g'],ok['ok1']) * pair(apk['g0'],ok['ok2'])
        right = pair(A,apk['h']) * pair(B,apk['h0'])
        if left == right:
            return 1
        return 0

    def Preopen(self,ck,apk,x,com):
        W = group.init(G2,1)
        Wj = {}
        for j in range(1,len(x)+1):
            W = W * (ck['hi'][ck['l']-j+1] ** x[j])
            Wjj = group.init(G2,1)
            for i in range(1,j):
                Wjj = Wjj * (ck['hi'][ck['l']-i+j+1] ** x[i])
            for i in range(j+1,len(x)+1):
                Wjj = Wjj * (ck['hi'][ck['l']-i+j+1] ** x[i])
            Wj[j] = Wjj
        c1 = {}
        c2 = {}
        r = group.random(ZR)
        r1 = group.random(ZR)
        upk1r = com['upk']['upk1']**r
        upk4r = com['upk']['upk4'] ** r
        for i in range(1,len(x)+1):
            c1i = (apk['egh'] ** x[i]) * pair(apk['k'][i],upk1r)
            c1[i] = c1i
            c2i = pair(apk['k'][i], upk4r)
            c2[i] = c2i
        c3 = apk['g'] ** r1
        c4 = (apk['g'] ** r) * (com['upk']['upk2'] ** r1)
        c5 = (apk['g0'] ** r) * (com['upk']['upk3'] ** r1)
        C = {'c1':c1,'c2':c2,'c3':c3,'c4':c4,'c5':c5}
        aop = W
        pop = {'Wj':Wj,'C':C}
        return aop,pop
    def Open(self,d,ok,aux,pop,aop):
        num = group.init(GT,1)
        for i in range(1, len(d['f'])+1):
            num = num * (pop['C']['c1'][i]**d['f'][i]) * (pop['C']['c2'][i]**aux[i])
        den = pair(pop['C']['c4']/(pop['C']['c3']**d['usk']['usk2']),ok['ok1']) * pair(pop['C']['c5']/(pop['C']['c3']**d['usk']['usk3']),ok['ok2'])
        y = num/(den**d['usk']['usk1'])
        Wy = aop ** d['alpha']
        for j in range(1, len(d['f']) + 1):
            Wy = Wy * (pop['Wj'][j] ** d['f'][j])
        op = Wy
        return y,op
    def OpenwithBSGS(self,d,ok,aux,pop,aop,L1,L2,n):
        num = group.init(GT,1)
        for i in range(1, len(d['f'])+1):
            num = num * (pop['C']['c1'][i]**d['f'][i]) * (pop['C']['c2'][i]**aux[i])
        den = pair(pop['C']['c4']/(pop['C']['c3']**d['usk']['usk2']),ok['ok1']) * pair(pop['C']['c5']/(pop['C']['c3']**d['usk']['usk3']),ok['ok2'])
        c = num/(den**d['usk']['usk1'])
        Wy = aop ** d['alpha']
        for j in range(1, len(d['f']) + 1):
            Wy = Wy * (pop['Wj'][j] ** d['f'][j])
        op = Wy
        y = self.BSGScompute(c,L1,L2,n)
        return y,op
    def Fopen(self,ck,d,x):
        y = 0
        for i in range(1, len(x)+1):
            y = y + d['f'][i] * x[i]
        W = group.init(G2, 1)
        Wy = group.init(G2, 1)
        for j in range(1, len(x) + 1):
            W = W * (ck['hi'][ck['l'] - j + 1] ** x[j])
            # Wj = group.init(G2, 1)
            for i in range(1, j):
                Wy = Wy * (ck['hi'][ck['l'] - i + j + 1] ** (d['f'][j] * x[i]))
            for i in range(j + 1, len(x) + 1):
                Wy = Wy * (ck['hi'][ck['l'] - i + j + 1] ** (d['f'][j] * x[i]))
        Wy = Wy * (W ** d['alpha'])
        op = Wy
        aop = W
        return y,op,aop
    def Ver(self,ck,com,y,op,aop):
        if pair(com['comf'],aop) == (ck['eg1hl']**y) * pair(ck['g'],op):
            return 1
        return 0