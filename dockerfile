# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory
WORKDIR /news-agg

# Copy the current directory contents into the container
COPY . /news-agg

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variables
ENV DATABASE_URL "sqlite:///./news_aggregator.db"
ENV NEWS_SOURCE_URL "https://lithosgraphein.com/"
ENV LOG_FILE "news_aggregator.log"
ENV HEROKU_API_KEY "HRKU-10def73c-0725-4800-a3bd-84f87b41cfa8"

# Copy the SQLite database file
COPY news_aggregator.db /news-agg/news_aggregator.db

# Run app.py when the container launches
CMD ["uvicorn", "src.news_aggregator.interfaces.api.main:app", "--host", "0.0.0.0", "--port", "80"]