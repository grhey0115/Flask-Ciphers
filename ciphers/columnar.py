class SingleColumnar:
    def __init__(self):
        self.last_grid = None
        self.last_order = None

    def _create_grid(self, text, key):
        """Create and return the columnar grid based on text and key."""
        width = len(key)
        text = text.upper().replace(' ', '_')

        # Calculate height and create the grid
        height = -(-len(text) // width)  # Ceiling division
        grid = [list(text[i * width:(i + 1) * width].ljust(width, '_')) for i in range(height)]

        return grid

    def _get_column_order(self, key):
        """Get the order of columns based on the sorted key."""
        key = key.upper()
        return [i for _, i in sorted((char, i) for i, char in enumerate(key))]

    def encrypt(self, text, key):
        if not text or not key:
            raise ValueError("Text and key cannot be empty.")

        grid = self._create_grid(text, key)
        column_order = self._get_column_order(key)

        # Encrypt by reading columns in sorted key order
        result = ''.join(''.join(row[col] for row in grid) for col in column_order)

        # Store for visualization
        self.last_grid = grid
        self.last_order = column_order

        return result.lower()

    def decrypt(self, text, key):
        if not text or not key:
            raise ValueError("Text and key cannot be empty.")

        width = len(key)
        height = -(-len(text) // width)  # Ceiling division
        column_order = self._get_column_order(key)

        # Calculate column lengths for uneven columns
        full_cols = len(text) % width or width
        col_heights = [height if i < full_cols else height - 1 for i in range(width)]

        # Fill the grid column by column
        grid = [[''] * width for _ in range(height)]
        pos = 0
        for col_idx in column_order:
            for row in range(col_heights[col_idx]):
                grid[row][col_idx] = text[pos]
                pos += 1

        # Decrypt by reading rows
        result = ''.join(''.join(row) for row in grid).replace('_', ' ').rstrip()

        # Store for visualization
        self.last_grid = grid
        self.last_order = column_order

        return result.lower()

    def get_visualization_data(self):
        """Return the grid and column order for visualization."""
        if self.last_grid is not None and self.last_order is not None:
            # Create formatted string representation
            grid_str = "\nColumnar Grid:\n"
            grid_str += "  " + " ".join(f" {i} " for i in range(len(self.last_grid[0]))) + "\n"
            for i, row in enumerate(self.last_grid):
                grid_str += f"{i} " + " ".join(f"[{cell}]" for cell in row) + "\n"
            
            return {
                'grid': self.last_grid,
                'column_order': self.last_order,
                'formatted_grid': grid_str  # Return the formatted grid as well
            }
        return None


class DoubleColumnar:
    def __init__(self):
        self.first_grid = None
        self.second_grid = None
        self.first_order = None
        self.second_order = None

    def _single_encrypt(self, text, key):
        single = SingleColumnar()
        return single.encrypt(text, key)

    def _single_decrypt(self, text, key):
        single = SingleColumnar()
        return single.decrypt(text, key)

    def encrypt(self, text, key1, key2):
        if not text or not key1 or not key2:
            raise ValueError("Text and both keys cannot be empty.")

        # First encryption
        first_cipher = SingleColumnar()
        first_result = first_cipher.encrypt(text, key1)
        self.first_grid = first_cipher.last_grid
        self.first_order = first_cipher.last_order

        # Second encryption
        second_cipher = SingleColumnar()
        final_result = second_cipher.encrypt(first_result, key2)
        self.second_grid = second_cipher.last_grid
        self.second_order = second_cipher.last_order

        return final_result.lower()

    def decrypt(self, text, key1, key2):
        if not text or not key1 or not key2:
            raise ValueError("Text and both keys cannot be empty.")

        # Decrypt in reverse order
        second_cipher = SingleColumnar()
        first_result = second_cipher.decrypt(text, key2)
        self.second_grid = second_cipher.last_grid
        self.second_order = second_cipher.last_order

        first_cipher = SingleColumnar()
        final_result = first_cipher.decrypt(first_result, key1)
        self.first_grid = first_cipher.last_grid
        self.first_order = first_cipher.last_order

        return final_result.lower().replace('_', ' ').rstrip()

    def get_visualization_data(self):
        """Return both grids and column orders for visualization."""
        if self.first_grid and self.second_grid:
            first_grid_str = "\nFirst Columnar Grid:\n"
            first_grid_str += "  " + " ".join(f" {i} " for i in range(len(self.first_grid[0]))) + "\n"
            for i, row in enumerate(self.first_grid):
                first_grid_str += f"{i} " + " ".join(f"[{cell}]" for cell in row) + "\n"

            second_grid_str = "\nSecond Columnar Grid:\n"
            second_grid_str += "  " + " ".join(f" {i} " for i in range(len(self.second_grid[0]))) + "\n"
            for i, row in enumerate(self.second_grid):
                second_grid_str += f"{i} " + " ".join(f"[{cell}]" for cell in row) + "\n"

            return {
                'first_grid': self.first_grid,
                'first_order': self.first_order,
                'second_grid': self.second_grid,
                'second_order': self.second_order,
                'first_grid_str': first_grid_str,
                'second_grid_str': second_grid_str
            }
        return None
