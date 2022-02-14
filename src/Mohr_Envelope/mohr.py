import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np

class Read:
    def __init__(self, promptFileName):
        self.fileName = promptFileName

    def readCsv(self):
        """
        Converts the csv data into pandas.DataFrame format and sorts them based on the confining pressure.

        :return: test_name, stress_Minor, stress_Major, circleCenter, circleRadius
        :rtype: Tuple[list[str], list[float], list[float], list[float], list[float]]
        """

        self.dataframe = pd.read_csv(self.fileName)

        self.dataframe.columns = range(self.dataframe.shape[1])

        self.dataframe[3] = (self.dataframe[2] + self.dataframe[1]) / 2  # center of Mohr Circle
        self.dataframe[4] = (self.dataframe[2] - self.dataframe[1]) / 2  # radius of Mohr Circle

        self.dataframe = self.dataframe.sort_values(by=[1])

        test_name, stress_Minor, stress_Major, circleCenter, circleRadius = self.dataframe[0].tolist(), \
                                                                            self.dataframe[1].tolist(), \
                                                                            self.dataframe[2].tolist(), \
                                                                            self.dataframe[3].tolist(), \
                                                                            self.dataframe[4].tolist()

        return test_name, stress_Minor, stress_Major, circleCenter, circleRadius


class ReadDF:
    def __init__(self, DataFrameLoaded):
        self.dataframe = DataFrameLoaded

    def loadDF(self):
        """
        Loads the data in pandas.DataFrame format and sorts them based on the confining pressure.

        :return: test_name, stress_Minor, stress_Major, circleCenter, circleRadius
        :rtype: Tuple[list[str], list[float], list[float], list[float], list[float]]
        """

        self.dataframe.columns = range(self.dataframe.shape[1])

        self.dataframe[3] = (self.dataframe[2] + self.dataframe[1]) / 2  # center of Mohr Circle
        self.dataframe[4] = (self.dataframe[2] - self.dataframe[1]) / 2  # radius of Mohr Circle

        self.dataframe = self.dataframe.sort_values(by=[1])

        test_name, stress_Minor, stress_Major, circleCenter, circleRadius = self.dataframe[0].tolist(), \
               self.dataframe[1].tolist(), \
               self.dataframe[2].tolist(), \
               self.dataframe[3].tolist(), \
               self.dataframe[4].tolist()

        return test_name, stress_Minor, stress_Major, circleCenter, circleRadius


class getEnvelope:
    def __init__(self):
        self.scaleX = np.linspace(1, 90, 9000, endpoint=True)  # 0.01 scale

    def getlineParam(self, angle, center, radius):
        """
        Analyse point with Least-Square Method, make "Failure envelope candidate" Line.

        :param angle: Angle of line to analyse
        :type angle: float
        :param center: Center of the Mohr Circle
        :type center: list[float]
        :param radius: Radius of the Mohr Circle
        :type radius: list[float]

        :return: slope (Slope of the regression line), intercept (Intercept of the regression line), meetPointX (X intersection), meetPointY (Y intersection)
        :rtype: list[float]
        """

        meetPointX = [center[i] - (radius[i] * np.cos(np.deg2rad(angle))) for i in
                      range(len(center))]  # tangent line - circle meet points x
        meetPointY = [radius[i] * np.sin(np.deg2rad(angle)) for i in
                      range(len(center))]  # tangent line - circle meet points y
        slope, intercept, r_value, p_value, std_err = stats.linregress(meetPointX,
                                                                       meetPointY)  # get line by least square method
        return slope, intercept, meetPointX, meetPointY

    def getreallineParam(self, _center, _radius):
        """
        Calculate averages of difference between distance from circle's center to "Failure envelope candidate" and circle's radius.

        :param _center: Center of the Mohr Circle
        :type _center: list[float]
        :param _radius: Radius of the Mohr Circle
        :type _radius: list[float]

        :return: Approx angle of the tangent to be drawn
        :rtype: float
        """

        Avgs = []  # save average differences

        for k in range(len(self.scaleX)):
            _slope, _intercept, _mx, _my = self.getlineParam(self.scaleX[k], _center, _radius)
            Avgs.append(np.mean(
                [_radius[i] - np.absolute(_slope * _center[i] + _intercept) / np.sqrt(_slope ** 2 + 1) for i in
                 range(len(_radius))]))  # add calculated average in list Avgs
        return round(self.scaleX[Avgs.index((min(Avgs)))], 2)


