import json

from DbRepo import CosmoRepository, DBRepository
from models.quiz_right import QuizRight


class Service:
    def __init__(self):
        self.cosmo = CosmoRepository()
        self.db = DBRepository()
        self.questions = []
        self.quantity_correct = 0
    def  BenefitSportInfo(self,query_result):
        return [
            {
                "platform": "GOOGLE_HANGOUTS",
                "payload": {
                    "hangouts": {
                        "header": {
                            "title": "Sport category",
                            "subtitle": f"{query_result['parameters']['benefits-sport']}"
                        },
                        "sections": [
                            {
                                "widgets": [
                                    {
                                        "textParagraph": {
                                            "text":"<b>Compensation of sports expenses (swimming pool, yoga, dancing, etc.)</b>\n\n 700 UAH per month The presence of payment receipt and document proving attendance of training lessons at least 4 times per month is required"
                                        }
                                    },

                                ]
                            }
                        ]
                    }
                },

            }
        ]

    def  BenefitGeneralInfo(self):
        return [
            {
                "platform": "GOOGLE_HANGOUTS",
                "payload": {
                    "hangouts": {
                        "header": {
                            "title": "What are the company benefits?",
                            "subtitle": "General Info"
                        },
                        "sections": [
                            {
                                "widgets": [
                                    {
                                        "textParagraph": {
                                            "text":"Devtorium cares about its people in various activities and important life events."
                                        }
                                    },
                                    {
                                        "textParagraph": {
                                            "text": "All benefits, except daily lunch refunds and English classes in the company's office,can be used after the <b>successful passing of the probation period</b>. "
                                        }
                                    },
                                    {
                                        "textParagraph": {
                                            "text": "Before having compensation, you should address to your <b>Canton Representative</b>,and announce that you had some recoverable costs and verify them in the agreed way (payment receipt, etc.).\n The compensation for expended money is added to the wage\n\n"
                                        }
                                    },
                                    {
                                        "keyValue": {
                                            "icon": "HOTEL_ROOM_TYPE",
                                            "content": " ",
                                            "topLabel": "Enter your question"
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                },

            }
        ]

    def OpenDialogOneAnswer(self, query_result):
        item = self.db.find({"type": "one_right"})
        print(item)
        card = QuizRight(item)
        return [{"payload": {
            "richContent": [
                card.uncheked_show()
            ]
        }
        }
        ]

    def OneAnswer(self, query_result):
        item = self.db.find({"type": "one_right"})
        print(item)
        card = QuizRight(item)
        return [{"payload": {
            "richContent": [
                card.show_right(query_result['parameters']['correct'])
            ]
        }
        }
        ]
    def UnknownAnswer(self, query_result):
        username = query_result['originalDetectIntentRequest']['payload']['data']['event']['user']['displayName']
        user_question = query_result["queryResult"]["queryText"]
        self.db.insert({"question": user_question,
                        "username": username,
                        "response": False})
        return [
            {
                "text": {
                    "text": [
                        "I don't know the answer to this question yet, but I will remember it"
                    ]

                }
            }
        ]
    def MultipleAnswer(self, query_result):
        item = self.db.find({"type": "multiple_right"})
        print(item)
        card = QuizRight(item)
        return [
            {
                "payload": card.show_multiple(),
                "platform": "GOOGLE_HANGOUTS"
            }
        ]

    def ShowMultipleAnswer(self, query_result, index):
        print(f"answer index {index}")
        card = QuizRight(self.questions[int(index - 1)])
        self.quantity_correct += card.correct_multiple(query_result['parameters']['number'])
        print(f"quantity_correct  {self.quantity_correct}")
        return [
            {
                "payload": card.show_right_multiple(query_result['parameters']['number']),
                "platform": "GOOGLE_HANGOUTS"
            }
        ]

    def ShowInputAnswer(self, query_result, index):
        print(f"answer index {index}")
        card = QuizRight(self.questions[int(index - 1)])
        self.quantity_correct += card.input_correct(query_result['parameters']['user-input'])
        print(f"quantity_correct  {self.quantity_correct}")
        return [
            {
                "payload": card.show_input_multiple(query_result['parameters']['user-input']),
                "platform": "GOOGLE_HANGOUTS"
            }
        ]

    def DisplayQuestion(self, query_result):
        self.questions = self.db.find_many({})

        # random.choices(list, k=3)
        index = query_result['parameters']['number_of_question']
        print(f"question  {self.questions[int(index - 1)]}")
        card = QuizRight(self.questions[int(index - 1)])

        return [
            {
                "payload": card.display_question(),
                "platform": "GOOGLE_HANGOUTS"
            }
        ]


def romanToInt(s):
    """
    :type s: str
    :rtype: int
    """
    roman = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000, 'IV': 4, 'IX': 9, 'XL': 40, 'XC': 90,
             'CD': 400, 'CM': 900}
    i = 0
    num = 0
    while i < len(s):
        if i + 1 < len(s) and s[i:i + 2] in roman:
            num += roman[s[i:i + 2]]
            i += 2
        else:
            # print(i)
            num += roman[s[i]]
            i += 1
    return num
