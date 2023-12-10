from gcodeparser import GcodeParser
from src.commander import Commander, DummyCommander
from src.tracer import Tracer, DummyTracer


class GCodeInterpreter:
    '''
    GCodeInterpreter class to interpret gcode and send commands to the robot
    
    Parameters
    ----------
    gcode_file : str
        The path to the gcode file to interpret
    commander : Commander
        The Commander object to send the commands to the robot
    '''
    gcode_file: str
    commander: Commander
    tracer: Tracer
    robot_pos: dict

    __slots__ = ('gcode_file', 'commander', 'robot_pos', 'tracer')

    origin_offset = {'X': 0.3, 'Y': 0.3, 'Z': 0.1}

    def __init__(self, gcode_file: str, commander: Commander, tracer: Tracer):
        self.gcode_file = gcode_file
        self.commander = commander
        self.tracer = tracer

        self.robot_pos = {'X': 0, 'Y': 0, 'Z': 0, 'E': 0, 'F': 0} # x y z extruder feedrate


    def next_line(self):
        """
        Get the next move line of gcode.
    
        Parameters
        ----------
        None
        
        Yields
        ------
        GcodeLine
            The next G command line of gcode.
        """

        print(f'Opening gcode file: {self.gcode_file}')

        with open(self.gcode_file, 'r') as f:
            gcode = f.read()

        parsed_gcode = GcodeParser(gcode, include_comments=False)
        for l in parsed_gcode.lines:
            # We only want to yield lines that are G0 or G1 commands
            if l.command[0] == 'G':
                yield l


    def send_commands(self):
        '''
        Send the commands to the robot
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        '''

        for line in self.next_line():

            # Send the command to the robot
            # If the command is a G0 we don't want to be extruding
            if line.command[1] == 0:
                # Update the robot's position with the new coordinates
                self.robot_pos.update(line.params)
                # Send the command, ignoring the extrusion and feedrate
                x = self.robot_pos['X'] / 1000 + self.origin_offset['X']
                y = self.robot_pos['Y'] / 1000 + self.origin_offset['Y']
                z = self.robot_pos['Z'] / 1000 + self.origin_offset['Z']

                if self.tracer.is_extruding():
                    self.tracer.disable()

                self.commander.move_g0(x, y, z)

            # If the command is a G1 we want to be extruding
            elif line.command[1] == 1:
                # Update the robot's position with the new coordinates
                self.robot_pos.update(line.params)
                # Send the command, ignoring the feedrate
                x = self.robot_pos['X'] / 1000 + self.origin_offset['X']
                y = self.robot_pos['Y'] / 1000 + self.origin_offset['Y']
                z = self.robot_pos['Z'] / 1000 + self.origin_offset['Z']
                e = self.robot_pos['E'] / 1000
                f = self.robot_pos['F'] / 1000

                if not self.tracer.is_extruding():
                    self.tracer.enable()
                    
                self.commander.move_g1(x, y, z, e, f)


def main():
    # Create a Commander object
    commander = DummyCommander()

    # Create a GCodeInterpreter object
    interpreter = GCodeInterpreter('gcode_files/test.gcode', commander)

    # Send the commands to the robot
    interpreter.send_commands()


if __name__ == '__main__':
    main()
