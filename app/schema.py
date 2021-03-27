# Define JSOn Schemas Here

# Example for an exam JSON that matches wih the EXAM_SCHEMA
# {
#   "exam":{
#     "questions":[
#       {
#         "number":"1",
#         "type":"MC",
#         "text":"What is 2+2",
#         "choices":[
#           {
#             "letter":"A",
#             "text":"1"
#           },
#           {
#             "letter":"B",
#             "text":"4"
#           }
#           ],
#         "answer":null
#       },
#       {
#         "number":"2",
#         "type":"ES",
#         "text":"What is Cloud Computing?",
#         "answer":null
#       }
#       ]
#   }
# }
EXAM_SCHEMA = {
    "type": "object",
    "properties": {
        "exam": {
            "description": "Exam object",
            "type": "object",
            "properties": {
                "questions": {
                    "description": "Questions in the exam",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "number": {},
                            "type": {},
                            "text": {},
                            "choices": {},
                            "answer": {}
                        },
                        "required": ["number", "type", "text", "answer"]
                    }
                }
            },
            "required": ["questions"]
        }
    },
    "required": ["exam"]
}

ANSWER_SCHEMA = {
    "type": "object",
    "properties": {
        "number": {
            "description": "Question Number",
            "type": "string",
        },
        "type": {
            "description": "Question Type --> ES:essay, MC:multiple choice",
            "type": "string"
        }
    },
    "required": ["number", "type"]
}