from pymongo import MongoClient


class DBRepository:

    def __init__(self, table):
        client = MongoClient(
            "mongodb+srv://root:nMoiWNI9fZAvAEf2@cluster0.hif69ym.mongodb.net/?retryWrites=true&w=majority")
        db = client.get_database('Train_Bot')
        self.table = db[table]

    def insert(self, param):
        self.table.insert_one(param)

    def find(self, filter):
        return self.table.find_one(filter)

    def update(self, filter, param):
        return self.table.update_one(filter, param)

    def find_many(self, filter):
        items = self.table.find(filter)
        return list(items)


class CosmoRepository:
    def __init__(self):
        self.items = DBRepository("Solar_system")

    def findPlanet(self, name):
        planet = self.items.find({"Name": name})
        return planet

    def filterPlanet(self, filter):
        planets = self.items.find_many({"Orbits": filter})
        return planets
