class Vigenere:
    def __init__(self):
        self.LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    def _prepare_key(self, text, key):
        """Prepare the key to match the length of the text, skipping spaces"""
        key = key.upper()
        key_repeated = ''
        key_index = 0
        
        for char in text.upper():
            if char.isalpha():
                # Only add key character if text character is a letter
                key_repeated += key[key_index % len(key)]
                key_index += 1
            else:
                # For spaces or other characters, add a placeholder
                key_repeated += char
                
        return key_repeated

    def encrypt(self, text, key):
        if not key:
            raise ValueError("Key cannot be empty")
        
        # Get the prepared key
        key_stream = self._prepare_key(text, key)
        result = ''
        
        for i, char in enumerate(text.upper()):
            if char in self.LETTERS:
                # Get positions of the text and key characters
                text_index = self.LETTERS.find(char)
                key_index = self.LETTERS.find(key_stream[i])
                
                # Apply Vigenère formula: (text_index + key_index) mod 26
                new_index = (text_index + key_index) % 26
                result += self.LETTERS[new_index].lower()  # Convert to lowercase
            else:
                # Keep spaces and other characters unchanged
                result += char
        
        return result
    
    def decrypt(self, text, key):
        if not key:
            raise ValueError("Key cannot be empty")
        
        # Get the prepared key
        key_stream = self._prepare_key(text, key)
        result = ''
        
        for i, char in enumerate(text.upper()):
            if char in self.LETTERS:
                # Get positions of the text and key characters
                text_index = self.LETTERS.find(char)
                key_index = self.LETTERS.find(key_stream[i])
                
                # Apply Vigenère decryption formula: (text_index - key_index) mod 26
                new_index = (text_index - key_index) % 26
                result += self.LETTERS[new_index].lower()  # Convert to lowercase
            else:
                # Keep spaces and other characters unchanged
                result += char
        
        return result 