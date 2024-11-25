import io
import base64
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

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
