from flask import Flask, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
import os
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
    # Query data for section-4
    section_4_data = task4.query_section_4_data(collection)
    section_4_chart = task4.create_section_4_chart(section_4_data)

    # Pass data and chart to the template
    return render_template(
        "home.html",
        title="Cloud Computing P1 Group 3",
        section_4_chart=section_4_chart,
    )


if __name__ == '__main__':
    app.run()
