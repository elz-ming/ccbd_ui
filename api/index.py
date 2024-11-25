import sys
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from flask import Flask, render_template

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.task1 import query_task1_data, create_task1_chart
from modules.task2 import query_task2_data, create_task2_chart
from modules.task3 import query_task3_data, create_task3_chart
from modules.task4 import query_task4_data, create_task4_chart
from modules.task5a import query_task5a_data, create_task5a_chart
from modules.task5b import query_task5b_data, create_task5b_chart
from modules.task6 import query_task6_data, create_task6_chart, query_task6_chart_data
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

    task3_data = query_task3_data(collection)
    task3_chart = create_task3_chart(task3_data)

    task4_data = query_task4_data(collection)
    task4_chart = create_task4_chart(task4_data)

    task5a_data, task5a_accuracy = query_task5a_data(collection)
    task5a_chart = create_task5a_chart(task5a_data)

    task5b_data, task5b_accuracy = query_task5b_data(collection)
    task5b_chart = create_task5b_chart(task5b_data)

    task6_data = query_task6_data(collection)
    task6_chart_data = query_task6_chart_data(collection)
    task6_chart = create_task6_chart(task6_chart_data)

    # Pass data and chart to the template
    return render_template(
        "home.html",
        task1_chart=task1_chart,
        task2_chart=task2_chart,
        task3_chart=task3_chart,
        task4_chart=task4_chart,
        task5a_accuracy=task5a_accuracy,
        task5a_chart=task5a_chart,
        task5a_data=task5a_data,
        task5b_accuracy=task5b_accuracy,
        task5b_chart=task5b_chart,
        task5b_data=task5b_data,
        task6_data=task6_data,
        task6_chart=task6_chart
    )


if __name__ == '__main__':
    app.run()
