from scipy.linalg import null_space
import numpy as np
import re

def balance(equation: str) -> str:
    # Validate and sanitize equation
    for char in "`~!@# \$%^&*_\\|;':\",./<>?":
        equation = equation.replace(char, "")
        
    if "=" not in equation or "++" in equation or "--" in equation:
        return "Invalid equation"
    
    if re.search(r"(?<![A-Za-z])\d+[A-Z][a-z]+", equation) != None:
        return "Invalid equation"
    
    if "-" in equation and "-}" not in equation:
        return "Invalid equation"
    
    if not any([char.isupper() for char in equation]):
        return "Invalid equation"
        
    try:
        equation.encode("ascii", "strict")
    except UnicodeEncodeError:
        return "Invalid equation"
        
    equation = equation.replace("[", "(").replace("]", ")")
    equation = equation.replace("{+}", "{1+}").replace("{-}","{1-}")
    reactants = re.split(r"(?<!{)\+(?!})", equation.split("=")[0])
    
    # Count elements
    elements = set()
    for i in range(len(equation) - 1):
        if equation[i].isupper():
            if equation[i + 1].isupper() or equation[i + 1].isnumeric():
                elements.add(equation[i])
            elif equation[i + 1].islower():
                elements.add(equation[i : i + 2])
        
    if equation[-1].isupper():
        elements.add(equation[-1])
                
    substances = np.array(re.split(r"(?<!{)[\+\=](?!})", equation))
    linearEqs = np.zeros((len(elements) + 1, len(substances)))

    for i, element in enumerate(elements):
        for j in range(len(substances)):
            occurences = [(match.start(), match.end() - 1) for match in re.finditer(element, substances[j])]
            count = 0
            
            # Count atoms in each substance
            for pos in occurences:
                leftParens = 0
                skippableParens = 0
                
                k = pos[1] + 1
                while k < len(substances[j]) and substances[j][k].isnumeric():
                    k += 1
                    
                subcount = int(substances[j][pos[1] + 1 : k]) if k - (pos[1] + 1) > 0 else 1
                    
                # Multiply the count by the subscript outside of the brackets
                for k in range(pos[0], -1, -1):
                    leftParens += 1 if substances[j][k] == "(" else 0
                                                
                for k in range(pos[1], len(substances[j])):
                    if substances[j][k] == ")":
                        if skippableParens == 0:
                            l = k + 1
                            while l < len(substances[j]) and substances[j][l].isnumeric():
                                l += 1
                                
                            if l - (k + 1) > 0:
                                subcount *= int(substances[j][k + 1 : l])
                        else:
                            skippableParens -= 1
                    elif substances[j][k] == "(":
                        skippableParens += 1
                        
                count += subcount
            
            linearEqs[i][j] = count if substances[j] in reactants else -count
    
    # Count charges
    if re.search(r"{\d*[\+\-]+}", equation) != None:
        for i in range(len(substances)):
            if substances[i].find("{") != -1 and substances[i].index("}") != -1:
                charge = substances[i][substances[i].index("{") + 1 : substances[i].index("}")][::-1].strip()
                if len(charge) > 0:
                    linearEqs[-1][i] = int(charge) if substances[i] in reactants else -int(charge)
            
    # Find nullspace and round numbers        
    coeffs = [value[0] for value in null_space(linearEqs)]
    minCoeff = min(coeffs)
    coeffs = map(lambda x: round(x / minCoeff, 3), coeffs)
    
    # Warning when unusual values are detected
    if any(filter(lambda x: x < 0 or x > 1000000, coeffs)):
        warning = "Some values are negative or too large. There may be a mistake in your equation"
    
    return " : ".join(map(lambda x, y: str(x) + y, coeffs, substances)) + warning

if __name__ == "__main__":
    print(balance("Fe{2+}+Cl2=Fe{3+}+Cl{-}"))