import sys, os, ConfigParser
sys.path.append('./lib')
sys.path.append('./lib/x64')
execfile('./Commands.py')

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

config = ConfigParser.ConfigParser()
config.read("./config.ini")

class PYMouseListener(Leap.Listener):
    def on_init(self, controller):
        print("Initialized")
        self.init_list_of_commands()

    def init_list_of_commands(self):
        self.commands = [
                ScreentapCommand(),
                SwiperightCommand(),
                SwipeleftCommand(),
                CounterclockwiseCommand(),
                ClockwiseCommand(),
                KeytapCommand()
        ]

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
            self.check_position(frame)
            self.check_motions(frame)

    def check_motions(self, frame):
        for command in self.commands:
            if(command.applicable(frame)):
                self.execute(frame, command.name)

    def execute(self, frame, command_name):
        number_for_fingers = self.get_fingers_code(frame)
        syscommand = config.get(command_name, number_for_fingers)
        if(syscommand != ""):
            os.system(syscommand)
            print(syscommand)

    def get_fingers_code(self, frame):
        return "%dfinger" % len(frame.fingers)

    def check_position(self, frame):
        finger = frame.fingers[0]
        x = finger.tip_position[0] / 10
        y = (250 - finger.tip_position[1]) / 25

        number_for_fingers = self.get_fingers_code(frame)
        command = config.get('move', number_for_fingers, raw=True)
        command = command % { 'x': x, 'y': y }
        os.system(command)

def main():
    listener = PYMouseListener()
    controller = Leap.Controller()
    controller.add_listener(listener)
    print("Press Enter to quit...")
    sys.stdin.readline()
    controller.remove_listener(listener)

if __name__ == "__main__":
    main()
