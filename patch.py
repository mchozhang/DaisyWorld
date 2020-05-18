#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A patch is a cell of the grid world in which can grow a daisy
"""
import math
import random


class Patch:
    SURFACE_ALBEDO = 0
    WHITE_ALBEDO = 0
    BLACK_ALBEDO = 0
    SOLAR_LUMINOSITY = 0
    DAISY_LIFETIME = 25
    INIT_TEMPERATURE = 0
    SIDE_LENGTH = 0

    BLACK_DAISY = 0
    WHITE_DAISY = 1
    EMPTY = 2

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.daisy = Patch.EMPTY
        self.daisy_age = 0
        self.temperature = Patch.INIT_TEMPERATURE

    def is_empty(self):
        """
        whether the patch is empty
        :return: boolean result
        """
        return self.daisy == Patch.EMPTY

    def grow_white_daisy(self):
        """
        grow a white daisy in this patch
        """
        self.daisy_age = random.randint(0, Patch.DAISY_LIFETIME)
        self.daisy = Patch.WHITE_DAISY

    def grow_black_daisy(self):
        """
        grow a black daisy in this patch
        """
        self.daisy_age = random.randint(0, Patch.DAISY_LIFETIME)
        self.daisy = Patch.BLACK_DAISY

    def daisy_dies(self):
        """
        the daisy in this patch dies
        """
        self.daisy_age = 0
        self.daisy = Patch.EMPTY

    def age(self, patches):
        """
        the daisy in this patch ages for 1 time step
        :param patches patches of the world
        """
        self.daisy_age += 1
        if self.daisy_age < Patch.DAISY_LIFETIME:
            self.seed(patches)
        else:
            self.daisy_dies()

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
        if random.uniform(0, 1) < threshold:
            # neighbors that are empty
            neighbors = [patches[pos] for pos in self.get_neighbors()
                         if patches[pos].daisy == Patch.EMPTY]
            if neighbors:
                # propagate a seed to one of the neighbors
                neighbor = neighbors[random.randint(0, len(neighbors) - 1)]
                if self.daisy == Patch.BLACK_DAISY:
                    neighbor.grow_black_daisy()
                elif self.daisy == Patch.WHITE_DAISY:
                    neighbor.grow_white_daisy()

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

    def __repr__(self):
        if self.is_empty():
            return "   "
        return " ❍ " if self.is_white() else " ✺ "
