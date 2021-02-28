# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, Toplevel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from pandas import DataFrame
import datetime

from proc_mem_monitor import PROGRAM_NAME, VERSION, COMBO_WIDTH, LABEL_WIDTH, \
    FIGURE_DPI, DEFAULT_REFRESH_INTERVAL


class ProcMemPlot:
    def __init__(self):
        self.selected_pid = None
        self.max_mem = 0

        # members for GUI
        self.window_plot = None

        self.figure_hist = None
        self.plot_axe_hist = None
        self.y_ax = None
        self.canvas_hist = None
        self.frame_toolbar = None
        self.toolbar_plot = None

        # members for plot data.
        self.time_hist = {}
        self.mem_hist = {}

    def plot_metrics(self):
        if not (self.window_plot is not None and tk.Toplevel.winfo_exists(self.window_plot)):
            return

        self.plot_axe_hist.clear()
        y_hist_dict = {'time': self.time_hist[self.selected_pid],
                       'mem': self.mem_hist[self.selected_pid]}
        y_hist_df = DataFrame(y_hist_dict, columns=['time', 'mem'])
        y_hist_df.plot(kind='line', legend=True, x='time', y='mem',
                        ax=self.plot_axe_hist, color='r', marker='.', fontsize=10)

        self.plot_axe_hist.set_ylabel('Memory(KB)')
        self.plot_axe_hist.set_title('Memory (KB) History')
        self.plot_axe_hist.set_ylim([500000, 200000000])
        self.canvas_hist.draw()

    def show_plot_window(self, root_window, pid):
        self.selected_pid = pid
        if self.window_plot is not None and tk.Toplevel.winfo_exists(self.window_plot):
            return

        self.window_plot = Toplevel(root_window)
        self.window_plot.title(PROGRAM_NAME + VERSION + ' - plot')

        cur_grid_row = 0
        # plot row
        self.figure_hist = plt.Figure(figsize=(10, 5), dpi=FIGURE_DPI)
        self.plot_axe_hist = self.figure_hist.add_subplot(111)
        self.canvas_hist = FigureCanvasTkAgg(self.figure_hist, self.window_plot)
        self.canvas_hist.get_tk_widget().grid(row=cur_grid_row, columnspan=4, sticky='nsew')
        cur_grid_row = cur_grid_row + 1

        # Plot navigation toolbar
        self.frame_toolbar = tk.Frame(self.window_plot)
        self.frame_toolbar.grid(row=cur_grid_row, columnspan=4)
        self.toolbar_plot = NavigationToolbar2Tk(self.canvas_hist, self.frame_toolbar)
        cur_grid_row = cur_grid_row + 1

    def update_history(self, mem_usages):
        for k in mem_usages.keys():
            pid = k

        if self.time_hist.get(pid) is None:
            self.time_hist[pid] = []
            self.mem_hist[pid] = []

        cur_time = datetime.datetime.now().strftime("%m/%d %H:%M")
        self.time_hist[pid].append(cur_time)
        self.mem_hist[pid].append(mem_usages[pid])
        if mem_usages[pid] > self.max_mem:
            self.max_mem = mem_usages[pid]
            print('INFO: @{} max memory={}'.format(cur_time, self.max_mem))
        #print('mem_usages', pid, mem_usages[pid])