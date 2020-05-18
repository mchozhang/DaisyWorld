#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np


def draw_plot(data):
    population = data["population"]
    temperature = data["temperature"]
    black = data["black-num"]
    white = data["white-num"]

    x_axis = list(range(len(population)))
    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.plot(x_axis, temperature, label='temperature')
    ax2.plot(x_axis, population, label='population')
    ax2.plot(x_axis, black, label='black')
    ax2.plot(x_axis, white, label='white')

    ax1.set_xlabel('ticks')
    ax1.set_ylabel('global temperature')
    ax2.set_xlabel('ticks')
    ax2.set_ylabel('population')
    plt.legend()
    plt.show()
