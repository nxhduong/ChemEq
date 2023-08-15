from tkinter import Tk, Button, Label, Text
import chem_eq

if __name__ == "__main__":
    window = Tk()
    window.title("ChemEq")
    window.geometry("500x400")
    
    heading = Label(text="ChemEq Chemical Equations Balancer")
    heading.pack()
    
    inputField = Text(width=60, height=3)
    inputField.insert("1.0", "Cu + H{+} + NO3{-} = Cu{2+} + NO + H2O")
    inputField.pack()
    
    button = Button(text="Balance")
    
    window.mainloop()