from timeit import default_timer as timer
from Crypto.Random import random
from charm.toolbox.pairinggroup import PairingGroup,G1,G2,GT,pair,ZR
import FPPB as IP_FPPB
number = 100
p1 = 2 ** 10
def Correctnesstest(Instantiation):
    l = 3
    rx = Instantiation.randomZr()
    pp = Instantiation.setup(l)
    pkA, skA = Instantiation.AKGen(pp)
    f = {}
    x = {}
    y = 0
    for i in range(1, l + 1):
        fi = random.randint(0,p1)
        xi = random.randint(0,p1)
        y = y + fi * xi
        f[i] = fi
        x[i] = xi
    if Instantiation.AKGenVer(pp, pkA) == 0:
        print("Assisted authority key verification fails!")
    else:
        print("Assisted authority key verification successes!")
    sk, pk = Instantiation.KGen(pp, skA, pkA, f)
    if Instantiation.KGenVer(pp, pkA, pk) == 0:
        print("Auditor key verification fails!")
    else:
        print("Auditor key verification successes!")
    L1, L2, n = Instantiation.BSGSinitlist(pkA['egh'])
    E, Cx = Instantiation.Escrow(pp, pkA, pk, x, rx)
    if Instantiation.EscrowVer(pp, pkA, pk, E, Cx) == 0:
        print("Escrow verification fails!")
    else:
        print("Escrow verification successes!")
    y1, pi = Instantiation.DecwithBSGS(pp, pkA, sk, pk, E, Cx,L1,L2,n)
    if y1 != y or Instantiation.Judge(pp, pk, E, Cx, y1, pi) == 0:
        print("Decryption fails!!!")
    else:
        print("Decryption successes!!!")
    
    

def Setuptest(Instantiation,l):
    t = 0
    for i in range(number):
        start = timer()
        Instantiation.setup(l)
        end = timer()
        t = t + (end - start)
    print(str(l) + "   " + str(t*1000/number))
def AKGentest(Instantiation,l):
    t = 0
    pp = Instantiation.setup(l)
    for i in range(number):
        start = timer()
        Instantiation.AKGen(pp)
        end = timer()
        t = t + (end - start)
    print(str(l) + "   " + str(t*1000/number))

def AKGenVertest(Instantiation,l):
    t = 0
    pp = Instantiation.setup(l)
    pkA, skA = Instantiation.AKGen(pp)
    for i in range(number):
        start = timer()
        Instantiation.AKGenVer(pp,pkA)
        end = timer()
        t = t + (end - start)
    print(str(l) + "   " + str(t*1000/number))

def Updatetest(Instantiation,l):
    t = 0
    pp = Instantiation.setup(l)
    pkA, skA = Instantiation.AKGen(pp)
    f = {}
    for i in range(1, l + 1):
        fi = random.randint(0,p1)
        f[i] = fi
    sk, pk = Instantiation.KGen(pp, skA, pkA, f)
    for i in range(number):
        start = timer()
        Instantiation.Update(pp,skA,pkA,f,sk,pk)
        end = timer()
        t = t + (end - start)
    print(str(l) + "   " + str(t*1000/number))

def KGentest(Instantiation,l):
    t = 0
    pp = Instantiation.setup(l)
    pkA, skA = Instantiation.AKGen(pp)
    f = {}
    for i in range(1, l + 1):
        fi = random.randint(0,p1)
        f[i] = fi
    for i in range(number):
        start = timer()
        Instantiation.KGen(pp,skA,pkA,f)
        end = timer()
        t = t + (end - start)
    print(str(l) + "   " + str(t*1000/number))

def KGenVertest(Instantiation,l):
    t = 0
    pp = Instantiation.setup(l)
    pkA, skA = Instantiation.AKGen(pp)
    f = {}
    for i in range(1, l + 1):
        fi = random.randint(0,p1)
        f[i] = fi
    sk, pk = Instantiation.KGen(pp, skA, pkA, f)
    for i in range(number):
        start = timer()
        Instantiation.KGenVer(pp,pkA,pk)
        end = timer()
        t = t + (end - start)
    print(str(l) + "   " + str(t*1000/number))
    
