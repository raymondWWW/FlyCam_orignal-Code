# Goal: Parse the M114 String into a destination and current position

from parse import *

# Consider using this library (might make things easier to find)
# https://pypi.org/project/parse/
# https://github.com/r1chardj0n3s/parse

# Help
# https://www.vipinajayakumar.com/parsing-text-with-python/

# M114 Detail
# https://marlinfw.org/docs/gcode/M114.html

sample = "X:1.45Y:2.67Z:100.09E:3.00 Count X: 4.00Y:5.00Z:102.00\nok"
sample2 = "wait\nwait\nok\nX:0.00 Y:0.00 Z0.000 E:0.0000"
# sample = "echo: Position"
# sample = sample.splitlines()
parsed_str = sample[0].split("Count")
dest = parsed_str[0]
# current = parsed_str[1]
# temp = current.split['\n']
# dest_parse = dest.split(":")

print("sample:", sample)
# print("parsed_str:", parsed_str)
print("dest:", dest)
# print("current:", current)
# print("dest_parse:", dest_parse)

# Single Search
result = search("X:{:.2f}", sample)
if result is not None:
    result2 = findall("X:{x:.2f}Y:{y:.2f}Z:{z:.2f}", sample)
    print("result2:", result2)
    for r in result2:
        print(r["z"])

else:
    print("Search did not find anything")


# Algorithm:
"""
Check if current position is destination position, if true take photo/video, else check position again

Send M114
Get receiving bytes
https://pythonhosted.org/pyserial/pyserial_api.html#serial.Serial.in_waiting
https://stackoverflow.com/questions/38645060/what-is-the-equivalent-of-serial-available-in-pyserial

if greater than 50 and less than 100, probably destination and current position information
Start parsing algorithm
 Search for "Count",
    if None (nothing found), send M114 again
    else send string to parse_position_information (return destination and current position dictionaries)
    

parse_position_information():
Assumes string is in this kind of format:
"X:1.45Y:2.67Z:100.09E:3.00 Count X: 4.00Yt:5.00Z:102.00\nok"
(Destination, Current)
or

"wait
wait
ok
X:1.45Y:2.67Z:100.09E:3.00
"

Initialize destination_position_dictionary and current_position_dictionary with keys: x, y, z
 use parse library findall() function to look for findall("X:{x:.2f}Y:{y:.2f}Z:{z:.2f}", input)
 store into dictionaries using for loop to iterate through results of findall()
 return dictionaries

Update:
- Include different sample inputs
- Search for only the X, Y, and Z
  - If none, keep waiting or request M114
  - If one, use that as current location
  - If two or more, use last one
 
"""

# Findall Test
# result = findall("R:{:.2f}", sample)
# print("result:", result)
# print("Result (loop):")
# for r in result:
#     print(len(r))


# TODO: Have condition if "None" is returned from search result
#   Figure out how to get no results for findall
#   Research how iterator objects work? https://docs.python.org/3/c-api/iterator.html
# TODO: Maybe do a findall instead to get X, Y, and Z
# TODO: Test if findall put results in order
# TODO: Consider doing virtual env in RPi