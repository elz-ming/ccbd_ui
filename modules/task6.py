import pandas as pd

def query_task6_data(collection):
    """Query MongoDB to retrieve data for Task 6."""
    document = collection.find_one({"file_name": "task6"})
    if not document:
        return []
    return document.get("data", [])