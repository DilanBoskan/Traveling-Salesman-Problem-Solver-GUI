# GUI modules
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
import tkinter.font
import tkinter.ttk as ttk
# Plotting
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
# Calculation
import threading
import tsp
import random
import math
import time
# System Modules
import sys
import os
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
# Images
from PIL import ImageTk  # nopep8
from PIL import Image  # nopep8


def open_image(path: str, size: tuple = None, keep_aspect: bool = True, rotate: int = 0) -> ImageTk.PhotoImage:
    """
    Open the image on the path and apply given settings\n
    Paramaters:
        path(str):
            Absolute path of the image
        size(tuple):
            first value - width
            second value - height
        keep_aspect(bool):
            keep aspect ratio of image and resize
            to maximum possible width and height
            (maxima are given by size)
        rotate(int):
            clockwise rotation of image
    Returns(ImageTk.PhotoImage):
        Image of path
    """
    img = Image.open(path).convert(mode='RGBA')
    ratio = img.height/img.width
    img = img.rotate(angle=-rotate)
    if size is not None:
        size = (int(size[0]), int(size[1]))
        if keep_aspect:
            img = img.resize((size[0], int(size[0] * ratio)), Image.ANTIALIAS)
        else:
            img = img.resize(size, Image.ANTIALIAS)
    return ImageTk.PhotoImage(img)


# Change the current working directory to the directory
# this file sits in
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(base_path)

# -Global Variables-
figure = plt.Figure(figsize=(15, 15), dpi=100)
axis = figure.add_subplot(111)
finished = False
total_distance = 0
city_indexes = []
width = 20
height = 20


