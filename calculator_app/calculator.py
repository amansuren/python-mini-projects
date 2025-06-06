import tkinter as tk
from tkinter import ttk

class CalculatorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Simple Calculator")

        self.current_input = ""
        self.expression = ""
        self.result_displayed = False # Track if result is on display

        # Styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton',
                        font=('Arial', 16),
                        padding=10,
                        relief='raised',
                        borderwidth=2,
                        )
        style.configure('TEntry',
                        font=('Arial', 20),
                        padding=15,
                        justify='right',
                        )
        style.configure('TLabel', font=('Arial', 12))

        # Colors
        self.bg_color = '#f0f0f0'  # Light gray background
        self.button_bg = '#e0e0e0'  # Light gray buttons
        self.button_hover = '#d0d0d0' # Slightly darker on hover
        self.display_bg = '#ffffff'  # White display
        self.result_color = '#228B22' # Forest Green for result

        master.configure(bg=self.bg_color)

        # Display Entry
        self.display = ttk.Entry(master,
                                 textvariable=tk.StringVar(value="0"),
                                 state='readonly',
                                 style='TEntry',
                                 background=self.display_bg)
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='ew')

        # Buttons
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 5, 0), ('←', 5, 1), ('(', 5, 2), (')', 5, 3),
        ]

        self.buttons = {} # Store buttons to change appearance

        for (text, row, col) in buttons:
            button = ttk.Button(master, text=text, style='TButton',
                                command=lambda t=text: self.button_click(t))
            button.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            master.grid_columnconfigure(col, weight=1)
            master.grid_rowconfigure(row, weight=1)

            self.buttons[text] = button #Store

            # Hover effect (improve with enter/leave)
            button.bind("<Enter>", self.on_enter)
            button.bind("<Leave>", self.on_leave)

        master.grid_rowconfigure(0, weight=1)

        # Set equal button color
        self.buttons['='].configure(style='Equal.TButton')
        style.configure('Equal.TButton', background='#4CAF50', foreground='white') # Green
        self.buttons['='].bind("<Enter>", lambda event: self.on_enter(event, '#45a049'))
        self.buttons['='].bind("<Leave>", lambda event: self.on_leave(event, '#4CAF50'))

        # Clear button color
        self.buttons['C'].configure(style='Clear.TButton')
        style.configure('Clear.TButton', background='#f44336', foreground='white') # Red
        self.buttons['C'].bind("<Enter>", lambda event: self.on_enter(event, '#d32f2f'))
        self.buttons['C'].bind("<Leave>", lambda event: self.on_leave(event, '#f44336'))

        # Backspace button color
        self.buttons['←'].configure(style='Backspace.TButton')
        style.configure('Backspace.TButton', background='#FF9800', foreground='white') # Orange
        self.buttons['←'].bind("<Enter>", lambda event: self.on_enter(event, '#e65100'))
        self.buttons['←'].bind("<Leave>", lambda event: self.on_leave(event, '#FF9800'))

    def on_enter(self, event, bg_color=None):
        """Handle button hover"""
        if bg_color is None:
           event.widget['background'] = self.button_hover
        else:
           event.widget['background'] = bg_color

    def on_leave(self, event, bg_color=None):
        """Handle button leave"""
        if bg_color is None:
            event.widget['background'] = self.button_bg
        else:
            event.widget['background'] = self.button_bg

    def button_click(self, text):
        if text == '=':
            self.handle_equals()
        elif text == 'C':
            self.handle_clear()
        elif text == '←':
            self.handle_backspace()
        else:
            self.handle_input(text)

    def handle_equals(self):
        try:
            self.expression = self.display.get()
            result = eval(self.expression)
            self.display.config(state='normal')
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
            self.display.config(state='readonly')
            self.current_input = str(result)
            self.expression = ""
            self.result_displayed = True

        except Exception as e:
            self.display.config(state='normal')
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")
            self.display.config(state='readonly')
            self.current_input = ""
            self.expression = ""
            self.result_displayed = True

    def handle_clear(self):
        self.display.config(state='normal')
        self.display.delete(0, tk.END)
        self.display.insert(0, "0")
        self.display.config(state='readonly')
        self.current_input = ""
        self.expression = ""
        self.result_displayed = False

    def handle_backspace(self):
        current = self.display.get()
        self.display.config(state='normal')
        self.display.delete(0, tk.END)
        self.display.insert(0, current[:-1] if len(current) > 1 else "0")
        self.display.config(state='readonly')
        self.current_input = current[:-1]
        self.expression = current[:-1]
        self.result_displayed = False

    def handle_input(self, text):
        if self.display.get() == "0" or self.result_displayed:
            self.display.config(state='normal')
            self.display.delete(0, tk.END)
            self.result_displayed = False
        self.display.config(state='normal')
        self.display.insert(tk.END, text)
        self.display.config(state='readonly')
        self.current_input += text
        self.expression += text

root = tk.Tk()
calculator = CalculatorGUI(root)
root.mainloop()
