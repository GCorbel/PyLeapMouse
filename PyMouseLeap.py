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
        self.swipeleft_count = 0
        self.swiperight_count = 0
        self.clockwise_count = 0
        self.counterclockwise_count = 0

    def on_connect(self, controller):
        print("Connected")

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print("Disconnected")

    def on_exit(self, controller):
        print("Exited")

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        if not frame.fingers.empty:
            # Gestures
            for gesture in frame.gestures():
                if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                    print("key tap")
                    os.system(Config.get('Commands', 'keytap'))

                if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                    print("screen tap")
                    os.system(Config.get('Commands', 'screentap'))

                if gesture.type == Leap.Gesture.TYPE_SWIPE:
                    swipe = SwipeGesture(gesture)
                    if swipe.direction[0] > 0:
                        self.swipeleft_count += 1
                        if self.swipeleft_count == 10:
                            print("to left")
                            os.system(Config.get('Commands', 'swiftleft'))
                    else:
                        self.swiperight_count += 1
                        if self.swiperight_count == 10:
                            print("to right")
                            os.system(Config.get('Commands', 'swiftright'))
                else:
                    self.swipeleft_count = 0
                    self.swiperight_count = 0


                if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                    circle = CircleGesture(gesture)

                    if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/4:
                        self.clockwise_count += 1
                        if self.clockwise_count == 10:
                            print("clockwise")
                            os.system(Config.get('Commands', 'clockwise'))
                    else:
                        self.counterclockwise_count += 1
                        if self.counterclockwise_count == 10:
                            print("counterclockwise")
                            os.system(Config.get('Commands', 'counterclockwise'))
                else:
                    self.clockwise_count = 0
                    self.counterclockwise_count = 0

def main():
    # Create a sample listener and controller
    listener = SampleListener()

    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print("Press Enter to quit...")
    sys.stdin.readline()

    # Remove the sample listener when done
    controller.remove_listener(listener)


if __name__ == "__main__":
    main()
