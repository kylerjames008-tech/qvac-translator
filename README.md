# Eng to Hindi Translator

A local AI translator that uses Tether's QVAC SDK to translate English to Hindi directly on your device. The model runs locally, so there's no API key, no usage bills, and your data never leaves your machine.

## Features

- Translate English text to Hindi
- 100% offline - no internet required after initial model download
- Privacy-focused - your text stays on your device

## Requirements

- Python 3.8+
- Node.js and npm (used by the SDK for the inference worker)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/qvac-hindi-translator.git
cd qvac-hindi-translator
```

2. Install the QVAC SDK:
```bash
pip install tetherto-qvac-sdk
```

3. Install Node.js and npm if you don't have them.

## Running

```bash
python app.py
```

The first run will download the translation model (~140MB). Subsequent runs will use the cached model.

## SDK Version

- tetherto-qvac-sdk: 0.19.1

## License

MIT License