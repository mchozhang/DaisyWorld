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

        # run for the specified tick time
        ticks = parameters["ticks"]
        for i in range(ticks):
            world.run(i)

        # draw a plot if matplotlib has been installed
        draw_plot(world.result())

        # output the result to a csv file
        world.output_csv(os.path.join(dir_path, 'result.csv'))


if __name__ == "__main__":
    main()
