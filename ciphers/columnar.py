class SingleColumnar:
    def __init__(self):
        pass

    def _create_grid(self, text, key):
        """Create and return the columnar grid"""
        # Get the width from key length
        width = len(key)
        # Convert spaces to underscores and convert to uppercase
        text = text.upper().replace(' ', '_')
        
        # Calculate height
        height = len(text) // width
        if len(text) % width != 0:
            height += 1
            
        # Create the grid and fill with text
        grid = []
        pos = 0
        for i in range(height):
            row = []
            for j in range(width):
                if pos < len(text):
                    row.append(text[pos])
                else:
                    row.append('_')  # Padding with underscore instead of X
                pos += 1
            grid.append(row)
            
        return grid

    def _get_column_order(self, key):
        """Get the order of columns based on the key"""
        # Create list of (character, position) pairs
        key = key.upper()
        key_with_positions = [(char, index) for index, char in enumerate(key)]
        # Sort by character and get original positions
        sorted_positions = [pos for _, pos in sorted(key_with_positions)]
        return sorted_positions

    def encrypt(self, text, key):
        if not text or not key:
            raise ValueError("Text and key cannot be empty")
            
        # Create the grid
        grid = self._create_grid(text, key)
        column_order = self._get_column_order(key)
        
        # Read off columns in the order determined by the key
        result = ''
        for col in column_order:
            for row in grid:
                result += row[col]
        
        # Store the grid for visualization
        self.last_grid = grid
        self.last_order = column_order
        
        return result.lower()

    def decrypt(self, text, key):
        if not text or not key:
            raise ValueError("Text and key cannot be empty")
            
        width = len(key)
        height = len(text) // width
        if len(text) % width != 0:
            height += 1
            
        # Create empty grid
        grid = [['' for _ in range(width)] for _ in range(height)]
        
        # Get column order
        column_order = self._get_column_order(key)
        
        # Calculate column lengths (for uneven columns)
        full_cols = len(text) % width
        if full_cols == 0:
            full_cols = width
            
        # Fill the grid column by column
        pos = 0
        for col_idx in range(width):
            # Get the actual column number from the order
            col = column_order.index(col_idx)
            # Determine column height
            col_height = height if col < full_cols else height - 1
            
            for row in range(col_height):
                if pos < len(text):
                    grid[row][col] = text[pos]
                    pos += 1
        
        # Read off the grid row by row and replace underscores with spaces
        result = ''
        for row in grid:
            result += ''.join(row)
        
        # Replace underscores with spaces in the final result
        result = result.lower().replace('_', ' ').rstrip()  # Remove trailing spaces
            
        # Store the grid for visualization
        self.last_grid = grid
        self.last_order = column_order
        
        return result

    def get_visualization_data(self):
        """Return the grid and column order for visualization"""
        if hasattr(self, 'last_grid') and hasattr(self, 'last_order'):
            # Create formatted string representation
            grid_str = "\nColumnar Grid:\n"
            grid_str += "  " + " ".join(f" {i} " for i in range(len(self.last_grid[0]))) + "\n"
            for i, row in enumerate(self.last_grid):
                grid_str += f"{i} " + " ".join(f"[{cell}]" for cell in row) + "\n"
            
            return {
                'grid': self.last_grid,
                'column_order': self.last_order,
                'formatted_grid': grid_str
            }
        return None 
    


class DoubleColumnar:
    def __init__(self):
        pass

    def _create_grid(self, text, key):
        """Create and return the columnar grid"""
        width = len(key)
        text = text.upper().replace(' ', '_')
        
        # Calculate height
        height = len(text) // width
        if len(text) % width != 0:
            height += 1
            
        # Create the grid and fill with text
        grid = []
        pos = 0
        for i in range(height):
            row = []
            for j in range(width):
                if pos < len(text):
                    row.append(text[pos])
                else:
                    row.append('_')  # Padding with underscore
                pos += 1
            grid.append(row)
            
        return grid

    def _get_column_order(self, key):
        """Get the order of columns based on the key"""
        key = key.upper()
        key_with_positions = [(char, index) for index, char in enumerate(key)]
        sorted_positions = [pos for _, pos in sorted(key_with_positions)]
        return sorted_positions

    def _single_encrypt(self, text, key):
        """Perform single columnar encryption"""
        grid = self._create_grid(text, key)
        column_order = self._get_column_order(key)
        
        # Read off columns in the order determined by the key
        result = ''
        for col in column_order:
            for row in grid:
                result += row[col]
        
        return result

    def _single_decrypt(self, text, key):
        """Perform single columnar decryption"""
        width = len(key)
        height = len(text) // width
        if len(text) % width != 0:
            height += 1
            
        # Create empty grid
        grid = [['' for _ in range(width)] for _ in range(height)]
        
        # Get column order
        column_order = self._get_column_order(key)
        
        # Calculate column lengths
        full_cols = len(text) % width
        if full_cols == 0:
            full_cols = width
            
        # Fill the grid column by column
        pos = 0
        for col_idx in range(width):
            col = column_order.index(col_idx)
            col_height = height if col < full_cols else height - 1
            
            for row in range(col_height):
                if pos < len(text):
                    grid[row][col] = text[pos]
                    pos += 1
        
        # Read off the grid row by row
        result = ''
        for row in grid:
            result += ''.join(row)
            
        return result

    def encrypt(self, text, key, key2):  # Changed parameter names to match Flask route
        """Perform double columnar encryption"""
        if not text or not key or not key2:
            raise ValueError("Text and both keys cannot be empty")
            
        # First encryption
        first_result = self._single_encrypt(text, key)
        self.first_grid = self._create_grid(text, key)
        self.first_order = self._get_column_order(key)
        
        # Second encryption
        final_result = self._single_encrypt(first_result, key2)
        self.second_grid = self._create_grid(first_result, key2)
        self.second_order = self._get_column_order(key2)
        
        return final_result.lower()

    def decrypt(self, text, key, key2):  # Changed parameter names to match Flask route
        """Perform double columnar decryption"""
        if not text or not key or not key2:
            raise ValueError("Text and both keys cannot be empty")
            
        # Decrypt in reverse order
        first_result = self._single_decrypt(text, key2)
        self.second_grid = self._create_grid(first_result, key2)
        self.second_order = self._get_column_order(key2)
        
        final_result = self._single_decrypt(first_result, key)
        self.first_grid = self._create_grid(final_result, key)
        self.first_order = self._get_column_order(key)
        
        # Replace underscores with spaces and clean up
        return final_result.lower().replace('_', ' ').rstrip()

    def get_visualization_data(self):
        """Return both grids and column orders for visualization"""
        if hasattr(self, 'first_grid') and hasattr(self, 'second_grid'):
            # Format first grid
            first_grid_str = "\nFirst Columnar Grid:\n"
            first_grid_str += "  " + " ".join(f" {i} " for i in range(len(self.first_grid[0]))) + "\n"
            for i, row in enumerate(self.first_grid):
                first_grid_str += f"{i} " + " ".join(f"[{cell}]" for cell in row) + "\n"
            
            # Format second grid
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