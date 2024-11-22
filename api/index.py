from flask import Flask, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import task1
import task4

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI)
db = client["project2"]
collection = db["output"]

app = Flask(__name__, template_folder="../templates",
            static_folder='../static')


@app.route('/')
def home():

    task1_data = task1.query_task1_data(collection)
    task1_chart = task1.create_task1_chart(task1_data)

    task4_data = task4.query_task4_data(collection)
    task4_chart = task4.create_task4_chart(task4_data)

    # Pass data and chart to the template
    return render_template(
        "home.html",
        task1_chart=task1_chart,
        task4_chart=task4_chart,
    )


if __name__ == '__main__':
    app.run()
