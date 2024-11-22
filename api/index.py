from flask import Flask, render_template
from pymongo import MongoClient
import matplotlib.pyplot as plt
import io
import base64
from dotenv import load_dotenv
import os
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI)
db = client["project2"]
collection = db["output"]

app = Flask(__name__, template_folder="../templates",
            static_folder='../static')


@app.route('/')
def home():
    # Query data for section-4
    section_4_data = query_section_4_data()
    section_4_chart = create_section_4_chart(section_4_data)

    # Pass data and chart to the template
    return render_template(
        "home.html",
        title="Cloud Computing P1 Group 3",
        section_4_chart=section_4_chart,
    )


def query_section_4_data():
    """Query MongoDB to retrieve data for section-4."""
    document = collection.find_one(
        {"file_name": "task4"})  # Query by file_name
    if not document:
        return []
    return document.get("data", [])


def create_section_4_chart(data):
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
