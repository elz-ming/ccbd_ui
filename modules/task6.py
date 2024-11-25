import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64


def query_task6_data(collection):
    """Query MongoDB to retrieve data for Task 6."""
    document = collection.find_one({"file_name": "task6"})
    if not document:
        return []
    return document.get("data", [])


def query_task6_chart_data(collection):
    """Retrieve pre-generated chart data for Task 6 from MongoDB."""
    document = collection.find_one({"file_name": "task6_chart_data"})
    if not document:
        return []
    return document.get("graph_data", [])


def create_task6_chart(graph_data):
    """Create a sentiment chart from stored graph data."""
    import pandas as pd
    import matplotlib.pyplot as plt
    import io
    import base64

    # Convert graph_data to a Pandas DataFrame
    df = pd.DataFrame(graph_data)

    # Melt the DataFrame for easier plotting
    df_melted = df.melt(id_vars="date", value_vars=["negative", "neutral", "positive"],
                        var_name="sentiment", value_name="proportion")

    plt.figure(figsize=(10, 6))

    # Plot the sentiment trends
    for sentiment, group_data in df_melted.groupby("sentiment"):
        color = "red" if sentiment == "negative" else "blue" if sentiment == "neutral" else "green"
        plt.plot(group_data["date"], group_data["proportion"], label=sentiment, color=color)

    # Highlight the predicted point
    prediction_data = df[df["date"].str.startswith("Predicted")]
    for sentiment in ["negative", "neutral", "positive"]:
        plt.scatter(
            prediction_data["date"],
            prediction_data[sentiment],
            color="red" if sentiment == "negative" else (
                "blue" if sentiment == "neutral" else "green"),
            s=200,  # Large size for the circle
            edgecolor="black",
            label=f"Predicted ({sentiment})"
        )

    # Customize the plot
    plt.xlabel("Date")
    plt.ylabel("Proportion")
    plt.title("Sentiment Proportions Over Time")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the chart as a Base64 string
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plt.close()
    return f"data:image/png;base64,{base64.b64encode(img.getvalue()).decode()}"