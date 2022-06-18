# FIUBA_REDES_TP3

## Install dependencies
```bash
$ pip3 install poetry
$ poetry config virtualenvs.in-project true
$ poetry install
```

## Initiating the project
```bash
$ poetry init
```

## Topology
### Description
The topology consists of *4* hosts and *n* switches:

| Host | IP Addr  |     MAC Addr      |  Attached to  |
|:----:|:--------:|:-----------------:|:-------------:|
|  h1  | 10.0.0.1 | 00:00:00:00:00:01 |      s1       |
|  h2  | 10.0.0.2 | 00:00:00:00:00:02 |      s1       |
|  h3  | 10.0.0.3 | 00:00:00:00:00:03 |      sn       |
|  h4  | 10.0.0.4 | 00:00:00:00:00:04 |      sn       |

![topology](resources/topology.png)


### Running the topology
The topology setup file is located at `linear_topo.py`. To run it, do:
```bash
$ sudo python linear_topo.py
```

## Firewall
### Running the firewall
The code for the firewall is located at `pox/pox/ext/firewall.py`.
To run it, do:
```bash
$ poetry run ./pox/pox.py log.level --DEBUG openflow.of_01 forwarding.l2_learning firewall
```

### Configuring the firewall
The firewall is configured by editing the `firewall_rules.py` file.
For example, if you want to block traffic from h1 to h2 using their
MAC addresses, you can do:
```
{
    "rules": [
        {
            "eth": ["00:00:00:00:00:01", "00:00:00:00:00:02"]
        }
    ]
}
```
Or if you want to block all traffic to TCP port 80, you can do:
```
{
    "rules": [
        {
            "tcp": {
                "dst": "80"
            }
        }
    ]
}
```
Or if you want to block all packets from host 1 such that the destination
port is 5001, you can do:
```
{
    "rules": [
        {
            "ipv4": {
                "src": "10.0.0.1"
            },
            "udp": {
                "dst": "5001"
            }
        }
    ]
}
```

Although it is obvious, note that the firwall will only block traffic
if the packet passes through the firewall. If you set the firewall in
the switch s1, and block traffic from h3 to h4, thet it won't block.

## Testing the firewall
### Iperf
In the mininet console, run:
```bash
mininet> xterm hX
```
Where X is the number of the host you want to test. This will open a
new terminal, where you can run the iperf command.
#### Server
```bash
# iperf -s -p <port> -i 1
```
### Client
```bash
# iperf -c <server_ip> -p <port> -t <transmission_duration>
```
For more information, see: [How to use iperf over mininet?](http://csie.nqu.edu.tw/smallko/sdn/iperf_mininet.htm)

## Additional resources
- [POX](https://noxrepo.github.io/pox-doc/html/)
- [Iperf](https://iperf.fr/)




