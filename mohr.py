from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import csv,sys

class Read():
	def __init__(self, promptFileName):
		self.fileName = promptFileName
	
	def readCsv(self):
		stress_Minor = [] #Minor stress
		stress_Major = [] #Major stress
		with open(self.fileName, newline='') as f:
			reader = csv.reader(f)
			for row in reader:
				stress_Minor.append(float(row[1])) #Reading Confining Stress
				stress_Major.append(float(row[2])) #Reading Axial Stress
		circleCenter = [(stress_Major[i]+stress_Minor[i])/2 for i in range(len(stress_Minor))] #center of Mohr Circle 
		circleRadius = [(stress_Major[i]-stress_Minor[i])/2 for i in range(len(stress_Minor))] #radius of Mohr Circle
		return stress_Minor, stress_Major, circleCenter, circleRadius
	
	
class getEnvelope():
	def __init__(self):
		self.scaleX = np.linspace(1, 90, 9000, endpoint=True) #0.01 scale
	
	def getlineParam(self, angle, center, radius):
		meetPointX = [center[i]-(radius[i]*np.cos(np.deg2rad(angle))) for i in range(len(center))] #tangent line - circle meet points x
		meetPointY = [radius[i]*np.sin(np.deg2rad(angle)) for i in range(len(center))]#tangent line - circle meet points y
		slope, intercept, r_value, p_value, std_err = stats.linregress(meetPointX, meetPointY) #get line by least square method
		return slope, intercept, meetPointX, meetPointY
		
	def getreallineParam(self, _center, _radius):
		Avgs=[] #save average differences
		f=open("test.txt","w")
		for k in range(len(self.scaleX)):
			_slope, _intercept, _mx, _my = self.getlineParam(self.scaleX[k], _center, _radius)
			Avgs.append(np.mean([_radius[i]-np.absolute(_slope*_center[i]+_intercept)/np.sqrt(_slope**2+1) for i in range(len(_radius))])) # add calculated average in list Avgs
		return round(self.scaleX[Avgs.index((min(Avgs)))],2)
		
		
class Visualize():
	def __init__(self):
		self.fig, self.ax = plt.subplots() 
		self.ax.axis('scaled')
		self.ax.axhline(0, color='black')
		self.ax.axvline(0, color='black')
		self.ax.set(xlabel=r'Normal Stress(MPa)', ylabel=r'Shear Stress(MPa)')
		
	def drawCircle(self, _radius_, _center_, _stress_Major):
		self.ax.set_xlim((-10,_stress_Major[-1]+200)) 
		self.ax.set_ylim((-_radius_[-1]-200,_radius_[-1]+200))
		for j in range(len(_stress_Major)):
			self.ax.add_artist(plt.Circle((_center_[j], 0), _radius_[j],edgecolor='red',label='Mohr Circle',fill=False)) #draw mohr circle
	
	def drawEnvelope(self, pointX, pointY, _slope, _intercept, _stress_Minor_, center, _degr):
		envelope = self.ax.plot(pointX+[1000],[(pointX[i]*_slope)+_intercept for i in range(len(pointX))]+[1000*_slope+_intercept],label='Failure Envelope')
		lineRadius = self.ax.plot([pointX[-1],center[-1]],[pointY[-1],0],label="Radius of Test {0} Mohr Circle".format(len(_stress_Minor_)))
		self.ax.text(center[-1],0, '%.2f° '%(_degr), fontsize=12) #theta angle
		self.ax.legend(fontsize=10)
		if _intercept<0: 
			self.ax.text(pointX[-1],pointY[-1], r'$y=%.2fx%.2f$'%(_slope,_intercept), fontsize=12)#equation of failure envelope
		else:
			self.ax.text(pointX[-1],pointY[-1], r'$y=%.2fx+%.2f$'%(_slope,_intercept), fontsize=12)
		
	def writepngFile(self):
		self.fig.savefig('Fig.png')
		

csvReader=Read(sys.argv[1])
sm, smj, cc, cr = csvReader.readCsv()		
env = getEnvelope()
ag = env.getreallineParam(cc, cr)
slp, icpt, mx, my = env.getlineParam(ag, cc, cr)
graph = Visualize()
graph.drawCircle(cr, cc, smj)
graph.drawEnvelope(mx, my, slp, icpt, sm, cc, ag)
graph.writepngFile()


