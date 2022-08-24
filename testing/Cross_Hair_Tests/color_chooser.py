"""
Source: https://github.com/PySimpleGUI/PySimpleGUI/issues/5584
"""

import PySimpleGUI as sg

from PIL import ImageColor


layout = [[sg.Input(key='-COLOR1-',enable_events=True), sg.ColorChooserButton('Color',key='-COLOR1b-')],
          [sg.Button('Go'), sg.Button('Exit')]  ]

window = sg.Window('Color chooser Test', layout)

while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == '-COLOR1-':
        window['-COLOR1b-'].update(button_color=values[event])
        rgb_color = ImageColor.getcolor(values[event], "RGB")
        print(f"RGB: {rgb_color}")

window.close()