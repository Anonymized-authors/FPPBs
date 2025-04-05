from charm.toolbox.pairinggroup import PairingGroup, G1, G2, GT, pair, ZR
def PiEProve(group, pp, xprove, wprove):
    (W, Wj, c1, c2, c3, c4, c5, Cx, pkA, pk) = xprove
    (x, r, r1, rx) = wprove
    rho = {}
    tau = group.random(ZR)
    tau1 = group.random(ZR)
    taurx = group.random(ZR)
    for i in range(1, pp['l'] + 1):
        rho[i] = group.random(ZR)
    T = group.init(G2, 1)
    T1 = {}
    for j in range(1, pp['l'] + 1):
        T = T * (pp['hi'][pp['l'] - j + 1] ** rho[j])
        T1j = group.init(G2, 1)
        for i in range(1, j):
            T1j = T1j * (pp['hi'][pp['l'] - i + j + 1] ** rho[i])
        for i in range(j + 1, pp['l'] + 1):
            T1j = T1j * (pp['hi'][pp['l'] - i + j + 1] ** rho[i])
        T1[j] = T1j
    upk1tau = pk['upk1'] ** tau
    upk4tau = pk['upk4'] ** tau
    T2 = {}
    T3 = {}
    T4 = pkA['g'] ** tau1
    T5 = (pkA['g'] ** tau) * (pk['upk2'] ** tau1)
    T6 = (pkA['g0'] ** tau) * (pk['upk3'] ** tau1)
    T7 = pp['v'] ** taurx
    for i in range(1, pp['l'] + 1):
        T2i = (pkA['egh'] ** rho[i]) * pair(pkA['k'][i], upk1tau)
        T2[i] = T2i
        T3i = pair(pkA['k'][i], upk4tau)
        T3[i] = T3i
        T7 = T7 * (pp['vi'][i] ** rho[i])
    e = group.hash(str(xprove) + str(T) + str(T1) + str(T2) + str(T3) + str(T4) + str(T5) + str(T6) + str(T7), ZR)
    z1 = {}
    z2 = tau - e * r
    z21 = tau1 - e * r1
    z22 = taurx - e * rx
    for i in range(1, pp['l'] + 1):
        z1[i] = rho[i] - (e * x[i])
    pi_E = {'T': T, 'T1': T1, 'T2': T2, 'T3': T3, 'T4': T4, 'T5': T5, 'T6': T6, 'T7': T7, 'z1': z1, 'z2': z2, 'z21': z21, 'z22': z22}
    return pi_E


def PiEVerify(group, pp, xprove, pi_E):
    (W, Wj, c1, c2, c3, c4, c5, Cx, pkA, pk) = xprove
    e = group.hash(str(xprove) + str(pi_E['T']) + str(pi_E['T1']) + str(pi_E['T2']) + str(pi_E['T3']) + str(pi_E['T4']) + str(pi_E['T5']) + str(pi_E['T6']) + str(pi_E['T7']), ZR)
    T = W ** e
    T1 = {}
    for j in range(1, pp['l'] + 1):
        T = T * (pp['hi'][pp['l'] - j + 1] ** pi_E['z1'][j])
        T1j = Wj[j] ** e
        for i in range(1, j):
            T1j = T1j * (pp['hi'][pp['l'] - i + j + 1] ** pi_E['z1'][i])
        for i in range(j + 1, pp['l'] + 1):
            T1j = T1j * (pp['hi'][pp['l'] - i + j + 1] ** pi_E['z1'][i])
        T1[j] = T1j
    upk1z2 = pk['upk1'] ** pi_E['z2']
    upk4z2 = pk['upk4'] ** pi_E['z2']
    T2 = {}
    T3 = {}
    T4 = (c3 ** e) * (pkA['g'] ** pi_E['z21'])
    T5 = (c4 ** e) * (pkA['g'] ** pi_E['z2']) * (pk['upk2'] ** pi_E['z21'])
    T6 = (c5 ** e) * (pkA['g0'] ** pi_E['z2']) * (pk['upk3'] ** pi_E['z21'])
    T7 = (Cx ** e) * (pp['v'] ** pi_E['z22'])
    for i in range(1, pp['l'] + 1):
        T2i = (c1[i] ** e) * (pkA['egh'] ** pi_E['z1'][i]) * pair(pkA['k'][i], upk1z2)
        T2[i] = T2i
        T3i = (c2[i] ** e) * pair(pkA['k'][i], upk4z2)
        T3[i] = T3i
        T7 = T7 * (pp['vi'][i] ** pi_E['z1'][i])
    if T == pi_E['T'] and T1 == pi_E['T1'] and T2 == pi_E['T2'] and T3 == pi_E['T3'] and T4 == pi_E['T4'] and T5 == pi_E['T5'] and T6 == pi_E['T6'] and T7 == pi_E['T7']:
        #print("Pi E verified")
        return 1
    #print("Pi E failed")
    return 0
