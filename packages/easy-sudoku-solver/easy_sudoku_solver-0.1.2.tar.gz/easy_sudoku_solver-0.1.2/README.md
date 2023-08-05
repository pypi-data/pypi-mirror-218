
# installation
```
pip install easy-sudoku-solver
```

# usage
```
from sudoku_solver import SudokuSolver
unsolved_sudoku = '090060100030201004200080000500103900000006000009000008300509800040000070000020000'
solver = SudokuSolver(x)
solution = solver.solve()
print(solution)
// '79436518283527169421698475358214396747389652116975243832751
9846941638275658427319'
```