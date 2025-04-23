from timeit import default_timer as timer
from Crypto.Random import random
import PPFE as IP_PPFE
number = 100
p1 = 2 ** 10
def Correctnesstest(Instantiation):
    l=3
    mpk, msk = Instantiation.setup(l)
    usk, upk = Instantiation.UKGen(mpk)
    f = []
    x = []
    y = 0
    for i in range(l):
        fi = random.randint(0, p1)
        xi = random.randint(0, p1)
        y = y + fi * xi
        f.append(fi)
        x.append(xi)
    idk, aux = Instantiation.IDKGen(mpk, f)
    dk = Instantiation.DKGen(msk, idk)
    if Instantiation.DKVer(mpk, dk, aux, f) == 0:
        print("Decryption key verification fails!")
    else:
        print("Decryption key verification successes!")
    C = Instantiation.Enc(mpk, x, upk)
    L1, L2, n = Instantiation.BSGSinitlist(mpk['egh'])
    y1 = Instantiation.DecwithBSGS(mpk, dk, aux, usk, C, f,L1,L2,n)
    if y1 != y:
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
def UKGentest(Instantiation):
    t = 0
    mpk, msk = Instantiation.setup(l)
    for i in range(number):
        start = timer()
        Instantiation.UKGen(mpk)
        end = timer()
        t = t + (end - start)
    print(t*1000/number)

def IDKGentest(Instantiation,l):
    t = 0
    mpk, msk = Instantiation.setup(l)
    f = []
    for i in range(l):
        fi = 2**32 - i
        f.append(fi)
    for i in range(number):
        start = timer()
        Instantiation.IDKGen(mpk,f)
        end = timer()
        t = t + (end - start)
    print(str(l) + "   " + str(t*1000/number))

def DKGentest(Instantiation,l):
    t = 0
    mpk, msk = Instantiation.setup(l)
    f = []
    for i in range(l):
        fi = 2**32 - i
        f.append(fi)
    idk, aux = Instantiation.IDKGen(mpk, f)
    for i in range(number):
        start = timer()
        Instantiation.DKGen(msk,idk)
        end = timer()
        t = t + (end - start)
    print(str(l) + "   " + str(t*1000/number))

def DKVertest(Instantiation,l):
    t = 0
    mpk, msk = Instantiation.setup(l)
    f = []
    for i in range(l):
        fi = 2**32 - i
        f.append(fi)
    idk, aux = Instantiation.IDKGen(mpk, f)
    dk = Instantiation.DKGen(msk,idk)
    for i in range(number):
        start = timer()
        Instantiation.DKVer(mpk,dk,aux,f)
        end = timer()
        t = t + (end - start)
    print(str(l) + "   " + str(t*1000/number))

def Enctest(Instantiation,l):
    t = 0
    mpk, msk = Instantiation.setup(l)
    usk, upk = Instantiation.UKGen(mpk)
    x = []
    for i in range(l):
        xi = 2**32 - i
        x.append(xi)
    for i in range(number):
        start = timer()
        Instantiation.Enc(mpk,x,upk)
        end = timer()
        t = t + (end - start)
    print(str(l) + "   " + str(t*1000/number))

def Dectest(Instantiation,l):
    t = 0
    mpk, msk = Instantiation.setup(l)
    usk, upk = Instantiation.UKGen(mpk)
    f = []
    x = []
    for i in range(l):
        fi = 2**32 - i
        xi = 2**32 - i
        f.append(fi)
        x.append(xi)
    idk, aux = Instantiation.IDKGen(mpk, f)
    dk = Instantiation.DKGen(msk, idk)
    C = Instantiation.Enc(mpk, x, upk)
    for i in range(number):
        start = timer()
        Instantiation.Dec(mpk,dk,aux,usk,C,f)
        end = timer()
        t = t + (end - start)
    print(str(l) + "   " + str(t*1000/number))
if __name__ == '__main__':
    Instantiation = IP_PPFE.PPFE()
    l = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

    Correctnesstest(Instantiation)

    print("Setuptest:")
    for i in l:
        Setuptest(Instantiation,i)

    print("UKGentest:")
    UKGentest(Instantiation)

    print("IDKGentest:")
    for i in l:
        IDKGentest(Instantiation,i)

    print("DKGentest:")
    for i in l:
        DKGentest(Instantiation,i)

    print("DKVertest:")
    for i in l:
        DKVertest(Instantiation,i)

    print("Enctest:")
    for i in l:
        Enctest(Instantiation,i)

    print("Dectest:")
    for i in l:
        Dectest(Instantiation,i)