from datetime import datetime


LATENCY_FREQUENCY = 15000 # 150 milliseconds OR 0.15 seconds
ATTACK_COUNT_FREQUENCY = 7 # max no. of consecutive attacks to be taken 


class BruteForceDetector:
    def __init__(self, start_time: datetime, blocked_ips: list[str], attack_counts: int = 0):
        self.start_time = start_time
        self.attack_counts = attack_counts
        self.blocked_ips = blocked_ips
        

    def start_daemon(self, host_ip_add: str):
        time_now: datetime = datetime.now()
        latency: datetime = time_now - self.start_time # difference btw consecutive requests
        if latency.microseconds >= LATENCY_FREQUENCY:
            self.attack_counts += 1
            if self.attack_counts >= ATTACK_COUNT_FREQUENCY:
                self.__block_ip_address__(ip=host_ip_add)
                self.__alert_daemon__()
        
        # update the daemon count
        self.start_time = time_now

        
    def __block_ip_address__(self, ip: str):
        self.blocked_ips.append(ip)
        print(f"     [BLOCKED] {ip}")
    
    
    def __alert_daemon__(self):
        self.attack_counts = 0 # set attack_count to zero after its being informed
        print("========ALERTED========")