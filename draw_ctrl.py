import tkinter as tk
from tkinter import ttk

class DrawCtrl(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.plot_cbox = ttk.Combobox(
            master,
            values=['default', 'stripplot', 'swarmplot', 'lineplot', 'scatterplot'],
            state='readonly',
            width=8)
        self.plot_cbox.current(0)
        self.plot_cbox.pack(side=tk.LEFT, padx=5)
        alpha_label = tk.Label(master, text='alpha:')
        alpha_label.pack(side=tk.LEFT, padx=5)
        self.alpha_cbox = ttk.Combobox(master, values=['0.5', '0.2', '0.1', '0.05'], state='readonly', width=4)
        self.alpha_cbox.current(0)
        self.alpha_cbox.pack(side=tk.LEFT, padx=1)

        caption_time = tk.Label(master, text='time:')
        caption_time.pack(side=tk.LEFT, padx=10)
        self.time_min_entry = ttk.Entry(master, width=12)
        self.time_min_entry.pack(side=tk.LEFT, padx=10)
        nyoro_time = tk.Label(master, text='～')
        nyoro_time.pack(side=tk.LEFT, padx=10)
        self.time_max_entry = ttk.Entry(master, width=12)
        self.time_max_entry.pack(side=tk.LEFT, padx=10)

    def set_entry(self, min_time, max_time):
        self.time_min_entry.delete(0,tk.END)
        self.time_min_entry.insert(tk.END,min_time)
        self.time_max_entry.delete(0,tk.END)
        self.time_max_entry.insert(tk.END,max_time)

    def get_mode(self):
        return self.plot_cbox.get()

    def get_alpha(self):
        return self.alpha_cbox.get()

    def get_time_min(self):
        return self.time_min_entry.get()

    def get_time_max(self):
        return self.time_max_entry.get()
