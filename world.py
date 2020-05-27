#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The daisy world is a square grid within which each patch can grow a daisy.
"""
import random
import csv
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
        Patch.SOIL_QUALITY_MODE = data["soil-quality-mode"]
        self.mode = data["mode"]

        # initialize the number of daisies
        white_init_num = int(self.area * white_init_rate)
        black_init_num = int(self.area * black_init_rate)

        # init global statistics
        # index of the list indicates the tick number of the statistics
        self.luminosity_list = [Patch.SOLAR_LUMINOSITY]
        self.global_temperature_list = [Patch.INIT_TEMPERATURE]
        self.population_list = [white_init_num + black_init_num]
        self.black_num_list = [black_init_num]
        self.white_num_list = [white_init_num]

        # initialize daisy positions
        white_indices, black_indices = set(), set()
        while len(white_indices) < white_init_num:
            r = random.randint(0, self.area - 1)
            if r not in white_indices:
                white_indices.add(r)

        while len(black_indices) < black_init_num:
            r = random.randint(0, self.area - 1)
            if r not in white_indices and r not in black_indices:
                black_indices.add(r)

        # initialize patches with daisies
        self.patches = dict()
        for x in range(self.length):
            for y in range(self.length):
                patch = Patch(x, y)
                index = x * self.length + y
                random_age = random.randint(0, Patch.MAX_AGE)
                if index in white_indices:
                    patch.grow_daisy(random_age, Patch.WHITE_DAISY)
                elif index in black_indices:
                    patch.grow_daisy(random_age, Patch.BLACK_DAISY)

                patch.calculate_temperature()
                self.patches[(x, y)] = patch

    def run(self, tick):
        """
        the world runs for 1 time step
        :param tick: the tick number
        """
        temperature, population, white, black = 0, 0, 0, 0

        # calculate the internal temperature of each patch
        self.calculate_temperature()

        # update patch data
        for x in range(self.length):
            for y in range(self.length):
                patch = self.patches[(x, y)]
                # energy absorbed from neighbors
                absorbed = sum([self.patches[pos].temperature / 16
                                for pos in patch.get_neighbors()])
                # calculate ultimate temperature after diffusion
                patch.temperature = patch.temperature * 0.5 + absorbed

                # daisies are aging
                patch.age(self.patches)

                # count global values
                temperature += patch.temperature
                if not patch.is_empty():
                    population += 1
                    if patch.is_white():
                        white += 1
                    else:
                        black += 1

        # adjust solar luminosity by mode
        self.adjust_solar_luminosity(tick)

        # record data
        self.luminosity_list.append(Patch.SOLAR_LUMINOSITY)
        self.global_temperature_list.append(temperature / self.area)
        self.population_list.append(population)
        self.black_num_list.append(black)
        self.white_num_list.append(white)

    def calculate_temperature(self):
        """
        each patch calculates its own temperature
        """
        for x in range(self.length):
            for y in range(self.length):
                self.patches[(x, y)].calculate_temperature()

    def adjust_solar_luminosity(self, tick):
        """
        change the solar luminosity based on the current mode
        :param tick: the tick number
        """
        if self.mode == "ramp-up-ramp-down":
            if 200 < tick < 400:
                Patch.SOLAR_LUMINOSITY += 0.005
            elif 600 < tick < 850:
                Patch.SOLAR_LUMINOSITY -= 0.0025

        elif self.mode == "cycle":
            if tick % 100 / 2 == 0:
                Patch.SOLAR_LUMINOSITY += 0.005
            else:
                Patch.SOLAR_LUMINOSITY -= 0.0025

    def result(self):
        """
        get the statistic of every tick in a dictionary
        :return: dictionary of the running result
        """
        res = dict()
        res["luminosity"] = self.luminosity_list
        res["temperature"] = self.global_temperature_list
        res["population"] = self.population_list
        res["black-num"] = self.black_num_list
        res["white-num"] = self.white_num_list
        return res

    def output_csv(self, path):
        """
        output the result as csv file
        """
        res = self.result()
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['tick', 'solar-luminosity', 'global-temperature',
                             'population', 'black-number', 'white-number'])

            for i in range(len(res["temperature"])):
                row = [i,
                       res["luminosity"][i],
                       res["temperature"][i],
                       res["population"][i],
                       res["black-num"][i],
                       res["white-num"][i]]
                writer.writerow(row)


