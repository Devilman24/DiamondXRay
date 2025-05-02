import base64
import binascii
import re
from urllib.parse import unquote
from typing import Tuple, Optional

class TextDecoder:
    @staticmethod
    def detect_base64(text: str) -> Optional[Tuple[str, str]]:
        """Base64 detection and decoding with enhanced validation"""
        try:
            # Check if it's valid Base64
            if len(text) % 4 != 0 or not re.match(r'^[A-Za-z0-9+/=]+$', text):
                return None
            
            decoded_bytes = base64.b64decode(text.encode(), validate=True)
            decoded = decoded_bytes.decode('utf-8', errors='strict')
            
            # Additional verification to avoid false positives
            if base64.b64encode(decoded_bytes).decode() == text:
                return ("Base64", decoded)
        except (binascii.Error, UnicodeDecodeError):
            pass
        return None

    @staticmethod
    def detect_hex(text: str) -> Optional[Tuple[str, str]]:
        """Hexadecimal detection and decoding"""
        clean_text = text.lower().replace(' ', '').replace(':', '')
        if not re.fullmatch(r'^[0-9a-f]+$', clean_text) or len(clean_text) % 2 != 0:
            return None
        
        try:
            decoded_bytes = binascii.unhexlify(clean_text)
            decoded = decoded_bytes.decode('utf-8', errors='strict')
            return ("Hex", decoded)
        except (binascii.Error, UnicodeDecodeError):
            return None

    @staticmethod
    def detect_binary(text: str) -> Optional[Tuple[str, str]]:
        """Binary detection and decoding"""
        clean_text = text.replace(' ', '')
        if not re.fullmatch(r'^[01]+$', clean_text) or len(clean_text) % 8 != 0:
            return None
        
        try:
            decoded = ''.join(
                chr(int(clean_text[i:i+8], 2)) 
                for i in range(0, len(clean_text), 8)
            )
            # Verify the result is readable
            if any(ord(c) < 32 and c not in '\n\r\t' for c in decoded):
                return None
            return ("Binary", decoded)
        except (ValueError, UnicodeDecodeError):
            return None

    @staticmethod
    def detect_url_encoding(text: str) -> Optional[Tuple[str, str]]:
        """URL Encoding detection and decoding"""
        if '%' not in text:
            return None
        
        try:
            decoded = unquote(text)
            if decoded != text and not any(ord(c) < 32 for c in decoded):
                return ("URL Encoding", decoded)
        except Exception:
            pass
        return None

    @staticmethod
    def detect_rot13(text: str) -> Optional[Tuple[str, str]]:
        """ROT13 detection and decoding"""
        if not text.isalpha():
            return None
        
        rot13 = text.translate(str.maketrans(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
            'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'))
        
        if rot13 != text:
            return ("ROT13", rot13)
        return None

    @staticmethod
    def detect_morse(text: str) -> Optional[Tuple[str, str]]:
        """Morse code detection and decoding"""
        morse_dict = {
            '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
            '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
            '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
            '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
            '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
            '--..': 'Z', '-----': '0', '.----': '1', '..---': '2',
            '...--': '3', '....-': '4', '.....': '5', '-....': '6',
            '--...': '7', '---..': '8', '----.': '9', '/': ' ', ' ': ' '
        }
        
        # Stricter Morse code validation
        if not all(c in '.- /' for c in text):
            return None
        
        try:
            decoded = ''.join(
                morse_dict.get(code, '') 
                for code in text.split(' ')
            )
            if len(decoded) > 0 and any(c.isalnum() for c in decoded):
                return ("Morse", decoded)
        except Exception:
            pass
        return None

    @staticmethod
    def detect_encoding(text: str) -> Tuple[str, str]:
        """Detects and decodes text using various encoding methods"""
        detectors = [
            TextDecoder.detect_base64,
            TextDecoder.detect_hex,
            TextDecoder.detect_binary,
            TextDecoder.detect_url_encoding,
            TextDecoder.detect_rot13,
            TextDecoder.detect_morse
        ]
        
        for detector in detectors:
            result = detector(text)
            if result is not None:
                return result
        
        return ("Unknown", text)

def main():
    while True:
        user_input = input("\nEnter text to decode (or 'quit' to exit): ").strip()
        
        if user_input.lower() in ('quit', 'exit', 'q'):
            break
        
        print("\n" + "="*50)
        print(f"Analysis for: '{user_input}'")
        print("="*50)
        
        encoding, decoded = TextDecoder.detect_encoding(user_input)
        
        if encoding != "Unknown":
            print(f"\nDetection: {encoding}")
            print(f"Decoded text: '{decoded}'")
            
            # Option to try decoding the result again
            if input("\nWould you like to try decoding the result again? (y/n) ").lower() == 'y':
                _, redecoded = TextDecoder.detect_encoding(decoded)
                if redecoded != decoded:
                    print(f"\nResult after re-decoding: '{redecoded}'")
        else:
            print("\nNo known encoding detected.")
            print(f"Original text: '{user_input}'")

if __name__ == "__main__":
    main()
