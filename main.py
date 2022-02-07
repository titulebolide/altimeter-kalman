import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import threading
from testdata import TestData
from models.model1 import model, data_index

dt = 1/10
td = TestData(dt)

U = np.array([[0]])
Z = np.array([[0]])

f, F, h, H, X, P, Q, R, get_U_Z = model(td,dt)

Xs = []
Ps = []
time = []

fig = plt.figure()
axs = []
for i in range(2):
    axs.append(fig.add_subplot(1,2,i+1))

def handle_data():
    global U,Z,X,F,f,P,Q,R,H,h,Xs,time

    if len(time) == 0:
        time.append(0)
    else:
        time.append(time[-1] + td.dt)

    U,Z = get_U_Z(td)

    Xkkm = f(X,U)
    Pkkm = F(X,U)@P@F(X,U).transpose() + Q
    v = Z - h(Xkkm)
    S = H(Xkkm)@Pkkm@H(Xkkm).transpose() + R
    K = Pkkm@H(Xkkm).transpose()@np.linalg.inv(S)
    X = Xkkm + K@v
    P = Pkkm - K@H(Xkkm)@Pkkm

    ##Save data
    Xs.append(X.tolist())
    Ps.append(P.tolist())

    td.update()

def animate(i):
    global U,Z,X,F,f,P,Q,R,H,h,Xs,axs,time,use_file

    for ax in axs:
        ax.clear()

    Xsarr = np.array(Xs)
    vz_baro_arr = np.array(td.record['vz_baro'])

    ax = axs[0]
    ax.plot(time, td.record["z_gps"], label="GPS")
    ax.plot(time, Xsarr[:,0,0], label="Kalman")
    ax.plot(time, td.record["z"], label="True")
    ax.legend()
    ax.set_title("z")

    ax = axs[1]
    ax.plot(time[1:], (Xsarr[1:,0,0] - Xsarr[:-1,0,0])/td.dt, label="Kalman")
    ax.plot(time, td.record["vz_baro"], label="Baro")
    ax.legend()
    ax.set_title("vz")


if __name__ == "__main__":
    for _ in range(1000):
        handle_data()
    animate(0)
    plt.show()