class Visualize:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax.axis('scaled')
        self.ax.set(xlabel=r'Normal Stress (MPa)', ylabel=r'Shear Stress (MPa)')

    def drawCircle(self, _radius_, _center_, _stress_Major, _test_name=None):
        """
        Draw the actual Mohr Circle domain.

        :param _radius_: Circle radius
        :type _radius_: list[float]
        :param _center_: Circle centers
        :type _center_: list[float]
        :param _stress_Major: Major Stress
        :type _stress_Major: list[float]
        :param _test_name: Name of the Mohr Circle being drawn
        :type _test_name: None or list[str]

        :return: matplotlib.Axes
        """

        self.ax.set_xlim(0, _stress_Major[-1] * 1.25)
        self.ax.set_ylim(0, _radius_[-1] * 1.25)
        # Patch Vs. ARTIST
        for j in range(len(_stress_Major)):
            if _test_name:
                self.ax.add_patch(plt.Circle((_center_[j], 0), _radius_[j], edgecolor='red', ls='--', label=_test_name[j],
                                          fill=False))  # draw mohr circle
            else:
                self.ax.add_patch(plt.Circle((_center_[j], 0), _radius_[j], edgecolor='red', ls='--',
                                          fill=False))  # draw mohr circle

        self.ax.legend(fontsize=10)

    def drawEnvelope(self, pointX, pointY, _slope, _intercept, _stress_Minor_, center, _degr):
        """
        Plot the failure envelope.

        :param pointX: Point on Envelope
        :type pointX: float
        :param pointY: Point on Envelope
        :type pointY: float
        :param _slope: Slope of 'failure envelope'
        :type _slope: float
        :param _intercept: Intercept of 'failure envelope'
        :type _intercept: float
        :param _stress_Minor_: No. of tests loaded
        :type _stress_Minor_: float
        :param center: Circle centers
        :type center: list[float]:
        :param _degr: Angle of constructed tangent
        :type _degr: float

        :return: matplotlib.Axes
        """

        # Draw Envelope
        envelope = self.ax.plot(pointX + [1000], [(pointX[i] * _slope) + _intercept for i in range(len(pointX))] + [
            1000 * _slope + _intercept], label='Failure Envelope')
        # Draw line radius for construction
        lineRadius = self.ax.plot([pointX[-1], center[-1]], [pointY[-1], 0],
                                  label="Radius of Test {0} Mohr Circle".format(len(_stress_Minor_)))
        self.ax.text(center[-1], 0, '%.2f° ' % _degr, fontsize=12)  # theta angle
        self.ax.legend(fontsize=10)
        if _intercept < 0:
            self.ax.text(pointX[-1], pointY[-1], r'$y=%.2fx%.2f$' % (_slope, _intercept),
                         fontsize=12)  # equation of failure envelope
        else:
            self.ax.text(pointX[-1], pointY[-1], r'$y=%.2fx+%.2f$' % (_slope, _intercept), fontsize=12)

    def writepngFile(self, savefilename):
        """
        Save the results of the Mohr Circle and Envelope.

        :param savefilename: Absolute path to the location of saving the image. matplotlib extensions supported.
        :type savefilename: str

        :return: Saves the image to the desired path
        """
        self.fig.show()
        self.fig.savefig(savefilename)


def read_csv(filename):
    """
    Name of file to be loaded in csv format. If you're using excel, write TestID in column A, σ3 in column B, and σ1 in column C.

    :param filename: CSV filename holding the results
    :type filename: str

    :return: test_name, stress_Minor, stress_Major, circleCenter, circleRadius
    :rtype: Tuple[list[str], list[float], list[float], list[float], list[float]]
    """

    print("Loading File %s" % filename)
    return Read(filename).readCsv()


def load_df(mohr_data):
    """
    Loads data to construct the failure envelope. The dataframe must be three columns with testname, confining pressure (s3), and max axial stress (s1). The column titles do not matter.

    :param mohr_data: DataFrame containing the mohr data. The dataframe must be three columns with testname, confining pressure (s3), and max axial stress (s1).
    :type mohr_data: pandas.DataFrame

    :return: test_name, stress_Minor, stress_Major, circleCenter, circleRadius
    :rtype: Tuple[list[str], list[float], list[float], list[float], list[float]]
    """

    print("Loading DataFrame")
    return ReadDF(mohr_data).loadDF()
