from flask import Flask, render_template
from pymongo import MongoClient
import matplotlib.pyplot as plt
import io
import base64
from dotenv import load_dotenv
import os
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

app = Flask(__name__)

# MongoDB connection
client = MongoClient(MONGODB_URI)
db = client["project2"]
collection = db['output']


@app.route('/')
def home():
    # Fetch a single document (e.g., by file_name or just the first document)
    document = collection.find_one({"file_name": "task4"})
    if not document:
        return "No data found in the database!"

    # Extract data from the document
    data = document["data"]

    # Generate chart
    chart_url = create_chart(data)

    return render_template("home.html", chart_url=chart_url)


def create_chart(data):
    # Extract columns from the data
    channels = [row["_channel"] for row in data]
    mean_trust = [row["mean_trust_score"] for row in data]

    # Create the chart
    plt.figure(figsize=(10, 6))
    plt.bar(channels, mean_trust, color="skyblue")
    plt.title("Mean Trust by Channel")
    plt.xlabel("Channel")
    plt.ylabel("Mean Trust")
    plt.xticks(rotation=45, ha="right")

    # Save the chart to a base64-encoded string
    img = io.BytesIO()
    plt.savefig(img, format="png", bbox_inches="tight")
    img.seek(0)
    chart_base64 = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return f"data:image/png;base64,{chart_base64}"


if __name__ == '__main__':
    app.run(debug=True)
