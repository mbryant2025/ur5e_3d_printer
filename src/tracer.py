from abc import ABC, abstractmethod


class Tracer(ABC):
    '''
    Tracer class to provide an interface to enable and disable extrusion
    '''

    @abstractmethod
    def enable(self):
        '''
        Move the robot to the given position
        '''
        pass

    @abstractmethod
    def disable(self):
        '''
        Move the robot to the given position and extrude
        '''
        pass

    @abstractmethod
    def is_extruding(self):
        '''
        Move the robot to the given position and extrude
        '''
        pass


class DummyTracer(Tracer):
    '''
    DummyTracer class to provide an interface to enable and disable extrusion
    '''

    def __init__(self):
        self.extruding = False

    def enable(self):
        '''
        Move the robot to the given position
        '''
        print(f'Emitting extrusion')
        self.extruding = True

    def disable(self):
        '''
        Move the robot to the given position and extrude
        '''
        print(f'Emitting stop extrusion')
        self.extruding = False

    def is_extruding(self):
        '''
        Move the robot to the given position and extrude
        '''
        return self.extruding


