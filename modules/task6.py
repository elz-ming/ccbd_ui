import pandas as pd

def query_task6_data(collection):
    """Query MongoDB to retrieve data for Task 6."""
    document = collection.find_one({"file_name": "task6"})
    if not document:
        return []
    return document.get("data", [])

def create_task6_table(data):
    """Convert data for Task 6 into an HTML table."""
    if not data:
        return "<p>No data available for task-6.</p>"
    
    # Convert data to a Pandas DataFrame
    df = pd.DataFrame(data)

    # Generate HTML table
    return df.to_html(classes="table table-striped", index=False)