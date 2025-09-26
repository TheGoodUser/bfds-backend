from enum import Enum

class AttackType(Enum):
    BRUTE_FORCE = "Brute Force Attack"
    DDOS = "Distributed Denial of Service"
    SQL_INJECTION = "SQL Injection"
    PHISHING = "Phishing"
    MAN_IN_THE_MIDDLE = "Man in the Middle"
    RANSOMWARE = "Ransomware"
    MALWARE = "Malware"
    CROSS_SITE_SCRIPTING = "Cross Site Scripting"
    ZERO_DAY = "Zero Day"
    INSIDER_THREAT = "Insider Threat"
    PASSWORD_SPRAY = "Password Spray"
    BOTNET = "Botnet"