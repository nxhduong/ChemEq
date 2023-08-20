# ChemEq
![](/res/app.png)

ChemEq is a simple chemical equations balancer written in Python. 

This program constructs a matrix based on the number of atoms of each element in each substance. Coefficients are then found by calculating the null space of the matrix.

Any contributions to this project are greatly appreciated.
## Requirements
If run from source code:
- Python 3.10-3.11
- NumPy and SciPy Python packages 
## Usage
- Run from source code:
1. Enter `python main.py` into the command line.
2. Input an unbalanced equation, e.g. CH4 + O2 = CO2 + H2O

- Pre-packaged releases are also available on the `Releases` page
### Notes: Valid equation format
- Reactants and products are separated by an equal sign (`=`)
- Each substance in the reactants or the products is separated by a plus sign (`+`)
- Atoms are grouped using round (`()`) or square (`[]`) brackets. Curly brackets must only be used to specify charges.

E.g.
```
Fe{2+} + Cl2 = Fe{3+} + Cl{-}
```
```
(Cr[CO(NH2)2]6)4[Cr(CN)6]3 + KMnO4 + HNO3 = K2Cr2O7 + CO2 + KNO3 + Mn(NO3)3 + H2O
```
## License
Distributed under the MIT license. Please see `LICENSE` for further information.
## Contact
- My GitHub: https://github.com/nxhduong
