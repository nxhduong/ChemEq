from chem_eq import balance
from tkinter import Tk, Button, Label, Text

defaultFont = ("Arial", 12)

def buttonOnClick():
    try:
        result, warn = balance(inputField.get("1.0", "end-1c"))
        resultText.config(text="Result:\n" + result + (warn or ""))
    except Exception as err:
        resultText.config(text="Result:\n" + err)

if __name__ == "__main__":
    # Setting up window
    window = Tk()
    window.title("ChemEq")
    window.geometry("500x400")
    window.resizable(False, True)
    window.config(padx=10, pady=10)
    
    heading = Label(text="ChemEq Chemical Equations Balancer", font=("Arial", 20))
    heading.pack(pady=10)
    
    label = Label(text="Input an unbalanced chemical equation:", justify="left", font=defaultFont)
    label.pack(anchor="w")
    
    inputField = Text(width=60, height=3)
    inputField.insert("1.0", "Cu + H{+} + NO3{-} = Cu{2+} + NO + H2O")
    inputField.pack()
    
    resultText = Label(text="Result:", font=defaultFont, wraplength=480)
    resultText.pack()
    
    button = Button(text="Balance", font=defaultFont, command=buttonOnClick)
    button.pack(side="bottom")
    
    window.mainloop()