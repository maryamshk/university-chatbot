
import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()
intents = {"intents": [
  {"tag": "greetings",
  "patterns": ["hello","hey","hi","good day","Greetings","what's up?","how is it going?"],
  "responses": ["Hello!","Hey!","What can I do for you?"]
  },

  {"tag": "name",
  "patterns": ["what is your name","name","what's your name","who are you","what should I call you"],
  "responses": ["You can call me Ribot","I'm Ribot","I'm Ribot your virtual assistant"]
  },

  {"tag": "courses",
  "patterns": ["what courses are available", "how many courses are there in this college"],
  "responses": ["Informatics College Pokhara has been in direct partnership with London Metropolitan University, \nUK to provide enviable higher education in IT and Business to students in Pokhara.\nFor Bachelors Degree in Information Technology we have been offering the specialization in BSc (Hons) Computing.\nFor Bachelors in Business Administration we have been offering the followings:\n\n1. BBA (Marketing) with International Business \n\n2. BBA (Accounting & Finance) with International Business\n\n3. BBA (International Business)"]
  },

   {"tag": "courseDuration",
  "patterns": ["how long will be BIT or BBA course", "how long will it take to complete BIT or BBA course"],
  "responses": ["Our college offers 3 year long BIT course and 3 and half year long BBA course."]
  },

   {"tag": "Location",
  "patterns": ["location","where is it located","what is the location of the college"],
  "responses": ["Informatics College Pokhara is located in Matepani-12, pokhara near Gandaki Hospital."]
  },

  {"tag": "semesters",
  "patterns": ["how many semesters are there in a year","how many semesters one should study in a year"],
  "responses": ["There are two semesters in a year."]
  },

  {"tag": "semDuration",
  "patterns": ["how many months are there in a semester","how long will be a single semester"],
  "responses": ["The single semester will be around 4 months."]
  },

  {"tag": "studentRequirements",
  "patterns": ["what are the student requirements for admission","entry requirements","admission requirements"],
  "responses": ["Academic Level\nNEB +2 overall aggregate of 2.2 CGPA (55%) or above with each subject (theory and practical) grade D+ or above, and SEE Mathematics score of C+ ( 50%) or above.\nFor A-Levels, a minimum of 3.5 credits and atleast a grade of D and above.\n\nEnglish Proficiency\nEnglish NEB XII Marks greater or equals to 60% or 2.4 GPA\nFor Level 4 or Year 1 BIT\nPass in General Paper or English Language or IELTS 5.5 or PTE 47/ Meeting UCAS Tariff points of 80.\nFor Level 4 or Year 1 BBA\nPass in General Paper or English Language or IELTS 5.5 or PTE 47/ Meeting UCAS Tariff points of 96."]
  },

  {"tag": "classes",
  "patterns": ["how many classes will be there in a day","how long are the classes?"],
  "responses": ["There may be two or three classes per day. Each class will be of 1 hour and 30 minutes."]
  },

  {"tag": "teachingStyle",
  "patterns": ["what is the teaching style of this college?","Is the teaching pattern different from other college?","what is the teaching format?"],
  "responses": ["Our college has different teaching patterns than other colleges of Nepal. We adopt a British teaching methodology, following the LTW techniques which stands for Lecture, Tutorial and Workshop.\nYou can provide us with your contact details and our counselors shall reach out to you and provide you with further details."]
  },

  {"tag": "exams",
  "patterns": ["what are the exams like?","What is the exam pattern"],
  "responses": ["There are assignments which carry more weight than your written exams. The assignments have deadlines which you should not exceed if you want to get better marks."]
  },

  {"tag": "hours",
  "patterns": ["what are your hours","when are you guys open","what your hours of operation"],
  "responses": ["You can message us here at any hours. But our college premises will be open from 7:00 am to 5:00 pm only."]
  },

  {"tag": "funActivities",
  "patterns": ["will there be any extra curriculum activities?","does the college conducts any fun program"],
  "responses": ["Yes, Of course. Our college not only provides excellent education but also encourage students to take part in different curriculum activities. The college conducts yearly programs like Sports meet, Carnival, Holi festival, and Christmas. \n Also our college has basketball court, badminton court, table tennis, chess, carrom board and many more refreshment zones."]
  },

  {"tag": "facilities",
  "patterns": ["what facilities are provided by the college?","what are the facilities of college for students", "what are the college infrastructures "],
  "responses": ["With excellent education facilities, Our College provides various other facilities like 24 hours internet, library, classes with AC, discusson room, canteen, parking space, and student service for any students queries."]
  },

  {"tag": "fee",
  "patterns": ["how much is the college fee","what is the fee structure"],
  "responses": ["Course BIT\nAdmission fee=RS 96,000\nYear 1\nUniversity and Exam fee= RS 100,000 Each semester fee=RS 69,000 Total fee= RS 334,000\nYear 2\nUniversity and Exam fee= RS 100,000 Each semester fee=RS 69,000 Total fee= RS 238,000\nYear 3\nUniversity and Exam fee= RS 100,000 Each semester fee=RS 69,000 Total fee= RS 238,000\nGrandTotal fee= RS 810,000\n\nCourse BBA\nAdmission fee=RS 96,000\nYear 1\nUniversity and Exam fee= RS 100,000 Each semester fee=RS 52,000 Total fee= RS 300,000\nYear 2\nUniversity and Exam fee= RS 100,000 Each semester fee=RS 52,000 Total fee= RS 204,000\nYear 3\nUniversity and Exam fee= RS 100,000 Each semester fee=RS 52,000 Total fee= RS 204,000\nYear 4\nUniversity and Exam fee= RS 50,000 Semester fee=RS 52,000 Total fee= RS 102,000\nGrandTotal fee= RS 810,000"]
  },

  {"tag": "goodbye",
  "patterns": ["cya","See you later","Goodbye","I am leaving","Have a Good Day","bye","see ya"],
  "responses": ["Sad to see you go :(","Talk you later","Goodbye"]
  },

  {"tag": "invalid",
    "patterns": ["","gvsd","asbhk"],
    "responses": ["Sorry, can't understand you", "Please give me more info", "Not sure I understand"]
  },

  {"tag": "thanks",
    "patterns": ["Thanks", "Thank you", "That's helpful", "Awesome, thanks", "Thanks for helping me"],
    "responses": ["Happy to help!", "Any time!", "My pleasure"]
  }
]}

words = []
classes = []
documents = []
ignore_letters = ['?', '!',',','.']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list,intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

classes = sorted(set(classes))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

training = []
output_empty = [0] * len(classes)

for document in documents:
    bag =[]
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training)

train_x = list(training[:, 0])
train_y = list(training[:, 1])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('chatbotmodel.h5', hist)

print('Done')