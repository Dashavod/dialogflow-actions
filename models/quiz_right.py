class QuizRight:
    def __init__(self, obj):
        self.type = obj['type']
        self.variants = obj.get('variants') or []
        self.question_text = obj['question_text']
        self.user_input = obj.get('correct_input') or ''
    def uncheked_show(self):
        res = [{
            "actionLink": "https://cloud.google.com/dialogflow/docs",
            "type": "info",
            "title": self.type,
            "subtitle": self.question_text
        }, ]
        for variant in self.variants:
            res.append({
                "text": variant['variant_value'],
                "type": "button",
                "icon": {
                    "type": "check_box_outline_blank",
                    "color": "#c67bff"
                },
                "event": {
                    "name": "Event_answer",
                    "languageCode": "en",
                    "parameters": {
                        "answer": variant['variant_value'],
                        "correct": variant['correct'],
                    }
                }})
        return res
    def show_right(self,query_result):
        res = [{
            "actionLink": "https://cloud.google.com/dialogflow/docs",
            "type": "info",
            "title": "You`re right" if query_result else "Wrong",
            "subtitle": self.question_text
        }, ]
        for variant in self.variants:
            res.append({
                "text": variant['variant_value'],
                "type": "button",
                "icon": {
                    "type": "check_box" if variant['correct'] else "check_box_outline_blank ",
                    "color": "#c67bff"
                }})
        return res
    def show_user_input(self):
        return {
            "hangouts": {
                "header": {
                    "title": self.type,
                    "subtitle": self.question_text
                }
            }
        }
    def display_question(self):
        response = ''
        match self.type:
            case 'one_right':
                response = self.show_multiple(),
            case 'multiple_right':
                response = self.show_multiple(),
            case 'user_input':
                response = [self.show_user_input()]
                print(response)

        return dict(response[0])
    def show_multiple(self):
        res = []
        index = 1
        for variant in self.variants:
            res.append({
                "widgets": [
                    {
                        "keyValue": {
                            "content": variant['variant_value'],
                            "topLabel": str(index)
                        }
                    }
                ]
            })
            index += 1
        return {
            "hangouts": {
                "header": {
                    "title": self.type,
                    "subtitle": self.question_text
                },
                "sections": res
            }
        }
    def correct_multiple(self,query):
        correct = 0
        index = 1
        for variant in self.variants:
            if index in list(query):
                correct = correct + 1 if variant['correct'] else correct
            index = index + 1
        return correct
    def show_right_multiple(self,query):
        res = []
        index = 1
        correct = 0
        for variant in self.variants:
            style = "color=\"#80e27e\"" if variant['correct'] else "color=\"#f44336\""

            if index in list(query):
                correct = correct + 1 if variant['correct'] else correct
                res.append({
                    "widgets": [
                        {
                            "keyValue": {
                                "icon": "HOTEL_ROOM_TYPE",
                                "content": f"<font {style}>{variant['variant_value']}</font>",
                                "topLabel": str(index)
                            }
                        }
                    ]
                })
            else:
                res.append({
                    "widgets": [
                        {
                            "keyValue": {
                                "content": f"<font {style}>{variant['variant_value']}</font>",
                                "topLabel": str(index)
                            }
                        }
                    ]
                })

            index = index + 1
        res.insert(0, {
            "widgets": [
                {
                    "keyValue": {
                        "content": str(correct),
                        "topLabel": "quantity correct answer"
                    }
                }
            ]
        })
        return {
            "hangouts": {
                "header": {
                    "title": self.type,
                    "subtitle": self.question_text
                },
                "sections": res
            }
        }
    def input_correct(self,query):
        return True if self.user_input == query else False
    def show_input_multiple(self,query):

        print(self)
        if self.user_input == query:
            correct = f"Your answer is correct {self.user_input} "
        else:
            correct = f"Your answer isn`t correct( \n Correct answer is {self.user_input} "
        return {
            "hangouts": {
                "header": {
                    "title": self.question_text,
                    "subtitle": correct
                }
            }
        }