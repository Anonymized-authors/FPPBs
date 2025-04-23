
from timeit import default_timer as timer

from Crypto.Random import random
from charm.toolbox.pairinggroup import PairingGroup,G1,G2,GT,pair,ZR
import PPFC as IP_PPFC
number = 100
p1 = 2 ** 10
def Correctnesstest(Instantiation):
    l = 3
    ck = Instantiation.setup(l)
    apk, ask = Instantiation.AKGen(ck)
    f = {}
    x = {}
    y = 0
    for i in range(1, l + 1):
        fi = random.randint(0,p1)
        xi = random.randint(0,p1)
        y = y + fi * xi
        f[i] = fi
        x[i] = xi
    com, d = Instantiation.Com(ck, apk, f)
    iok, aux = Instantiation.IOKGen(apk, f)
    ok = Instantiation.OKGen(ask, iok)
    if Instantiation.OKVer(apk, ok, aux, f) == 0:
        print("Open key verification fails!")
    else:
        print("Open key verification successes!")
    aop, pop = Instantiation.Preopen(ck, apk, x, com)
    L1, L2, n = Instantiation.BSGSinitlist(apk['egh'])
    y1, op = Instantiation.OpenwithBSGS(d, ok, aux, pop, aop,L1,L2,n)
    if y1 != y or Instantiation.Ver(ck, com, y, op, aop) == 0:
        print("Opening fails!!!")
    else:
        print("Opening successes!!!")
    y2, op2, aop2 = Instantiation.Fopen(ck, d, x)
    if y2 != y or Instantiation.Ver(ck, com, y2, op2, aop2) == 0:
        print("Fast Opening fails!!!")
    else:
        print("Fast opening successes!!!")

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
    ck = Instantiation.setup(l)
    for i in range(number):
        start = timer()
        Instantiation.AKGen(ck)
        end = timer()
        t = t + (end - start)
    print(str(l) + "   " + str(t*1000/number))

def Comtest(Instantiation,l):
    t = 0
    ck = Instantiation.setup(l)
    apk, ask = Instantiation.AKGen(ck)
    f = {}
    for i in range(1, l + 1):
        fi = random.randint(0,p1)
        f[i] = fi
    for i in range(number):
        start = timer()
        Instantiation.Com(ck,apk,f)
        end = timer()
        t = t + (end - start)
    print(str(l) + "   " + str(t*1000/number))

def IOKGentest(Instantiation,l):
    t = 0
    ck = Instantiation.setup(l)
    apk, ask = Instantiation.AKGen(ck)
    f = {}
    for i in range(1, l + 1):
        fi = random.randint(0,p1)
        f[i] = fi
    for i in range(number):
        start = timer()
        Instantiation.IOKGen(apk,f)
        end = timer()
        t = t + (end - start)
    print(str(l) + "   " + str(t*1000/number))

def OKGentest(Instantiation,l):
    t = 0
    ck = Instantiation.setup(l)
    apk, ask = Instantiation.AKGen(ck)
    f = {}
    for i in range(1, l + 1):
        fi = random.randint(0,p1)
        f[i] = fi
    idk, aux = Instantiation.IOKGen(apk, f)
    for i in range(number):
        start = timer()
        Instantiation.OKGen(ask,idk)
        end = timer()
        t = t + (end - start)
    print(str(l) + "   " + str(t*1000/number))

def OKVertest(Instantiation,l):
    t = 0
    ck = Instantiation.setup(l)
    apk, ask = Instantiation.AKGen(ck)
    f = {}
    for i in range(1, l + 1):
        fi = random.randint(0,p1)
        f[i] = fi
    idk, aux = Instantiation.IOKGen(apk, f)
    ok = Instantiation.OKGen(ask,idk)
    for i in range(number):
        start = timer()
        Instantiation.OKVer(apk,ok,aux,f)
        end = timer()
        t = t + (end - start)
    print(str(l) + "   " + str(t*1000/number))

def PreOpentest(Instantiation,l):
    t = 0
    x = {}
    f = {}
    ck = Instantiation.setup(l)
    apk, ask = Instantiation.AKGen(ck)
    for i in range(1, l + 1):
        xi = random.randint(0,p1)
        x[i] = xi
        fi = random.randint(0,p1)
        f[i] = fi
    com, d = Instantiation.Com(ck, apk, f)
    for i in range(number):
        start = timer()
        Instantiation.Preopen(ck,apk,x,com)
        end = timer()
        t = t + (end - start)
    print(str(l) + "   " + str(t*1000/number))

def Opentest(Instantiation,l):
    t = 0
    x = {}
    f = {}
    ck = Instantiation.setup(l)
    apk, ask = Instantiation.AKGen(ck)
    for i in range(1, l + 1):
        xi = random.randint(0,p1)
        x[i] = xi
        fi = random.randint(0,p1)
        f[i] = fi
    com, d = Instantiation.Com(ck, apk, f)
    iok, aux = Instantiation.IOKGen(apk, f)
    ok = Instantiation.OKGen(ask, iok)
    aop, pop = Instantiation.Preopen(ck, apk, x, com)
    for i in range(number):
        start = timer()
        Instantiation.Open(d, ok, aux, pop, aop)
        end = timer()
        t = t + (end - start)
    print(str(l) + "   " + str(t*1000/number))
def FOpentest(Instantiation,l):
    t = 0
    x = {}
    f = {}
    ck = Instantiation.setup(l)
    apk, ask = Instantiation.AKGen(ck)
    for i in range(1, l + 1):
        xi = random.randint(0,p1)
        x[i] = xi
        fi = random.randint(0,p1)
        f[i] = fi
    com, d = Instantiation.Com(ck, apk, f)
    for i in range(number):
        start = timer()
        Instantiation.Fopen(ck,d,x)
        end = timer()
        t = t + (end - start)
    print(str(l) + "   " + str(t*1000/number))

def Vertest(Instantiation):
    t = 0
    l = 10
    x = {}
    f = {}
    ck = Instantiation.setup(l)
    apk, ask = Instantiation.AKGen(ck)
    for i in range(1, l + 1):
        xi = random.randint(0,p1)
        x[i] = xi
        fi = random.randint(0,p1)
        f[i] = fi
    com, d = Instantiation.Com(ck, apk, f)
    y, op, aop = Instantiation.Fopen(ck, d, x)
    for i in range(number):
        start = timer()
        Instantiation.Ver(ck,com,y,op,aop)
        end = timer()
        t = t + (end - start)
    print(str(t*1000/number))

if __name__ == '__main__':
    Instantiation = IP_PPFC.PPFC()
    number = 100
    l = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

    Correctnesstest(Instantiation)

    print("Vertest:")
    Vertest(Instantiation)

    print("Setuptest:")
    for i in l:
        Setuptest(Instantiation,i)

    print("AKGentest:")
    for i in l:
        AKGentest(i)

    print("Comtest:")
    for i in l:
        Comtest(Instantiation,i)

    print("IOKGentest:")
    for i in l:
        IOKGentest(Instantiation,i)

    print("OKGentest:")
    for i in l:
        OKGentest(Instantiation,i)

    print("OKVertest:")
    for i in l:
        OKVertest(Instantiation,i)

    print("PreOpentest:")
    for i in l:
        PreOpentest(Instantiation,i)

    print("Opentest:")
    for i in l:
        Opentest(Instantiation,i)

    print("FOpentest:")
    for i in l:
        FOpentest(Instantiation,i)

    print("Vertest:")
    Vertest(Instantiation)