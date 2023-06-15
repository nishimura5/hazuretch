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
        master.title("はずれっち")
        input_frame = ttk.Frame(master)
        button_frame = ttk.Frame(master)
        graph_frame = ttk.Frame(master)
        hazure_frame = ttk.Frame(master)

        self.input_data = Inputdata(input_frame)
        input_frame.pack()

        load_button = ttk.Button(button_frame, text="CSVを開く", width=15, command=lambda:[self.input_data.load_and_plot(canvas, ax), self.update_control()])
        load_button.grid(row=0, column=0)
        plot_cbox = ttk.Combobox(button_frame, values=['stripplot', 'swarmplot', 'none'], state='readonly')
        plot_cbox.grid(row=0, column=1, padx=10)
        plot_cbox.bind("<<ComboboxSelected>>", lambda _ : [self.input_data.set_plot(canvas, ax, plot_cbox.get(), self.time_min_entry.get(), self.time_max_entry.get())])

        caption_time = tk.Label(button_frame, text='time:')
        caption_time.grid(row=0, column=2)
        self.time_min_entry = ttk.Entry(button_frame, width=12)
        self.time_min_entry.grid(row=0, column=3)
        nyoro_time = tk.Label(button_frame, text='～')
        nyoro_time.grid(row=0, column=4)
        self.time_max_entry = ttk.Entry(button_frame, width=12)
        self.time_max_entry.grid(row=0, column=5)

        button_frame.pack(pady=5)

        dpi = 120
        fig, ax = plt.subplots(figsize=(1200/dpi,900/dpi), dpi=dpi)
        fig.canvas.mpl_connect("button_press_event", self.click)
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)

        toolbar = NavigationToolbar2Tk(canvas, graph_frame)
        toolbar.pack()
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        graph_frame.pack()

        self.column_cbox = ttk.Combobox(toolbar, state='readonly')
        self.column_cbox.pack(side=tk.LEFT, padx=10)
        self.remove_lower_entry = ttk.Entry(toolbar, width=8)
        self.remove_lower_entry.pack(side=tk.LEFT)
        nyoro = tk.Label(toolbar, text='～')
        nyoro.pack(side=tk.LEFT)
        self.remove_upper_entry = ttk.Entry(toolbar, width=8)
        self.remove_upper_entry.pack(side=tk.LEFT)
        output_button = ttk.Button(toolbar, text="除去", width=10, command=lambda:[self.remove_plots()])
        output_button.pack(side=tk.LEFT, padx=10)

        hazure_frame.pack()

        master.protocol("WM_DELETE_WINDOW", toolbar.quit)

    def update_control(self):
        self.column_cbox['value'] = list(self.input_data.src_df.columns)
        self.time_min_entry.delete(0,tk.END)
        self.time_min_entry.insert(tk.END,self.input_data.time_min)
        self.time_max_entry.delete(0,tk.END)
        self.time_max_entry.insert(tk.END,self.input_data.time_max)

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

        time_min = self.time_min_entry.get()
        time_max = self.time_max_entry.get()
        self.input_data.remove_src(col, remove_lower, remove_upper, time_min, time_max)
        ## 除去後のデータをCSV出力
        self.input_data.plot(time_min=time_min, time_max=time_max)

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
        self.time_min = '00:00:00'
        self.time_max = '00:00:00'

    def load_and_plot(self, canvas, ax):
        self.canvas = canvas
        self.ax = ax
        self.load_file()
        self.plot(mode='none')

    def set_plot(self, canvas, ax, mode, time_min, time_max):
        self.canvas = canvas
        self.ax = ax
        self.plot(mode, time_min, time_max)

    def load_file(self):
        script_path = os.getcwd()
        ## ↓pyinstallerでexeにすると意図しないディレクトリを指示したのでやめる
#        script_path = os.path.abspath(os.path.dirname(__file__))
        file_path = filedialog.askopenfilename(initialdir=script_path)
        self.src_df = pd.read_csv(file_path, index_col='time')
        self.time_min = min(self.src_df.index)
        self.time_max = max(self.src_df.index)

    def remove_src(self, col, remove_lower, remove_upper, time_min, time_max):
        tar_df = self.src_df.loc[time_min:time_max, :]
        tar_df.loc[(tar_df[col] >= remove_lower)&(tar_df[col] <= remove_upper), col] = np.nan
        self.src_df.loc[time_min:time_max, :] = tar_df
        self.src_df.to_csv('./dst.csv')

    def plot(self, mode='none', time_min=None, time_max=None):
        if time_min is not None and time_max is not None:
            plot_df = self.src_df.loc[time_min:time_max, :]
        else:
            plot_df = self.src_df

        y_max = max(plot_df.max())
        y_min = min(plot_df.min())

        col_num = len(self.src_df.columns)

        self.ax.cla()
        self.ax.set_ylim(y_min, y_max)
        sns.violinplot(data=plot_df, linewidth=1, inner=None, facecolor='None', ax=self.ax)
        if mode == 'swarmplot':
            sns.swarmplot(data=plot_df, size=2, palette=['black' for x in range(col_num)], alpha=0.5, ax=self.ax)
        elif mode == 'stripplot':
            sns.stripplot(data=plot_df, size=2, palette=['black' for x in range(col_num)], alpha=0.2, ax=self.ax)
        else:
            pass
        sns.boxplot(data=plot_df, linewidth=1, fliersize=2, color='lightgray', width=0.1, ax=self.ax)

        ## 箱ひげ図とバイオリンプロットの塗を透明にする処理、removeで全部のデータが消えたカラムは直後のplotでax.collectionsがなくなるのでcol_numの値を上書きするようにしている
        if col_num > len(self.ax.collections):
            col_num = len(self.ax.collections)
        for idx in range(col_num):
            self.ax.collections[idx].set_facecolor('None')

        self.canvas.draw()

def main():
    win = tk.Tk()
    app = App(master=win)
    app.mainloop()

if __name__=="__main__":
    main()