def Escrowtest(Instantiation,l):
    t = 0
    x = {}
    f = {}
    pp = Instantiation.setup(l)
    rx = Instantiation.randomZr()
    pkA, skA = Instantiation.AKGen(pp)
    for i in range(1, l + 1):
        xi = random.randint(0,p1)
        x[i] = xi
        fi = random.randint(0,p1)
        f[i] = fi
    sk, pk = Instantiation.KGen(pp,skA,pkA,f)
    for i in range(number):
        start = timer()
        Instantiation.Escrow(pp,pkA,pk,x,rx)
        end = timer()
        t = t + (end - start)
    print(str(l) + "   " + str(t*1000/number))
    
def EscrowVertest(Instantiation,l):
    t = 0
    x = {}
    f = {}
    pp = Instantiation.setup(l)
    rx = Instantiation.randomZr()
    pkA, skA = Instantiation.AKGen(pp)
    for i in range(1, l + 1):
        xi = random.randint(0,p1)
        x[i] = xi
        fi = random.randint(0,p1)
        f[i] = fi
    sk, pk = Instantiation.KGen(pp,skA,pkA,f)
    E, Cx = Instantiation.Escrow(pp, pkA, pk, x, rx)
    for i in range(number):
        start = timer()
        Instantiation.EscrowVer(pp,pkA,pk,E,Cx)
        end = timer()
        t = t + (end - start)
    print(str(l) + "   " + str(t*1000/number))
    
def Dectest(Instantiation,l):
    t = 0
    x = {}
    f = {}
    pp = Instantiation.setup(l)
    rx = Instantiation.randomZr()
    pkA, skA = Instantiation.AKGen(pp)
    for i in range(1, l + 1):
        xi = random.randint(0,p1)
        x[i] = xi
        fi = random.randint(0,p1)
        f[i] = fi
    sk, pk = Instantiation.KGen(pp, skA, pkA, f)
    E, Cx = Instantiation.Escrow(pp, pkA, pk, x, rx)
    for i in range(number):
        start = timer()
        Instantiation.Dec(pp,pkA,sk,pk,E,Cx)
        end = timer()
        t = t + (end - start)
    print(str(l) + "   " + str(t*1000/number))

def Judgetest(Instantiation):
    t = 0
    l = 10
    x = {}
    f = {}
    y = 0
    pp = Instantiation.setup(l)
    rx = Instantiation.randomZr()
    pkA, skA = Instantiation.AKGen(pp)
    for i in range(1, l + 1):
        xi = random.randint(0,p1)
        x[i] = xi
        fi = random.randint(0,p1)
        f[i] = fi
        y = y + fi * xi
    sk, pk = Instantiation.KGen(pp, skA, pkA, f)
    E, Cx = Instantiation.Escrow(pp, pkA, pk, x, rx)
    y1, pi = Instantiation.Dec(pp,pkA,sk,pk,E,Cx)
    for i in range(number):
        start = timer()
        Instantiation.Judge(pp,pk,E,Cx,y,pi)
        end = timer()
        t = t + (end - start)
    print(str(t*1000/number))
    
if __name__ == '__main__':
    Instantiation = IP_FPPB.FPPB()
    number = 100
    l = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

    Correctnesstest(Instantiation)

    print("Setuptest:")
    for i in l:
        Setuptest(Instantiation,i)
        
    print("AKGentest:")
    for i in l:
        AKGentest(Instantiation,i)
        
    print("AKGenVertest:")
    for i in l:
        AKGenVertest(Instantiation,i)
        
    print("KGentest:")
    for i in l:
        KGentest(Instantiation,i)
        
    print("KGenVertest:")
    for i in l:
        KGenVertest(Instantiation,i)
        
    print("Escrowtest:")
    for i in l:
        Escrowtest(Instantiation,i)
        
    print("EscrowVertest:")
    for i in l:
        EscrowVertest(Instantiation,i)
        
    print("Dectest:")
    for i in l:
        Dectest(Instantiation,i)
        
    print("Judgetest:")
    Judgetest(Instantiation)
    
    print("Updatetest:")
    for i in l:
        Updatetest(Instantiation,i)
