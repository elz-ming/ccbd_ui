import io
import base64
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def query_task3_data(collection):
    """Query MongoDB to retrieve data for Task 3."""
    document = collection.find_one(
        {"file_name": "task3"})  # Query by file_name
    if not document:
        return None
    return document["data"]  # Return the 'data' field


def create_task3_chart(data):
    """Generate a bar chart for Task 3 using Matplotlib."""
    if not data:
        raise ValueError("Data for Task 3 is empty or None")

    # Extract country names and counts
    countries = [item["country"] for item in data]
    counts = [item["count"] for item in data]

    # Generate the bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(countries, counts, color="skyblue")
    plt.title("Task 3: Count by Country")
    plt.xlabel("Country")
    plt.ylabel("Count")
    plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
    plt.tight_layout()

    # Save chart to Base64
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    chart_base64 = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return f"data:image/png;base64,{chart_base64}"
