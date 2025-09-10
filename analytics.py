import io
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Response, jsonify, send_file

# Utilizzo medio per ora del giorno
def hourly_plot(df):
    hourly_mean = df.groupby("hr")["cnt"].mean()
    plt.figure(figsize=(10,5))
    sns.lineplot(x=hourly_mean.index, y=hourly_mean.values, marker="o")
    plt.title("Average rentals per hour")
    plt.xlabel("Hour of the day")
    plt.ylabel("Average rentals")
    plt.grid(True)
    plt.savefig("hourly.png")
    img = io.BytesIO()
    img.seek(0)
    plt.close()
    return send_file(
        img,
        mimetype="image/png",
        as_attachment=True,
        download_name="hourly.png"  # questo sarà il nome del file nel download
    )

def weekday_plot(df):
    # Utilizzo medio per giorno della settimana
    weekday_mean = df.groupby("weekday")["cnt"].mean()
    plt.figure(figsize=(8,5))
    sns.barplot(x=weekday_mean.index, y=weekday_mean.values)
    plt.title("Average rentals per weekday")
    plt.xlabel("Weekday (0=Sunday, 6=Saturday)")
    plt.ylabel("Average rentals")
    plt.savefig("weekday.png")
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plt.close()
    return Response(img.getvalue(), mimetype="image/png")

def month_plot(df):
    # Utilizzo medio per mese
    monthly_mean = df.groupby("mnth")["cnt"].mean()
    plt.figure(figsize=(10,5))
    sns.lineplot(x=monthly_mean.index, y=monthly_mean.values, marker="o")
    plt.title("Average rentals per month")
    plt.xlabel("Month")
    plt.ylabel("Average rentals")
    plt.grid(True)
    plt.savefig("month.png")
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plt.close()
    return Response(img.getvalue(), mimetype="image/png")

def holyday_stats(df):
    # Statistiche festività
    holiday_stats = df.groupby("holiday")["cnt"].agg(["mean", "std"])
    return jsonify(holiday_stats.to_dict())

def distribution_casual_registered(df):
    # Distribuzione casual vs registered
    casual_registered = df[["casual", "registered"]].sum()
    plt.figure(figsize=(6,6))
    casual_registered.plot(kind="pie", autopct="%1.1f%%", startangle=90, colors=["skyblue","salmon"])
    plt.title("Casual vs Registered Users")
    plt.ylabel("")
    plt.savefig("casual_registered.png")
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plt.close()
    return Response(img.getvalue(), mimetype="image/png")

def heatmap(df):
    # Heatmap hour × weekday
    hour_weekday_mean = df.groupby(["weekday","hr"])["cnt"].mean().unstack()
    plt.figure(figsize=(12,6))
    sns.heatmap(hour_weekday_mean, cmap="YlGnBu")
    plt.title("Heatmap of average rentals by hour and weekday")
    plt.xlabel("Hour of day")
    plt.ylabel("Weekday (0=Sunday)")
    plt.savefig("heatmap.png")
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plt.close()
    return Response(img.getvalue(), mimetype="image/png")

def trend_weekly(df):
    # Trend temporale (media mobile settimanale)
    df["cnt_7d_avg"] = df["cnt"].rolling(window=7).mean()
    plt.figure(figsize=(12,5))
    plt.plot(df["dteday"], df["cnt_7d_avg"], color="green")
    plt.title("7-day moving average of rentals")
    plt.xlabel("Date")
    plt.ylabel("Average rentals")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.savefig("trend_weekly.png")
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plt.close()
    return Response(img.getvalue(), mimetype="image/png")
