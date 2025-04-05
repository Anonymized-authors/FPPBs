from timeit import default_timer as timer
from Crypto.Random import random
import BFE as IP_BFE
number = 100
p1 = 2 ** 10

def Correctnesstest(Instantiation):
    l=3
    pp,msk = Instantiation.setup(l)
    y = {}
    sy = 0
    for i in range(1, l + 1):
        yi = random.randint(0, p1)
        sy = sy + msk[i] * yi
        y[i] = yi
    sy1 = Instantiation.KDerwithBSGS(pp,y,msk)
    if sy1 != sy:
        print("Key derivation fails!!!")
    print("Key derivation successes!!!")

def KDertest(Instantiation,l):
    t = 0
    pp,msk = Instantiation.setup(l)
    y = {}
    for i in range(1, l + 1):
        yi = random.randint(0, p1)
        y[i] = yi
    for i in range(number):
        start = timer()
        Instantiation.KDer(pp,y,msk)
        end = timer()
        t = t + (end - start)
    print(str(l) + "   " + str(t*1000/number))


if __name__ == '__main__':
    Instantiation = IP_BFE.BFE()
    l = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

    Correctnesstest(Instantiation)

    print("KDertest:")
    for i in l:
        KDertest(Instantiation,i)

