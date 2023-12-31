import os

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib
from matplotlib import ticker

## only for mac?
matplotlib.use("tkagg")

import pandas as pd
import seaborn as sns

from remove_ctrl import RemoveCtrl
from draw_ctrl import DrawCtrl
from fill import interpolate

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        master.geometry("1000x600")
        master.title("はずれっち")
        input_frame = ttk.Frame(master)
        button_frame = ttk.Frame(master)
        graph_frame = ttk.Frame(master)
        fill_frame = ttk.Frame(master)

        self.input_data = Inputdata(input_frame)
        input_frame.pack()

        load_button = ttk.Button(
            button_frame,
            text="CSVを開く",
            width=10,
            command=lambda:[
                self.input_data.load_and_plot(canvas, ax),
                self.update_control()
                ])
        load_button.pack(side=tk.LEFT, padx=10)

        ## 描画コントロール
        self.dc = DrawCtrl(button_frame)

        ## 描画ボタンを押すとplot_modeが確定する、plot_modeは除去値エントリーのクリック入力の分岐に使用している
        self.plot_mode = ''
        draw_button = ttk.Button(
            button_frame,
            text="描画",
            width=7,
            command=lambda:[
                self.input_data.set_plot(
                    canvas,
                    ax,
                    self.dc.get_mode(),
                    self.dc.get_alpha(),
                    self.dc.get_time_min(),
                    self.dc.get_time_max()),
                self.set_plot_mode(self.dc.get_mode())
                ])
        draw_button.pack(side=tk.LEFT, padx=10)

        button_frame.pack(pady=5)

        ## グラフ
        dpi = 100
        fig, ax = plt.subplots(figsize=(1200/dpi,600/dpi), dpi=dpi)
        fig.canvas.mpl_connect("button_press_event", self.click)
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)

        toolbar = NavigationToolbar2Tk(canvas, graph_frame)
        toolbar.pack()
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.X, expand=False)
        graph_frame.pack()

        ## 除去コントロール
        self.remove_frame1 = RemoveCtrl(toolbar)
        and_label = ttk.Label(toolbar, text='AND')
        and_label.pack(side=tk.LEFT)
        self.remove_frame2 = RemoveCtrl(toolbar)

        ## グラフクリックでentryにyの値を入れる用のbind
        ## self.focusedには↓のlower1, upper1, lower2, upper2のいずれかが入る
        self.focused = ''
        self.remove_frame1.remove_lower_entry.bind("<FocusIn>", func=lambda e, code='lower1': self.set_focused(code))
        self.remove_frame1.remove_upper_entry.bind("<FocusIn>", func=lambda e, code='upper1': self.set_focused(code))
        self.remove_frame2.remove_lower_entry.bind("<FocusIn>", func=lambda e, code='lower2': self.set_focused(code))
        self.remove_frame2.remove_upper_entry.bind("<FocusIn>", func=lambda e, code='upper2': self.set_focused(code))

        output_button = ttk.Button(toolbar, text="除去", width=7, command=lambda:[self.remove_plots()])
        output_button.pack(side=tk.LEFT, padx=10)

        ## 補完コントロール
        tk.Label(fill_frame, text='連続するnanが').pack(side=tk.LEFT)
        limit_entry = ttk.Entry(fill_frame, width=4)
        limit_entry.pack(side=tk.LEFT)
        tk.Label(fill_frame, text='個以内なら補完する').pack(side=tk.LEFT, padx=(0, 10))
        output_button = ttk.Button(fill_frame, text="補完", width=10, command=lambda:[self.fill_plots(limit_entry.get())])
        output_button.pack()
        fill_frame.pack()

        master.protocol("WM_DELETE_WINDOW", toolbar.quit)

    def update_control(self):
        '''
        「CSVを開く」ボタンをクリックすると、新たに読み込まれたCSVに対応した値にentryやcomboboxが更新される。
        '''
        self.remove_frame1.set_cols(list(self.input_data.src_df.columns))
        self.remove_frame2.set_cols(list(self.input_data.src_df.columns))
        self.dc.set_entry(self.input_data.time_min, self.input_data.time_max)

    def remove_plots(self):
        '''
        「除去」ボタンをクリックすると、指定したカラムの指定した値範囲のデータがnanに置き換えられる。
        除去後のデータは「dst.csv」に保存され、srcのcsvは変更されない。
        '''
        col_x, remove_lower_x, remove_upper_x = self.remove_frame1.get_val()
        col_y, remove_lower_y, remove_upper_y = self.remove_frame2.get_val()
        time_min = self.dc.get_time_min()
        time_max = self.dc.get_time_max()

        if col_x == 'none' and col_y == 'none':
            return
        elif col_y != 'none' and col_x == 'none':
            self.input_data.remove_src(col_y, remove_lower_y, remove_upper_y, time_min, time_max)
        elif col_x != 'none' and col_y == 'none':
            self.input_data.remove_src(col_x, remove_lower_x, remove_upper_x, time_min, time_max)
        else:
            self.input_data.remove_src_and(
                [col_x, col_y],
                [remove_lower_x, remove_lower_y],
                [remove_upper_x, remove_upper_y],
                time_min, time_max)

        print(col_x, remove_lower_x, remove_upper_x)
        print(col_y, remove_lower_y, remove_upper_y)

        if self.plot_mode in ['stripplot', 'swarmplot']:
            mode = 'default'
        else:
            mode = self.plot_mode
        self.input_data.plot(time_min=time_min, time_max=time_max, mode=mode)

    def fill_plots(self, limit):
        time_min = self.dc.get_time_min()
        time_max = self.dc.get_time_max()

        self.input_data.fill_src(limit, time_min, time_max)

        if self.plot_mode in ['stripplot', 'swarmplot']:
            mode = 'default'
        else:
            mode = self.plot_mode
        self.input_data.plot(time_min=time_min, time_max=time_max, mode=mode)

    def set_plot_mode(self, plot_mode):
        '''
        「描画」ボタンをクリックすると、プロットモード(self.plot_mode)が確定する。
        「swarmplot」はデータ数が多いと(10000を超えたあたりから)描画が非常に遅くなるので注意。
        '''
        self.plot_mode = plot_mode

    def click(self, event):
        '''
        除去領域entryをフォーカスした後、グラフ領域をクリックすると、フォーカスしたentryにクリックした値が入力される。
        「scatterplot」のときのみ、横軸と縦軸に値が同時に入る。
        '''
        x_val, y_val = (event.xdata, event.ydata)
        if self.plot_mode == 'scatterplot':
            self.remove_frame1.set_col(1)
            self.remove_frame2.set_col(2)
            if 'lower' in self.focused:
                self.remove_frame1.set_entry('lower', str(x_val))
                self.remove_frame2.set_entry('lower', str(y_val))
            elif 'upper' in self.focused:
                self.remove_frame1.set_entry('upper', str(x_val))
                self.remove_frame2.set_entry('upper', str(y_val))
        else:
            if '1' in self.focused:
                self.remove_frame1.set_entry(self.focused, str(y_val))
            elif '2' in self.focused:
                self.remove_frame2.set_entry(self.focused, str(y_val))
        
