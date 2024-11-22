from flask import Flask, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import io
import base64
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI)
db = client["project2"]
collection = db["output"]

app = Flask(__name__, template_folder="../templates",
            static_folder='../static')


@app.route('/')
def home():
    task1_data = query_task1_data(collection)
    task1_chart = create_task1_chart(task1_data)

    task2_data = query_task2_data(collection)
    task2_chart = create_task2_chart(task2_data)

    task4_data = query_task4_data(collection)
    task4_chart = create_task4_chart(task4_data)

    # Pass data and chart to the template
    return render_template(
        "home.html",
        task1_chart=task1_chart,
        task2_chart=task2_chart,
        task4_chart=task4_chart,
    )


def query_task1_data(collection):
    """Query MongoDB to retrieve data for task1."""
    document = collection.find_one(
        {"file_name": "task1"})  # Query by file_name
    if not document:
        return None
    return document  # Return the full document for Task 1


def create_task1_chart(task1_data):
    """Generate a bar chart for Task 1 using Matplotlib."""
    if not task1_data:
        return None

    # Extract airline and airport data
    airlines = task1_data["airlines"]
    airports = task1_data["airports"]

    # Generate separate charts for airlines and airports
    airline_labels = [item["airline"] for item in airlines]
    airline_counts = [item["count"] for item in airlines]

    airport_labels = [item["airport"] for item in airports]
    airport_counts = [item["count"] for item in airports]

    # Plot airlines chart
    plt.figure(figsize=(10, 6))
    plt.bar(airline_labels, airline_counts, color="skyblue")
    plt.title("Task 1: Airline Delays")
    plt.xlabel("Airline")
    plt.ylabel("Delay Count")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Save airline chart to Base64 string
    airline_img = io.BytesIO()
    plt.savefig(airline_img, format="png")
    airline_img.seek(0)
    airline_chart_base64 = base64.b64encode(airline_img.getvalue()).decode()
    plt.close()

    # Plot airports chart
    plt.figure(figsize=(8, 5))
    plt.bar(airport_labels, airport_counts, color="lightgreen")
    plt.title("Task 1: Airport Delays")
    plt.xlabel("Airport")
    plt.ylabel("Delay Count")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Save airport chart to Base64 string
    airport_img = io.BytesIO()
    plt.savefig(airport_img, format="png")
    airport_img.seek(0)
    airport_chart_base64 = base64.b64encode(airport_img.getvalue()).decode()
    plt.close()

    return {
        "airline_chart": f"data:image/png;base64,{airline_chart_base64}",
        "airport_chart": f"data:image/png;base64,{airport_chart_base64}"
    }


def query_task2_data(collection):
    """Query MongoDB to retrieve data for Task 2."""
    document = collection.find_one(
        {"file_name": "task2"})  # Query by file_name
    if not document:
        return None
    return document["data"]


def create_task2_chart(data):
    """Generate a grouped bar chart for Task 2 using Matplotlib."""
    if not data:
        return None

    # Group data by airline
    airlines = {}
    for row in data:
        airline = row["airline"]
        negativereason = row["negativereason"]
        count = row["count"]

        if airline not in airlines:
            airlines[airline] = {}
        airlines[airline][negativereason] = count

    # Prepare chart data
    categories = list(set(reason for reasons in airlines.values()
                      for reason in reasons.keys()))
    airlines_sorted = sorted(airlines.keys())
    chart_data = {reason: [airlines[airline].get(
        reason, 0) for airline in airlines_sorted] for reason in categories}

    # Generate grouped bar chart
    x = range(len(airlines_sorted))
    bar_width = 0.1
    plt.figure(figsize=(12, 6))
    for i, (reason, counts) in enumerate(chart_data.items()):
        plt.bar([pos + i * bar_width for pos in x],
                counts, width=bar_width, label=reason)

    # Chart formatting
    plt.title("Negative Reasons per Airline")
    plt.xlabel("Airlines")
    plt.ylabel("Count")
    plt.xticks([pos + (len(categories) - 1) * bar_width /
               2 for pos in x], airlines_sorted, rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()

    # Save chart to Base64
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    chart_base64 = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return f"data:image/png;base64,{chart_base64}"
  
  
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


if __name__ == '__main__':
    app.run()
