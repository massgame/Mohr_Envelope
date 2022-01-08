# /////////////////////////////////////////////////////////////// #
# !python3.6
# -*- coding: utf-8 -*-
# Python Script initially created on 2019-04-17 
# Compiled by Aly @ Grasselli Geomechanics Group, UofT, 2019 
# Created using PyCharm 
# Current Version - Dated Apr 23, 2018
# /////////////////////////////////////////////////////////////// #

import math
import os

# /// TIMER FUNCTION /// #

'''
Function to calculate the time
    Inputs:
        - Difference in time in seconds
    Returns:
        - Time in minutes and seconds
'''

def calc_timer_values(end_time):
    minutes, sec = divmod(end_time, 60)
    if end_time < 60:
        return ("\033[1m%.2f seconds\033[0m" % end_time)
    else:
        return ("\033[1m%d minutes and %d seconds\033[0m." % (minutes, sec))


# /// ADMINISTRATIVE AND SORTING OF FILES IN FOLDER /// #

''' 
Function to make a string bold for printing (on terminal)
    Inputs:
        - A string
    Returns:
        - Red / Green /Bold string
'''

def red_text(val):  # RED Bold text
    tex = "\033[1;31m%s\033[0m" % val
    return tex


def green_text(val):  # GREEN Bold text
    tex = "\033[1;92m%s\033[0m" % val
    return tex


def bold_text(val):  # Bold text
    tex = "\033[1m%s\033[0m" % val
    return tex


def docstring_creator(df):
    docstring = 'Index:\n'
    docstring = docstring + f'    {df.index}\n'
    docstring = docstring + 'Columns:\n'
    for col in df.columns:
        docstring = docstring + f'    Name: {df[col].name}, dtype={df[col].dtype}, nullable: {df[col].hasnans}\n'
        print(docstring)

def eng_string( x, format='%s', si=False):
    """
    Returns float/int value <x> formatted in a simplified engineering format -
    using an exponent that is a multiple of 3.

    format: printf-style string used to format the value before the exponent.

    si: if true, use SI suffix for exponent, e.g. k instead of e3, n instead of
    e-9 etc.

    E.g. with format='%.2f':
        1.23e-08 => 12.30e-9
             123 => 123.00
          1230.0 => 1.23e3
      -1230000.0 => -1.23e6

    and with si=True:
          1230.0 => 1.23k
      -1230000.0 => -1.23M
    """

    sign = ''
    if x < 0:
        x = -x
        sign = '-'
    exp = int( math.floor( math.log10( x)))
    exp3 = exp - ( exp % 3)
    x3 = x / ( 10 ** exp3)

    if si and exp3 >= -24 and exp3 <= 24 and exp3 != 0:
        exp3_text = 'yzafpnum kMGTPEZY'[ ( exp3 - (-24)) / 3]
    elif exp3 == 0:
        exp3_text = ''
    else:
        exp3_text = r'e$^{%s}$' % exp3

    return ( '%s'+'%0.2f'+'%s') % ( sign, x3, exp3_text)


def findDirectories(dir_path, check_files = False):
    """

    :param dir_path:
    :type dir_path: str
    :param check_files:
    :type check_files: bool

    :return:
    :rtype: list[str]
    """

    os.chdir(dir_path) # cd to the base directory path
    list_of_dir = []
    list_of_files = []
    # Get the list of files/directories
    directory_contents = os.listdir('.')

    if not check_files:  # Check Folders
        for item in directory_contents:
            if os.path.isdir(item):
                list_of_dir.append(item)
        return list_of_dir

    else:  # Check Files
        for item in directory_contents:
            if os.path.isfile(item):
                list_of_files.append(item)

        return list_of_files

if __name__ == "__main__":
    try:
        text = "StandAlone Run"
        red_text(text)
        green_text(text)
        bold_text(text)
    except KeyboardInterrupt:
        # print("\n\033[1;31;0mTERMINATED BY USER\n")
        exit("TERMINATED BY USER")

