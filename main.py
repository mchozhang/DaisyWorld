#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
main function
"""
import sys
import os
import json
from world import World
from utils import draw_plot


def main():
    """
    initialize the world from the parameter file
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parameter_file = os.path.join(dir_path, sys.argv[1])
    with open(parameter_file) as file:
        parameters = json.load(file)
        world = World(parameters)

        ticks = parameters["ticks"]
        for i in range(ticks):
            world.print_world()
            world.run(i)

        # draw a plot
        draw_plot(world.output())


if __name__ == "__main__":
    main()
