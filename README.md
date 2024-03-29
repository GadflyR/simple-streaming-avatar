# Simple real-time chatbot avatar
The robot's face has two modes: it keeps its mouth closed when not speaking, with only natural head movements; and it makes speaking movements when speaking.

# Notice
Replace openai.api_key with your own api key. You can get it from here: https://platform.openai.com/api-keys

# Requirements
`pip install openai pygame cv2 speech_recognition threading time`

# Advantages over similar products
1. Compared with character ai, Pi and other software, it has the function of voice or real-time interactive character avatar, which enhances the customer's intuitive experience, enables full voice dialogue, and frees both hands.
   
2. Compared with websites such as D-ID and HeyGen that generate lip-syncing videos of characters, and all other real-time dialogue robots developed based on lip-syncing technology (such as Wav2Lip, Sadtalker), the presentation of the picture does not incur any cost and is relatively without delay. time (within 2.5 seconds for manual testing, far exceeding the response speed of most open source digital human projects). This is because our large language model and tts service are both streaming applications.
   
3. Compared with existing real-time interactive chat digital people such as Call Annie, our program has almost no configuration requirements for both the client and the server, because all that needs to be done is to quickly switch between two videos.


# Tech Stack
ASR: SpeechRecognition by Google

LLM: OpenAI GPT-3.5-turbo

TTS: OpenAI tts-1


Videos were AI generated by D-ID

# Supporting Languages
English and Chinese
