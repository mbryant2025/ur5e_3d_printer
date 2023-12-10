import argparse
from src.move import ROSCommander
from src.gcode import GCodeInterpreter
from src.tracer import DummyTracer


def main(gcode_file):
    # Create a Commander object
    commander = ROSCommander()

    # Create a Tracer object
    tracer = DummyTracer()

    # Move the robot to the start position
    commander.start_sequence()

    # Create a GCodeInterpreter object with the provided gcode file
    interpreter = GCodeInterpreter(gcode_file, commander, tracer)

    # Send the commands to the robot
    interpreter.send_commands()


if __name__ == '__main__':
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description='Process GCode file for robot movement')
    parser.add_argument('gcode_file', help='Path to the GCode file')
    args = parser.parse_args()

    # Call main function with the provided GCode file argument
    main(args.gcode_file)
