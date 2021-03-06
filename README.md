# Traveling Salesman Problem Solver GUI
A desktop application written in python that lets the user select certain points on a 20x20 grid, which are then connected with the shortest possible route.
<p align="center">
    <img src="showcase.gif" alt="GUI Showcase"/>
</p>

[![Downloads](https://img.shields.io/github/downloads/DilanBoskan/Traveling-Salesman-Problem-Solver-GUI/total.svg)](https://github.com/DilanBoskan/Traveling-Salesman-Problem-Solver-GUI/releases/latest)

## Motivation
Personal interest to provide an aesthetically pleasing and efficient GUI to solve an algorithmic, relatively difficult problem.

## Features
* Solve the TSP
* Save the solution as an image
    * Supported file types:<br>png, jpg, jpeg, pdf, pgf, ps, raw, rgba, svg, sv, tif, tiff
* Easy and intuitive to use grid for selecting points (20x20)
* Fullscreen the solution
* Choose between multiple length representations
    * Miles, Yards, Foot, Inches, Kilometres, Metres, Centimetres, Millimetres
* Timer

## Installation
Requires: **Python 3.7** or above<br>

```pip install --no-cache-dir -r requirements.txt```

## How to use

Run Source code: ```python main.py```<br>
Convert to executable (.exe):
1. ```pyinstaller --distpath [EXPORT DIRECTORY] --hidden-import tkinter --exclude-module PySide2 --exclude-module PyQt5 -w main.py```
2. Copy pulp folder *"[PYTHON PATH]/Lib/site-packages/pulp"* inside *"[EXPORT DIRECTORY]/main"* folder
3. Run *"[EXPORT DIRECTORY]/main/main.exe"*

## Additional Info
Project Start: 23.10.2020 <sub>(DD.MM.YYYY)</sub><br>
Project End: 24.10.2020 <sub>(DD.MM.YYYY)</sub><br><br>
Time spent: 05:15 <sub>(HH:MM)</sub>