#        print(self.focused, x_val, y_val)

    def set_focused(self, code):
        self.focused = code

class Inputdata(ttk.Frame):
    def __init__(self, input_frame):
        self.time_min = '00:00:00'
        self.time_max = '00:00:00'

    def load_and_plot(self, canvas, ax):
        self.canvas = canvas
        self.ax = ax
        self.load_file()
        self.plot(mode='default')

    def set_plot(self, canvas, ax, mode, alpha, time_min, time_max):
        self.canvas = canvas
        self.ax = ax
        self.plot(mode, alpha, time_min, time_max)

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

    def remove_src_and(self, cols, remove_lowers, remove_uppers, time_min, time_max):
        tar_df = self.src_df.loc[time_min:time_max, :]
        tar_df.loc[
            (tar_df[cols[0]] >= remove_lowers[0])&(tar_df[cols[0]] <= remove_uppers[0])&
            (tar_df[cols[1]] >= remove_lowers[1])&(tar_df[cols[1]] <= remove_uppers[1]),
              cols] = np.nan
        self.src_df.loc[time_min:time_max, :] = tar_df
        self.src_df.to_csv('./dst.csv')

    def fill_src(self, limit, time_min, time_max):
        tar_df = self.src_df.loc[time_min:time_max, :]
        limit = int(limit)
        tar_df = interpolate(tar_df, limit)
        self.src_df.loc[time_min:time_max, :] = tar_df
        self.src_df.to_csv('./dst.csv')

    def plot(self, mode='default', alpha='0.5', time_min=None, time_max=None):
        alpha = float(alpha)
        if time_min is not None and time_max is not None:
            plot_df = self.src_df.loc[time_min:time_max, :]
        else:
            plot_df = self.src_df

        y_max = max(plot_df.max())
        y_min = min(plot_df.min())

        col_num = len(self.src_df.columns)

        self.ax.cla()
        self.ax.set_ylim(y_min, y_max)

        if mode == 'lineplot':
            tick_interval = len(plot_df.index) / 10
            self.ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_interval)) 
#            sns.lineplot(data=plot_df, dashes=False, linewidth=1, ax=self.ax)
            plot_df.plot(use_index=True, kind='line', ax=self.ax)
        elif mode == 'scatterplot':
            sns.scatterplot(
                data=plot_df,
                x=plot_df.columns[0],
                y=plot_df.columns[1],
                size=2,
                edgecolor='none',
                alpha=alpha,
                legend=False,
                ax=self.ax)
        else:
            self.ax.xaxis.set_major_locator(ticker.MultipleLocator(1)) 
            sns.violinplot(data=plot_df, linewidth=1, showmeans=True, inner=None, ax=self.ax)
            for collection in self.ax.collections:
                collection.set_facecolor('none')

            if mode == 'swarmplot':
                sns.swarmplot(data=plot_df, size=2, palette=['black' for x in range(col_num)], alpha=alpha, ax=self.ax)
            elif mode == 'stripplot':
                sns.stripplot(data=plot_df, size=2, palette=['black' for x in range(col_num)], alpha=alpha, ax=self.ax)
            else:
                pass
            sns.boxplot(data=plot_df, linewidth=1, fliersize=2, color='lightgray', width=0.1, ax=self.ax)

        self.canvas.draw()

def main():
    win = tk.Tk()
    app = App(master=win)
    app.mainloop()

if __name__=="__main__":
    main()
