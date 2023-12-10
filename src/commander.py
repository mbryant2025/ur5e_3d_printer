from abc import ABC, abstractmethod


class Commander(ABC):
    '''
    Commander class to provide an interface to move the robot
    Provides methods as perscribed by the GCodeInterpreter -- dependency injection
    '''

    @abstractmethod
    def move_g0(self, x: float, y: float, z: float):
        '''
        Move the robot to the given position
        '''
        pass

    @abstractmethod
    def move_g1(self, x: float, y: float, z: float, e: float, f: float):
        '''
        Move the robot to the given position and extrude
        '''
        pass


class DummyCommander(Commander):
    '''
    DummyCommander class to provide an interface to move the robot
    Provides methods as perscribed by the GCodeInterpreter -- dependency injection
    '''

    def move_g0(self, x: float, y: float, z: float):
        '''
        Move the robot to the given position
        '''
        print(f'G0 command sent to robot: x={x}, y={y} z={z}')

    def move_g1(self, x: float, y: float, z: float, e: float, f: float):
        '''
        Move the robot to the given position and extrude
        '''
        print(f'G1 command sent to robot: x={x}, y={y} z={z} e={e} f={f}')
