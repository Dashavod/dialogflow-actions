import json

from DbRepo import CosmoRepository


class Service:
    def __init__(self):
        self.cosmo = CosmoRepository()

    def TestCard(self, query_result):

        return [
            {
                "payload": {
                    "richContent": [
                        {
                            "accessibilityText": "Dialogflow across platforms",
                            "rawUrl": "https://images.cnbctv18.com/wp-content/uploads/2018/05/10.jpg",
                            "type": "image"
                        },
                        {
                            "type": "info",
                            "subtitle": "Build natural and rich conversational experiences",
                            "title": "Dialogflow",
                            "actionLink": "https://cloud.google.com/dialogflow/docs"
                        },
                        {
                            "event": {
                                "parameters": {},
                                "languageCode": "en",
                                "name": "Event_cosmo"
                            },
                            "type": "button",
                            "text": "Radius",
                            "icon": {
                                "type": "explore",
                                "color": "#c67bff"
                            }
                        },
                        {
                            "icon": {
                                "color": "#c67bff",
                                "type": "cached"
                            },
                            "event": {
                                "parameters": {},
                                "languageCode": "en",
                                "name": "Event_orbit"
                            },
                            "text": "Orbit",
                            "type": "button"
                        },
                        {
                            "event": {
                                "languageCode": "en",
                                "parameters": {},
                                "name": "Event_info"
                            },
                            "text": "Info",
                            "icon": {
                                "color": "#c67bff",
                                "type": "info"
                            },
                            "type": "button"
                        },
                        {
                            "event": {
                                "languageCode": "en",
                                "parameters": {},
                                "name": "Event_comparsion"
                            },
                            "text": "Comparsion",
                            "icon": {
                                "color": "#c67bff",
                                "type": "thumbs_up_down"
                            },
                            "type": "button"
                        }
                    ]
                }
            }
        ]

    def OrbitPlanet(self, query_result):
        item = query_result.get('parameters')
        planet = item.get('planet')
        res = self.cosmo.filterPlanet(planet)
        names = []
        text = ''
        for i in res:
            names.append({'name': i['Name'], 'number_rome': i['Number'], 'number': romanToInt(i['Number'])})
        names.sort(key=lambda x: x.get('number'))
        orbits = []
        for i in names: orbits.append(f" {i['number_rome']} {i['name']},\n")
        res = {
            "type": "description",
            "title": f'in orbit {planet}',
            "text": orbits
        }
        return [
            {
                "payload": {
                    "richContent": [
                        res
                    ]
                }
            }
        ]

    def InfoPlanet(self, query_result):
        item = query_result.get('parameters')
        planet = item.get('planet')
        generalInfo = self.cosmo.findPlanet(planet)
        res = self.cosmo.filterPlanet(planet)
        names = []
        for i in res:
            names.append({'name': i['Name'], 'number_rome': i['Number'], 'number': romanToInt(i['Number'])})
        names.sort(key=lambda x: x.get('number'))
        text = [f"Orbit: {generalInfo['Orbits']}",
                f"Number in orbit:{generalInfo['Number']}",
                f"Radius: {generalInfo['Distance']}000km",
                f"Period: {generalInfo['O_Period']} days",
                f"Incl:{generalInfo['Incl']}",
                f"Eccen:{generalInfo['Eccen']}",
                f"Discoverer:{generalInfo['Discoverer']}",
                f"Date: {generalInfo['Date']}",
                f"Pseudonym:{generalInfo['AKA']}"]
        orbits = []
        for i in names: orbits.append(f" {i['number_rome']} {i['name']}")
        res = {
            "type": "description",
            "title": f"On orbit{generalInfo['Name']}:",
            "text": text
        }
        orb = {
            "type": "description",
            "title": f"on orbit {generalInfo['Name']}:",
            "text": orbits
        }
        return [
            {
                "payload": {
                    "richContent": [
                        res,
                        orb
                    ]
                }
            }
        ]

    def RadiusPlanet(self, query_result):
        item = query_result.get('parameters')
        planet = item.get('planet')
        res = self.cosmo.findPlanet(planet)
        title = query_result.get('queryText')
        text = [f"Radius of {planet} is", f"{res['Distance']}000km"]
        res = {
            "type": "description",
            "title": title,
            "text": text
        }

        return [
            {
                "payload": {
                    "richContent": [
                        res
                    ]
                }
            }
        ]

    def ComparsionPlanet(self, query_result):

        item = query_result.get('parameters')
        first_operand = item.get('first_operand')
        second_operand = item.get('second_operand')

        firstInfo = self.cosmo.findPlanet(first_operand[0])
        secondInfo = self.cosmo.findPlanet(second_operand[0])

        if (abs(float(firstInfo['O_Period'])) > abs(float(secondInfo['O_Period']))):
            title = f"{first_operand[0]} greater then {second_operand[0]}"
        else:
            title = f"{second_operand[0]} greater then {first_operand[0]}"

        text = [f"{first_operand[0]} have {firstInfo['O_Period']} days",
                f" {second_operand[0]} have {secondInfo['O_Period']} days"]

        res = {
            "type": "description",
            "title": title,
            "text": text
        }
        return [
            {
                "payload": {
                    "richContent": [
                        res
                    ]
                }
            }
        ]

    def OpenDialogOneAnswear(self, query_result):
        return [
            {
                "card": {
                    "title": "title",
                    "subtitle": "subtitle google chat",
                    "imageUri": "https://c.tadst.com/gfx/1200x630/sunrise.png?1",
                    "buttons": [
                        {
                            "text": "fg",
                            "postback": "https://help.obsidian.md/How+to/Format+your+notes"
                        }
                    ]
                },
                "platform": "GOOGLE_HANGOUTS"
            },
            {
                "payload": {
                    "richContent": [
                        [
                            {
                                "type": "info",
                                "actionLink": "https://example.com",
                                "title": "Info item title",
                                "subtitle": "Info item subtitle",
                                "image": {
                                    "src": {
                                        "rawUrl": "https://example.com/images/logo.png"
                                    }
                                }
                            }
                        ]
                    ]
                }
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
