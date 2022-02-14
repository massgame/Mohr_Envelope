import math
import Mohr_Envelope as mohr
import pandas as pd

''' 
LOAD DATA FROM CSV
'''

tn, sm, smj, cc, cr = mohr.read_csv(r'./mohr_trial.csv')

# Create Envelope
env = mohr.getEnvelope()
ag = env.getreallineParam(cc, cr)
slp, icpt, mx, my = env.getlineParam(ag, cc, cr)

# Get c-Phi information
print("Cohesion\t%0.2f" % icpt)
print("Friction Angle\t%0.2f" % math.degrees(math.atan(slp)))

# Visualize Mohr Envelope
graph = mohr.Visualize()
graph.drawCircle(cr, cc, smj)
graph.drawEnvelope(mx, my, slp, icpt, sm, cc, ag)

# Save Envelope
graph.writepngFile(r'Absolute file path to save')

''' 
LOAD DATA AS DATAFRAME 
'''

# Data from testing Shale rock
# data = {'Name': ["TA", "TB", "TC"], "S3": [5, 10, 15], "S1": [84.5, 86.3, 111.0]}
# df = pd.DataFrame(data)
# Load DataFrame
# tn, sm, smj, cc, cr = mohr.load_df(df)

# Create Envelope
env = mohr.getEnvelope()
ag = env.getreallineParam(cc, cr)
slp, icpt, mx, my = env.getlineParam(ag, cc, cr)

# Get c-Phi information
print("Cohesion\t%0.2f" % icpt)
print("Friction Angle\t%0.2f" % math.degrees(math.atan(slp)))

# Visualize Mohr Envelope
graph = mohr.Visualize()
graph.drawCircle(cr, cc, smj)
graph.drawEnvelope(mx, my, slp, icpt, sm, cc, ag)

# Save Envelope
graph.writepngFile(r'Absolute file path to save')