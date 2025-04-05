from charm.core.math.elliptic_curve import G, ZR
from charm.toolbox.ecgroup import ECGroup, elliptic_curve
from charm.toolbox.eccurve import secp256k1, secp160k1, prime256v1
def PiUProve(group, pp, xprove, wprove):
    (h, ci) = xprove
    (x, y, r) = wprove
    xrho = group.random(ZR)
    rho = {} # y
    tau = {} # r
    for i in range(1, pp['l'] + 1):
        rho[i] = group.random(ZR)
        tau[i] = group.random(ZR)
    T = pp['g']**xrho
    T1 = {}
    T2 = {}
    for i in range(1, pp['l'] + 1):
        c1i = pp['g'] ** tau[i]
        c2i = (pp['f'] ** rho[i]) * (h ** tau[i])
        T1[i] = c1i
        T2[i] = c2i
    e = group.hash(str(xprove)+str(T)+str(T1)+str(T2),ZR)
    z1 = {}
    z2 = {}
    z = xrho - e * x
    for i in range(1, pp['l'] + 1):
        z1[i] = rho[i] - (e * y[i])
        z2[i] = tau[i] - (e * r[i])
    piU = {'T': T, 'T1': T1, 'T2': T2, 'z1': z1, 'z2': z2, 'z': z}
    return piU
def PiUVerify(group, pp, xprove, piU):
    (h, ci) = xprove
    e = group.hash(str(xprove) + str(piU['T'])+ str(piU['T1'])+ str(piU['T2']), ZR)
    T = (h ** e) * (pp['g'] ** piU['z'])
    T1 = {}
    T2 = {}
    for i in range(1, pp['l'] + 1):
        T1i = (ci[i][0] ** e) * (pp['g'] ** piU['z2'][i])
        T2i = (ci[i][1] ** e) * (pp['f'] ** piU['z1'][i]) * (h ** piU['z2'][i])
        T1[i] = T1i
        T2[i] = T2i
    if T == piU['T'] and T1 == piU['T1'] and T2 == piU['T2']:
        return 1
    return 0
def PiAUTProve(group, pp, xprove, wprove):
    (c1sky, c2sky, hi,h,ci) = xprove
    (msk, r1) = wprove
    r1rho = group.random(ZR)
    rho = {}  # msk
    for i in range(1, pp['l'] + 1):
        rho[i] = group.random(ZR)
    T = {}
    T1 = pp['g'] ** r1rho
    T2 = h ** r1rho
    for i in range(1, pp['l'] + 1):
        Ti = pp['g'] ** rho[i]
        T1 = T1 * (ci[i][0] ** rho[i])
        T2 = T2 * (ci[i][1] ** rho[i])
        T[i] = Ti
    e = group.hash(str(xprove) +str(T)+ str(T1) + str(T2), ZR)
    z1 = {}
    z = r1rho - e * r1
    for i in range(1, pp['l'] + 1):
        z1[i] = rho[i] - (e * msk[i])
    piAUT = {'T': T, 'T1': T1, 'T2': T2, 'z1': z1, 'z': z}
    return piAUT
def PiAUTVerify(group, pp, xprove, piAUT):
    (c1sky, c2sky, hi,h,ci) = xprove
    e = group.hash(str(xprove) + str(piAUT['T'])+ str(piAUT['T1'])+ str(piAUT['T2']), ZR)
    T = {}
    T1 = (c1sky ** e) * (pp['g'] ** piAUT['z'])
    T2 = (c2sky ** e) * (h ** piAUT['z'])
    for i in range(1, pp['l'] + 1):
        Ti = (hi[i] ** e) * (pp['g'] ** piAUT['z1'][i])
        T[i] = Ti
        T1 = T1 * (ci[i][0] ** piAUT['z1'][i])
        T2 = T2 * (ci[i][1] ** piAUT['z1'][i])
    if T == piAUT['T'] and T1 == piAUT['T1'] and T2 == piAUT['T2']:
        return 1
    return 0
