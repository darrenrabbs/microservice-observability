
package main

import (
	"net/http"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

var (
	requests = prometheus.NewCounterVec(
		prometheus.CounterOpts{
			Name: "http_requests_total",
			Help: "Total number of HTTP requests",
		},
		[]string{"path"},
	)
)

func init() {
	prometheus.MustRegister(requests)
}

func handler(w http.ResponseWriter, r *http.Request) {
	requests.WithLabelValues(r.URL.Path).Inc()
	w.Write([]byte("Hello, World!"))
}

func main() {
	http.Handle("/metrics", promhttp.Handler())
	http.HandleFunc("/", handler)
	http.ListenAndServe(":8080", nil)
}
