import time
import pygame
from openai import OpenAI
import cv2
import threading
import speech_recognition as sr

client = OpenAI(api_key="sk-***")
messages = [{"role": "system", "content": "You are Q-bot. Remember to keep your answer short."}]

space = cv2.VideoCapture('video/space.mp4')
speaking = cv2.VideoCapture('video/speaking.mp4')
is_playing_audio = False
cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Video', 600, 600)


def gpt(content):
    global is_playing_audio
    sentence, file_num = "", 1
    message = {"role": "user", "content": content}
    messages.append(message)
    reply = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages, stream=True, max_tokens=128)

    for chunk in reply:
        if chunk.choices:
            word = chunk.choices[0].delta.content
            if word:  # Ensure word is not empty
                sentence += word
                if ((file_num == 1 and word.endswith((',', '.', '!', '?', '。', '，', '？', '！', '……'))) or
                        word.endswith(('.', '!', '?', '。', '！', '？', '……'))):
                    print(sentence.strip())
                    output_file = "temp/" + str(file_num) + ".mp3"
                    audio_response = client.audio.speech.create(model="tts-1", voice="nova", input=sentence)
                    audio_response.stream_to_file(output_file)
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.05)
                    audio_thread = threading.Thread(target=play_audio, args=(output_file,))
                    audio_thread.start()
                    file_num += 1
                    sentence = ""


def asr():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while pygame.mixer.music.get_busy():
            time.sleep(0.05)
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Please speak...")
        while True:
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
                try:
                    text = recognizer.recognize_google(audio, language='zh')
                    print("voice: " + text)
                    return text
                except sr.UnknownValueError:
                    # print("Google can't recognize your voice")
                    pass
                except sr.RequestError as e:
                    print(f"Google request error; {e}")
                    return False
            except sr.WaitTimeoutError:
                pass


def handle_input():
    while 1:
        if not is_playing_audio:
            t = asr()
            # t = input('type: ')
            if t:
                contents = t
            else:
                contents = input("Please enter your message: ")
            gpt(contents)


def play_audio(voice_file):
    global is_playing_audio
    pygame.mixer.music.load(voice_file)
    is_playing_audio = True
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.05)
    is_playing_audio = False


def main():
    pygame.mixer.init()
    input_thread = threading.Thread(target=handle_input)
    input_thread.daemon = True  # 将线程设置为守护线程
    input_thread.start()
    while True:
        if is_playing_audio:
            ret, frame = speaking.read()
            if not ret:
                speaking.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
        else:
            ret, frame = space.read()
            if not ret:
                space.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

        cv2.imshow('Video', frame)
        if cv2.waitKey(delay=30) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()
