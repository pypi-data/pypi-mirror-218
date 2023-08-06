from pystax.checker import DomainProbe
probe = DomainProbe()

domain_result = probe.probe_domain("example.com")
print(domain_result)

domain_result = probe.probe_domain("example.org")
print(domain_result)

domain_result = probe.probe_domain("hgwhd.xty")
print(domain_result)

domain_result = probe.probe_domain("404.com")
print(domain_result)

domain_result = probe.probe_domain("gov.uk")
print(domain_result)

ip_result = probe.probe_ip("192.168.0.1")
print(ip_result)

ip_result = probe.probe_ip("19462904")
print(ip_result)

ip_result = probe.probe_ip("999.999.999.999")
print(ip_result)

ip_result = probe.probe_ip("1.1.1.1")
print(ip_result)

ip_result = probe.probe_ip("127.0.0.1")
print(ip_result)





