import tkinter as tk
from tkinter import ttk

import numpy as np
import matplotlib
matplotlib.use("macosx")
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import pandas as pd
import seaborn as sns

class Inputdata(ttk.Frame):
    def __init__(self, input_frame):
        pass

    def plot(self, canvas, ax):
        src_df = pd.read_csv('./src.csv', index_col='time')
        col_num = len(src_df.columns)

        ax.cla()
        ax.set_ylim(0, 10)
        sns.violinplot(data=src_df, linewidth=1, inner=None, facecolor='None', ax=ax)
        sns.swarmplot(data=src_df, size=2, palette=['black' for x in range(col_num)], alpha=0.4, ax=ax)
        sns.boxplot(data=src_df, linewidth=1, color='lightgray', width=0.1, ax=ax)
        for idx in range(col_num):
            ax.collections[idx].set_facecolor('None')

        canvas.draw()

if __name__=="__main__":
    root = tk.Tk()
    root.title("data-keiko")

    input_frame = ttk.Frame(root)
    button_frame = ttk.Frame(root)
    graph_frame = ttk.Frame(root)

    input_data = Inputdata(input_frame)
    input_frame.pack()

    draw_button = tk.Button(button_frame, text="描画", width=15, command=lambda:input_data.plot(canvas, ax))
    draw_button.grid(row=0, column=0)
    button_frame.pack()

    dpi = 200
    fig, ax = plt.subplots(dpi=dpi)
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.get_tk_widget().pack()
    graph_frame.pack()

    root.mainloop()
