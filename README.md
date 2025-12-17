# GPT Voice Chatbot

A voice-based conversational AI assistant powered by OpenAI's GPT-3.5-turbo and Whisper models. Speak to the assistant through your microphone and receive intelligent responses.

## Features

- 🎤 **Voice Input** – Records audio from microphone using SoundDevice
- 🔊 **Speech-to-Text** – Converts speech to text using OpenAI Whisper
- 🤖 **AI Responses** – Generates intelligent responses with GPT-3.5-turbo
- 🛡️ **Content Filtering** – Filters banned words from user input
- 📝 **Conversation Logging** – Saves all interactions to timestamped log files
- 🔄 **Continuous Conversation** – Maintains conversation history for context-aware responses

## Requirements

- Python 3.8+
- OpenAI API Key
- Microphone

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/elifkeskin/GPT_ile_Sesli_Asistan.git
   cd GPT_ile_Sesli_Asistan
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

Run the voice chatbot:
```bash
python gpt_voice_chat.py
```

### Voice Commands

- **Speak normally** – The assistant will listen for 5 seconds and respond
- **Say "çık", "çıkış", "kapat", "bitir", or "dur"** – Exits the program

## Project Structure

```
GPT_ile_Sesli_Asistan/
├── gpt_voice_chat.py    # Main application
├── requirements.txt     # Python dependencies
├── .env                 # API keys (not tracked in git)
├── .gitignore          # Git ignore rules
├── LICENSE             # MIT License
├── logs/               # Conversation logs
└── README.md           # This file
```

## How It Works

1. **Recording** – Captures 5 seconds of audio from the microphone
2. **Transcription** – Sends audio to OpenAI Whisper API for speech-to-text
3. **Filtering** – Checks for and filters banned words
4. **Response Generation** – Sends transcribed text to GPT-3.5-turbo
5. **Logging** – Records all interactions to log files

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `DURATION` | 5 | Recording duration in seconds |
| `FS` | 44100 | Audio sampling rate (Hz) |
| `BANNED_WORDS` | ["zararlı"] | List of words to filter |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
