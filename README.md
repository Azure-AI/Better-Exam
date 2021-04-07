<p align="center"><a href="https://betterexam.herokuapp.com" target="_blank" rel="noopener noreferrer"><img width="150" src="/app/static/asset/favicon/android-chrome-192x192.png" alt="Better Exam Logo"></a></p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://forthebadge.com/images/badges/made-with-python.svg" alt="python"></a>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python version"></a>
  <a href="https://betterexam.herokuapp.com" target="_blank"><img src="https://img.shields.io/website-up-down-green-red/http/betterexam.herokuapp.com.svg" alt="website status"></a>
  <a href="https://github.com/Azure-AI/Azure-AI-Hackaton/actions/workflows/main.yml"><img src="https://github.com/Azure-AI/Azure-AI-Hackaton/actions/workflows/main.yml/badge.svg" alt="license"></a>
  <a href="https://visitor-badge.glitch.me/badge?page_id=Azure-AI.Azure-AI-Hackaton"><img src="https://visitor-badge.glitch.me/badge?page_id=Azure-AI.Azure-AI-Hackaton" alt="license"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/Azure-AI/Azure-AI-Hackaton.svg" alt="license"></a>
</p>


# ⭐️ Better Exam
Better Exam is a service that makes it easier for students who are visually impaired to take an exam. The core functionality of this service is built on Azure [Cognitive Speech Services](https://azure.microsoft.com/en-us/services/cognitive-services/speech-services/). 

Check out our demo video:

<a href="http://www.youtube.com/watch?v=9JhEJ3t6EK8"><img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white"></a>

## 💡 Motivation
With the more attention that is being paid to accessibility for all people, we thought that the traditional format for exams could be enhanced so that the people with disabilities, especially the visually impaired, can have a better experience.

Many parts of modern society and life are still not suitable for people with disabilities; education is one of them. Education is a vital part of modern life, but not everyone has an equal chance at it. Although there have been significant improvements in this regard in recent years, many gifted students don’t get the chance to realize their full potential owing to the lacking educational facilities in their area. That's why we came up with the idea of **Better Exam**.

**Better Exam** is an online web platform (soon with a Mobile Application) that lets the students take their exams by only using their **voice** and **intuitive touch screen gestures**. This application can be especially useful in times like now, when most students cannot attend their schools due to problems, such as COVID-19 pandemic, and the schools’ virtual learning systems are not prepared to handle them.

## 🚀 What it does
- **Better Exam** uses the **Text-to-Speech** and **Speech-to-Text** services from Azure Cognitive Services to both ***read the questions*** for the students and ***write their answers*** in a PDF file. 
- Students can access exams via special **links** or **QR codes** which their teachers would provide. This way, teachers can **publish an exam in a flash**.
- Teachers can use the **exam design tool** we created to design exams. Our service supports long-answer, short-answer, and multiple-choice questions right now, but more will be added in the future. At last, the system generates a link and a QR code for the exam to make publishing an exam easier for both **in-person and remote conditions**.

In details:
- The teacher enters the questions into the system.
- The exam questions are converted into a JSON file that includes the information about the exam.
- Each question’s text is sent to the Azure Text-to-Speech service from our server and the returned WAV file is stored on the server under the audio files related to this specific exam.
- A link is generated for the particular exam which should be distributed among the students.
- The students enter the exam via the generated link, speak with the platform as instructed, and state their name.
- The students are greeted with an optional tutorial on how to use the platform.
- Each question is on a separate page and students can traverse between them by swiping left and right. On each page, first, the question’s audio is played out. Then, the students can record their own answers to the question.
- The recorded voice is sent to our servers and is converted to text by using the Azure Speech-to-Text service.
- At the end of the exam, all the answers and questions are combined into one final PDF file and emailed to the teacher.

## 🔧 How we built it
### 🖼 The Big Picture:

At a high level, this system can be broken into three major sections:
- Azure
- Server
- Client

![architecture](/app/static/asset/image/arch.jpg)
### 🖥 Server:

We use Flask and Python for the server-side of our platform. Using Flask, we wrote several APIs to let our client get and post information to the server. The main function of our server-side was to execute the appropriate action in response to client requests. Our server is also where we communicate with Azure Cognitive services to generate the audio and text files. The details of how Azure services were used in our project are a follow:
* **Azure Cognitive Service - Text-to-Speech:** We used the Text-to-Speech service to send SSMLs containing each of the exam questions to Azure servers where these questions were converted into audio recordings. By using the neural voices and tinkering with the SSML, we created voice recordings really close to natural human talk. 
* **Azure Cognitive Service - Speech-to-Text:** We used a Speech-to-Text service to create text answers to each question. Students' answers, which were previously recorded, were sent to the service and the returned text was inserted into a JSON containing the exam questions.  In the end, a PDF file was generated using this JSON. We used the Continues Speech Detection function of the Speech-to-Text API so that we would not face any problem with long voice recordings.
<br/>
We also used Azure App Services and Heroku to deploy a live version of our project on the internet. Azure App Services made the deployment process super easy since we just had to give our project’s git repository to Azure App Service and everything else was done by Azure automatically. 


### 📱 Client:

We used HTML, CSS, Javascript, Jinja2, and Bootstrap to write the client-side. On the client-side, teachers can enter exam questions in specific forms. After writing all of the questions, a JSON is created containing all of these questions and is then sent over to the server for processing. Also, a link is generated for the exam and the teacher can share it with the students.<br/>

Students connect to the exam using the shared link. What the students will be interacting with is a series of pages that each has their own specific audio recordings. These audio recordings are sent over to the client-side from the server based on the page that the student is on. To interact with the pages, several simple gestures are defined that will be explained at the beginning of the exam using an audio recording. On each question page, first, the audio recording is played, then students can use the defined gestures to record their answer, and finally, the audio recording is submitted to the server-side so that it can be converted into text.<br/>

Our main focus on the client-side was to make the interaction as intuitive as possible so that students don’t get confused with complex instructions and the risk of forgetting the instructions is minimized.
<br/>

## 🧗 Challenges we ran into
One of the main challenges we faced was deciding on how we wanted to obtain the exam questions. At first, we planned on using the Azure Form Recognizer service to extract the question texts from exam papers but the variety of exam papers and the personal preferences in writing them made it so that we decided on using our own platform for writing the exam.<br/>

One other challenge was designing the client-side in a way that can be both intuitive and simple to use while keeping the possibility of mistakes when using it to a minimum. We believe the current client is pretty good but there is always room for improvements, especially after getting feedback from users.<br/>

The last challenge was using the Speech services. This was our first time working with these services and at the beginning, we had some problem finding the proper API to use and how to actually make use of the services. But the well-written documentation for the APIs and sample codes helped us a lot in solving this challenge. <br/>


## 👓 What we learned

During this project, we learned to work with Azure Cognitive Services, specially Text-to-Speech and Speech-to-Text service, which was an amazing experience. We didn't fully test the limits of these services, but from what we could see, working with them was super easy and the results were outstanding. We also honed our programming skills and knowledge during the course of the development which were all valuable experiences. 

## 🎯 What's next for Better Exam
Right now we are only supporting English in the MVP of our project. However, with the variety of supported languages by Azure Speech services and Azure Translator, the usage of the Better Exam platform can be expanded greatly.<br/>

Also, with the advancement of Azure Computer Vision and Azure Form Recognizer, we might be able to use them effectively to extract the text the exam questions from papers besides our current teacher’s client.

Better Exam is currently optimized only for desktop browsers. We plan to bring it to mobile phones in the near future


## 📚 Attribution
- Azure:
  - https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-speech-to-text?tabs=windowsinstall&pivots=programming-language-python#continuous-recognition
  - https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/python/console/speech_sample.py
  - https://github.com/Azure-Samples/cognitive-services-speech-sdk/issues/345
- Flask:
  - https://flask.palletsprojects.com/en/1.0.x/tutorial/
