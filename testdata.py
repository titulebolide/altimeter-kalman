import numpy as np
import random

class TestData:
    def __init__(self, dt):
        self.P_0 = 102500
        self.z = 1000
        self.zmin = 500
        self.zmax = 1500
        self.vz = 0
        self.vzmin = -10
        self.vzmax = 10
        self.az = 0
        self.az_capt = self.az
        self.dt = dt
        self.p = self.ztop(self.z)
        self.p_capt = self.p
        self.az_capt_std_dev = 0.1
        self.p_capt_std_dev = 3
        self.vz_baro = 0
        self.z_gps = self.z
        self.std_dev_gps = 10
        self.record = {}

    def walls(self,t):
        return ((t-0.5)*2)**3

    def ztop(self,z, tsea = 288):
        return self.P_0*np.exp(-0.02897*9.81*z/8.314/tsea)

    def ptoz(self,p, tsea = 288):
        return - 8.314*tsea/0.02897/9.81*np.log(p/self.P_0)

    def update(self):
        daz = random.random() - 0.5 - 0.1*self.walls((self.z-self.zmin)/(self.zmax-self.zmin))
        daz = daz - self.az*0.2 - 0.05*self.walls((self.vz-self.vzmin)/(self.vzmax-self.vzmin))
        self.az = self.az + self.dt*daz
        self.vz = self.vz + self.dt*self.az
        self.z = self.z + self.dt*self.vz
        self.p = self.ztop(self.z)
        old_p = self.p_capt
        self.p_capt = self.p_capt + self.dt*(self.p - self.p_capt) + np.random.normal(scale = self.p_capt_std_dev)
        self.az_capt = self.az + np.random.normal(scale = self.az_capt_std_dev)
        self.vz_baro = (self.ptoz(self.p_capt) - self.ptoz(old_p))/self.dt
        self.z_gps = self.z + + np.random.normal(scale = self.std_dev_gps)
        
        for att in dir(self):
            if not att.startswith("_"):
                value = getattr(self, att)
                if type(value) in (float, int, np.float64):
                    if not att in self.record:
                        self.record[att] = []
                    self.record[att].append(value)
