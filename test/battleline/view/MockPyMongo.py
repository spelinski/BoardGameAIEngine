listOfDatabases = []


class MockMongoClient(object):

    def __init__(self, host, port):
        pass

    def __getitem__(self, database_name):
        for instance in listOfDatabases:
            if instance.name == database_name:
                return instance
        newDatabase = MockDatabase(database_name)
        listOfDatabases.append(newDatabase)
        return newDatabase

    def drop_database(self, database_name):
        pass


class MockDatabase(object):

    def __init__(self, database_name):
        self.name = database_name
        self.collection_name_list = [""]
        self.games = MockGameCollection()

    def collection_names(self, include_system_collections):
        return self.collection_name_list

    def create_collection(self, collection_name, capped=False, size=0, max=0):
        self.collection_name_list = [collection_name]


class MockGameCollection(object):

    def __init__(self):
        self.my_GameEntry = ""

    def insert_one(self, entry_info):
        self.my_GameEntry = MockGameEntry(entry_info)
        return self.my_GameEntry

    def update(self, id_json, update_json):
        self.my_GameEntry.update(update_json)

    def find(self, id_json):
        return self.my_GameEntry


class MockGameEntry(object):

    def __init__(self, init_json):
        self.inserted_id = 1
        self.entry_info = init_json

    def next(self):
        return self.entry_info

    def update(self, update_json):
        for name in update_json:
            if name == "$push":
                for realName in update_json[name]:
                    self.entry_info[realName] = [update_json[name][realName]]
            elif name == "$set":
                for realName in update_json[name]:
                    self.entry_info[realName] = update_json[name][realName]
            else:
                self.entry_info[name] = update_json[name]
