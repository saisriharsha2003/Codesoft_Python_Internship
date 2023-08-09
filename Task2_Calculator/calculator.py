import tkinter as tk
import math

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        
        self.result_var = tk.StringVar()
        self.create_widgets()
        
    def create_widgets(self):
        entry = tk.Entry(self.root, textvariable=self.result_var, justify="right", font=("Arial", 16))
        entry.grid(row=0, column=0, columnspan=8, padx=10, pady=10, ipadx=10, ipady=10)
        
        num_buttons = [
            '7', '8', '9',
            '4', '5', '6',
            '1', '2', '3',
            'C', '0', '.'
        ]
        
        operation_buttons1 = [
            '/', '*', '-', '+',
        ]
        
        operation_buttons2 = [
            '=', 'x^y', '√', 'x²'
        ]
        
        row = 1
        col = 0
        for button_label in num_buttons:
            button = tk.Button(self.root, text=button_label, command=lambda label=button_label: self.on_button_click(label), font=("Arial", 14), padx=20, pady=20)
            button.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        row = 1
        col = 3
        for button_label in operation_buttons1:
            button = tk.Button(self.root, text=button_label, command=lambda label=button_label: self.on_button_click(label), font=("Arial", 14), padx=20, pady=20)
            button.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            row += 1
        
        row = 1
        col = 5
        for button_label in operation_buttons2:
            button = tk.Button(self.root, text=button_label, command=lambda label=button_label: self.on_button_click(label), font=("Arial", 14), padx=20, pady=20)
            button.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            row += 1
        
        for r in range(1, 6):
            self.root.grid_rowconfigure(r, weight=1)
        for c in range(6):
            self.root.grid_columnconfigure(c, weight=1)
        
    def on_button_click(self, button_label):
        current_text = self.result_var.get()
        
        if button_label == 'C':
            self.result_var.set('')
        elif button_label == '=':
            try:
                result = eval(current_text)
                self.result_var.set(result)
            except:
                self.result_var.set('Error')
        elif button_label == 'x^y':
            self.result_var.set(current_text + '**')
        elif button_label == '√':
            try:
                result = math.sqrt(eval(current_text))
                self.result_var.set(result)
            except:
                self.result_var.set('Error')
        elif button_label == 'x²':
            try:
                result = eval(current_text)**2
                self.result_var.set(result)
            except:
                self.result_var.set('Error')
        else:
            self.result_var.set(current_text + button_label)

if __name__ == '__main__':
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