class MainWindow(tk.Tk):
    # --Constants--
    # None

    def __init__(self):
        # Run the __init__ method on the tk.Tk class
        super().__init__()
        # --Window Settings--
        self.withdraw()
        self.title('TSP Solver')
        self.configure(bg='#FFFFFF')  # Set background color
        self.update()

        # --Variables--
        self.fullscreen = False
        self.distanceModes = ['Miles', 'Yards', 'Foot', 'Inches',
                              'Kilometres', 'Metres', 'Centimetres', 'Millimetres']
        self.button_to_coords = {}
        self.points = []
        self.best_cities = []
        self.lines = []
        self.annotations = []
        self.distanceMode_var = tk.StringVar(value=self.distanceModes[0])
        # Images
        self.maximize_img = open_image('img/maximize.png',
                                       size=(15, 15))
        self.minimize_img = open_image('img/minimize.png',
                                       size=(15, 15))

        # --Widgets--
        self.create_widgets()
        self.configure_widgets()
        self.place_minimize()

        # -Other-
        self.update_total_distance()
        self.update_time_elapsed(0)
        self.deiconify()

    # -Widget Methods-

    def create_widgets(self):
        """Create window widgets"""
        self.top_Frame = tk.Frame(self,
                                  bg='#FFF')
        self.fill_top_Frame()
        self.leftLabel_Frame = tk.Frame(self,
                                        bg='#FFF')
        self.bottomLabel_Frame = tk.Frame(self,
                                          bg='#FFF')
        self.fill_label_Frames()
        self.grid_Frame = tk.Frame(self)
        self.fill_grid_Frame()
        self.plot_Frame = tk.Frame(self)
        self.plot_wig = FigureCanvasTkAgg(figure, self.plot_Frame).get_tk_widget()  # nopep8
        self.fill_plot_Frame()
        self.resize_Button = ttk.Button(self,
                                        command=self.switch_fullscreen)

    def configure_widgets(self):
        """Change widget styling and appearance"""

    def place_minimize(self):
        """Minimize Window"""
        # -Update Geometry-
        window_width = 1150
        window_height = 650
        self.geometry('{width}x{height}+{xpad}+{ypad}'.format(
            width=int(window_width),
            height=int(window_height),
            xpad=int(self.winfo_screenwidth()/2 -
                     window_width/2),
            ypad=int(self.winfo_screenheight()/2 - 30 -
                     window_height/2)))
        self.resizable(False, False)
        # -Update Widgets Position-
        self.top_Frame.place(x=0, y=0, width=0, height=80,
                             relx=0, rely=0, relwidth=1, relheight=0)
        self.leftLabel_Frame.place(x=0, y=100, width=50, height=500,
                                   relx=0, rely=0, relwidth=0, relheight=0)
        self.bottomLabel_Frame.place(x=50, y=600, width=500, height=50,
                                     relx=0, rely=0, relwidth=0, relheight=0)
        self.grid_Frame.place(x=50, y=100, width=500, height=500,
                              relx=0, rely=0, relwidth=0, relheight=0)
        self.plot_Frame.place(x=-500 - 50, y=100, width=500, height=500,
                              relx=1, rely=0, relwidth=0, relheight=0)
        self.plot_wig.place(x=0, y=0, width=0, height=0,
                            relx=0, rely=0, relwidth=1, relheight=1)
        self.resize_Button.place(x=-30, y=-30, width=25, height=25,
                                 relx=1, rely=1, relwidth=0, relheight=0)
        self.resize_Button.configure(image=self.maximize_img)

    def place_maximize(self):
        """Maximize Window"""
        # -Update Geometry-
        window_height = self.winfo_screenheight() - 70
        window_width = window_height
        # Set Geometry and Center Window
        self.geometry('{width}x{height}+{xpad}+{ypad}'.format(
            width=int(window_width),
            height=int(window_height),
            xpad=int(self.winfo_screenwidth()/2 -
                     window_width/2),
            ypad=int(self.winfo_screenheight()/2 - 35 -
                     window_height/2)))
        self.resizable(True, True)
        # -Update Widgets Position-
        self.top_Frame.place_forget()
        self.leftLabel_Frame.place_forget()
        self.bottomLabel_Frame.place_forget()
        self.grid_Frame.place_forget()
        self.plot_Frame.place(x=10, y=0, width=-10*2, height=-30,
                              relx=0, rely=0, relwidth=1, relheight=1)
        self.resize_Button.configure(image=self.minimize_img)

    def switch_fullscreen(self):
        """
        Switch between minimize and maximize
        """
        if self.fullscreen:
            self.place_minimize()
            self.fullscreen = False
        else:
            self.place_maximize()
            self.fullscreen = True

    def refill_grid_Frame(self):
        """
        Reset all clicked buttons on the grid
        """
        for wig in self.grid_Frame.winfo_children():
            row = self.button_to_coords[wig.winfo_name()]['row']
            col = self.button_to_coords[wig.winfo_name()]['col']
            wig.grid(row=row,
                     column=col,
                     ipady=50)

    def fill_label_Frames(self):
        """
        Fill the label Frames
        """
        for x in range(width):
            self.bottomLabel_Frame.columnconfigure(x, weight=1)
            label = tk.Label(self.bottomLabel_Frame,
                             text=x, bg='#FFF')
            label.place(relx=1/width * x, relwidth=1/width)
        self.leftLabel_Frame.columnconfigure(0, weight=1)
        for y in range(height):
            self.leftLabel_Frame.rowconfigure(y, weight=1)
            label = tk.Label(self.leftLabel_Frame,
                             text=(height - 1) - y, anchor=tk.E,
                             bg='#FFF')
            label.place(x=-4, relx=0,
                        relwidth=1, rely=1/height * y, relheight=1/height)

    def fill_top_Frame(self):
        """Fill Frame with neccessary widgets"""
        # -Create Widgets-
        font = tk.font.Font(size=15)
        self.title_Label = tk.Label(self.top_Frame, font=font, bg='#FFF',
                                    text='Traveling Salesman Problem Solver')
        self.reset_Button = ttk.Button(self.top_Frame,
                                       text='Reset',
                                       command=self.reset)
        font = tk.font.Font(size=10)
        self.distance_Label = tk.Label(self.top_Frame,
                                       font=font, bg='#FFF',
                                       anchor=tk.E,
                                       text='Show distance in',)
        self.distance_Optionmenu = ttk.Combobox(self.top_Frame,
                                                textvariable=self.distanceMode_var,
                                                justify=tk.CENTER,
                                                values=self.distanceModes,
                                                takefocus=False, state='readonly',)
        self.bind('<<ComboboxSelected>>',
                  lambda e: self.update_total_distance())
        font = tk.font.Font(size=9)
        self.wait_Label = tk.Label(self.top_Frame,
                                   font=font, bg='#FFF',
                                   text='',)
        self.calculate_Button = ttk.Button(self.top_Frame,
                                           text='Calculate',
                                           command=self.simulate)
        # -Place Widgets-
        self.title_Label.place(x=0, y=0, width=0, height=-26,
                               relx=0, rely=0, relwidth=1, relheight=1)
        self.reset_Button.place(x=50, y=-26, width=70, height=26,
                                relx=0, rely=1, relwidth=0, relheight=0)
        self.distance_Label.place(x=-150, y=-26, width=130, height=26,
                                  relx=0.5, rely=1, relwidth=0, relheight=0)
        self.distance_Optionmenu.place(x=0, y=-23, width=150, height=23,
                                       relx=0.5, rely=1, relwidth=0, relheight=0)
        self.wait_Label.place(x=15, y=-26, width=150, height=26,
                              relx=0.75, rely=1, relwidth=0, relheight=0)
        self.calculate_Button.place(x=-70 - 50, y=-26, width=70, height=26,
                                    relx=1, rely=1, relwidth=0, relheight=0)

    def fill_grid_Frame(self):
        """Fill Frame with neccessary widgets"""
        # -Create and Place Widgets-
        for x in range(width):
            self.grid_Frame.columnconfigure(x, weight=1)
            for y in range(height):
                self.grid_Frame.rowconfigure(y, weight=1)
                button = ttk.Button(self.grid_Frame,)
                self.button_to_coords[button.winfo_name()] = {
                    'row': y,
                    'col': x
                }
                button.configure(command=lambda wig=button: self.draw_point(wig))  # nopep8
                button.grid(row=y,
                            column=x,
                            ipady=50)

    def fill_plot_Frame(self):
        """
        Fill the matplotlib graph
        """
        axis.clear()

        axis.set_xlim(-0.5, width - 1 + 0.5)
        axis.set_ylim(-0.5, height - 1 + 0.5)

        axis.xaxis.set_major_locator(MultipleLocator(1))
        axis.yaxis.set_major_locator(MultipleLocator(1))

        axis.grid(alpha=0.2)
        self.update_total_distance()
        # Update canvas
        figure.canvas.draw()
        figure.canvas.flush_events()

    def reset(self):
        """
        Reset whole application
        """
        self.refill_grid_Frame()
        self.points.clear()
        self.fill_plot_Frame()
        global total_distance
        global finished
        finished = True
        total_distance = 0
        self.update_total_distance()
        self.update_time_elapsed(0)
        self.calculate_Button.configure(state=tk.NORMAL)

    def draw_point(self, wig):
        """
        Draws a point on the plot based on the widget that was clicked
        """
        # Remove widget from grid
        wig.grid_forget()
        # -Get coords-
        # Invert row
        row = (height - 1) - self.button_to_coords[wig.winfo_name()]['row']
        col = self.button_to_coords[wig.winfo_name()]['col']
        # -Draw point-
        axis.scatter(col, row, s=40, c='red', zorder=1)
        self.points.append((col, row))
        # -Update canvas-
        figure.canvas.draw()
        figure.canvas.flush_events()

    def draw_final_solution(self):
        """
        Draw all lines connecting each point
        """
        global total_distance
        total_distance = 0
        bbox_props = dict(fc="#FFFFFF", ec="#000000", lw=1, alpha=0.8)
        city_indexes.insert(0, city_indexes[-1])
        for i, idx in enumerate(city_indexes[:-1]):
            # Get coords
            x1 = self.points[idx][0]
            y1 = self.points[idx][1]
            x2 = self.points[city_indexes[i+1]][0]
            y2 = self.points[city_indexes[i+1]][1]

            # Draw line
            self.lines.append(axis.plot([x1, x2], [y1, y2],
                                        c='grey', lw=1.5, zorder=0)[0])

            # Calculate distance
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            total_distance += distance
            # Round distance
            distance = round(distance, 2)
            if distance.is_integer():
                distance = int(distance)
            # Display distance
            self.annotations.append(axis.annotate(distance, xy=(x1 + (x2-x1)/2, y1 + (y2-y1)/2),
                                                  size=8, zorder=2,
                                                  bbox=bbox_props))
        else:
            # Round total distance
            total_distance = round(total_distance, 2)
            if total_distance.is_integer():
                total_distance = int(total_distance)
            self.update_total_distance()

    def update_total_distance(self):
        """
        Update the title of the plot
        """
        axis.set_title(f'{total_distance} {self.distanceMode_var.get().lower()}')  # nopep8
        # Update canvas
        figure.canvas.draw()
        figure.canvas.flush_events()

    def update_time_elapsed(self, seconds):
        """
        Update total time elapsed
        """
        self.wait_Label.configure(text=f"Time Elapsed: {time.strftime('%H:%M:%S', time.gmtime(seconds))}")  # nopep8

    def simulate(self):
        """
        Solve the TSP
        """
        global finished
        global city_indexes
        if len(self.points) < 2:
            tk.messagebox.showerror(title='Too Few Points',
                                    message='Please make sure you select at least 2 points for the Traveling Salesman Problem!')
            return
        self.calculate_Button.configure(state=tk.DISABLED)
        # Reset variables
        finished = False
        city_indexes = []
        # Clear previous solution
        for line in self.lines:
            line.remove()
        self.lines.clear()
        for annotation in self.annotations:
            annotation.remove()
        self.annotations.clear()
        # Start Timer
        stime = time.perf_counter()

        def calculate():
            global finished
            global city_indexes
            city_indexes = tsp.tsp(self.points)[1]
            finished = True
        threading.Thread(target=calculate).start()

        def draw():
            global finished
            global city_indexes
            while not finished:
                # Wait for solution
                self.update_time_elapsed(time.perf_counter() - stime)
                self.update()
            else:
                # Finished Solving the TSP
                self.draw_final_solution()
        draw()

        # Update canvas
        figure.canvas.draw()
        figure.canvas.flush_events()

        self.calculate_Button.configure(state=tk.NORMAL)
        print(f'Time: {round(time.perf_counter() - stime, 2)}s')


if __name__ == "__main__":
    # Create Window
    root = MainWindow()

    root.mainloop()
