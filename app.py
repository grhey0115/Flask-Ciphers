from flask import Flask, render_template, request, jsonify
from ciphers.caesar import Caesar
from ciphers.vigenere import Vigenere
from ciphers.playfair import Playfair
from ciphers.columnar import SingleColumnar, DoubleColumnar

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        data = request.get_json()
        text = data.get('text', '')
        key = data.get('key', '')
        cipher_type = data.get('cipher_type', '')

        if not text:
            return jsonify({'success': False, 'error': 'Text cannot be empty'})

        # Process encryption based on the cipher type
        if cipher_type == 'double-columnar':
            if not key:
                return jsonify({'success': False, 'error': 'Key is required for Double-Columnar cipher'})
            cipher = DoubleColumnar()
            result = cipher.encrypt(text, key)
            viz_data = cipher.get_visualization_data()
            return jsonify({'success': True, 'result': result, 'visualization': viz_data})

        elif cipher_type == 'caesar':
            if not key.isdigit():
                return jsonify({'success': False, 'error': 'Key must be a number for Caesar cipher'})
            cipher = Caesar()
            result = cipher.encrypt(text, int(key))

        elif cipher_type == 'vigenere':
            if not key:
                return jsonify({'success': False, 'error': 'Key is required for Vigenere cipher'})
            cipher = Vigenere()
            result = cipher.encrypt(text, key)

        elif cipher_type == 'playfair':
            if not key:
                return jsonify({'success': False, 'error': 'Key is required for Playfair cipher'})
            cipher = Playfair()
            result = cipher.encrypt(text, key)

        elif cipher_type == 'single-columnar':
            if not key:
                return jsonify({'success': False, 'error': 'Key is required for Single Columnar cipher'})
            cipher = SingleColumnar()
            result = cipher.encrypt(text, key)
            viz_data = cipher.get_visualization_data()
            return jsonify({
                'success': True, 
                'result': result, 
                'visualization': viz_data
            })

        else:
            return jsonify({'success': False, 'error': 'Invalid cipher type'})

        return jsonify({'success': True, 'result': result})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        data = request.get_json()
        text = data.get('text', '')
        key = data.get('key', '')
        cipher_type = data.get('cipher_type', '')

        if not text:
            return jsonify({'success': False, 'error': 'Text cannot be empty'})

        # Process decryption based on the cipher type
        if cipher_type == 'double-columnar':
            if not key:
                return jsonify({'success': False, 'error': 'Key is required for Double-Columnar cipher'})
            cipher = DoubleColumnar()
            result = cipher.decrypt(text, key)
            viz_data = cipher.get_visualization_data()
            return jsonify({'success': True, 'result': result, 'visualization': viz_data})

        elif cipher_type == 'caesar':
            if not key.isdigit():
                return jsonify({'success': False, 'error': 'Key must be a number for Caesar cipher'})
            cipher = Caesar()
            result = cipher.decrypt(text, int(key))

        elif cipher_type == 'vigenere':
            if not key:
                return jsonify({'success': False, 'error': 'Key is required for Vigenere cipher'})
            cipher = Vigenere()
            result = cipher.decrypt(text, key)

        elif cipher_type == 'playfair':
            if not key:
                return jsonify({'success': False, 'error': 'Key is required for Playfair cipher'})
            cipher = Playfair()
            result = cipher.decrypt(text, key)

        elif cipher_type == 'single-columnar':
            if not key:
                return jsonify({'success': False, 'error': 'Key is required for Single Columnar cipher'})
            cipher = SingleColumnar()
            result = cipher.decrypt(text, key)
            viz_data = cipher.get_visualization_data()
            return jsonify({
                'success': True, 
                'result': result, 
                'visualization': viz_data
            })

        else:
            return jsonify({'success': False, 'error': 'Invalid cipher type'})

        return jsonify({'success': True, 'result': result})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
