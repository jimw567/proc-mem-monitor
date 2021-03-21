# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, Toplevel, scrolledtext, messagebox
from tksheet import Sheet
import subprocess
import os
import json
import shutil
import datetime
import argparse
from pathlib import Path
import socket

from proc_mem_monitor.proc_mem_plot import ProcMemPlot
from proc_mem_monitor.proc_mem_handler import get_mem_usages
from proc_mem_monitor import VERSION, LABEL_WIDTH, COMBO_WIDTH, STATUS_CODES, \
                DEFAULT_REFRESH_INTERVAL, __resource_path__, __icon__, \
                SHEET_PID_COL, SHEET_CPU_COL, SHEET_RSS_COL, SHEET_CMD_COL, \
                SHEET_LAST_UPDATED_COL


#hostname = socket.gethostname()
hostname = 'host1'
proc_mem_plot = ProcMemPlot(hostname)


def show_plot_window():
    proc_mem_plot.show_plot_window(root_window)


###############################################################################
# root window
###############################################################################

root_window = tk.Tk()
root_window.geometry('1200x400+20+20')
root_window.title('Process Memory Monitor ' + VERSION + ' - ' + hostname)
root_window_icon = tk.PhotoImage(file=str(__icon__))
root_window.iconphoto(True, root_window_icon)
root_window.grid_columnconfigure(0, weight=0)
root_window.grid_columnconfigure(1, weight=0)
root_window.grid_columnconfigure(2, weight=0)
root_window.grid_columnconfigure(3, weight=1)

cur_grid_row = 0
label_pattern = ttk.Label(root_window, text="Command Pattern", width=LABEL_WIDTH, anchor='w')
label_pattern.grid(row=cur_grid_row, column=0,  sticky='w', padx=10, pady=10)
combo_pattern = ttk.Combobox(root_window, width=COMBO_WIDTH)
combo_pattern['values'] = []
combo_pattern.grid(row=cur_grid_row, column=1, sticky='w', pady=10)
cur_grid_row = cur_grid_row + 1

# sheet for pattern
sheet_proc = Sheet(root_window,
                   default_row_index="numbers", total_rows=200, total_columns=5)
sheet_proc.enable_bindings(("single_select",  # "single_select" or "toggle_select"
                            "drag_select",  # enables shift click selection as well
                            "column_drag_and_drop",
                            "row_drag_and_drop",
                            #"column_select",
                            "row_select",
                            "column_width_resize",
                            "double_click_column_resize",
                            "arrowkeys",
                            #"row_height_resize",
                            #"double_click_row_resize",
                            "right_click_popup_menu",
                            "rc_select",
                            #"rc_insert_column",
                            #"rc_delete_column",
                            #"rc_insert_row",
                            #"rc_delete_row",
                            "copy",
                            "cut",
                            "paste",
                            "delete",
                            "undo",
                            "edit_cell"))
sheet_proc.grid(row=cur_grid_row, columnspan=4, sticky='nswe')
root_window.grid_rowconfigure(cur_grid_row, weight=1)
sheet_proc.set_cell_data(0, SHEET_PID_COL, 'PID')
sheet_proc.set_cell_data(0, SHEET_CPU_COL, '%CPU')
sheet_proc.set_cell_data(0, SHEET_RSS_COL, 'RSS(GB)')
sheet_proc.set_cell_data(0, SHEET_CMD_COL, 'CMD')
sheet_proc.set_cell_data(0, SHEET_LAST_UPDATED_COL, 'Last Updated')
sheet_proc.column_width(column=SHEET_PID_COL, width=150)
sheet_proc.column_width(column=SHEET_CPU_COL, width=100)
sheet_proc.column_width(column=SHEET_RSS_COL, width=100)
sheet_proc.column_width(column=SHEET_CMD_COL, width=450)
sheet_proc.column_width(column=SHEET_LAST_UPDATED_COL, width=200)
cur_grid_row = cur_grid_row + 1
sheet_proc_last_row = 0

# command buttons
button_plot = ttk.Button(root_window, text="Plot", command=show_plot_window)
button_plot.grid(row=cur_grid_row, column=1, pady=10)
cur_grid_row = cur_grid_row + 1


def update_sheet_proc(mem_usage):
    global sheet_proc_last_row

    last_udpated = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    row = 1
    for k in mem_usage.keys():
        sheet_proc.set_cell_data(row, SHEET_PID_COL, k)
        sheet_proc.set_cell_data(row, SHEET_CPU_COL, mem_usage[k]['cpu'])
        sheet_proc.set_cell_data(row, SHEET_RSS_COL, mem_usage[k]['rss'])
        sheet_proc.set_cell_data(row, SHEET_CMD_COL, mem_usage[k]['cmd'])
        sheet_proc.set_cell_data(row, SHEET_LAST_UPDATED_COL, last_udpated)
        row = row + 1

    if sheet_proc_last_row > row:
        # clear contents from previous dump
        for r in range(row, sheet_proc_last_row+1):
            sheet_proc.set_cell_data(r, SHEET_PID_COL, '')
            sheet_proc.set_cell_data(r, SHEET_CPU_COL, '')
            sheet_proc.set_cell_data(r, SHEET_RSS_COL, '')
            sheet_proc.set_cell_data(r, SHEET_CMD_COL, '')
            sheet_proc.set_cell_data(r, SHEET_LAST_UPDATED_COL, '')

    # udpate the last row count
    sheet_proc_last_row = row

    sheet_proc.refresh()


# refresh database every DEFAULT_REFRESH_INTERVAL seconds
def refresh_database():
    global patterns

    #selected_pattern = combo_pattern.current()
    #pattern = patterns[selected_pattern]
    pattern = combo_pattern.get()
    mem_usages = get_mem_usages(pattern)

    if mem_usages is not None:
        update_sheet_proc(mem_usages)
        proc_mem_plot.update_history(mem_usages)
        proc_mem_plot.plot_metrics()

    # add refresh_database back to the eventloop
    root_window.after(DEFAULT_REFRESH_INTERVAL*1000, refresh_database)


def main():
    global prev_pattern, patterns

    parser = argparse.ArgumentParser()
    parser.add_argument('--config-file', dest='config_file', default=None,
                        help='Specify a JSON file for getting the data')
    args = parser.parse_args()

    home = os.path.expanduser("~")
    user_config_file = home + '/proc-mem-monitor-config.json'
    default_config_file = __resource_path__ / 'proc-mem-monitor-config.json'
    if Path(user_config_file).exists():
        config_file = Path(user_config_file)
    elif default_config_file.exists():
        config_file = default_config_file

    with open(config_file, 'r') as fp:
        config_dict = json.load(fp)

    # get total memory
    command = ['free', '-g']
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    free_out = p.stdout.read().decode('utf-8')
    mem_line = free_out.strip().split('\n')[1]
    proc_mem_plot.total_mem = int(mem_line.split()[1])

    patterns = config_dict.get('patterns', [])
    combo_pattern['values'] = patterns
    if len(patterns) > 0:
        combo_pattern.current(0)

    root_window.after(DEFAULT_REFRESH_INTERVAL*1000, refresh_database)
    root_window.mainloop()


if __name__ == '__main__':
    main()



