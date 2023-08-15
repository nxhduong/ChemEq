# ChemEq
A simple chemical equations balancer, written in Python.
## Usage
Enter python  into the command line.
Input an unbalanced equation, e.g. CH4 + O2 = CO2 + H2O
Or use
## Further reading: Balancing a chemical equation using matrix operations
To balance a chemical equation using matrix operations, we first need to represent the equation as a system of linear equations. We can do this by creating a matrix that represents the coefficients of the elements in each compound. For example, consider the following equation:

CH4 + O2 -> CO2 + H2O

We can represent this equation as a system of linear equations:

C: 1x + 0y - 1z = 0
H: 4x + 0y - 2w = 0
O: 2y - 2z - 1w = 0
where x, y, z, and w are the coefficients of CH4, O2, CO2, and H2O, respectively. The first equation represents the conservation of carbon atoms, the second equation represents the conservation of hydrogen atoms, and the third equation represents the conservation of oxygen atoms.

We can represent this system of linear equations as a matrix:

1 0 -1 0
4 0 0 -2
0 2 -2 -1
Each row corresponds to an equation and each column corresponds to a compound. The first column corresponds to CH4, the second column corresponds to O2, the third column corresponds to CO2, and the fourth column corresponds to H2O.

To solve for the coefficients of the balanced equation, we need to find the nullspace of the matrix. The nullspace of a matrix is the set of all vectors that, when multiplied by the matrix, result in a zero vector. In other words, balancing a chemical equation requires finding the values of x, y, z, and w that satisfy the system of linear equations.