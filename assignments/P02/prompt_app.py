from re import I
from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import VSplit, Window , HSplit
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings

import sys
import schedulers
from time import sleep
import threading

fcfs_buffer = Buffer()  # Editable buffer.
sjf_buffer = Buffer()  # Editable buffer.
rr_buffer = Buffer()  # Editable buffer.
srt_buffer = Buffer()  # Editable buffer.
pb_buffer = Buffer()  # Editable buffer.

fcfs_window = Window(content=BufferControl(buffer=fcfs_buffer))
sjf_window = Window(content=BufferControl(buffer=sjf_buffer))
rr_window = Window(content=BufferControl(buffer=rr_buffer))
srt_window = Window(content=BufferControl(buffer=srt_buffer))
pb_window = Window(content=BufferControl(buffer=pb_buffer))

root_container = HSplit([
    VSplit([
        # One window that holds the BufferControl with the default buffer on
        # the left.
        fcfs_window,
        # A vertical line in the middle. We explicitly specify the width, to
        # make sure that the layout engine will not try to divide the whole
        # width by three for all these windows. The window will simply fill its
        # content by repeating this character.
        Window(width=1, char='|'),

        # Display the text 'Hello world' on the right.
        rr_window,
    ]),
    
    Window(height=1, char='-'),

    VSplit([
        # One window that holds the BufferControl with the default buffer on
        # the left.
        fcfs_window,
        # A vertical line in the middle. We explicitly specify the width, to
        # make sure that the layout engine will not try to divide the whole
        # width by three for all these windows. The window will simply fill its
        # content by repeating this character.
        Window(width=1, char='|'),

        # Display the text 'Hello world' on the right.
        rr_window,
    ]), 
    
    Window(height=1, char='-'),
    
    VSplit([
        # One window that holds the BufferControl with the default buffer on
        # the left.
        fcfs_window,
        # A vertical line in the middle. We explicitly specify the width, to
        # make sure that the layout engine will not try to divide the whole
        # width by three for all these windows. The window will simply fill its
        # content by repeating this character.
        Window(width=1, char='|'),

        # Display the text 'Hello world' on the right.
        rr_window,
    ]), 
])
layout = Layout(root_container)


kb = KeyBindings()

help_str = ""


def run_time_step_dummy():
    while True:
        fcfs_buffer.insert_text("next event triggered\n", overwrite = True)
        rr_buffer.insert_text("next event triggered and updated\n", overwrite = True)

help_str += """
    Pressing Ctrl-Q will exit the user interface.
"""

@kb.add('c-q')
def exit_(event):
    #Setting a return value means: quit the event loop that drives the user
    #interface and return this value from the `Application.run()` call.
    event.app.exit()


help_str += """
    Pressing Ctrl-c will pause simulatior runs
"""
@kb.add('c-c')
def exit_(event):
    schedulers.Pause = True


help_str += """
    Pressing Ctrl-s will run simulation 
"""
@kb.add('c-s')
def exit_(event):
    schedulers.Pause = True

help_str += """
    Pressing Ctrl-n will run next time step in simulation
"""
@kb.add('c-n')
def exit_(event):
    #schedulers.Pause = True
    run_time_step_dummy()

if len(sys.argv)> 1:
    print(help_str)
    sys.exit()

test = threading.Thread(target = run_time_step_dummy )
test.start()
app = Application(layout=layout, key_bindings=kb, full_screen=True)
app.run() # You won't be able to Exit this app


