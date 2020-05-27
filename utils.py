#!/usr/bin/env python
# -*- coding: utf-8 -*-


def draw_plot(data):
    try:
        import matplotlib.pyplot as plt
    except:
        return

    luminosity = data["luminosity"]
    population = data["population"]
    temperature = data["temperature"]
    black = data["black-num"]
    white = data["white-num"]

    x_axis = list(range(len(population)))
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 10), dpi=80)

    ax1.plot(x_axis, luminosity, label='luminosity')
    ax2.plot(x_axis, temperature, label='temperature')
    ax3.plot(x_axis, population, label='population')
    ax3.plot(x_axis, black, label='black')
    ax3.plot(x_axis, white, label='white')
    ax3.legend(loc='upper right')

    ax1.set_xlabel('ticks')
    ax1.set_ylabel('Luminosity')
    ax2.set_xlabel('ticks')
    ax2.set_ylabel('Global Temperature')
    ax3.set_xlabel('ticks')
    ax3.set_ylabel('Population')
    plt.show()
