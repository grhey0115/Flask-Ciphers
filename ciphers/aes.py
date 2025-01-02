from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

class AESCipher:
    def __init__(self):
        self.block_size = AES.block_size

    def _check_key(self, key):
        """Ensure the key is exactly 32 bytes by padding or truncating"""
        if not key:
            raise ValueError("Key cannot be empty")
        
        # Convert to bytes and handle length
        key_bytes = key.encode('utf-8')
        if len(key_bytes) < 32:
            # Pad with zeros if too short
            key_bytes = key_bytes.ljust(32, b'0')
        elif len(key_bytes) > 32:
            # Truncate if too long
            key_bytes = key_bytes[:32]
        
        return key_bytes

    def encrypt(self, text, key):
        try:
            # Convert inputs
            key = self._check_key(key)
            text = text.encode('utf-8')
            
            # Generate random IV
            iv = get_random_bytes(self.block_size)
            
            # Create cipher and encrypt
            cipher = AES.new(key, AES.MODE_CBC, iv)
            padded_text = pad(text, self.block_size)
            encrypted_text = cipher.encrypt(padded_text)
            
            # Combine IV and ciphertext and encode to base64
            result = base64.b64encode(iv + encrypted_text).decode('utf-8')
            
            # Store visualization data
            self.last_operation = {
                'mode': 'CBC',
                'key_length': len(key) * 8,
                'iv': iv.hex(),
                'block_size': self.block_size * 8,
                'padded_length': len(padded_text)
            }
            
            return result
            
        except Exception as e:
            raise ValueError(f"Encryption failed: {str(e)}")

    def decrypt(self, text, key):
        try:
            # Convert inputs
            key = self._check_key(key)
            
            # Decode from base64
            ciphertext = base64.b64decode(text.encode('utf-8'))
            
            # Extract IV and ciphertext
            iv = ciphertext[:self.block_size]
            encrypted_text = ciphertext[self.block_size:]
            
            # Create cipher and decrypt
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted_padded = cipher.decrypt(encrypted_text)
            decrypted_text = unpad(decrypted_padded, self.block_size)
            
            # Store visualization data
            self.last_operation = {
                'mode': 'CBC',
                'key_length': len(key) * 8,
                'iv': iv.hex(),
                'block_size': self.block_size * 8,
                'padded_length': len(decrypted_padded)
            }
            
            return decrypted_text.decode('utf-8')
            
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")

    def get_visualization_data(self):
        """Return visualization data for the last operation"""
        if hasattr(self, 'last_operation'):
            info = self.last_operation
            return {
                'aes_info': f"""
AES Configuration:
-----------------
Mode: {info['mode']}
Key Length: {info['key_length']} bits
Block Size: {info['block_size']} bits
IV: {info['iv']}
Padded Data Length: {info['padded_length']} bytes
                """.strip()
            }
        return None 