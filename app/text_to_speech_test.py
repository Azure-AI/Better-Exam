from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig



speech_config = SpeechConfig(subscription="2a32fa5f2c504b34bd6ba61d496fed6f",region="westeurope")
synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=None)

message ="Hello, I am BEAM, your personal exam assistant and I will be guiding you through your exam. Please first tell me your name by long tapping on the screen until you hear a beep sound. long tap on the screen again when you finished saying your name. You will hear a beep sound again and I will guide you to the next page."
message2 = "Before starting your exam, I need to let you know about some basic instructions of exam, "\
"If you already know the instructions you can swipe left to start your exam........,"\
"Exam pages have one question each and by swiping left and right you can jump between pages........,"\
"On each page you will be played a recording reading the question for you. If you needed to rehear the question, just simply double tap on the page to play the recording again.,"\
"To record your answer, long tap on screen until you hear a beep sound, you can then speak your answer. When you finished answering the question long tap on the screen again to submit your answer.,"\
"If the type of the question is multiple choices, please just say the right letter as your answer.,"\
"When you finished your exam please swipe to last page of exam for your exam to be sent to the examiner."

result = synthesizer.speak_text_async(message2).get()
stream = AudioDataStream(result)
stream.save_to_wav_file("app/static/asset/audio/second.wav")