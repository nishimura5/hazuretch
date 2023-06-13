import os

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import pandas as pd
import seaborn as sns

class Inputdata(ttk.Frame):
    def __init__(self, input_frame):
        self.file_path = ''

    def load_and_plot(self, canvas, ax):
        self.load_file()
        self.plot(canvas, ax)

    def load_file(self):
        script_path = os.path.abspath(os.path.dirname(__file__))
        file_path = filedialog.askopenfilename(initialdir=script_path)
        self.src_df = pd.read_csv(file_path, index_col='time')

    def plot(self, canvas, ax):
        col_num = len(self.src_df.columns)

        ax.cla()
        ax.set_ylim(0, 10)
        sns.violinplot(data=self.src_df, linewidth=1, inner=None, facecolor='None', ax=ax)
        sns.swarmplot(data=self.src_df, size=2, palette=['black' for x in range(col_num)], alpha=0.4, ax=ax)
        sns.boxplot(data=self.src_df, linewidth=1, color='lightgray', width=0.1, ax=ax)
        for idx in range(col_num):
            ax.collections[idx].set_facecolor('None')

        canvas.draw()

def click(event):
    x_val, y_val = (event.xdata, event.ydata)
    print(x_val, y_val)


if __name__=="__main__":
    root = tk.Tk()
    root.title("バイオリン箱ヒゲ")
    root.geometry("800x600")

    input_frame = ttk.Frame(root)
    button_frame = ttk.Frame(root)
    graph_frame = ttk.Frame(root)

    input_data = Inputdata(input_frame)
    input_frame.pack()

    draw_button = tk.Button(button_frame, text="開く", width=15, command=lambda:input_data.load_and_plot(canvas, ax))
    draw_button.grid(row=0, column=0)
    button_frame.pack()

    dpi = 200
    fig, ax = plt.subplots(dpi=dpi)
    fig.canvas.mpl_connect("button_press_event", click)
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.get_tk_widget().pack()

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.pack()

    graph_frame.pack()

    root.protocol("WM_DELETE_WINDOW", toolbar.quit)
    root.mainloop()
