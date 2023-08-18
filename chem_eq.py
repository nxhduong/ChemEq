from scipy.linalg import null_space
import numpy as np
import re

def balance(equation: str) -> tuple[str, str]:
    """
    Balance the given equation.
    Return the balanced equation, and a warning if unsual values are suspected. 
    Will raise ValueError if the equation is impossible, nor in correct format.
    
    E.g. "Fe{2+} + Cl2 = Fe{3+} + Cl{-}" -> "2.0Fe{2+} : 1.0Cl2 : 2.0Fe{3+} : 2.0Cl{-}"
    """
    
    # Sanitize equation
    equation = equation.replace("[", "(").replace("]", ")")
    for char in "`~!@# \$%^&*_\\|;':\",./<>?":
        equation = equation.replace(char, "")
    
    # Detect some common mistakes    
    if "=" not in equation:
        raise ValueError("Invalid equation")
    if re.search(r"(?<![A-Za-z])\d+[A-Z][a-z]+", equation) != None:
        raise ValueError("Invalid equation")
    if "-" in equation and "-}" not in equation:
        raise ValueError("Invalid equation")
    if re.search(r"[a-z][a-z]", equation) != None:
        raise ValueError("Invalid equation")
        
    try:
        equation.encode("ascii", "strict")
    except UnicodeEncodeError:
        raise ValueError("Invalid equation")
    
    reactants = re.split(r"\+(?!})", equation.split("=")[0])
    
    # Count elements
    elements = set()
    for i in range(len(equation) - 1):
        if equation[i].isupper():
            if equation[i + 1].islower():
                elements.add(equation[i : i + 2])
            else:
                elements.add(equation[i])
        
    if equation[-1].isupper():
        elements.add(equation[-1])
                
    substances = np.array(re.split(r"[\+\=](?!})", equation))
    linearEqs = np.zeros((len(elements) + 1, len(substances)))

    for i, element in enumerate(elements):
        for j, substance in enumerate(substances):
            count = 0
            occurences = []
            
            for indices in re.finditer(element + r"(?![a-z])", substance):
                occurences.append((indices.start(), indices.end() - 1))
            
            # Count atoms in each substance
            for pos in occurences:
                skippableParens = 0
                k = pos[1] + 1
                
                while k < len(substance) and substance[k].isnumeric():
                    k += 1    
                subcount = int(substance[pos[1] + 1 : k]) if k - (pos[1] + 1) > 0 else 1
                    
                # Multiply the count by the subscript outside of the brackets                                                
                for k in range(pos[1], len(substance)):
                    if substance[k] == ")":
                        if skippableParens == 0:
                            l = k + 1
                            while l < len(substance) and substance[l].isnumeric():
                                l += 1
                            if l - (k + 1) > 0:
                                subcount *= int(substance[k + 1 : l])
                        else:
                            skippableParens -= 1
                    elif substance[k] == "(":
                        skippableParens += 1
                        
                count += subcount
            linearEqs[i][j] = count if substance in reactants else -count
    
    # Count charges
    chargeSigns = {
        "+": 1,
        "-": -1,
        "++": 2,
        "--": -2
    }
    for i, substance in enumerate(substances):
        if "{" in substance and "}" in substance:
            charge = substance[substance.index("{") + 1 : substance.index("}")][::-1]
            
            if charge in chargeSigns:
                linearEqs[-1][i] = chargeSigns[charge] if substance in reactants else -chargeSigns[charge]
            else:
                try:
                    linearEqs[-1][i] = int(charge) if substance in reactants else -int(charge)
                except ValueError:
                    continue
            
    # Find nullspace and round numbers
    try:        
        coeffs = [value[0] for value in null_space(linearEqs)]
    except IndexError as err:
        # Empty vector
        raise ValueError("Invalid equation. " + err)
    
    if all(coeff < 0 for coeff in coeffs):
        coeffs = [-coeff for coeff in coeffs]
    
    minCoeff = min(coeffs)
    coeffs = [round(coeff / minCoeff, 4) for coeff in coeffs]

    # Warning when there are unusual values
    warn = None
    if [coeff for coeff in coeffs if not 0 < coeff < 1000000]:
        warn = "Some values are negative or too large. There may be a mistake in your equation."

    return " : ".join([str(coeff) + substance for coeff, substance in zip(coeffs, substances)]), warn

if __name__ == "__main__":
    print(balance("Fe{2+}+Cl2=Fe{3+}+Cl{-}"))
    print(balance("(Cr[CO(NH2)2]6)4[Cr(CN)6]3+KMnO4+HNO3=K2Cr2O7+CO2+KNO3+Mn(NO3)3+H2O"))