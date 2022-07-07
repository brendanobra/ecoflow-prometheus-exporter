#hat tip https://trstringer.com/quick-and-easy-prometheus-exporter/
import os
import time
from prometheus_client import start_http_server, Gauge, Enum,Counter
import requests

class AppMetrics:
    """
    Representation of Prometheus metrics and loop to fetch and transform
    application metrics into Prometheus metrics.
    """
    def __init__(self, endpoint,serial_number,app_key, secret_key, array_capacity, polling_interval_seconds=5):
        self.endpoint = endpoint
        self.serial_number = serial_number
        self.app_key = app_key
        self.secret_key = secret_key
        self.array_capacity = array_capacity
        self.polling_interval_seconds = polling_interval_seconds
        # Prometheus metrics to collect
        self.state_of_charge = Gauge("ecoflow_state_of_charge", "state of charge")
        self.remaining_time = Gauge("ecoflow_remaining_time", "instantaneous remaining run time")
        self.watts_out = Gauge("ecoflow_watts_out", "Watts out")
        self.watts_in = Gauge("ecoflow_watts_in", "Watts in")
        self.total_array_capacity = Gauge("ecoflow_total_array_capacity","total solar capacity")
        self.health = Enum("app_health", "Health", states=["healthy", "unhealthy"])
        self.successful_polls = Counter("ecoflow_successful_polls","Number of succesful calls to IOT API")
        self.failed_polls = Counter("ecoflow_failed_polls","Number of failed calls to IOT API")
        self.total_array_capacity.set(array_capacity)


    def run_metrics_loop(self):
        """Metrics fetching loop"""
        while True:
            self.fetch()
            time.sleep(self.polling_interval_seconds)

    def fetch(self):
        """
        Get metrics from application and refresh Prometheus metrics with
        new values.
        """
        # Fetch raw status data from the application
        headers = {'Content-Type' : 'application/json',
            'appKey': self.app_key.strip(),
            'secretKey': self.secret_key.strip()}
        resp = requests.get(url=f"{self.endpoint}/?sn={self.serial_number}", headers=headers)
        status_data = resp.json()
        if int(status_data["code"]) == 0:
            data=status_data['data']
            self.state_of_charge.set(int(data['soc']))
            self.remaining_time.set(int(data['remainTime']))
            self.watts_in.set( int(data['wattsInSum']))
            self.watts_out.set( int(data['wattsOutSum']))
            self.successful_polls.inc()
        else:
            print("failed with: {}".format(resp))
            self.failed_polls.inc()  
            
def main():
    """Main entry point"""
    polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "30"))
    ecoflow_endpoint=str(os.getenv("ECOFLOW_ENDPOINT", 
        "https://api.ecoflow.com/iot-service/open/api/device/queryDeviceQuota"))
    device_sn=str(os.getenv("DEVICE_SN"))
    app_key=str(os.getenv("APP_KEY"))
    secret_key=str(os.getenv("SECRET_KEY"))
    array_capacity = int(os.getenv("ARRAY_CAPACITY", "1200"))
    
    exporter_port = int(os.getenv("EXPORTER_PORT", "9090"))
    print("starting ecoflow exporter")
    app_metrics = AppMetrics(
        endpoint = ecoflow_endpoint,
        serial_number = device_sn,
        app_key= app_key,
        secret_key=secret_key,
        array_capacity = array_capacity,
        polling_interval_seconds=polling_interval_seconds
    )
    start_http_server(exporter_port)
    app_metrics.run_metrics_loop()

if __name__ == "__main__":
    main()
