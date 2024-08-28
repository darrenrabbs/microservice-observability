#!/bin/sh

# Wait for the microservice to be available
until curl -s http://microservice:8080/ > /dev/null; do
  echo "Waiting for the microservice to be up..."
  sleep 3
done

# Wait for VictoriaMetrics to be available
until curl -s http://victoria-metrics:8428/vmui > /dev/null; do
  echo "Waiting for VictoriaMetrics to be up..."
  sleep 3
done

# Run the test script
echo "All services are up! Running tests..."
python3 test_metrics.py