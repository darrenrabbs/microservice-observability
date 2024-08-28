import logging
import time

import requests

# Configuration
microservice_url = "http://microservice:8080"
victoria_metrics_query_url = "http://victoria-metrics:8428/api/v1/query"
metric_name = "http_requests_total"

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to send a request to the microservice
def send_request_to_microservice():
    logging.debug(f"Sending request to microservice at {microservice_url}")
    try:
        response = requests.get(microservice_url)
        logging.debug(f"Received response from microservice: {response.status_code}")
        return response.status_code == 200
    except requests.RequestException as e:
        logging.error(f"Error while sending request to microservice: {e}")
        return False

# Function to query VictoriaMetrics for the current metric value
def get_metric_value(metric_name):
    query = f"{metric_name}"
    logging.debug(f"Querying VictoriaMetrics for metric: {query}")
    try:
        response = requests.get(victoria_metrics_query_url, params={'query': query})
        logging.debug(f"Received response from VictoriaMetrics: {response.status_code}")
        data = response.json()
        logging.debug(f"Response data: {data}")
        if data['status'] == 'success' and data['data']['result']:
            metric_value = float(data['data']['result'][0]['value'][1])
            logging.info(f"{metric_name} has value: {metric_value}")
            return metric_value
        else:
            logging.warning(f"No valid result found for metric: {metric_name}")
            return None
    except requests.RequestException as e:
        logging.error(f"Error while querying VictoriaMetrics: {e}")
        return None
    except ValueError as e:
        logging.error(f"Error parsing response data: {e}")
        return None

# Main function to test the metric presence
def test_metric_presence():
    # Send a request to the microservice to ensure there's some activity
    if send_request_to_microservice():
        logging.info("Successfully pinged the microservice.")
    else:
        logging.error("Failed to ping the microservice.")
        return

    # Wait a few seconds to allow Prometheus and VictoriaMetrics to scrape the new data
    time.sleep(10)  # Add a delay to ensure data is available

    # Get the metric value
    metric_value = get_metric_value(metric_name)
    if metric_value is not None and metric_value > 0:
        logging.info(f"Success: {metric_name} is present with a value of {metric_value}.")
    else:
        logging.error(f"Failure: {metric_name} is not present or has a non-positive value.")

# Run the test
if __name__ == "__main__":
    test_metric_presence()