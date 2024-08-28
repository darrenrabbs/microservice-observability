# Build the Docker image for the microservice
docker_build('microservice:latest', 'src')

# Apply the rendered Helm templates
k8s_yaml('k8s/microservice.yaml')

# Deploy Prometheus and VictoriaMetrics
k8s_yaml('k8s/prometheus.yaml')
k8s_yaml('k8s/victoria-metrics.yaml')

# Ensure the Kubernetes resources depend on the Docker build
k8s_resource('microservice', port_forwards=['8080:8080'])

# Port forward for Prometheus and VictoriaMetrics UI
k8s_resource('prometheus', port_forwards=['9090:9090'])
k8s_resource('victoria-metrics', port_forwards=['8428:8428'])

# Suppress unused image warnings
update_settings(suppress_unused_image_warnings=["microservice-image"])

# Build the Docker image for the tests
docker_build('test-metrics-image', 'tests')

# Define and apply the job to run the test container
test_metrics_job = """
apiVersion: batch/v1
kind: Job
metadata:
  name: test-metrics-job
spec:
  template:
    spec:
      containers:
      - name: test-metrics-container
        image: test-metrics-image:latest
        command: ["/bin/sh", "-c", "./entrypoint.sh"]
      restartPolicy: Never
"""
k8s_yaml(blob(test_metrics_job))