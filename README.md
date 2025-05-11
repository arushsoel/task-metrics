# Prequisites
    Need to have Docker and Python installed
# Run the App with Docker
1. Clone the repository

    git clone https://github.com/your-username/task-metrics.git
    cd task-metrics

2. Build the Docker image

    docker build -t task-metrics .

3. Run the container

    docker run -d --name metrics -p 8080:8080 task-metrics

4. Send Test Requests

    python tools/feed_test_data.py(run in another terminal can use python or python3)

    curl localhost:8080/metrics | grep task_duration_seconds(check in another terminal)
