import mohr
import pandas as pd
import math
data = {'Name': ["TA", "TB", "TC"], "S3": [5, 10, 15], "S1": [84.5, 86.3, 111.0]}


df = pd.DataFrame(data)

tn, sm, smj, cc, cr = mohr.load_df(df)
print(tn, sm, smj, cc, cr)

env = mohr.getEnvelope()
ag = env.getreallineParam(cc, cr)
slp, icpt, mx, my = env.getlineParam(ag, cc, cr)
graph = mohr.Visualize()
graph.drawCircle(cr, cc, smj)
graph.drawEnvelope(mx, my, slp, icpt, sm, cc, ag)
graph.writepngFile(r'mohr_trial_df1.png')

# Get c-Phi information
print("Cohesion\t%0.2f" % icpt)

print("Friction Angle\t%0.2f" % math.degrees(math.atan(slp)))
#
# tn, sm, smj, cc, cr = mohr.read_csv(r'/mohr_trial.csv')
# print(tn, sm, smj, cc, cr)
#
# env = mohr.getEnvelope()
# ag = env.getreallineParam(cc, cr)
# slp, icpt, mx, my = env.getlineParam(ag, cc, cr)
# import math
# phi = math.degrees(math.atan(slp))
# print(phi)
#
# graph = mohr.Visualize()
# graph.drawCircle(cr, cc, smj)
# graph.drawEnvelope(mx, my, slp, icpt, sm, cc, ag)
# graph.writepngFile(r'/mohr_trial_csv.pdf')