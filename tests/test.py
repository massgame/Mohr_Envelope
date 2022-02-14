import math
import pandas as pd
import mohr
import operator as op

import matplotlib
import matplotlib.pyplot as plt

# plt.rcParams['figure.constrained_layout.use'] = True
# plt.rcParams["figure.figsize"] = [6, 6]
# plt.rcParams["date.autoformatter.minute"] = "%H:%M:%S"
# matplotlib.rcParams["mathtext.fontset"] = 'dejavuserif'
# matplotlib.rcParams['font.family'] = ['arial']
# matplotlib.rcParams['font.size'] = 8


df = pd.read_excel(r"/external/ownCloud/2020_PETRONAS/Milling_Updates.xlsx", sheet_name='Sample Summary')
# # print(df.columns)
# # exit()
# grouped_df = df.groupby(['Orientation', 'Proposed Test'])
# grouped_df_ori = df.groupby(['Confining Pressure (MPa)', 'Proposed Test'])
#
# def print_mh_data(sub_a_group):
#     mohf_df = sub_a_group[['Sample ID', 'Confining Pressure (MPa)', 'Max Stress (MPa) ', 'Orientation', 'Eavg (GPa)', 'Poisson Ratio (-)']]
#     print(mohf_df['Sample ID'], mohf_df['Max Stress (MPa) '])
#
#     # Load DataFrame
#     mohf_df = mohf_df.reset_index(drop=True)
#     tn, sm, smj, cc, cr = mohr.load_df(mohf_df)
#     # Create Envelope
#     env = mohr.getEnvelope()
#     ag = env.getreallineParam(cc, cr)
#     slp, icpt, mx, my = env.getlineParam(ag, cc, cr)
#
#     # Get c-Phi information
#     print(key)
#     print("Cohesion\t%0.2f" % icpt)
#     print("Friction Angle\t%0.2f" % math.degrees(math.atan(slp)))
#
# UP = [op.ge, "lt"]
# Ori = [0.0, 45.0, 90.0]
#
# for key, item in grouped_df:
#     for or_type in Ori:
#         if key == (or_type, 'TRI'):
#             a_group = grouped_df.get_group(key)
#             upper_group = a_group[a_group['Depth Bottom (m)'].lt(950)]
#             print_mh_data(upper_group)
#             lower_group = a_group[a_group['Depth Bottom (m)'].gt(950)]
#             print_mh_data(lower_group)
#
#
# Conf = [5, 10, 15]
#
# for plot_info in ['Max Stress (MPa) ', 'Eavg (GPa)', 'Poisson Ratio (-)']:
#     fig_layout, ax = plt.subplots()
#
#     for key, item in grouped_df_ori:
#         for conf_type in Conf:
#             if key == (conf_type, 'TRI'):
#                 a_group = grouped_df_ori.get_group(key)
#                 upper_group = a_group[a_group['Depth Bottom (m)'].lt(950)]
#                 lower_group = a_group[a_group['Depth Bottom (m)'].gt(950)]
#
#                 ax.plot(lower_group['Orientation'], lower_group[plot_info], label = "Lower at %s MPa Confinement" % conf_type, marker ='.', ls ='--')
#                 ax.plot(upper_group['Orientation'], upper_group[plot_info], label = "Upper at %s MPa Confinement" % conf_type, marker ='x', ls ='--')
#
#     plt.xlabel('Bedding Orientation')
#     plt.ylabel(plot_info)
#     plt.xticks([0, 45, 90])
#
#     fig_layout.legend()
#     fig_layout.tight_layout()
#     fig_layout.savefig(r"/external/ownCloud/2020_PETRONAS/01_Test_Results/Triaxial/" + plot_info + '.pdf')
#     fig_layout.show()
# exit()
# # for i in d_group:
# #     print(i)
# #     # ast = i.loc[i['Proposed Test'] == "TRI"]
# #     # print(ast)
# # print(d_group)

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
graph = mohr.Visualize_User_Defined()

dfplot = graph.plot_Mohr_Circle(cr, cc, smj, edgecolor='black', ls='-')
graph.plot_Mohr_Envelope(mx, my, slp, icpt, sm, cc, ag, color='r')

dfplot.axis('scaled')
dfplot.set_title("Mohr Circle")
dfplot.set_xlim(0, max(smj) * 1.25)
dfplot.set_ylim(0, max(cr) * 1.25)
dfplot.set(xlabel=r'Normal Stress (MPa)', ylabel=r'Shear Stress (MPa)')

dfplot.legend()
plt.savefig('/home/aly/Desktop/mohr.png')
plt.show()
exit()
graph = mohr.Visualize()
graph.drawCircle(cr, cc, smj, _test_name=tn)
graph.drawEnvelope(mx, my, slp, icpt, sm, cc, ag)

# Save Envelope
graph.writeFile(r'/home/aly/Desktop/mohr_Auto.pdf')
exit()
''' 
LOAD DATA AS DATAFRAME 
'''

# Data from testing Shale rock
data = {'Name': ["TA", "TB", "TC"], "S3": [5, 10, 15], "S1": [84.5, 86.3, 111.0]}
df = pd.DataFrame(data)
# Load DataFrame
tn, sm, smj, cc, cr = mohr.load_df(df)

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
graph.writeFile(r'Absolute file path to save')