import numpy as np

def model(td,dt):
    f = lambda X,U : np.array([
        [X[0,0] + dt*U[0,0]]
    ])
    F = lambda X,U : np.array([
        [1]
    ])
    h = lambda X : np.array([
        [X[0,0]]
    ])
    H = lambda X : np.array([
        [1]
    ])

    X = np.array([
        [1000]
    ])
    P = np.array([
        [10]
    ])**2
    Q = np.array([
        [dt*0.5]
    ])**2
    R = np.array([
        [5]
    ])**2

    def get_U_Z(td):
        return np.array([[td.vz_baro]]),np.array([[td.z_gps]])

    return f, F, h, H, X, P, Q, R, get_U_Z

data_index = {
    "z" : 0
}
