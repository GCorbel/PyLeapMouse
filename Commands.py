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

class LongCommand(object):
    def __init__(self):
        self.detected = 0

    def applicable(self, frame):
        if self.__check__(frame):
            self.detected += 1
            if self.detected == 20:
                return True
        else:
            self.detected = 0
        return False

class SwiperightCommand(LongCommand):
    def __init__(self):
        self.name = "swiperight"

    def __check__(self, frame):
        swipe = SwipeGesture(frame.gestures()[0])
        return(swipe.type == Leap.Gesture.TYPE_SWIPE and swipe.direction[0] < 0)

class SwipeleftCommand(LongCommand):
    def __init__(self):
        self.name = "swipeleft"

    def __check__(self, frame):
        swipe = SwipeGesture(frame.gestures()[0])
        return(swipe.type == Leap.Gesture.TYPE_SWIPE and swipe.direction[0] > 0)

class ClockwiseCommand(LongCommand):
    def __init__(self):
        self.name = "clockwise"

    def __check__(self, frame):
        circle = CircleGesture(frame.gestures()[0])
        return(circle.type == Leap.Gesture.TYPE_CIRCLE and
                circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/4)


class CounterclockwiseCommand(LongCommand):
    def __init__(self):
        self.name = "counterclockwise"

    def __check__(self, frame):
        circle = CircleGesture(frame.gestures()[0])
        return (circle.type == Leap.Gesture.TYPE_CIRCLE and
                circle.pointable.direction.angle_to(circle.normal) > Leap.PI/4)
