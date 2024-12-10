class Caesar:
    def __init__(self):
        self.LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        
    def encrypt(self, text, key):
        result = ''
        text = text.upper()
        
        for char in text:
            if char in self.LETTERS:
                # Find the position in the alphabet
                position = self.LETTERS.find(char)
                # Apply the shift
                new_position = (position + key) % 26
                # Add the new character to the result
                result += self.LETTERS[new_position]
            else:
                result += char
                
        return result
    
    def decrypt(self, text, key):
        return self.encrypt(text, -key) 