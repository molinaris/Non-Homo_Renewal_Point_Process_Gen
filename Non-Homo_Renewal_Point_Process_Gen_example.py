from scipy.stats import norm
from scipy.signal import convolve
from scipy.ndimage.filters import gaussian_filter
import spkCounting
import numpy as np
import pylab as plt

class Ppg(object):
	def __init__(self, N, dt):
		self.dt 	= dt
		self.aux	= 1
		self.N 		= N
		self.yi 	= 0
		for i in range(N):
			self.aux = self.aux * np.random.uniform()
		self.thres 	= -(1/N)*np.log(self.aux)

	def integrate(self,y):
		spk = 0
		self.yi = self.yi + y*self.dt*1e-3
		if self.yi >= self.thres:
			spk = 1
			self.yi = 0
			self.aux = 1
			for i in range(self.N):
				self.aux = self.aux * np.random.uniform()
			self.thres = -(1/self.N)*np.log(self.aux)
		return spk

## SIMULATION CONFIG
tstop = 10000 #[ms]
dt = 0.05 #[ms]
time = np.arange(0,tstop + dt, dt)
S = np.zeros(len(time), dtype=np.intc)
ppg = Ppg(25,dt)

# Modulating signals
fs = 0.5                                    #Modulating frequency [Hz]
#y = 10*np.sin(2*np.pi*fs*time/1000) + 10   #Sinusoidal
#y = 10 + 5*(time/1000)        
#y = 20*np.ones(len(time))
y = np.interp(time,[0,tstop/2,tstop],[0,50,0])

for i in range(len(time)):
	spk = ppg.integrate(y[i])
	if spk == 1:
		S[i] = 1


window = 100
yest = spkCounting.spkCount(S, time, dt, window)


w = window/dt
spiketrain = S*1e3/dt
yest2 = gaussian_filter(spiketrain, w)

plt.figure()
plt.plot(time,yest, label= 'Spike counting')
plt.plot(time,yest2, label = 'Gaussian filter')
plt.plot(time,y, label = 'Modulation Signal')
plt.legend()
plt.xlabel('Time [ms]')
plt.ylabel('Firing Rate [imps/s]')

plt.plot(time,S)
plt.show()