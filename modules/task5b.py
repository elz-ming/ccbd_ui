import io
import base64
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

matplotlib.use('Agg')  # Use a non-interactive backend

def query_task5b_data(collection):
    """Query MongoDB to retrieve data for task-5."""
    document = collection.find_one({"file_name": "task5b"})  # Query by file_name
    if not document:
        return [], None  # Return empty list and None if document is not found
    return document.get("data", []), document.get("accuracy")  # Return data and accuracy


def create_task5b_chart(data):
    """Generate a bar chart for task-5 using Matplotlib."""
    if not data:
        return None

    # Extract sentiment distribution
    sentiments = [item["airline_sentiment_gold"] for item in data]
    sentiment_counts = pd.Series(sentiments).value_counts()

    # Create the chart
    plt.figure(figsize=(8, 5))
    sentiment_counts.plot(kind="bar", color="skyblue")
    plt.title("Sentiment Distribution")
    plt.xlabel("Sentiment")
    plt.ylabel("Count")
    plt.xticks(rotation=0)
    plt.tight_layout()

    # Save the chart to a Base64 string
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    chart_base64 = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return f"data:image/png;base64,{chart_base64}"