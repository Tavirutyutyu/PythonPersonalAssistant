import subprocess

def speak(text):
    try:
        subprocess.run(['festival', '--tts'], input=text, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error in speech synthesis: {e}")