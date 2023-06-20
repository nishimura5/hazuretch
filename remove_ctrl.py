import tkinter as tk
from tkinter import ttk

class RemoveCtrl(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.column_cbox = ttk.Combobox(master, values=['none'], state='readonly', width=10)
        self.column_cbox.current(0)
        self.remove_lower_entry = ttk.Entry(master, width=6)
        self.nyoro = tk.Label(master, text='～')
        self.remove_upper_entry = ttk.Entry(master, width=6)
        self.column_cbox.pack(side=tk.LEFT, padx=5)
        self.remove_lower_entry.pack(side=tk.LEFT)
        self.nyoro.pack(side=tk.LEFT)
        self.remove_upper_entry.pack(side=tk.LEFT)

    def set_entry(self, code, val):
        if 'lower' in code:
            self.remove_lower_entry.delete(0,tk.END)
            self.remove_lower_entry.insert(tk.END,val)
        elif 'upper' in code:
            self.remove_upper_entry.delete(0,tk.END)
            self.remove_upper_entry.insert(tk.END,val)

    def set_cols(self, cols):
        self.column_cbox['value'] = ['none', *cols]

    def set_col(self, current):
        self.column_cbox.current(current)

    def get_val(self):
        col = self.column_cbox.get()
        remove_lower = self.remove_lower_entry.get()
        remove_upper = self.remove_upper_entry.get()
        if self._is_float(remove_lower) and self._is_float(remove_upper):
            remove_lower = float(remove_lower)
            remove_upper = float(remove_upper)
        else:
            return 'none', 0, 0
        return col, remove_lower, remove_upper

    def _is_float(self, string):
        if string.replace(".", "").isnumeric():
            return True
        else:
            return False
