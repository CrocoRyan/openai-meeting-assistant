from datetime import datetime

import pymongo


class AssistantDBManager:
    def __init__(self, connection_string):
        # Establishing connections and initializing collections
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client["assistant_db"]
        self.assistants_collection = self.db["user_history"]

        # Check if the wildcard index already exists
        index_exists = any(
            index.get('key', {}).get('$**') == 1 for index in self.assistants_collection.list_indexes()
        )

        # Create the wildcard index if it does not exist
        if not index_exists:
            self.assistants_collection.create_index([("$**", 1)])
            print("Created wildcard index.")
        else:
            print("Wildcard index already exists.")

    def check_user_exists(self, user_id):
        # Check if user exists in the assistants collection
        user = self.assistants_collection.find_one({"userID": user_id})
        return user is not None

    def get_user_latest_index(self, user_id):
        # Retrieve user data based on user ID from the assistants collection
        result_cursor = self.assistants_collection.find({"userID": user_id}, {'innerIndex': 1}).sort(
            [("innerIndex", -1)]).limit(1)
        latest_index = next(result_cursor, None)

        if latest_index is None:
            return -1
        else:
            return latest_index['innerIndex']

    def insert_data(self, user_id, thread_id, time_stamp):
        # Insert new data into the assistants collection
        time_stamp = datetime.fromtimestamp(time_stamp)
        # index=self.get_user_latest_index(user_id)+1
        index = self.get_user_latest_index(user_id) + 1
        new_data = {
            "userID": user_id,
            "threadID": thread_id,
            "createdTime": time_stamp,
            "innerIndex": index,
            "summary": None
        }
        self.assistants_collection.insert_one(new_data)
        return new_data

    def get_user_snapshots(self, user_id):
        # Retrieve user data based on user ID from the assistants collection
        result = self.assistants_collection.find({"userID": user_id},
                                                 {'innerIndex': 1, 'createdTime': 1, 'threadID': 1})
        # .sort([("innerIndex", -1)])
        return result if result.count() > 0 else None

    def get_doc_by_thread(self, thread_id):
        return self.assistants_collection.find_one({"threadID": thread_id})

    def get_user_data(self, user_id):
        # Retrieve user data based on user ID from the assistants collection
        user_data = self.assistants_collection.find_one({"userID": user_id})
        return user_data

    def append_message(self, user_id, thread_id, message, message_type):
        # Find the document for the user
        user_doc = self.assistants_collection.find_one({"userID": user_id, "threadID": thread_id})
        timestamp = datetime.utcnow()

        if user_doc:
            # Depending on the command type, append the command to the unified list
            if message_type == "user":
                self.assistants_collection.update_one(
                    {"_id": user_doc["_id"]},
                    {
                        "$push": {
                            "messages": {
                                "type": "user",
                                "content": message,
                                "timestamp": timestamp,
                            }
                        }
                    },
                )
            elif message_type == "assistant_response":
                self.assistants_collection.update_one(
                    {"_id": user_doc["_id"]},
                    {
                        "$push": {
                            "messages": {
                                "type": "assistant",
                                "content": message,
                                "timestamp": timestamp,
                            }
                        }
                    },
                )
            return True
        else:
            # If the user document is not found, return False
            return False

# if __name__ == '__main__':
#     as1= AssistantDBManager(connection_string="mongodb://localhost:27017")
#     print(as1.get_doc_by_thread('thread_BUtgC0pS7hlLyypkYi7qZ7tO1'))
