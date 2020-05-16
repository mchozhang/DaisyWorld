#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The daisy world is a square grid within which each patch can grow a daisy.
"""
import random
from patch import Patch


class World:
    def __init__(self, data):
        # parse initial data from data dictionary
        white_init_rate = data["white-start"]
        black_init_rate = data["black-start"]
        self.margin = data["margin"]
        self.area = data["area"]
        Patch.WHITE_ALBEDO = data["white-albedo"]
        Patch.BLACK_ALBEDO = data["black-albedo"]
        Patch.SOLAR_LUMINOSITY = data["solar-luminosity"]
        Patch.SURFACE_ALBEDO = data["surface-albedo"]
        Patch.INIT_TEMPERATURE = data["init-temperature"]

        # initial daisy positions
        white_init_num = int(self.area * white_init_rate)
        black_init_num = int(self.area * black_init_rate)

        # init global statistics
        self.global_temperature = Patch.INIT_TEMPERATURE
        self.population = white_init_num + black_init_num

        white_indices, black_indices = set(), set()
        while len(white_indices) < white_init_num:
            r = random.randint(0, self.area - 1)
            if r not in white_indices:
                white_indices.add(r)

        while len(black_indices) < black_init_num:
            r = random.randint(0, self.area - 1)
            if r not in white_indices and r not in black_indices:
                black_indices.add(r)

        # initial patches
        self.patches = dict()
        for i in range(self.margin):
            for j in range(self.margin):
                patch = Patch(i, j)
                index = i * self.margin + j
                if index in white_indices:
                    patch.grow_white_daisy()
                elif index in black_indices:
                    patch.grow_black_daisy()
                self.patches[(i, j)] = patch

    def run(self):
        """
        the world runs for 1 time step
        """
        temperature = 0
        population = 0
        white, black = 0, 0

        for i in range(self.margin):
            for j in range(self.margin):
                patch = self.patches[(i, j)]
                patch.calculate_temperature()
                if patch.is_empty():
                    patch.sprout(self.patches)
                else:
                    patch.age()
                    if patch.is_white():
                        white += 1
                    else:
                        black += 1
                    population += 1
                temperature += patch.temperature

                # if not patch.is_empty():
                #     if patch.is_white():
                #         white += 1
                #     else:
                #         black += 1
                #     population += 1

        self.global_temperature = temperature / self.area
        print("temperature:", self.global_temperature,
              "population:", population,
              "black:", black,
              "white:", white)

    def print_world(self):
        """
        print the world in an 8 * 8 grid
        """
        top_row = """
            ┌───┬───┬───┬───┬───┬───┬───┬───┐
          0 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│"""
        mid_row = """
            ├───┼───┼───┼───┼───┼───┼───┼───┤
         {} │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│"""
        bot_row = """
            ├───┼───┼───┼───┼───┼───┼───┼───┤
          7 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
            └───┴───┴───┴───┴───┴───┴───┴───┘
         y/x  0   1   2   3   4   5   6   7"""

        template = """
            ┌───┬───┬───┬───┬───┬───┬───┬───┐
          0 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
            ├───┼───┼───┼───┼───┼───┼───┼───┤
          1 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
            ├───┼───┼───┼───┼───┼───┼───┼───┤
          2 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
            ├───┼───┼───┼───┼───┼───┼───┼───┤
          3 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
            ├───┼───┼───┼───┼───┼───┼───┼───┤
          4 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
            ├───┼───┼───┼───┼───┼───┼───┼───┤
          5 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
            ├───┼───┼───┼───┼───┼───┼───┼───┤
          6 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
            ├───┼───┼───┼───┼───┼───┼───┼───┤
          7 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
            └───┴───┴───┴───┴───┴───┴───┴───┘
         y/x  0   1   2   3   4   5   6   7"""

        cells = [str(self.patches[(x, y)])
                 for x in range(self.margin) for y in range(self.margin)]
        print(template.format(*cells))


