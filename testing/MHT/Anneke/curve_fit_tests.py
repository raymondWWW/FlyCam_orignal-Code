"""
Tests for scipy's curve_fit function

Sources:
https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html

Sample curve functions to use:
https://pythonguides.com/python-scipy-curve-fit/


Error Bars Calculation?
https://stackoverflow.com/questions/14581358/getting-standard-errors-on-fitted-parameters-using-the-optimize-leastsq-method-i
https://stackoverflow.com/a/21844726

"""

import numpy as np
import pandas as pd
import time

from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
from os.path import join, isfile


# def expfunc(x, y, z, s):
#     return y * np.exp(-z * x) + s


def expfunc(x, a, b, c):
    return a * np.exp(-b * x) - c


def sine(x, a, b):
    return a * np.sin(b * x)


def calc_pb_lattice(c, delta_e):
    c0= 1.66e9 # saturated binding in a lattice with 1nm^3 positions, in nM
    numerator = (c/c0)*np.exp(-delta_e)
    return numerator/(1+numerator)


def natural_log(x, a, b):
    return a * np.log(x) - b


def main5():

    param_range = np.arange(0, -100, -1)

    csv_folder = r'D:\Documents\SF State\Dr. E Lab\MHT\Data\8-31-2022\08312022_MeI_stds_run2\Plots'
    csv_file = r'exp_mei_curve.csv'

    # Join csv folder and file
    # If it is not a file, print that file doesn't exist and break out of function
    csv_full_path = join(csv_folder, csv_file)
    print(f"csv_full_path: {csv_full_path}")

    # Use pandas to open CSV file to dataframe
    df = pd.read_csv(csv_full_path)

    print(df.head(5))

    # ppm is x-axis, color difference is y-axis
    x = df.ppm / 1000
    y = df.d / 100

    # ans = expfunc(x, *param)
    concentrations = np.linspace(0, 25, num=100)
    # ans = calc_pb_lattice(concentrations, *param)

    for param in param_range:
        print(f"param: {param}")
        ans = calc_pb_lattice(concentrations, param)

        plt.plot(1000 * x, 100 * y, 'o', color='black', label="data")
        plt.plot(1000 * concentrations, 100 * ans, '--', color='blue', label="optimized")
        plt.show(block=False)
        time.sleep(1)

    pass


def main4():
    x = np.linspace(0, 5, 60)
    y = expfunc(x, 3.1, 2.3, 1.0)

    random_numgen = np.random.default_rng()
    noise_y = 0.3 * random_numgen.normal(size=x.size)

    y_new = y + noise_y
    plt.plot(x, y_new, 'b-', label='data')

    p_opt, p_cov = curve_fit(expfunc, x, y_new)

    opt_data = expfunc(x, *p_opt)

    plt.plot(x, opt_data, 'r-', label="optimized")
    plt.legend()
    plt.show()

    plt.show()

    pass


def main3():
    csv_folder = r'D:\Documents\SF State\Dr. E Lab\MHT\Data\8-31-2022\08312022_MeI_stds_run2\Plots'
    csv_file = r'exp_mei_curve.csv'

    # Join csv folder and file
    # If it is not a file, print that file doesn't exist and break out of function
    csv_full_path = join(csv_folder, csv_file)
    print(f"csv_full_path: {csv_full_path}")

    # Use pandas to open CSV file to dataframe
    df = pd.read_csv(csv_full_path)

    print(df.head(5))

    # ppm is x-axis, color difference is y-axis
    scale_x = 1000
    scale_y = 100
    x = df.ppm / scale_x
    y = df.d / scale_y

    deltae_guess = [-5] # your delta E guess based on your previous explorations
    deltae_lower = -10
    deltae_upper = 0 # what's the largest delta E could be and still have binding be favorable?

    # param, param_cov = curve_fit(expfunc, x, y)
    # param, param_cov = curve_fit(calc_pb_lattice, x, y, deltae_guess, bounds=[deltae_lower, deltae_upper])
    param, param_cov = curve_fit(natural_log, x, y)
    print(f"exp function coefficients: {param}")
    print(f"Covariance of coefficients: {param_cov}")

    # ans = expfunc(x, *param)
    concentrations = np.linspace(0, 25, num=100)
    # ans = calc_pb_lattice(concentrations, *param)
    ans = natural_log(concentrations, *param)
    # Answer equation: y = 276.25 * ln(x) - 240.55

    plt.errorbar(scale_x * x, scale_y * y, fmt='ro', yerr=scale_y*0.2, capsize=6, label="data")

    # plt.plot(scale_x * x, 100 * y, 'o', color='black', label="data")
    plt.plot(scale_x * concentrations, scale_y * ans, '--', color='blue', label="optimized")
    plt.legend()
    plt.xlabel("ppm")
    plt.ylabel("Color difference")
    plt.show()

    pass


def main2():
    # Curve fit using Patra's data now.

    csv_folder = r'D:\Documents\SF State\Dr. E Lab\MHT\Data\8-31-2022\08312022_MeI_stds_run2\Plots'
    csv_file = r'08312022_MeI_stds_run2_well1_hsv_data.csv'

    # Join csv folder and file
    # If it is not a file, print that file doesn't exist and break out of function
    csv_full_path = join(csv_folder, csv_file)
    print(f"csv_full_path: {csv_full_path}")

    # Use pandas to open CSV file to dataframe
    df = pd.read_csv(csv_full_path)

    # print(df.head(5))

    x = df.time
    y = df.s

    # Plot RGB data, as an example
    # plt.plot(x, y, 'o', color='blue', label="h")
    # plt.plot(x, df.s, 'o', color='black', label="s")
    # plt.plot(x, df.v, 'o', color='violet', label="v")
    #
    # plt.legend()
    # plt.show()

    # Would dataframe work with curve fit?

    param, param_cov = curve_fit(expfunc, x, y, maxfev=600)
    print(f"exp function coefficients: {param}")
    print(f"Covariance of coefficients: {param_cov}")

    # y * np.exp(-z * x) + s
    ans = param[0] * np.exp(-param[1] * x) - param[2]

    plt.plot(x, df.s, 'o', color='black', label="s")
    plt.plot(x, ans, '--', color='black', label="Optimized Data")
    plt.legend()
    plt.xlabel("Time (s)")
    plt.ylabel("Saturation")
    plt.show()


    pass


def main():
    # Source: https://www.geeksforgeeks.org/scipy-curve-fitting/

    # Create sample data

    # Create linear range of 40 evenly spaced numbers from 0 to 10
    x = np.linspace(0, 10, num=40)

    # Create sine-like plot from x array, make amplitude stretch to 3.45 vertically.
    # Stretch horizontally 1.334.
    # Then make it scatter by making random values shift up or down so it's not a perfect replica of a sine wave.
    y = 3.45 * np.sin(1.334 * x) + np.random.normal(size=40)

    # plt.scatter(x, y)
    # plt.show()

    # Use test function that models sine wave pattern

    param, param_cov = curve_fit(sine, x, y)

    print(f"Sine function coefficients: {param}")
    print(f"Covariance of coefficients: {param_cov}")

    # Create sine data using curve_fit parameters (the a and b from the test function)
    ans = param[0] * np.sin(param[1] * x)

    plt.plot(x, y, 'o', color='red', label="data")
    plt.plot(x, ans, "--", color='blue', label="optimized data")
    plt.legend()
    plt.show()

    pass


if __name__ == "__main__":
    # main()
    # main2()
    main3()
    # main4()
    # main5()
