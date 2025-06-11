import os

class SparseMatrix:
    def __init__(self, matrix_file_path=None, rows=None, cols=None):
        if matrix_file_path:
            self._read_matrix_file(matrix_file_path)
        else:
            self.rows = rows
            self.cols = cols
            self.data = [{} for _ in range(rows)]

    def _read_matrix_file(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        try:
            with open(path, 'r') as file:
                lines = [line.strip() for line in file if line.strip()]

                # Determine starting line for entries:
                start_idx = 0
                # Check if first two lines are rows= and cols= headers; ignore their values
                if len(lines) >= 2 and lines[0].startswith("rows=") and lines[1].startswith("cols="):
                    start_idx = 2

                entries = lines[start_idx:]

                max_row = -1
                max_col = -1
                parsed_entries = []

                for i, entry in enumerate(entries, start=start_idx + 1):
                    if not (entry.startswith('(') and entry.endswith(')')):
                        raise ValueError(f"Invalid format at line {i}: {entry}")

                    parts = entry[1:-1].split(',')
                    if len(parts) != 3:
                        raise ValueError(f"Expected 3 elements at line {i}, got: {parts}")

                    try:
                        r, c, val = map(int, parts)
                    except ValueError:
                        raise ValueError(f"Non-integer value at line {i}: {entry}")

                    if r > max_row:
                        max_row = r
                    if c > max_col:
                        max_col = c

                    parsed_entries.append((r, c, val))

                # Now set matrix size based on max indices found
                self.rows = max_row + 1
                self.cols = max_col + 1
                self.data = [{} for _ in range(self.rows)]

                # Insert entries into data structure
                for r, c, val in parsed_entries:
                    self.set_value(r, c, val)

        except Exception as e:
            raise e  # propagate exception

    def set_value(self, row, col, value):
        if value != 0:
            self.data[row][col] = value
        elif col in self.data[row]:
            del self.data[row][col]

    def get_value(self, row, col):
        return self.data[row].get(col, 0)

    def _resize(self, new_rows, new_cols):
        # Extend rows
        if new_rows > self.rows:
            for _ in range(new_rows - self.rows):
                self.data.append({})
            self.rows = new_rows

        # Update cols to new_cols if larger
        if new_cols > self.cols:
            self.cols = new_cols

    def add(self, other):
        # Resize both matrices to max dimension
        max_rows = max(self.rows, other.rows)
        max_cols = max(self.cols, other.cols)
        self._resize(max_rows, max_cols)
        other._resize(max_rows, max_cols)

        return self._apply_elementwise(other, lambda x, y: x + y)

    def subtract(self, other):
        # Resize both matrices to max dimension
        max_rows = max(self.rows, other.rows)
        max_cols = max(self.cols, other.cols)
        self._resize(max_rows, max_cols)
        other._resize(max_rows, max_cols)

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
        with open(path, 'w') as f:
            f.write(f"rows={self.rows}\ncols={self.cols}\n")
            for r in range(self.rows):
                for c, v in self.data[r].items():
                    f.write(f"({r},{c},{v})\n")

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
        op = input("Your choice (1/2/3): ").strip()
        if op not in {'1', '2', '3'}:
            print("Invalid choice. Please enter 1, 2, or 3.")
            return

        fileA = input("Enter the first matrix file path: ").strip()
        fileB = input("Enter the second matrix file path: ").strip()

        print("Loading matrices...")
        A = SparseMatrix(matrix_file_path=fileA)
        B = SparseMatrix(matrix_file_path=fileB)

        if op == '1':
            result = A.add(B)
        elif op == '2':
            result = A.subtract(B)
        elif op == '3':
            result = A.multiply(B)

        output = input("Enter filename to save result (e.g., result.txt): ").strip()
        result.save_to_file(output)
        print(f"✅ Success: Results saved to '{output}'.\n")
        result.show()

    except FileNotFoundError as fnf_err:
        print(f"❌ File error: {fnf_err}")
    except (ValueError, IndexError) as data_err:
        print(f"❌ Data error: {data_err}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
