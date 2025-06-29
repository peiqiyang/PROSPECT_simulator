
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import exp1
from modules.calctav import calctav

def prospect_d(N, Cab, Car, Cw, Cm, wl, nr, Kab, Kcar, Kw, Km):
    # 合成吸收系数并加入安全下限，避免 0 或负数造成 exp1 爆炸
    Kall_raw = (Cab * Kab + Car * Kcar + Cw * Kw + Cm * Km) / N
    Kall = np.maximum(Kall_raw, 1e-6)  # 防止除以0或log(0)

    # 透射率计算（精确近似）
    t1 = (1 - Kall) * np.exp(-Kall)
    t2 = Kall**2 * exp1(Kall)
    plt.figure()
    plt.plot(wl,Kall)
    plt.figure()
    tau = t1 + t2

    # 表面光学
    talf = calctav(40, nr)
    ralf = 1 - talf
    t12 = calctav(90, nr)
    r12 = 1 - t12
    t21 = t12 / (nr**2)
    r21 = 1 - t21

    denom = 1 - (r21**2) * (tau**2)
    Ta = talf * tau * t21 / denom
    Ra = ralf + r21 * tau * Ta
    t = t12 * tau * t21 / denom
    r = r12 + r21 * tau * t

    # 多层 Stokes
    D = np.sqrt((1 + r + t) * (1 + r - t) * (1 - r + t) * (1 - r - t))
    rq = r**2
    tq = t**2
    a = (1 + rq - tq + D) / (2 * r)
    b = (1 - rq + tq + D) / (2 * t)
    bNm1 = b**(N - 1)
    bN2 = bNm1**2
    a2 = a**2
    denom2 = a2 * bN2 - 1
    Rsub = a * (bN2 - 1) / denom2
    Tsub = bNm1 * (a2 - 1) / denom2

    j = (r + t >= 1)
    Tsub[j] = t[j] / (t[j] + (1 - t[j]) * (N - 1))
    Rsub[j] = 1 - Tsub[j]

    denom_final = 1 - Rsub * r
    refl = Ra + Ta * Rsub * t / denom_final
    tran = Ta * Tsub / denom_final

    return refl, tran
