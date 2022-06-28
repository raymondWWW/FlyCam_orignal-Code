"""
Code to mimic Arduino's Map function

Maps one range onto another. It's basically ratios.

Allows for float values now, may need to have a constrain ability since it may max out.

Sources:
https://www.arduino.cc/reference/en/language/functions/math/map/
*Math formula at the end
"""


def constrain(x_out, out_min, out_max):
    # Will constrain x_out to within the out min/max range
    result = x_out

    # If x_out is too low, make it out_min
    if x_out < out_min:
        result = out_min
    # else if x_out is too high, make out_max
    elif x_out > out_max:
        result = out_max

    return result


def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def map_range2(x, in_min, in_max, out_min, out_max):
    # map_range with Constrain

    # Init default value, which is just x. May need to change this for debugging.
    result = x

    # Calculate x in the output range
    x_out = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    # Constrain to the out min/max values, if needed
    # Will return x_out if not needed
    x_out_constrained = constrain(x_out, out_min, out_max)

    # Store x_out_constrained into result
    result = x_out_constrained

    return result


def map_range2_int(x, in_min, in_max, out_min, out_max):
    # map_range with Constrain

    # Init default value, which is just x. May need to change this for debugging.
    result = x

    # Calculate x in the output range
    x_out = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    # Constrain to the out min/max values, if needed
    # Will return x_out if not needed
    x_out_constrained = constrain(x_out, out_min, out_max)

    # Store x_out_constrained into result after rounding and convert to int
    result = int(round(x_out_constrained))

    return result


def main():

    x = 16000
    in_min = 16000
    in_max = 24000
    out_min = 0
    out_max = 255

    x_out = map_range2_int(x, in_min, in_max, out_min, out_max)

    print(f"x_out: {x_out}")

    pass


if __name__ == "__main__":
    main()
