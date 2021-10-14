"""
Short demo of drone functionality.  For the full list of available commands
check:

https://djitellopy.readthedocs.io/en/latest/tello/
"""

from tello import Drone

with Drone() as d:
    d.start_video('video.avi')
    d.takeoff()
    d.move_forward(50)
    d.rotate_clockwise(360)
    d.wait(5.0)
    d.land()
