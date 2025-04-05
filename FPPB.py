from hashlib import sha256

from timeit import default_timer as timer
from charm.core.math import pairing
from charm.toolbox.pairinggroup import PairingGroup,G1,G2,GT,pair,ZR
from gmpy2 import iroot

import Pi
class FPPB():
    def __init__(self):
        global group
        self.group = PairingGroup('a128bit')
        global p
        p = 2 ** 22
    def randomZr(self):
        return self.group.random(ZR)
    def setup(self,l):
        g = self.group.random(G1)
        h = self.group.random(G2)
        v = self.group.random(G1)
        gi = {}
        hi = {}
        vi = {}
        a = self.group.random(ZR)
        for i in range(1,l+1):
            gi[i] = g**(a**i)
            hi[i] = h ** (a ** i)
            vi[i] = self.group.random(G1)
        for i in range(l+2,2*l+1):
            hi[i] = h ** (a ** i)
        eg1hl = pair(gi[1],hi[l])
        pp= {'g':g,'h':h,'v':v,'l':l,'gi':gi,'hi':hi,'vi':vi,'eg1hl':eg1hl}
        return pp

    def AKGen(self, pp):
        g = pp['g']
        h = pp['h']
        g0 = self.group.random(G1)
        h0 = self.group.random(G2)
        s = {}
        t = {}
        k = {}
        for i in range(1,pp['l']+1):
            si = self.group.random(ZR)
            ti = self.group.random(ZR)
            s[i] = si
            t[i] = ti
            ki = (g ** si) * (g0 ** ti)
            k[i] = ki
        xprove = (k,g,g0)
        wprove = (s,t)
        #pi_key1 = self.Pikey1Prove(pp,xprove,wprove)
        pi_key1 = Pi.Pikey1Prove(self.group,pp,xprove,wprove)
        egh = pair(g, h)
        pkA = {'g': g, 'h': h, 'g0': g0, 'h0': h0, 'k': k, 'egh': egh, 'pi_key1': pi_key1}
        skA = {'s': s, 't': t}
        return pkA, skA
    def AKGenVer(self,pp,pkA):
        xprove = (pkA['k'], pkA['g'], pkA['g0'])
        #if self.Pikey1Verify(pp,xprove,pkA['pi_key1']):
        if Pi.Pikey1Verify(self.group,pp,xprove,pkA['pi_key1']):
            return 1
        return 0

    def BSGSinitlist(self, g):
        n = iroot(p, 2)[0] + 1
        L1 = []
        L2 = []
        L1.append(self.group.init(GT, 0))
        L2.append(self.group.init(GT, 0))
        for i in range(1, n):
            L1.append(g ** i)
            L2.append(g ** (self.group.init(ZR, int(n * i))))
        return L1, L2, n

    def BSGScompute(self, h, L1, L2, n):
        for i in range(len(L2)):
            L2[i] = h / L2[i]
            for j in range(len(L1)):
                if L1[j] == L2[i]:
                    return j + i * n
        return None

            
    def KGen(self,pp,skA,pkA,f):
        # auditor
        omega = self.group.random(ZR)
        comf = pp['g'] ** omega
        for i in range(1,len(f)+1):
            comf = comf * (pp['gi'][i] ** f[i])
        usk1 = self.group.random(ZR)
        usk2 = self.group.random(ZR)
        usk3 = self.group.random(ZR)
        upk1 = pkA['h'] ** usk1
        upk2 = pkA['g'] ** usk2
        upk3 = pkA['g'] ** usk3
        upk4 = pkA['h0'] ** usk1
        x2prove = (comf,upk1,upk2,upk3,upk4,pkA['h'],pkA['g'],pkA['h0'])
        w2prove = (omega,f,usk1,usk2,usk3)
        # pi_key2 = self.Pikey2Prove(pp, x2prove, w2prove)
        # print(self.Pikey2Verify(pp,x2prove,pi_key2))
        pi_key2 = Pi.Pikey2Prove(self.group, pp, x2prove, w2prove)
        iok = {}
        u = {}
        for i in range(1, len(f) + 1):
            u[i] = self.group.random(ZR)
            iok[i] = (pkA['h'] ** f[i]) * (pkA['h0'] ** u[i])
        xprove = (iok, pkA['h'], pkA['h0'])
        wprove = (f, u)
        pi_key3 = Pi.Pikey1Prove(self.group,pp,xprove,wprove)
        # assisted authority
        #if self.Pikey3Verify(pp,xprove,pi_key3) == 0:
        if Pi.Pikey1Verify(self.group,pp,xprove,pi_key3) == 0:
            return 0
        ok1 = self.group.init(G2, 1)
        ok2 = self.group.init(G2, 1)
        for i in range(1, len(iok) + 1):
            ok1 = ok1 * iok[i] ** skA['s'][i]
            ok2 = ok2 * iok[i] ** skA['t'][i]
        # auditor
        A = self.group.init(G1, 1)
        B = self.group.init(G1, 1)
        for i in range(1, len(f) + 1):
            A = A * pkA['k'][i] ** f[i]
            B = B * pkA['k'][i] ** u[i]
        left = pair(pkA['g'], ok1) * pair(pkA['g0'], ok2)
        right = pair(A, pkA['h']) * pair(B, pkA['h0'])
        if left != right:
            return 0
        sk = {'omega':omega,'f':f,'u':u,'usk1': usk1, 'usk2': usk2, 'usk3': usk3, 'ok1': ok1, 'ok2': ok2}
        pk = {'comf':comf,'upk1': upk1, 'upk2': upk2, 'upk3': upk3, 'upk4': upk4, 'pi_key2': pi_key2}
        return sk,pk
    def KGenVer(self,pp,pkA,pk):
        xprove = (pk['comf'], pk['upk1'], pk['upk2'], pk['upk3'], pk['upk4'], pkA['h'], pkA['g'], pkA['h0'])
        if Pi.Pikey2Verify(self.group,pp,xprove,pk['pi_key2']):
            return 1
        return 0

    def Escrow(self,pp,pkA,pk,x,rx):
        W = self.group.init(G2,1)
        Wj = {}
        for j in range(1,len(x)+1):
            W = W * (pp['hi'][pp['l']-j+1] ** x[j])
            Wjj = self.group.init(G2,1)
            for i in range(1,j):
                Wjj = Wjj * (pp['hi'][pp['l']-i+j+1] ** x[i])
            for i in range(j+1,len(x)+1):
                Wjj = Wjj * (pp['hi'][pp['l']-i+j+1] ** x[i])
            Wj[j] = Wjj
        c1 = {}
        c2 = {}
        r = self.group.random(ZR)
        r1 = self.group.random(ZR)
        upk1r = pk['upk1']**r
        upk4r = pk['upk4'] ** r
        for i in range(1,len(x)+1):
            c1i = (pkA['egh'] ** x[i]) * pair(pkA['k'][i],upk1r)
            c1[i] = c1i
            c2i = pair(pkA['k'][i], upk4r)
            c2[i] = c2i
        c3 = pkA['g'] ** r1
        c4 = (pkA['g'] ** r) * (pk['upk2'] ** r1)
        c5 = (pkA['g0'] ** r) * (pk['upk3'] ** r1)
        Cx = pp['v']**rx
        for i in range(1, len(x) + 1):
            Cx = Cx * (pp['vi'][i] ** x[i])
        xprove = (W, Wj,c1,c2,c3,c4,c5,Cx, pkA, pk)
        wprove = (x,r,r1,rx)
        pi_E = Pi.PiEProve(self.group,pp,xprove,wprove)

        E = {'W':W,'Wj':Wj,'c1':c1,'c2':c2,'c3':c3,'c4':c4,'c5':c5,'pi_E':pi_E,'xprove':xprove}
        return E,Cx

    def EscrowVer(self,pp,pkA,pk,E,Cx):
        if Pi.PiEVerify(self.group,pp,E['xprove'],E['pi_E']):
            return 1
        return 0
    def Dec(self,pp,pkA,sk,pk,E,Cx):
        num = self.group.init(GT,1)
        for i in range(1, pp['l']+1):
            num = num * (E['c1'][i]**sk['f'][i]) * (E['c2'][i]**sk['u'][i])
        den = pair(E['c4']/(E['c3']**sk['usk2']),sk['ok1']) * pair(E['c5']/(E['c3']**sk['usk3']),sk['ok2'])
        y = num/(den**sk['usk1'])
        pi = E['W'] ** sk['omega']
        for j in range(1, pp['l']+ 1):
            pi = pi * (E['Wj'][j] ** sk['f'][j])
        return y,pi
    def DecwithBSGS(self,pp,pkA,sk,pk,E,Cx,L1,L2,n):
        num = self.group.init(GT,1)
        for i in range(1, pp['l']+1):
            num = num * (E['c1'][i]**sk['f'][i]) * (E['c2'][i]**sk['u'][i])
        den = pair(E['c4']/(E['c3']**sk['usk2']),sk['ok1']) * pair(E['c5']/(E['c3']**sk['usk3']),sk['ok2'])
        c = num/(den**sk['usk1'])
        y = self.BSGScompute(c, L1, L2, n)
        pi = E['W'] ** sk['omega']
        for j in range(1, pp['l']+ 1):
            pi = pi * (E['Wj'][j] ** sk['f'][j])
        return y,pi
    def Judge(self,pp,pk,E,Cx,y,pi):
        if pair(pk['comf'],E['W']) == (pp['eg1hl']**int(y)) * pair(pp['g'],pi):
            return 1
        return 0
    def Update(self,pp,skA,pkA,f1,sk,pk):
        # auditor
        omega = self.group.random(ZR)
        comf1 = pp['g'] ** omega
        for i in range(1,len(f1)+1):
            comf1 = comf1 * (pp['gi'][i] ** f1[i])
        x2prove = (comf1,pk['upk1'],pk['upk2'],pk['upk3'],pk['upk4'],pkA['h'],pkA['g'],pkA['h0'])
        w2prove = (omega,f1,sk['usk1'],sk['usk2'],sk['usk3'])
        # pi_key2 = self.Pikey2Prove(pp, x2prove, w2prove)
        # print(self.Pikey2Verify(pp,x2prove,pi_key2))
        pi_key2 = Pi.Pikey2Prove(self.group, pp, x2prove, w2prove)
        iok = {}
        u = {}
        for i in range(1, len(f1) + 1):
            u[i] = self.group.random(ZR)
            iok[i] = (pkA['h'] ** f1[i]) * (pkA['h0'] ** u[i])
        xprove = (iok, pkA['h'], pkA['h0'])
        wprove = (f1, u)
        pi_key3 = Pi.Pikey1Prove(self.group,pp,xprove,wprove)
        # assisted authority
        #if self.Pikey3Verify(pp,xprove,pi_key3) == 0:
        if Pi.Pikey1Verify(self.group,pp,xprove,pi_key3) == 0:
            return 0
        ok1 = self.group.init(G2, 1)
        ok2 = self.group.init(G2, 1)
        for i in range(1, len(iok) + 1):
            ok1 = ok1 * iok[i] ** skA['s'][i]
            ok2 = ok2 * iok[i] ** skA['t'][i]
        # auditor
        A = self.group.init(G1, 1)
        B = self.group.init(G1, 1)
        for i in range(1, len(f1) + 1):
            A = A * pkA['k'][i] ** f1[i]
            B = B * pkA['k'][i] ** u[i]
        left = pair(pkA['g'], ok1) * pair(pkA['g0'], ok2)
        right = pair(A, pkA['h']) * pair(B, pkA['h0'])
        if left != right:
            return 0
        sk['omega'] = omega
        sk['f'] = f1
        sk['u'] = u
        sk['ok1'] = ok1
        sk['ok2'] = ok2
        pk['comf'] = comf1
        pk['pi_key2'] = pi_key2
        return sk,pk


number = 100

