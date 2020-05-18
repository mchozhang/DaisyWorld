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
        self.length = data["side-length"]
        self.area = self.length ** 2
        Patch.WHITE_ALBEDO = data["white-albedo"]
        Patch.BLACK_ALBEDO = data["black-albedo"]
        Patch.SOLAR_LUMINOSITY = data["solar-luminosity"]
        Patch.SURFACE_ALBEDO = data["surface-albedo"]
        Patch.INIT_TEMPERATURE = data["init-temperature"]
        Patch.SIDE_LENGTH = self.length

        # initial daisy positions
        white_init_num = int(self.area * white_init_rate)
        black_init_num = int(self.area * black_init_rate)

        # init global statistics
        self.global_temperature = Patch.INIT_TEMPERATURE
        self.population = white_init_num + black_init_num
        self.black_num = black_init_num
        self.white_num = white_init_num

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
        for x in range(self.length):
            for y in range(self.length):
                patch = Patch(x, y)
                index = x * self.length + y
                if index in white_indices:
                    patch.grow_white_daisy()
                elif index in black_indices:
                    patch.grow_black_daisy()
                self.patches[(x, y)] = patch

    def run(self, tick):
        """
        the world runs for 1 time step
        """
        temperature = 0
        population = 0
        white, black = 0, 0
        print("tick:", tick,
              "temperature:", self.global_temperature,
              "population:", self.population,
              "black:", self.black_num,
              "white:", self.white_num)

        diffusion_counter = dict()

        for x in range(self.length):
            for y in range(self.length):
                patch = self.patches[(x, y)]
                patch.calculate_temperature()
                patch.age(self.patches)
                diffusion_counter[(x, y)] = patch.temperature * 0.5

        for x in range(self.length):
            for y in range(self.length):
                patch = self.patches[(x, y)]
                # diffuse and absorb energy
                absorbed = sum([diffusion_counter[pos] / 8
                                for pos in patch.get_neighbors()])
                diffused = diffusion_counter[(x, y)]
                patch.temperature = patch.temperature - diffused + absorbed

                # count global values
                temperature += patch.temperature
                if not patch.is_empty():
                    population += 1
                    if patch.is_white():
                        white += 1
                    else:
                        black += 1

        self.global_temperature = temperature / self.area
        self.population = population
        self.black_num = black
        self.white_num = white

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
                 for x in range(self.length) for y in range(self.length)]
        print(template.format(*cells))
