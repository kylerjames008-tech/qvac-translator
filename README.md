# QVAC English to Japanese Translator

An offline, on-device English to Japanese translation app using Tether's QVAC SDK.

## Features

- **On-device inference**: No API keys, no cloud usage bills. Your data stays local.
- **Offline capable**: Once downloaded, works without internet.
- **Fast & Private**: Runs directly on your machine.

## Requirements

- Python 3.8+
- Node.js/npm (for QVAC SDK worker)

## Installation

1. Clone or download this repository.
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install the QVAC SDK worker (requires Node.js/npm):
   ```bash
   npm install -g @qvac/sdk@0.19.1
   ```

## Usage

Run the application:
```bash
python app.py
```

Enter English text when prompted, and it will be translated to Japanese.

## Tech Stack

- SDK: [tetherto-qvac-sdk](https://pypi.org/project/tetherto-qvac-sdk/) (v0.19.1)
- Model: Llama 3.2 1B Instruct (for translation via prompt)
- Task: Translation (on-device completion)

## How It Works

This app uses the QVAC SDK to run an LLM locally on your machine. Instead of calling a cloud API, the model runs entirely on-device, making translation private and offline-capable.

## Credits

Built with [QVAC SDK](https://github.com/tetherto/qvac) by [@tether](https://x.com/tether).
