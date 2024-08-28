# Microservice Observability with Prometheus, VictoriaMetrics, and Tilt

This repository demonstrates how to set up observability for a microservice using Prometheus and VictoriaMetrics in a local Kubernetes environment orchestrated with Tilt. The project showcases the benefits of using these tools to monitor and collect metrics from a microservice, ensuring that your applications are healthy and performant.

## Table of Contents

- [Introduction](#introduction)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Running the Demo](#running-the-demo)
- [Observability Workflow](#observability-workflow)
  - [Prometheus](#prometheus)
  - [VictoriaMetrics](#victoriametrics)
- [Test Automation](#test-automation)
- [Conclusion](#conclusion)
- [Next Steps](#next-steps)

## Introduction

In modern cloud-native applications, observability is crucial for understanding the health and performance of your services. This demo project shows how to implement observability in a Kubernetes environment using Prometheus to scrape metrics from a microservice and VictoriaMetrics to store and query these metrics. Tilt is used to streamline local development by managing the Kubernetes resources and Docker images.

## Project Structure

```
microservice-observability/
├── charts/
│   ├── microservice/
│   │   ├── templates/
│   │   │   ├── deployment.yaml
│   │   │   ├── service.yaml
│   │   └── Chart.yaml
│   │   └── values.yaml
├── k8s/
│   ├── prometheus.yaml
│   └── victoria-metrics.yaml
├── src/
│   ├── main.go
│   ├── Dockerfile
├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── test_metrics.py
│   └── entrypoint.sh
├── Tiltfile
└── README.md
```

### Explanation of Key Components

- **src/**: Contains the Go microservice source code and Dockerfile.
- **k8s/**: Kubernetes YAML configurations for Prometheus and VictoriaMetrics.
- **tests/**: Contains the Python test script and Dockerfile for verifying the observability setup.
- **Tiltfile**: Tilt configuration file that manages the deployment of resources in the local Kubernetes environment.

## Setup and Installation

### Prerequisites

- **Docker**: Ensure Docker is installed and running.
- **Tilt**: Install Tilt from the official [Tilt website](https://tilt.dev/).
- **Kubernetes**: Use a local Kubernetes setup such as `kind` or `minikube`.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/darrenrabbs/microservice-observability.git
   cd microservice-observability
   ```

2. Start the local Kubernetes environment (if using kind):
   ```
   kind create cluster --name observability-cluster
   ```

3. Use Tilt to start all services:
```
   tilt up
```

This will build the Docker images, deploy the microservice, Prometheus, and VictoriaMetrics to the local Kubernetes cluster, and run the observability tests

## Running the Demo

After running tilt up, all services will be deployed locally. You can monitor the progress in the Tilt UI, accessible via http://localhost:10350/. The microservice, Prometheus, and VictoriaMetrics will be up and running.

	•	Microservice: Available at http://localhost:8080.
	•	Prometheus UI: Available at http://localhost:9090.
	•	VictoriaMetrics UI: Available at http://localhost:8428/vmui.

## Observability Workflow

### Prometheus

Prometheus is an open-source systems monitoring and alerting toolkit that scrapes metrics from configured targets at given intervals, evaluates rule expressions, and displays the results. In this demo:

	•	Scraping Metrics: Prometheus is configured to scrape metrics from the microservice. The http_requests_total metric, which tracks the number of HTTP requests received by the microservice, is an example.
	•	Data Storage and Queries: Prometheus stores these metrics and makes them available for querying via its powerful query language, PromQL

### VictoriaMetrics
VictoriaMetrics is a fast, cost-effective, and scalable monitoring solution and time-series database. In this demo:
	•	Receiving Data: Prometheus forwards the scraped metrics to VictoriaMetrics using the remote_write configuration.
	•	Storing Metrics: VictoriaMetrics stores the metrics for long-term analysis, making it easier to scale and manage large volumes of metrics data.
	•	Querying Data: VictoriaMetrics provides a UI and API for querying the stored metrics, similar to Prometheus but optimized for larger data volumes and longer retention.

### Test Automation
A Python script is included in this project to verify that the http_requests_total metric is correctly captured and stored:

	•	The test script sends a request to the microservice and then queries VictoriaMetrics to ensure the metric is present.
	•	The script is containerized and run as a Kubernetes job, automated through Tilt.

## Conclusion
This project demonstrates how to implement a robust observability setup using Prometheus and VictoriaMetrics in a local Kubernetes environment with Tilt. By following this guide, you can easily monitor your microservices, ensuring they are operating as expected and quickly diagnosing any issues that arise.