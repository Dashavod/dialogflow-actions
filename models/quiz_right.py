class QuizRight:
    def __init__(self, obj):
        self.type = obj['type']
        self.variants = obj['variants']
        self.question_text = obj['question_text']
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
        print(res)
        return res
    def show_right(self,query_result):
        print(query_result)
        res = [{
            "actionLink": "https://cloud.google.com/dialogflow/docs",
            "type": "info",
            "title": "You`re right" if query_result['parameters']['correct'] else "Wrong",
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
        print(res)
        return res

    def show_multiple(self):
        res = []
        index = 1
        for variant in self.variants:
            res.append({
                "widgets": [
                    {
                        "keyValue": {
                            "content": variant['variant_value'],
                            "topLabel": index
                        }
                    }
                ]
            })
            index += 1
        print(res)
        return {
            "hangouts": {
                "header": {
                    "title": self.type,
                    "subtitle": self.question_text
                },
                "sections": res
            }
        }

    def show_right_multiple(self,query):
        res = []
        index = 1
        print(query)
        correct = 0
        for variant in self.variants:
            style = "color=\"#80e27e\"" if variant['correct'] else "color=\"#f44336\""

            if index in list(query['parameters']['number']):
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
        print(f"show_right_multiple  {int(correct)}")
        return {
            "hangouts": {
                "header": {
                    "title": self.type,
                    "subtitle": self.question_text
                },
                "sections": res
            }
        }