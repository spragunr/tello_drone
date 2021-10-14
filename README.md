# tello_drone
Python 3 library for controlling DJI Tello Drones

This library provides a thin wrapper around the
[DJITelloPy](https://github.com/damiafuentes/DJITelloPy) library,
which itself is a wrapper around the [official DJI Tello Python
SDK](https://github.com/dji-sdk/Tello-Python). The main advantage of
this library is that it makes it simple to view and record video
during execution.

To install dependencies:

```
pip install https://github.com/damiafuentes/DJITelloPy/archive/master.zip
pip install opencv-python
```

## Example usage:

```java
from tello import Drone

with Drone() as d:
    d.start_video('video.avi')
    d.takeoff()
    d.move_forward(50)
    d.rotate_clockwise(360)
    d.wait(5.0)
    d.land()
```

The full list of available methods can be found at <https://djitellopy.readthedocs.io/en/latest/tello/>.


