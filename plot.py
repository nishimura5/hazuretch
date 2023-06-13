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
        pass

    def plot(self, file_path, canvas, ax):
        src_df = pd.read_csv(file_path, index_col='time')
        col_num = len(src_df.columns)

        ax.cla()
        ax.set_ylim(0, 10)
        sns.violinplot(data=src_df, linewidth=1, inner=None, facecolor='None', ax=ax)
        sns.swarmplot(data=src_df, size=2, palette=['black' for x in range(col_num)], alpha=0.4, ax=ax)
        sns.boxplot(data=src_df, linewidth=1, color='lightgray', width=0.1, ax=ax)
        for idx in range(col_num):
            ax.collections[idx].set_facecolor('None')

        canvas.draw()

class SrcFile:
    def __init__(self):
        self.file_path = ''

    def load_file(self):
        script_path = os.path.abspath(os.path.dirname(__file__))
        print(script_path)
        self.file_path = filedialog.askopenfilename(initialdir=script_path)

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

    src_file = SrcFile()

    load_button = tk.Button(button_frame, text="読み込み", width=15, command=lambda:src_file.load_file())
    load_button.grid(row=0, column=0)
    draw_button = tk.Button(button_frame, text="描画", width=15, command=lambda:input_data.plot(src_file.file_path, canvas, ax))
    draw_button.grid(row=0, column=1)
    button_frame.pack()

    dpi = 200
    fig, ax = plt.subplots(figsize=(800/dpi, 530/dpi), dpi=dpi)
    fig.canvas.mpl_connect("button_press_event", click)
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.get_tk_widget().pack()
    graph_frame.pack()

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.pack()

    root.mainloop()