def Pikey2Prove(group, pp, xprove, wprove):
    (comf, upk1, upk2, upk3, upk4, h, g, h0) = xprove
    (omega, f, usk1, usk2, usk3) = wprove
    rho = {}
    tau = group.random(ZR)
    tau1 = group.random(ZR)
    tau2 = group.random(ZR)
    tau3 = group.random(ZR)
    T1 = h ** tau1
    T2 = g ** tau2
    T3 = g ** tau3
    T4 = h0 ** tau1
    T = g ** tau
    for i in range(1, pp['l'] + 1):
        rhoi = group.random(ZR)
        rho[i] = rhoi
        T = T * (pp['gi'][i] ** rhoi)
    e = group.hash(str(xprove) + str(T) + str(T1) + str(T2) + str(T3) + str(T4), ZR)
    z1 = {}
    z2 = tau - e * omega
    z21 = tau1 - e * usk1
    z22 = tau2 - e * usk2
    z23 = tau3 - e * usk3
    for i in range(1, pp['l'] + 1):
        z1[i] = rho[i] - e * f[i]
    pi_key2 = {'T': T, 'T1': T1, 'T2': T2, 'T3': T3, 'T4': T4, 'z1': z1, 'z2': z2, 'z21': z21, 'z22': z22, 'z23': z23}
    return pi_key2


def Pikey2Verify(group, pp, xprove, pi_key2):
    (comf, upk1, upk2, upk3, upk4, h, g, h0) = xprove
    e = group.hash(str(xprove) + str(pi_key2['T']) + str(pi_key2['T1']) + str(pi_key2['T2']) + str(pi_key2['T3']) + str(pi_key2['T4']), ZR)
    T = (g ** pi_key2['z2']) * (comf ** e)
    for i in range(1, pp['l'] + 1):
        T = T * (pp['gi'][i] ** pi_key2['z1'][i])
    T1 = (upk1 ** e) * (h ** pi_key2['z21'])
    T2 = (upk2 ** e) * (g ** pi_key2['z22'])
    T3 = (upk3 ** e) * (g ** pi_key2['z23'])
    T4 = (upk4 ** e) * (h0 ** pi_key2['z21'])
    if T == pi_key2['T'] and T1 == pi_key2['T1'] and T2 == pi_key2['T2'] and T3 == pi_key2['T3'] and T4 == pi_key2['T4']:
        #print("Pi key2 verified")
        return 1
    #print("Pi key2 failed")
    return 0


def Pikey1Prove(group, pp, xprove, wprove):
    (k, g, g0) = xprove
    (s, t) = wprove
    rho = {}
    tau = {}
    T = {}
    for i in range(1, pp['l'] + 1):
        rhoi = group.random(ZR)
        taui = group.random(ZR)
        rho[i] = rhoi
        tau[i] = taui
        Ti = (g ** rhoi) * (g0 ** taui)
        T[i] = Ti
    e = group.hash(str(xprove) + str(T), ZR)
    z1 = {}
    z2 = {}
    for i in range(1, pp['l'] + 1):
        z1[i] = rho[i] - e * s[i]
        z2[i] = tau[i] - e * t[i]
    pi_key1 = {'T': T, 'z1': z1, 'z2': z2}
    return pi_key1


def Pikey1Verify(group, pp, xprove, pi_key1):
    (k, g, g0) = xprove
    T = {}
    e = group.hash(str(xprove) + str(pi_key1['T']), ZR)
    for i in range(1, pp['l'] + 1):
        Ti = (k[i] ** e) * (g ** pi_key1['z1'][i]) * (g0 ** pi_key1['z2'][i])
        T[i] = Ti
    if T == pi_key1['T']:
        #print("Pi key1 verified")
        return 1
    #print("Pi key1 failed")
    return 0
