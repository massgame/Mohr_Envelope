# Mohr_Envelope
Visualize Mohr Circle and Failure Envelope 
for Python 3.5.2

Why I made this code?
-------------
I had to write Geological Engineering Lab report about triaxial test, and this report requires drawing mohr circle and failure envelope. first one is an easy job, but next one isn't. we can do many things by Excel, but drawing common tangent line of mohr circles isn't in the thing. the choice was only two : First, Use Matlab. Second. Draw by hand. however, i didn't want to write report by hand and i didn't have matlab.

Therefore, I used numpy and scipy and matplotlib and these worked fine. maybe my juniors would encounter this problem. so i wrote this code to help my juniors.

As you can see, my major isn't Computer Science, so code would look like spagetti. but it works!

How it works?
-------------
If you don't know about Mohr's Circle, [read this][mohr]
[mohr]:https://en.wikipedia.org/wiki/Mohr's_circle
1. Draw Mohr circles in various σ1(major principle stress) and σ3(minor principle stress) condition. and determine point which meets circle's tangent line on each mohr circles. these point is determined by (x1-rcos(a),rsin(a)).
2. Use these point and Least-Square Method, make "Failure envelope candidate" Line. 
3. Calculate averages of differents between distance from circle's center to "Failure envelope candidate"  and circle's radius.
4. increase a(a: angle, 1~90) and repeat. Failure envelope candidate at angle a which have lowest averages of different is real failure envelope.
5. Draw Mohr circles and failure envelope.


How to use
-------------
Prior to the beginning, You have to install [numpy], [scipy], [matplotlib]
[numpy]:http://www.numpy.org/
[scipy]:https://www.scipy.org/
[matplotlib]:http://matplotlib.org/

Accepted data formats are either .csv files or Panda DataFrames

Input
-------------
### csv file format:

>Test_name, σ3, σ1

If you're using excel, write TestID in column A, σ3 in column B, and σ1 in column C.

### Panda DataFrames format:
```
Columns:
    Name: Test_Name, dtype=object, nullable: False
    Name: σ3, dtype=int64, nullable: False
    Name: σ1, dtype=int64, nullable: False
```

Examples
-------------


```python
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

# Visualize Mohr Envelope 
graph = mohr.Visualize()
graph.drawCircle(cr, cc, smj)
graph.drawEnvelope(mx, my, slp, icpt, sm, cc, ag)

# Save Envelope
graph.writepngFile(r'Absolute file path to save')
```