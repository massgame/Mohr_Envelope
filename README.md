# Mohr_Envelope
Visualize Mohr Circle and Failure Envelope using triaxial test data.
Compatible with Python 3.5.2+

Why I made this code?
-------------
This work was motivated by triaxial test for a Geological Engineering Laboratory report. The report requires drawing mohr circle and failure envelope. A major drawback of using Excel is that it is not possible to draw a common tangent line of mohr circles isn't in the thing. Manual and Matlab are two available options, however, I didn't want to manual draw the circles and I didn't have Matlab.

The solution was to revert to Python. Using the python packages numpy and scipy and matplotlib, I was able to obtain a working version of this. And I decided to write this script to help the juniors.

The script is not exhaustive, as I am no Computer Science major, but it does the job. And works!!

How it works?
-------------
If you don't know about Mohr's Circle [read this](https://en.wikipedia.org/wiki/Mohr's_circle)
1. Draw Mohr circles in various σ1(major principle stress) and σ3(minor principle stress) condition. and determine point which meets circle's tangent line on each mohr circles. these point is determined by (x1-rcos(a),rsin(a)).
2. Use these point and Least-Square Method, make "Failure envelope candidate" Line. 
3. Calculate averages of differences between distance from circle's center to "Failure envelope candidate" and circle's radius.
4. Increase a(a: angle, 1~90) and repeat. Failure envelope candidate at angle which have lowest average of the differences is real failure envelope.
5. Draw Mohr circles and failure envelope.


How to use
-------------
Prior to the beginning, the following packages need to be installed:
* [numpy](http://www.numpy.org/)
* [scipy](https://www.scipy.org/)
* [matplotlib](http://matplotlib.org/)

Accepted data formats are either .csv files or Panda DataFrames

Input
-------------
### csv file format:

If you're using excel, write TestID in column A, σ3 in column B, and σ1 in column C. The csv **should not** contain a header. The script will ignore any columns after the third. 

```
> Test_name, σ3, σ1
```

### Pandas DataFrame format:

The column header names do not really matter.

```
Columns:
    Name: Test_Name, dtype=object, nullable: False
    Name: σ3, dtype=int64, nullable: False
    Name: σ1, dtype=int64, nullable: False
```

Examples
-------------


```python3
import math
import Mohr_Envelope as mohr
import pandas as pd

''' 
LOAD DATA FROM CSV
'''

tn, sm, smj, cc, cr = mohr.read_csv(r'Absolute file path')

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
> Cohesion	18.69
print("Friction Angle\t%0.2f" % math.degrees(math.atan(slp)))
> Friction Angle	29.68

''' 
VISUALIZATION  
'''

# Standard Visualize Mohr Envelope 
graph = mohr.Visualize()
graph.drawCircle(cr, cc, smj)
graph.drawEnvelope(mx, my, slp, icpt, sm, cc, ag)

# Save Envelope
graph.writeFile(r'Absolute file path to save')

####

# Advanced Visualize Mohr Envelope
adv_graph = mohr.Visualize()

# You can use **plt_kwargs and have control over the plot of the Mohr circle.
advanced_plot = adv_graph.plot_Mohr_Circle(cr, cc, smj, edgecolor='black', ls='-')
adv_graph.plot_Mohr_Envelope(mx, my, slp, icpt, sm, cc, ag, color='r')

# Control over the Axes Canvas
advanced_plot.axis('scaled')
advanced_plot.set_title("Mohr Circle")
advanced_plot.set_xlim(0, max(smj) * 1.25)
advanced_plot.set_ylim(0, max(cr) * 1.25)
advanced_plot.set(xlabel=r'Normal Stress (MPa)', ylabel=r'Shear Stress (MPa)')

# Show Legend
advanced_plot.legend()

# Show and Save figure
plt.savefig('/home/aly/Desktop/mohr.png')
plt.show()
```