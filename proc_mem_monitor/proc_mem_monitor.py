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

from proc_mem_monitor.proc_mem_plot import ProcMemPlot
from proc_mem_monitor.proc_mem_handler import get_mem_usages
from proc_mem_monitor import VERSION, LABEL_WIDTH, COMBO_WIDTH, STATUS_CODES, \
                DEFAULT_REFRESH_INTERVAL, __resource_path__, __icon__, \
                SHEET_HOST_COL, SHEET_DEVICE_COL, SHEET_CU_COL, SHEET_CU_STATUS_COL, \
                SHEET_LAST_UPDATED_COL


auto_refresh_plot_seconds = 0
proc_mem_plot = ProcMemPlot()


def show_plot_window():
    pid = '28395'
    proc_mem_plot.show_plot_window(root_window, pid)


###############################################################################
# root window
###############################################################################
root_window = tk.Tk()
root_window.geometry('1500x400+20+20')
root_window.title('Process Memory Monitor ' + VERSION)
root_window_icon = tk.PhotoImage(file=str(__icon__))
root_window.iconphoto(True, root_window_icon)
root_window.grid_columnconfigure(0, weight=0)
root_window.grid_columnconfigure(1, weight=0)
root_window.grid_columnconfigure(2, weight=0)
root_window.grid_columnconfigure(3, weight=1)

cur_grid_row = 0
label_cluster = ttk.Label(root_window, text="Cluster", width=LABEL_WIDTH, anchor='w')
label_cluster.grid(row=cur_grid_row, column=0,  sticky='w')
combo_cluster = ttk.Combobox(root_window, width=COMBO_WIDTH)
combo_cluster['values'] = []
combo_cluster.grid(row=cur_grid_row, column=1, sticky='w')
cur_grid_row = cur_grid_row + 1

# sheet for cluster
sheet_cluster = Sheet(root_window,
                      default_row_index="numbers",
                      total_rows=200,
                      total_columns=5
                      )
sheet_cluster.enable_bindings(("single_select",  # "single_select" or "toggle_select"
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
sheet_cluster.grid(row=cur_grid_row, columnspan=4, sticky='nswe')
root_window.grid_rowconfigure(cur_grid_row, weight=1)
sheet_cluster.set_cell_data(0, 0, 'Host')
sheet_cluster.set_cell_data(0, 1, 'Device ID::Shell')
sheet_cluster.set_cell_data(0, 2, 'Compute Unit (CU)')
sheet_cluster.set_cell_data(0, 3, 'CU Status')
sheet_cluster.set_cell_data(0, 4, 'Last Updated')
sheet_cluster.column_width(column=SHEET_HOST_COL, width=150)
sheet_cluster.column_width(column=SHEET_DEVICE_COL, width=500)
sheet_cluster.column_width(column=SHEET_CU_COL, width=400)
sheet_cluster.column_width(column=SHEET_CU_STATUS_COL, width=100)
sheet_cluster.column_width(column=SHEET_LAST_UPDATED_COL, width=200)
cur_grid_row = cur_grid_row + 1

# command buttons
button_plot = ttk.Button(root_window, text="plot", command=show_plot_window)
button_plot.grid(row=cur_grid_row, column=2)
cur_grid_row = cur_grid_row + 1


# get xbutil dump from each host in round robin fashion every XBUTIL_REFRESH_INTERVAL
def refresh_database():
    global auto_refresh_host_idx, clusters, auto_refresh_sheet_row, \
           auto_refresh_plot_seconds

    selected_cluster = combo_cluster.current()
    refresh_host = clusters[combo_cluster['values'][selected_cluster]][auto_refresh_host_idx]

    mem_usages = get_mem_usages(['28349', '28395'])

    if mem_usages is not None:
        proc_mem_plot.update_history(mem_usages)

    proc_mem_plot.plot_metrics()

    # add refresh_database back to the eventloop
    root_window.after(DEFAULT_REFRESH_INTERVAL*1000, refresh_database)


def main():
    global plot_metric, prev_cluster_name, clusters, auto_refresh_host_idx, \
           auto_refresh_sheet_row

    parser = argparse.ArgumentParser()
    parser.add_argument('--json-file', dest='json_file', default=None,
                        help='Specify a JSON file for getting the data')
    parser.add_argument('--plot-type', dest='plot_metric', default='power',
                        help='Specify plot type: power, temperature, or voltage')
    args = parser.parse_args()
    plot_metric = args.plot_metric

    home = os.path.expanduser("~")
    user_config_file = home + '/proc-mem-monitor-config.json'
    default_config_file = __resource_path__ / 'proc-mem-monitor-config.json'
    cluster_names = []
    if Path(user_config_file).exists():
        config_file = Path(user_config_file)
    elif default_config_file.exists():
        config_file = default_config_file

    with open(config_file, 'r') as fp:
        xbutil_config_json = json.load(fp)

    clusters = xbutil_config_json.get('clusters', [])
    for k in clusters.keys():
        cluster_names.append(k)

    combo_cluster['values'] = cluster_names
    if len(cluster_names) > 0:
        combo_cluster.current(0)
        # populate the cluster spreadsheet
        row = 1
        for host in clusters[cluster_names[0]]:
            sheet_cluster.set_cell_data(row, 0, host)
            row = row + 1
        prev_cluster_name = cluster_names[0]
        auto_refresh_host_idx = 0
        auto_refresh_sheet_row = 1

    root_window.after(DEFAULT_REFRESH_INTERVAL*1000, refresh_database)
    root_window.mainloop()


if __name__ == '__main__':
    main()



