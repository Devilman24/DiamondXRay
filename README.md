
# 💎 DiamondXRay ![Python Version](https://img.shields.io/badge/python-3.8+-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![GitHub stars](https://img.shields.io/github/stars/devilman24/DiamondXRay?style=social)

> The Swiss Army knife of automatic decoding - Your ultimate tool for cracking encoded messages

![DiamondXRay Banner](https://via.placeholder.com/1200x400.png?text=DiamondXRay+Banner+Showcasing+Multiple+Encoding+Types) *← [Custom banner to add]*

## 🌟 Key Features
- **Smart detection** of encoding formats
- **Multi-layer cascade decoding**
- **Intuitive CLI interface** with history and suggestions
- **Easily extensible** with new decoders
- **Python API** for integration into your projects

## 📋 Supported Formats
| Format        | Example                  | Auto-Detection |
|---------------|--------------------------|----------------|
| Base64        | `SGVsbG8gd29ybGQ=`       | ✅             |
| Hexadecimal   | `48656c6c6f20776f726c64` | ✅             |
| Binary        | `01001000 01100101`      | ✅             |
| URL Encoding  | `%48%65%6c%6c%6f`        | ✅             |
| ROT13         | `Uryyb Jbeyq`            | ✅             |
| Morse Code    | `.... . .-.. .-.. ---`   | ✅             |

## 🚀 Quick Installation

```bash
git clone https://github.com/devilman24/DiamondXRay.git
cd DiamondXRay
pip install -r requirements.txt
```

## 💻 Basic Usage

### Interactive Mode
```bash
python3 diamondxray.py
```

### Complete Example
```text
┌──(user㉿host)-[~/DiamondXRay]
└─$ python3 diamondxray.py

Enter text to decode (or 'quit' to exit): JXZlciBkZWNvZGVkIQ==

==================================================
Text analysis: 'JXZlciBkZWNvZGVkIQ=='
==================================================

[🔍] Detected: Base64 (Confidence: 99%)
[💎] Result: "%ver decoded!"

[?] Decode this result again? (y/n): y

[🔍] Detected: URL Encoding (Confidence: 100%)
[✨] Final message: "Never decoded!"
```

## ⚙️ Advanced Features

### Direct Decoding
```bash
python3 diamondxray.py "Your encoded text"
```

### Module Usage
```python
from diamondxray import Decoder

result = Decoder.analyze("SGVsbG8gd29ybGQh")
print(f"Format: {result.format}, Text: {result.text}")
```

## 🛠 How to Add a Decoder

1. Create a new method in `decoders.py`:
```python
@staticmethod
def detect_customformat(text: str) -> Optional[DecodeResult]:
    """Custom detection"""
    if is_customformat(text):
        return DecodeResult("CustomFormat", decode_customformat(text))
    return None
```

2. Add to detection pipeline:
```python
DECODERS = [
    ...,
    Decoder.detect_customformat
]
```

## 🤝 Contributing
Contributions are welcome! Please check our [Contribution Guidelines](CONTRIBUTING.md).

## 📜 License
🎭! © 2025 Devilman24 - See [LICENSE](LICENSE) for details.
```
