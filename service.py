from DbRepo import CosmoRepository

class Service:
    def __init__(self):
        self.cosmo = CosmoRepository()

    def OrbitPlanet(self, query_result):
        item = query_result.get('parameters')
        planet = item.get('planet')
        res = self.cosmo.filterPlanet(planet)
        names = []
        text = 'in orbit {planet}'
        for i in res:
            names.append({'name': i['Name'], 'number_rome': i['Number'], 'number': romanToInt(i['Number'])})
        names.sort(key=lambda x: x.get('number'))

        for i in names: text = f" {text} - {i['number_rome']} {i['name']},\n"
        return text

    def InfoPlanet(self, query_result):
        item = query_result.get('parameters')
        planet = item.get('planet')
        generalInfo = self.cosmo.findPlanet(planet)
        res = self.cosmo.filterPlanet(planet)
        names = []
        for i in res:
            names.append({'name': i['Name'], 'number_rome': i['Number'], 'number': romanToInt(i['Number'])})
        names.sort(key=lambda x: x.get('number'))
        text = f"{generalInfo['Name']}:\nOrbit: {generalInfo['Orbits']} \nNumber in orbit:{generalInfo['Number']}\n Radius: {generalInfo['Distance']}000km \nPeriod: {generalInfo['O_Period']} days \nIncl:{generalInfo['Incl']}\nEccen:{generalInfo['Eccen']}\nDiscoverer:{generalInfo['Discoverer']}\nDate: {generalInfo['Date']} \nPseudonym:{generalInfo['AKA']}\nOn orbit {planet}:"

        for i in names: text = f" {text} - {i['number_rome']} {i['name']},\n"
        return text

    def RadiusPlanet(self, query_result):
        item = query_result.get('parameters')
        planet = item.get('planet')
        res = self.cosmo.findPlanet(planet)
        text = f"Radius of {planet} is {res['Distance']}000km"
        return text

    def ComparsionPlanet(self, query_result):
        item = query_result.get('parameters')
        first_operand = item.get('first_operand')
        second_operand = item.get('second_operand')
        print(f'{first_operand[0]} + {second_operand[0]}')
        firstInfo = self.cosmo.findPlanet(first_operand[0])
        secondInfo = self.cosmo.findPlanet(second_operand[0])
        if (abs(float(firstInfo['O_Period'])) > abs(float(secondInfo['O_Period']))):
            text=f"{first_operand[0]} greater then {second_operand[0]}"
        else:
            text=f"{second_operand[0]} greater then {first_operand[0]}"

        text=f"{text} \n {first_operand[0]} have {firstInfo['O_Period']} days\n {second_operand[0]} have {secondInfo['O_Period']} days\n "

        return text





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