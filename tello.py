"""
The Drone class is a subclass of the Tello class provided by the DJITelloPy
library:
https://github.com/damiafuentes/DJITelloPy

This class just adds context manager functionality and a simpler interface
for recording and displaying video.  The documentation for inherited
functionality can be found here:

https://djitellopy.readthedocs.io/en/latest/tello/

author: Nathan Sprague
version: 10/14/2021
"""

from threading import Thread
import time
from djitellopy import Tello
import cv2


class Drone(Tello):
    """
    Drone class enables access to a wifi-connected Tello drone.
    Sample usage::

    with my_drone as Drone():
        my_drone.takeoff()
        my_drone.move_forward(50)
        my_drone.rotate_clockwise(360)
        my_drone.land()

    """

    def __init__(self):
        super().__init__()
        self.video_thread = None
        self.video_showing = False
        self.video_file_name = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, type, value, traceback):
        self.end_video()

    def start_video(self, file_name=None):
        """
        Turn on video display.

        :param file_name: name of file to save video
        """
        self.video_file_name = file_name
        self.video_showing = True
        self.streamon()
        time.sleep(.5)
        self.frame_read = self.get_frame_read()
        time.sleep(.5)
        self.video_thread = Thread(target=self._show_video_thread)
        self.video_thread.start()

    def end_video(self):
        """
        Stop video display and store video file (if recording).
        """
        if self.video_showing:
            self.video_showing = False
            self.frame_read.stop()
            self.video_thread.join()

    def _show_video_thread(self):
        writer = None
        if self.video_file_name is not None:
            height, width, _ = self.frame_read.frame.shape
            writer = cv2.VideoWriter(self.video_file_name,
                                     cv2.VideoWriter_fourcc(*'XVID'),
                                     20, (width, height))

        while self.video_showing:
            img = self.frame_read.frame
            if writer is not None:
                writer.write(img)

            time.sleep(.01)
            cv2.imshow("drone", img)
            cv2.waitKey(33)

        if writer is not None:
            writer.release()
        cv2.destroyAllWindows()
        time.sleep(.1)

    def wait(self, seconds):
        """
        Tell the drone to pause before executing the next command.
        :param seconds: Number of seconds to wait.
        """
        time.sleep(seconds)
