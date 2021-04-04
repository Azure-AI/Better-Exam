from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig
import azure.cognitiveservices.speech as speechsdk


message ="<break time=\"2000ms\"/>, Hello, I am BEAM, your personal exam assistant. I will be guiding you through your exam. Please first tell me your name by long tapping on the screen."
message2 = "Before starting your exam, I need to let you know about some basic instructions of exam, <break time=\"200ms\"/> "\
"If you already know the instructions you can swipe left to start your exam <break time=\"2000ms\"/>,"\
"Exam pages have one question each and by swiping left and right, you can jump between pages. <break time=\"500ms\"/>"\
"On each page, you will be played a recording reading the question for you. <break time=\"100ms\"/>, If you needed to rehear the question, just simply double tap on the page to play the recording again.<break time=\"500ms\"/>"\
"To record your answer, long tap on screen.<break time=\"1000ms\"/>, When you finished answering the question long tap on the screen again to submit your answer. <break time=\"300ms\"/>"\
"If the type of the question is multiple choices,specify your chosen option by saying choice 1, 2, 3, or 4. <break time=\"200ms\"/>"\
"When you finished your exam please swipe to last page of exam for your exam to be sent to the examiner."





ssml_string_speak = "<speak version=\"1.0\" xmlns=\"https://www.w3.org/2001/10/synthesis\" xml:lang=\"en-US\">"
ssml_string_voice = "<voice name=\"en-US-AriaNeural\">"
ssml_string_prosody = "<prosody rate=\"0.85\">"
ssml_string_break = "<break time=\"500ms\"/>"
ssml_string_prosody_end = "</prosody>"
ssml_string_voice_end = "</voice>"
ssml_string_speak_end = "</speak>"


ssml_message = ssml_string_speak + ssml_string_voice +ssml_string_prosody+message2 +ssml_string_prosody_end + ssml_string_voice_end + ssml_string_speak_end


print(ssml_message)
speech_config = SpeechConfig(subscription="2a32fa5f2c504b34bd6ba61d496fed6f",region="westeurope")
synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=None)
result = synthesizer.speak_ssml_async(ssml_message).get()
stream = AudioDataStream(result)
stream.save_to_wav_file_async("instruction2.mp3")
print("File saved")
