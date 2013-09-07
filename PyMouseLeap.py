################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import sys, os, ConfigParser
sys.path.append('./lib')
sys.path.append('./lib/x64')
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

Config = ConfigParser.ConfigParser()
Config.read("./config.ini")

class SampleListener(Leap.Listener):
    def on_init(self, controller):
        print("Initialized")
        self.commands = [
                ScreentapCommand(),
                SwiperightCommand(),
                SwipeleftCommand(),
                CounterclockwiseCommand(),
                ClockwiseCommand(),
                KeytapCommand()
        ]
        self.old_x = None

    def on_connect(self, controller):
        print("Connected")

        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        print("Disconnected")

    def on_exit(self, controller):
        print("Exited")

    def on_frame(self, controller):
        frame = controller.frame()

        if len(frame.fingers) > 0:
            self.get_position(frame)

            for command in self.commands:
                if(command.applicable(frame)):
                    number_for_fingers = self.get_number_for_fingers_string(frame)
                    syscommand = Config.get(command.name, number_for_fingers)
                    if(syscommand != ""):
                        os.system(syscommand)
                        print(syscommand)

    def get_number_for_fingers_string(self, frame):
        return "%dfinger" % len(frame.fingers)

    def get_position(self, frame):
        finger = frame.fingers[0]
        x = finger.tip_position[0] / 10
        y = (250 - finger.tip_position[1]) / 25

        number_for_fingers = self.get_number_for_fingers_string(frame)
        command = Config.get('move', number_for_fingers, raw=True)
        command = command % { 'x': x, 'y': y }
        os.system(command)

class ScreentapCommand():
    def __init__(self):
        self.name = "screentap"

    def applicable(self, frame):
        return(frame.gestures()[0].type == Leap.Gesture.TYPE_SCREEN_TAP)

class KeytapCommand():
    def __init__(self):
        self.name = "keytap"

    def applicable(self, frame):
        return(frame.gestures()[0].type == Leap.Gesture.TYPE_KEY_TAP)

class SwiperightCommand():
    def __init__(self):
        self.name = "swiperight"

    def applicable(self, frame):
        swipe = SwipeGesture(frame.gestures()[0])
        return(swipe.type == Leap.Gesture.TYPE_SWIPE and swipe.direction[0] < 0)

class SwipeleftCommand():
    def __init__(self):
        self.name = "swipeleft"

    def applicable(self, frame):
        swipe = SwipeGesture(frame.gestures()[0])
        return(swipe.type == Leap.Gesture.TYPE_SWIPE and swipe.direction[0] > 0)

class ClockwiseCommand():
    def __init__(self):
        self.name = "clockwise"

    def applicable(self, frame):
        circle = CircleGesture(frame.gestures()[0])
        return(circle.type == Leap.Gesture.TYPE_CIRCLE and
                circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/4)

class CounterclockwiseCommand():
    def __init__(self):
        self.name = "counterclockwise"

    def applicable(self, frame):
        circle = CircleGesture(frame.gestures()[0])
        return(circle.type == Leap.Gesture.TYPE_CIRCLE and
                circle.pointable.direction.angle_to(circle.normal) > Leap.PI/4)

def main():
    listener = SampleListener()
    controller = Leap.Controller()
    controller.add_listener(listener)
    print("Press Enter to quit...")
    sys.stdin.readline()
    controller.remove_listener(listener)


if __name__ == "__main__":
    main()
