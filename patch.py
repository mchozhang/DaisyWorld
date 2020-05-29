#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A patch is a cell of the grid world in which can grow a daisy
"""
import math
import random


class Patch:
    # the albedo(percentage of solar energy absorbed) of empty patches
    SURFACE_ALBEDO = 0
    WHITE_ALBEDO = 0
    BLACK_ALBEDO = 0

    # solar energy
    SOLAR_LUMINOSITY = 0

    # max age for all daisies
    MAX_AGE = 25

    # temperature of the world
    INIT_TEMPERATURE = 0

    # the size of the world
    SIDE_LENGTH = 0

    # extension parameters
    INIT_SOIL_QUALITY = 1
    SOIL_QUALITY_MODE = False
    FLEXIBLE_DAISY_LIFETIME = False

    # types of daisy
    BLACK_DAISY = 0
    WHITE_DAISY = 1
    EMPTY = 2

    def __init__(self, x, y):
        # position attributes
        self.x = x
        self.y = y
        self.pos = (x, y)

        # daisy attributes
        self.daisy = Patch.EMPTY
        self.daisy_age = 0
        self.daisy_lifetime = Patch.MAX_AGE
        self.lifetime_bonus = 0

        # temperature of the patch
        self.temperature = Patch.INIT_TEMPERATURE

        # soil quality, only useful when the mode is turned on
        self.soil_quality = Patch.INIT_SOIL_QUALITY

    def is_empty(self):
        """
        whether the patch is empty
        :return: boolean result
        """
        return self.daisy == Patch.EMPTY

    def grow_daisy(self, age=0, color=0):
        """
        grow a black daisy in this patch
        :param age initial age
        :param color color of the daisy
        """
        self.daisy = color
        self.daisy_age = age
        self.lifetime_bonus = 0
        self.daisy_lifetime = Patch.MAX_AGE

    def daisy_dies(self):
        """
        the daisy in this patch dies
        """
        self.daisy_age = 0
        self.lifetime_bonus = 0
        self.daisy_lifetime = 0
        self.daisy = Patch.EMPTY

    def age(self, patches):
        """
        the daisy in this patch ages for 1 time step
        :param patches patches of the world
        """
        if Patch.SOIL_QUALITY_MODE:
            self.soil_quality_changes()

        if Patch.FLEXIBLE_DAISY_LIFETIME:
            self.daisy_lifetime_changes()

        if self.is_empty():
            return

        self.daisy_age += 1
        if self.daisy_age < self.daisy_lifetime:
            self.seed(patches)
        else:
            self.daisy_dies()

    def daisy_lifetime_changes(self):
        """
        daisy lifetime changes as the temperature changes
        """
        if 18 < self.temperature < 25:
            # daisy lifetime increases when temperature is livable
            self.lifetime_bonus += 1
            if self.lifetime_bonus == 3:
                self.daisy_lifetime += 1
                self.lifetime_bonus = 0
        else:
            # daisy lifetime decreases when temperature is unlivable
            self.daisy_lifetime -= 1
            self.lifetime_bonus = 0

    def soil_quality_changes(self):
        """
        change soil quality as daisy grows
        """
        if self.is_empty() and self.soil_quality < 1:
            # soil quality increases when no daisy is growing
            self.soil_quality += 0.01

        elif self.soil_quality > 0.01:
            # soil quality degrades when a daisy is growing
            self.soil_quality -= 0.01

    def seed(self, patches):
        """
        propagate seed to neighbors if temperature permits
        :param patches: all the patches
        """
        # parabola with a peak of 1, temperature in range of [5, 40]
        # will have positive threshold value and probability to propagate seeds
        threshold = \
            0.1457 * self.temperature - 0.0032 * self.temperature ** 2 - 0.6443

        # probability to obtain a seed from neighbor and grow a new daisy
        probability = random.uniform(0, 1)
        if Patch.SOIL_QUALITY_MODE:
            probability = random.uniform(0, 1) / self.soil_quality

        if probability < threshold:
            # neighbors that are empty
            neighbors = [patches[pos] for pos in self.get_neighbors()
                         if patches[pos].daisy == Patch.EMPTY]
            if neighbors:
                # propagate a seed to one of the neighbors
                neighbor = neighbors[random.randint(0, len(neighbors) - 1)]
                neighbor.grow_daisy(color=self.daisy)

    def calculate_temperature(self):
        """
        calculate internal temperature by the energy absorbed
        """
        # calculate the absorbed luminosity
        if self.is_empty():
            absorbed_luminosity = \
                (1 - Patch.SURFACE_ALBEDO) * Patch.SOLAR_LUMINOSITY
        else:
            albedo = \
                Patch.WHITE_ALBEDO if self.is_white() else Patch.BLACK_ALBEDO
            absorbed_luminosity = (1 - albedo) * Patch.SOLAR_LUMINOSITY

        # calculate the local heating effect
        if absorbed_luminosity > 0:
            local_heating = 72 * math.log(absorbed_luminosity) + 80
        else:
            local_heating = 80

        # set the temperature at to be the average of the current temperature
        # and the local-heating effect
        self.temperature = (self.temperature + local_heating) / 2

    def is_white(self):
        """
        whether this patch has a white daisy
        :return: boolean result
        """
        return self.daisy == Patch.WHITE_DAISY

    def get_neighbors(self):
        """
        get list of neighbor positions
        :param: all the patches
        :return: position list
        """
        dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                (0, 1), (1, -1), (1, 0), (1, 1)]
        return [(self.x + dx, self.y + dy)
                for dx, dy in dirs if Patch.valid_pos(self.x + dx, self.y + dy)]

    @staticmethod
    def valid_pos(x, y):
        """
        whether the position is valid
        :return: boolean result
        """
        return -1 < x < Patch.SIDE_LENGTH and -1 < y < Patch.SIDE_LENGTH