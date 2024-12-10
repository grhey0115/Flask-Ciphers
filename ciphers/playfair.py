class Playfair:
    def __init__(self):
        self.alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'  
    def _create_matrix(self, key):
        key = key.upper().replace('J', 'I')
        key_chars = []
        for c in key:
            if c not in key_chars and c.isalpha():
                key_chars.append(c)

        matrix_chars = key_chars + [c for c in self.alphabet if c not in key_chars]
        matrix = [matrix_chars[i:i + 5] for i in range(0, 25, 5)]
        return matrix

    def _find_position(self, char, matrix):
        for i in range(5):
            for j in range(5):
                if matrix[i][j] == char:
                    return i, j
        return None

    def _prepare_text(self, text, for_decryption=False):
        # Convert to uppercase and replace J with I
        text = text.upper().replace('J', 'I')
        
        cleaned_text = ''
        self.space_positions = []
        char_count = 0
        
        for i, char in enumerate(text):
            if char.isalpha():
                cleaned_text += char
                char_count += 1
            elif char == ' ' and for_decryption:
                self.space_positions.append(char_count)

        pairs = []
        i = 0
        while i < len(cleaned_text):
            if i == len(cleaned_text) - 1:
                pairs.append(cleaned_text[i] + 'X')
                i += 1
            elif cleaned_text[i] == cleaned_text[i + 1]:
                pairs.append(cleaned_text[i] + 'X')
                i += 1
            else:
                pairs.append(cleaned_text[i] + cleaned_text[i + 1])
                i += 2

        return pairs

    def encrypt(self, text, key):
        if not text or not key:
            raise ValueError("Text and key cannot be empty")

        matrix = self._create_matrix(key)
        pairs = self._prepare_text(text)
        result = ''

        for pair in pairs:
            row1, col1 = self._find_position(pair[0], matrix)
            row2, col2 = self._find_position(pair[1], matrix)

            if row1 == row2:
                result += matrix[row1][(col1 + 1) % 5]
                result += matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                result += matrix[(row1 + 1) % 5][col1]
                result += matrix[(row2 + 1) % 5][col2]
            else:
                result += matrix[row1][col2]
                result += matrix[row2][col1]

        self.last_grid = matrix
        return result.lower()

    def decrypt(self, text, key):
        if not text or not key:
            raise ValueError("Text and key cannot be empty")

        matrix = self._create_matrix(key)
        pairs = self._prepare_text(text, for_decryption=True)
        decrypted = ''

        for pair in pairs:
            row1, col1 = self._find_position(pair[0], matrix)
            row2, col2 = self._find_position(pair[1], matrix)

            if row1 == row2:
                decrypted += matrix[row1][(col1 - 1) % 5]
                decrypted += matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                decrypted += matrix[(row1 - 1) % 5][col1]
                decrypted += matrix[(row2 - 1) % 5][col2]
            else:
                decrypted += matrix[row1][col2]
                decrypted += matrix[row2][col1]

        # Insert spaces back into the decrypted text
        result = ''
        char_count = 0
        space_index = 0
        
        for char in decrypted.lower():
            if space_index < len(self.space_positions) and char_count == self.space_positions[space_index]:
                result += ' '
                space_index += 1
            result += char
            char_count += 1

        self.last_grid = matrix
        return result

    def get_visualization_data(self):
        """Return the grid and formatted string visualization"""
        if hasattr(self, 'last_grid'):
            # Create formatted string representation
            grid_str = "\nPlayfair 5x5 Grid:\n"
            grid_str += "  " + " ".join(f" {i} " for i in range(5)) + "\n"  # Column numbers
            for i, row in enumerate(self.last_grid):
                grid_str += f"{i} " + " ".join(f"[{cell}]" for cell in row) + "\n"
            
            return {
                'grid': self.last_grid,
                'formatted_grid': grid_str
            }
        return None
