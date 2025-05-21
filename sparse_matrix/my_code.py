class SparseMatrix:
    def __init__(self, matrix_file_path=None, rows=None, cols=None):
        if matrix_file_path:
            self._read_matrix_file(matrix_file_path)
        else:
            self.rows = rows
            self.cols = cols
            self.data = [{} for _ in range(rows)]

    def _read_matrix_file(self, path):
        try:
            with open(path, 'r') as file:
                lines = [line.strip() for line in file if line.strip()]
                self.rows = int(lines[0].split('=')[1])
                self.cols = int(lines[1].split('=')[1])
                self.data = [{} for _ in range(self.rows)]
                for entry in lines[2:]:
                    r, c, val = map(int, entry[1:-1].split(','))
                    self.set_value(r, c, val)
        except Exception as e:
            raise e

    def set_value(self, row, col, value):
        if value != 0:
            self.data[row][col] = value
        elif col in self.data[row]:
            del self.data[row][col]

    def get_value(self, row, col):
        return self.data[row].get(col, 0)

    def add(self, other):
        return self._apply_elementwise(other, lambda x, y: x + y)

    def subtract(self, other):
        return self._apply_elementwise(other, lambda x, y: x - y)

    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError("Matrix dimensions do not match for multiplication")

        result = SparseMatrix(rows=self.rows, cols=other.cols)
        transposed = [{} for _ in range(other.cols)]

        for r in range(other.rows):
            for c, val in other.data[r].items():
                transposed[c][r] = val

        for r in range(self.rows):
            for c, val in self.data[r].items():
                for k, t_val in transposed[c].items():
                    res = result.get_value(r, k) + val * t_val
                    result.set_value(r, k, res)

        return result

    def _apply_elementwise(self, other, operation):
        result = SparseMatrix(rows=self.rows, cols=self.cols)
        for r in range(self.rows):
            for c, v in self.data[r].items():
                result.set_value(r, c, v)
            for c, v in other.data[r].items():
                res_val = operation(result.get_value(r, c), v)
                result.set_value(r, c, res_val)
        return result

    def save_to_file(self, path):
        try:
            with open(path, 'w') as f:
                f.write(f"rows={self.rows}\ncols={self.cols}\n")
                for r in range(self.rows):
                    for c, v in self.data[r].items():
                        f.write(f"({r},{c},{v})\n")
        except Exception as e:
            raise e

    def show(self):
        print("Sparse Matrix Contents:")
        for row_index, row in enumerate(self.data):
            if row:
                row_display = ' '.join(f"[{row_index}, {col}] = {val}" for col, val in sorted(row.items()))
                print(row_display)
            else:
                print(f"[{row_index}] Empty row")

def main():
    try:
        print("Select an operation:\n 1. Add\n 2. Subtract\n 3. Multiply")
        op = int(input("Your choice (1/2/3): ").strip())
        fileA = input("Enter the first matrix file path: ").strip()
        fileB = input("Enter the second matrix file path: ").strip()

        A = SparseMatrix(matrix_file_path=fileA)
        B = SparseMatrix(matrix_file_path=fileB)

        if op == 1:
            result = A.add(B)
        elif op == 2:
            result = A.subtract(B)
        elif op == 3:
            result = A.multiply(B)
        else:
            print("Invalid choice.")
            return

        output = input("Enter filename to save result: ").strip()
        result.save_to_file(output)
        print(f"Success: Results saved to '{output}'.")
        print("\nResulting Matrix:")
        result.show()

    except Exception as err:
        print(f"An error occurred: {err}")

if __name__ == "__main__":
    main()
