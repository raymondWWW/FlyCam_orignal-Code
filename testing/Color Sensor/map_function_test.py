"""
Code to mimic Arduino's Map function

Maps one range onto another. It's basically ratios.

Sources:
https://www.arduino.cc/reference/en/language/functions/math/map/
*Math formula at the end
"""


def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def main():

    x = 11
    in_min = 10
    in_max = 20
    out_min = 0
    out_max = 100

    x_out = map_range(x, in_min, in_max, out_min, out_max)

    print(f"x_out: {x_out}")
    pass


if __name__ == "__main__":
    main()
