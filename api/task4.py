import io
import base64
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')


def query_task4_data(collection):
    """Query MongoDB to retrieve data for section-4."""
    document = collection.find_one(
        {"file_name": "task4"})  # Query by file_name
    if not document:
        return []
    return document.get("data", [])


def create_task4_chart(data):
    """Generate a bar chart for section-4 using Matplotlib."""
    if not data:
        return None

    # Extract data
    channels = [item["_channel"] for item in data]
    mean_trust_scores = [item["mean_trust_score"] for item in data]

    # Create the chart
    plt.figure(figsize=(10, 6))
    plt.bar(channels, mean_trust_scores, color="skyblue")
    plt.title("Mean Trust Score by Channel")
    plt.xlabel("Channel")
    plt.ylabel("Mean Trust Score")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Save the chart to a Base64 string
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    chart_base64 = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return f"data:image/png;base64,{chart_base64}"
