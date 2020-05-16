#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
main function
"""
import sys
import os
import json
from world import World


def main():
    """
    initialize the world from the parameter file
    :return:
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parameter_file = os.path.join(dir_path, sys.argv[1])
    with open(parameter_file) as file:
        parameters = json.load(file)
        world = World(parameters)
        # world.print_world()

        ticks = parameters["ticks"]
        for i in range(ticks):
            # world.print_world()
            world.run()


if __name__ == "__main__":
    main()