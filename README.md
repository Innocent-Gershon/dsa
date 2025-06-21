================================================================================
                SPARSE MATRIX OPERATIONS - PROGRAM DOCUMENTATION
================================================================================

💡 ABOUT THE PROGRAM
---------------------
This Python program allows you to perform operations on large sparse matrices:
  ➕ Addition
  ➖ Subtraction
  ✖️ Multiplication

It is optimized to handle matrices that mostly contain zero values efficiently
using dictionaries to store only non-zero elements.

================================================================================
📁 PROJECT STRUCTURE
---------------------

Organize your files like this:

/dsa/sparse_matrix/
 ├── my_code.py              <- The main Python program
 ├── sample_inputs/          <- Folder containing sample sparse matrix files
 │    ├── easy_sample_01_2.txt
 │    ├── easy_sample_01_3.txt
 │    └── ... other samples ...
 ├── result_add.txt          <- Output file generated after operations
 └── README.txt              <- (This file)

================================================================================
📝 INPUT FILE FORMAT
---------------------

Each input file should contain:
1. A `rows=` line  (optional — will be inferred if missing)
2. A `cols=` line  (optional — will be inferred if missing)
3. A list of values like: (row_index, column_index, value)

Only non-zero entries are listed. All other cells are assumed to be 0.

✅ EXAMPLE FILE:
---------------------
rows=5
cols=6
(0,1,8)
(1,2,4)
(3,5,10)

If `rows` and `cols` are not provided, they will be inferred based on the largest
row and column indices found in the file.

================================================================================
🚀 HOW TO RUN THE PROGRAM
---------------------------

1. Open a terminal in the `sparse_matrix` folder.
2. Run the program:

   python my_code.py

3. Follow the on-screen prompts:

-------------------
Select an operation:
 1. Add
 2. Subtract
 3. Multiply

Your choice (1/2/3): 1
Enter the first matrix file path: sample_inputs/easy_sample_01_2.txt
Enter the second matrix file path: sample_inputs/easy_sample_01_3.txt
Enter filename to save result (e.g., result.txt): result_add.txt
-------------------

4. Output will be:
   - Saved to the file you specified
   - Displayed in the terminal

================================================================================
⚠️ RULES FOR OPERATIONS
------------------------

✔️ Addition & Subtraction:
- Matrices do NOT need to be the same size.
- Smaller matrix will be auto-padded with zeros to match the larger one.

✔️ Multiplication:
- Number of columns in Matrix A MUST equal number of rows in Matrix B.
- If not, an error will be displayed.

================================================================================
❌ COMMON ERRORS & FIXES
------------------------

1. ❌ File not found:
   ➤ Make sure you typed the correct relative path from the current folder.
   ➤ Example: `sample_inputs/easy_sample_01_2.txt`

2. ❌ Invalid format:
   ➤ Make sure each line with values uses parentheses and 3 integers.
   ➤ Example: (1,3,10)

3. ❌ Matrix dimensions do not match for multiplication:
   ➤ Check the shape rules for matrix multiplication.

================================================================================
📦 OUTPUT FORMAT
------------------------

Saved output file will look like this:

rows=5
cols=6
(0,1,13)
(1,2,8)
(3,5,10)

It follows the same format as the input for reuse or further operations.

================================================================================
👨🏽‍💻 AUTHOR & CREDITS
------------------------

Written for:
  ➤ Programming Assignment 2: Sparse Matrices
  ➤ Course: Data Structures and Algorithms for Engineers

Feel free to reuse or improve this for academic learning only.

HAPPY CODING! 🚀
================================================================================
