
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys

st1=[] #Minor stress
st2=[] #Major stress

with open(sys.argv[1], newline='') as f:
	reader = csv.reader(f)
	for row in reader:
		st1.append(float(row[1])) #Reading Confining Stress
		st2.append(float(row[2])) #Reading Axial Stress
		
circlecenter=[(st2[i]+st1[i])/2 for i in range(len(st1))] #center of Mohr Circle 
circleradius=[(st2[i]-st1[i])/2 for i in range(len(st1))] #radius of Mohr Circle
X = np.linspace(1, 90, 9000, endpoint=True) #0.01 scale
Avgs=[] #save average differences

f=open("output.txt","w")
for k in range(len(X)):
	degreex=[circlecenter[i]-(circleradius[i]*np.cos(np.deg2rad(X[k]))) for i in range(len(circlecenter))] #tangent line - circle meet points x
	degreey=[circleradius[i]*np.sin(np.deg2rad(X[k])) for i in range(len(circlecenter))]#tangent line - circle meet points y
	slope, intercept, r_value, p_value, std_err=stats.linregress(degreex,degreey) #get line by least square method
	Distances=[(np.absolute(slope*circlecenter[i]+intercept)/np.sqrt(slope**2+1)) for i in range(len(degreex))] #get distance between line and center point of circle
	Avgs.append(np.mean([circleradius[i]-Distances[i] for i in range(len(circleradius))])) # add calculated average in list Avgs
	
degr=round(X[Avgs.index((min(Avgs)))],2) #get a degree which has lowest differences
degreex=[circlecenter[i]-(circleradius[i]*np.cos(np.deg2rad(degr))) for i in range(len(circlecenter))] #tangent line - circle meet points x
degreey=[circleradius[i]*np.sin(np.deg2rad(degr)) for i in range(len(circlecenter))] #tangent line - circle meet points y
slope, intercept, r_value, p_value, std_err=stats.linregress(degreex,degreey) #get line by least square method



fig, ax = plt.subplots() 
ax.axis('scaled')
ax.axhline(0, color='black')
ax.axvline(0, color='black')
ax.set(xlabel=r'Normal Stress(MPa)', ylabel=r'Shear Stress(MPa)')
ax.set_xlim((-10,st2[-1]+200)) 
ax.set_ylim((-circleradius[-1]-200,circleradius[-1]+200))

for j in range(len(st1)):
	ax.add_artist(plt.Circle((circlecenter[j], 0), circleradius[j],edgecolor='red',label='Mohr Circle',fill=False)) #draw mohr circle

linet=ax.plot(degreex+[1000],[(degreex[i]*slope)+intercept for i in range(len(degreex))]+[1000*slope+intercept],label='Failure Envelope')
linef=ax.plot([degreex[-1],circlecenter[-1]],[degreey[-1],0],label="Radius of Test {0} Mohr Circle".format(len(st1)))
ax.legend(fontsize=10)
if intercept<0: 
	ax.text(degreex[-1],degreey[-1], r'$y=%.2fx%.2f$'%(slope,intercept), fontsize=12)
	f.write("===============\n Internal Friction Angle : {0:.2f}° \n Cohesion : {1:.2f} MPa \n Failure Envelope equation : y={2:.2f}x{1:.2f}\n===============".format(90-degr,intercept,slope))
else:
	ax.text(degreex[-1],degreey[-1], r'$y=%.2fx+%.2f$'%(slope,intercept), fontsize=12)
	f.write("===============\n Internal Friction Angle : {0:.2f}° \n Cohesion : {1:.2f} MPa \n Failure Envelope equation : y={2:.2f}x+{1:.2f}\n===============".format(90-degr,intercept,slope))
	
f.close()
ax.text(circlecenter[-1],0, '%.2f° '%(degr), fontsize=12) #equation of failure envelope
fig.savefig('Fig.png')
