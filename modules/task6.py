import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import io
import base64


def query_task6_data(collection):
    """Query MongoDB to retrieve data for Task 6."""
    document = collection.find_one({"file_name": "task6"})
    if not document:
        return []
    return document.get("data", [])


def create_task6_chart(df, predictions, date_encoded):
    """Generate a sentiment trend chart including predictions."""
    # Append predictions to the DataFrame
    prediction_row = {"date": f"Predicted (Day {date_encoded})", **predictions, "date_encoded": date_encoded}
    prediction_row = pd.DataFrame([prediction_row])
    df = pd.concat([df, prediction_row], ignore_index=True)

    # Melt the DataFrame for easier plotting
    df_melted = df.melt(id_vars="date", value_vars=["negative", "neutral", "positive"],
                        var_name="sentiment", value_name="proportion")

    plt.figure(figsize=(8, 5))

    # Define colors for sentiments
    sentiment_colors = {"negative": "red", "neutral": "blue", "positive": "green"}

    # Plot trend lines for each sentiment
    for sentiment, group_data in df_melted.groupby("sentiment"):
        plt.plot(group_data["date"], group_data["proportion"], label=sentiment, color=sentiment_colors[sentiment])

    # Highlight predictions
    prediction_data = df_melted[df_melted["date"].str.startswith("Predicted")]
    for sentiment, color in sentiment_colors.items():
        sentiment_data = prediction_data[prediction_data["sentiment"] == sentiment]
        plt.scatter(
            sentiment_data["date"],
            sentiment_data["proportion"],
            color=color,
            s=100,
            edgecolor="black",
            label=f"Predicted ({sentiment})"
        )

    # Customize plot
    plt.xlabel("Date")
    plt.ylabel("Proportion")
    plt.title("Sentiment Proportions Over Time")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save chart to Base64 string
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plt.close()
    return f"data:image/png;base64,{base64.b64encode(img.getvalue()).decode()}"

def preprocess_task6_data(data):
    """Preprocess Task 6 data for regression analysis."""
    df = pd.DataFrame(data)
    required_columns = ["date", "sentiment"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Aggregate sentiment counts grouped by date
    sentiment_counts_by_date = df.groupby("date")["sentiment"].value_counts().unstack(fill_value=0)

    # Calculate proportions
    sentiment_proportions = sentiment_counts_by_date.div(sentiment_counts_by_date.sum(axis=1), axis=0)

    # Reset index to include 'date' as a column
    sentiment_proportions.reset_index(inplace=True)

    # Map dates to numerical values
    unique_dates = sorted(sentiment_proportions["date"].unique())
    date_mapping = {date: idx + 1 for idx, date in enumerate(unique_dates)}
    sentiment_proportions["date_encoded"] = sentiment_proportions["date"].map(date_mapping)

    # Split features (X) and labels (y)
    X = sentiment_proportions[["date_encoded"]]
    y = sentiment_proportions[["negative", "neutral", "positive"]]

    return sentiment_proportions, X, y

def train_task6_models(X, y):
    """Train separate linear regression models for each sentiment."""
    models = {}
    for sentiment in y.columns:
        model = LinearRegression()
        model.fit(X, y[sentiment])
        models[sentiment] = model
    return models

def predict_task6_sentiments(models, date_encoded):
    """Predict sentiment proportions for a given encoded date."""
    X_pred = np.array([[date_encoded]])
    predictions = {sentiment: model.predict(X_pred)[0] for sentiment, model in models.items()}
    return predictions