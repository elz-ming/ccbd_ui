import io
import base64
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')


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
