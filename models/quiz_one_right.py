class QuizOneRight:
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
                        "answear": variant['variant_value'],
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
