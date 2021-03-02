# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, Toplevel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from pandas import DataFrame
import datetime
import socket
from proc_mem_monitor import PROGRAM_NAME, VERSION, COMBO_WIDTH, LABEL_WIDTH, \
    FIGURE_DPI, DEFAULT_REFRESH_INTERVAL


class ProcMemPlot:
    def __init__(self, hostname=None):
        self.peak_mem = 0
        self.total_mem = 1024
        self.pause_plot = 0
        self.hostname = hostname

        # members for GUI
        self.window_plot = None

        self.figure_hist = None
        self.plot_axe_hist = None
        self.y_ax = None
        self.canvas_hist = None
        self.frame_toolbar = None
        self.toolbar_plot = None
        self.button_plot_pause = None

        # members for plot data.
        self.time_hist = {}
        self.mem_hist = {}

    def plot_metrics(self):
        if (not (self.window_plot is not None and \
                 tk.Toplevel.winfo_exists(self.window_plot))) or \
            self.time_hist.get('rss_total') is None or self.pause_plot == 1:
            return

        self.plot_axe_hist.clear()
        y_hist_dict = {'time': self.time_hist['rss_total'],
                       'mem': self.mem_hist['rss_total']}
        y_hist_df = DataFrame(y_hist_dict, columns=['time', 'mem'])
        y_hist_df.plot(kind='line', legend=True, x='time', y='mem',
                        ax=self.plot_axe_hist, color='r', marker='.', fontsize=10)

        self.plot_axe_hist.set_ylabel('Memory(GB)')
        self.plot_axe_hist.set_title('Memory (GB) History - max=' + str(self.peak_mem))
        self.plot_axe_hist.set_ylim([0, self.total_mem])
        self.canvas_hist.draw()

    def toggle_pause_plot(self):
        if self.pause_plot == 0:
            self.pause_plot = 1
            self.button_plot_pause['text'] = 'Resume'
        else:
            self.pause_plot = 0
            self.button_plot_pause['text'] = 'Pause'
  
    def show_plot_window(self, root_window):
        if self.window_plot is not None and tk.Toplevel.winfo_exists(self.window_plot):
            return

        self.window_plot = Toplevel(root_window)
        self.window_plot.geometry('1200x600+20+500')
        self.window_plot.title(PROGRAM_NAME + ' ' + VERSION + ' - plot - ' + self.hostname)
        self.window_plot.grid_columnconfigure(0, weight=1)

        cur_grid_row = 0
        # plot row
        self.figure_hist = plt.Figure(figsize=(10, 5), dpi=FIGURE_DPI)
        self.plot_axe_hist = self.figure_hist.add_subplot(111)
        self.canvas_hist = FigureCanvasTkAgg(self.figure_hist, self.window_plot)
        self.canvas_hist.get_tk_widget().grid(row=cur_grid_row, column=0, sticky='nsew')
        self.window_plot.grid_rowconfigure(cur_grid_row, weight=1)
        cur_grid_row = cur_grid_row + 1

        # Plot navigation toolbar
        self.frame_toolbar = tk.Frame(self.window_plot)
        self.frame_toolbar.grid(row=cur_grid_row, column=0)
        self.toolbar_plot = NavigationToolbar2Tk(self.canvas_hist, self.frame_toolbar)
        cur_grid_row = cur_grid_row + 1

        # command buttons
        self.button_plot_pause = ttk.Button(self.window_plot, text="Pause", 
                                            command=self.toggle_pause_plot)
        self.button_plot_pause.grid(row=cur_grid_row, column=0)
        cur_grid_row = cur_grid_row + 1

    def update_history(self, mem_usages):
        if self.time_hist.get('rss_total') is None:
            self.time_hist['rss_total'] = []
            self.mem_hist['rss_total'] = []

        cur_time = datetime.datetime.now().strftime("%m/%d %H:%M")
        self.time_hist['rss_total'].append(cur_time)
        self.mem_hist['rss_total'].append(mem_usages['rss_total']['rss'])
        if mem_usages['rss_total']['rss'] > self.peak_mem:
            self.peak_mem = mem_usages['rss_total']['rss']
            print('INFO: @{} peak memory={} total memory={}'.format(
                cur_time, self.peak_mem, self.total_mem))
