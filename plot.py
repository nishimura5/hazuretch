import os

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib

## only for mac?
matplotlib.use("tkagg")

import pandas as pd
import seaborn as sns

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        master.geometry("800x600")
        master.title("バイオリン箱ひげ")
        input_frame = ttk.Frame(master)
        button_frame = ttk.Frame(master)
        graph_frame = ttk.Frame(master)
        hazure_frame = ttk.Frame(master)

        self.input_data = Inputdata(input_frame)
        input_frame.pack()

        load_button = tk.Button(button_frame, text="開く", width=15, command=lambda:[self.input_data.load_and_plot(canvas, ax), self.update_col_cbox()])
        load_button.grid(row=0, column=0)
        plot_cbox = ttk.Combobox(button_frame, values=['stripplot', 'swarmplot', 'none'], state='readonly')
        plot_cbox.grid(row=0, column=1)
        plot_cbox.bind("<<ComboboxSelected>>", lambda _ : [self.input_data.set_plot(canvas, ax, plot_cbox.get())])

        button_frame.pack()

        dpi = 200
        fig, ax = plt.subplots(figsize=(800/dpi,500/dpi), dpi=dpi)
        fig.canvas.mpl_connect("button_press_event", self.click)
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)

        toolbar = NavigationToolbar2Tk(canvas, graph_frame)
        toolbar.pack()
        canvas.get_tk_widget().pack()
        graph_frame.pack()

        self.column_cbox = ttk.Combobox(hazure_frame, state='readonly')
        self.column_cbox.grid(row=0, column=0)
        self.remove_lower_entry = tk.Entry(hazure_frame)
        self.remove_lower_entry.grid(row=0, column=1)
        self.remove_upper_entry = tk.Entry(hazure_frame)
        self.remove_upper_entry.grid(row=0, column=2)
        output_button = tk.Button(hazure_frame, text="除去", width=10, command=lambda:[self.remove_plots()])
        output_button.grid(row=0, column=3)

        hazure_frame.pack()

        master.protocol("WM_DELETE_WINDOW", toolbar.quit)

    def update_col_cbox(self):
        self.column_cbox['value'] = list(self.input_data.src_df.columns)

    def remove_plots(self):
        col = self.column_cbox.get()
        remove_lower = self.remove_lower_entry.get()
        remove_upper = self.remove_upper_entry.get()
        if self._is_float(remove_lower) and self._is_float(remove_upper):
            remove_lower = float(remove_lower)
            remove_upper = float(remove_upper)
        else:
            return
        print(col, remove_lower, remove_upper)

        self.input_data.src_df[(self.input_data.src_df[col] >= remove_lower)&(self.input_data.src_df[col] <= remove_upper)] = np.nan
        ## 除去後のデータをCSV出力
        self.input_data.src_df.to_csv('./dst.csv')
        self.input_data.plot()

    def _is_float(self, string):
        if string.replace(".", "").isnumeric():
            return True
        else:
            return False

    def click(self, event):
        x_val, y_val = (event.xdata, event.ydata)
        print(x_val, y_val)

class Inputdata(ttk.Frame):
    def __init__(self, input_frame):
        self.y_max = 100
        self.y_min = -100

    def load_and_plot(self, canvas, ax):
        self.canvas = canvas
        self.ax = ax
        self.load_file()
        self.plot(mode='none')

    def set_plot(self, canvas, ax, mode):
        self.canvas = canvas
        self.ax = ax
        self.plot(mode=mode)

    def load_file(self):
        script_path = os.path.abspath(os.path.dirname(__file__))
        file_path = filedialog.askopenfilename(initialdir=script_path)
        self.src_df = pd.read_csv(file_path, index_col='time')
        self.y_max = max(self.src_df.max())
        self.y_min = min(self.src_df.min())

    def plot(self, mode='none'):
        col_num = len(self.src_df.columns)

        self.ax.cla()
        self.ax.set_ylim(self.y_min, self.y_max)
        sns.violinplot(data=self.src_df, linewidth=1, inner=None, facecolor='None', ax=self.ax)
        if mode == 'swarmplot':
            sns.swarmplot(data=self.src_df, size=2, palette=['black' for x in range(col_num)], alpha=0.4, ax=self.ax)
        elif mode == 'stripplot':
            sns.stripplot(data=self.src_df, size=2, palette=['black' for x in range(col_num)], alpha=0.4, ax=self.ax)
        else:
            pass
        sns.boxplot(data=self.src_df, linewidth=1, color='lightgray', width=0.1, ax=self.ax)
        for idx in range(col_num):
            self.ax.collections[idx].set_facecolor('None')

        self.canvas.draw()

def main():
    win = tk.Tk()
    app = App(master=win)
    app.mainloop()

if __name__=="__main__":
    main()
