from custom.controller import CustomController
from simulator.metrics import Metrics
from simulator.plant import Plant
from simulator.requirements import Requirements
from simulator.simulator import Simulator

import os, getopt, sys

import pdb

# Temporary constants


def usage():
    ustr = ("Usage: python3 main.py -a <algorithm> -d <directory>\n"
            "\n"
            "\t-d, --directory\t\tdirectory where files are located\n"
            )
    print(ustr)

def main(dir_idx=None):
    directory = None
    plant_yaml = None
    requirements_yaml = None

    # Parse arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:", ["help", "dir"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    # Print help if no arguments
    if len(opts) == 0:
        usage()
        sys.exit()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-d", "--directory") and os.path.exists(arg):
            directory = arg
            plant_yaml = os.path.join(directory, "plant.yaml")
            requirements_yaml = os.path.join(directory, "requirements.yaml")
            yamls = [plant_yaml, requirements_yaml]
            for yaml in yamls:
                if not os.path.exists(yaml):
                    raise FileExistsError("%s does not exist" % (yaml))
        else:
            raise ValueError("Unknown (opt, arg): (%s, %s)" % (opt, arg))
    
    # Initialize classes
    requirements = Requirements(requirements_yaml)
    metrics = Metrics(directory, requirements) 

    plant = Plant(plant_yaml, requirements)
    controller = CustomController(requirements, plant, metrics)

    simulator = Simulator(plant, controller, requirements, metrics, directory)

    # Simulate system
    END_TIME = 10000
    DELTA_TIME = 1
    simulator.simulate(END_TIME, DELTA_TIME)

if __name__ == "__main__":
    dir_idx = 0
    main(dir_idx)
