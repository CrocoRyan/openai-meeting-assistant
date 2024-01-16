# Meeting Minutes Assistant - A Flask Project

## Project Overview

This project focuses on creating a Meeting Minutes Assistant, a Telegram chatbot designed to facilitate the
transcription and summarization of meeting minutes. It utilizes the latest Azure Speech-to-Text services coupled with
OpenAI's GPT models to deliver accurate and concise meeting summaries.

### Key Features:

- **Real-Time Transcription**: Leverages Azure's Speech-to-Text service to transcribe meetings in real-time.
- **AI Summarization**: Uses OpenAI's GPT models to generate summaries of the transcribed text, focusing on key
  points and decisions.
- **Multi-Conversation Support**: Capable of managing multiple meeting minutes assistant sessions simultaneously.
- **Persistent Storage**: GPT's Conversation memory and summary records are stored securely in a Azure Cosmos DB database for future
  reference.
- **Interactive Telegram Bot**: A user-friendly chatbot interface on Telegram to interact with users, handle requests,
  and deliver transcriptions and summaries.

## Technical Stack

- **Backend Framework**: Flask
- **Speech-to-Text Service**: Azure Speech-to-Text
- **AI Model**: OpenAI's GPT Assistant
- **Database**: Azure Cosmos DB
- **Chatbot Interface**: Telegram API
- **Hosting/Deployment**: Docker, Azure Container Registry + Azure App Service 

### System Architecture
![Alt Text](./system_architecture.svg)
<img src="./system_architecture.svg">

## Getting Started

### Prerequisites

- Python 3.x(3.8+)
- Flask
- Azure Cosmos DB
- Azure and OpenAI API keys
- Telegram Bot access

### Installation & Setup

1. **Clone the repository:**
   ```
   git clone [repository-url]
   ```

2. **Install required packages:**
   ```
   pip install -r requirements.txt
   ```

3. **Set up environment variables(find them under config_[env].json:**
    - Azure SPEECH-TO-TEXT API Key: SPEECH_KEY
    - Azure Service Region: SPEECH_REGION
    - OpenAI API Key: OPENAI_API_KEY
    - PRE-TRAINED ASSISTANT ID: ASSISTANT_ID
    - MongoDB URI: DATABASE_URI
    - Telegram bot token: BOT_TOKEN
    - Debug Mode: DEBUG

4. **Run the Flask application:**
   ```
   python3 app.py
   ```
   
### Run in Docker container

```
docker build --no-cache -t openai-meeting-assistant:latest . 
docker run -d -p 5000:5000 --name meeting-assistant openai-meeting-assistant:latest
```

## Usage

1. **Start a conversation with the Telegram bot.**
2. **Initiate a meeting transcription by sending a voice message or starting a live audio feed.**
3. **Receive real-time transcriptions and request summaries as needed.**
4. **Access past transcripts and summaries memory from the MongoDB database.**
5. TBD


## License

[Specify License]

---

**Note**: This project is not officially affiliated with Azure, OpenAI, or Telegram.
