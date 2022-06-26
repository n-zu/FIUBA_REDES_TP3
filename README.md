# FIUBA_REDES_TP3

## Install dependencies

```console
$ pip3 install poetry
$ poetry config virtualenvs.in-project true
$ poetry install
```

If the dependencies are not recognized, you can manually switch to the venv them by running the following command:

```console
$ poetry shell
```

### Mininet

Visit the [mininet documentation](http://mininet.org/download/) to learn how to get started with Mininet.

#### Notes

- when using a vm, you might want to disable `virtualenvs.in-project`
- when using virtualbox, you need to forward a port to connect to the vm (NAT adapter)

## Initiating the project

```console
$ poetry init
```

## Topology

### Description

The topology consists of _4_ hosts and _n_ switches:

| Host | IP Addr  |     MAC Addr      | Attached to |
| :--: | :------: | :---------------: | :---------: |
|  h1  | 10.0.0.1 | 00:00:00:00:00:01 |     s1      |
|  h2  | 10.0.0.2 | 00:00:00:00:00:02 |     s1      |
|  h3  | 10.0.0.3 | 00:00:00:00:00:03 |     sn      |
|  h4  | 10.0.0.4 | 00:00:00:00:00:04 |     sn      |

![topology](resources/topology.png)

### Running the topology

The topology setup file is located at `linear_topo.py`. To run it, do:

```console
$ sudo python linear_topo.py
```

## Firewall

### Running the firewall

The code for the firewall is located at `pox/pox/ext/firewall.py`.
To run it, do:

```console
$ poetry run ./pox/pox.py log.level --DEBUG openflow.of_01 forwarding.l2_learning firewall
```

You may add `--rules={rules file}` at the end to change the source of the rules.

### Configuring the firewall

The firewall is configured by editing the `firewall_rules.json` file by default.
For example, if you want to block traffic from h1 to h2 using their
MAC addresses, you can do:

```json
{
  "rules": [
    {
      "eth": ["00:00:00:00:00:01", "00:00:00:00:00:02"]
    }
  ]
}
```

Or if you want to block all traffic to TCP port 80, you can do:

```json
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

```json
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

Although it is obvious, note that the firewall will only block traffic
if the packet passes through the firewall. If you set the firewall in
the switch s1, and block traffic from h3 to h4, thet it won't block.

## Testing the firewall

### Iperf

In the mininet console, run:

```console
mininet> xterm hX
```

Where X is the number of the host you want to test. This will open a
new terminal, where you can run the iperf command.

#### Server

```console
$ iperf -s -p <port> -i 1
```

#### Client

```console
$ iperf -c <server_ip> -p <port> -t <transmission_duration>
```

For more information, see: [How to use iperf over mininet?](http://csie.nqu.edu.tw/smallko/sdn/iperf_mininet.htm)

## Additional resources

- [POX](https://noxrepo.github.io/pox-doc/html/)
- [Iperf](https://iperf.fr/)

### Troubleshooting

#### Error creating interface (File exists)

Error:

```
Traceback (most recent call last):
  File "linear_topo.py", line 53, in <module>
    main()
  File "linear_topo.py", line 49, in main
    linear_topo(n_switches)
  File "linear_topo.py", line 27, in linear_topo
    net.addLink(switches[i], switches[i + 1])
  File "/usr/local/lib/python3.8/dist-packages/mininet/net.py", line 406, in addLink
    link = cls( node1, node2, **options )
  File "/usr/local/lib/python3.8/dist-packages/mininet/link.py", line 456, in __init__
    self.makeIntfPair( intfName1, intfName2, addr1, addr2,
  File "/usr/local/lib/python3.8/dist-packages/mininet/link.py", line 501, in makeIntfPair
    return makeIntfPair( intfname1, intfname2, addr1, addr2, node1, node2,
  File "/usr/local/lib/python3.8/dist-packages/mininet/util.py", line 270, in makeIntfPair
    raise Exception( "Error creating interface pair (%s,%s): %s " %
Exception: Error creating interface pair (s1-eth1,s2-eth1): RTNETLINK answers: File exists
```

Solution:

You can see the open interfaces with:

```console
$ ip link
```

And delete the conflicting interfaces:

```console
$ sudo ip link delete s1-eth1
$ sudo ip link delete s2-eth1
```
