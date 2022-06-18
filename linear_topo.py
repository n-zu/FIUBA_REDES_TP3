from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info


def linear_topo(n_switches: int):
    net = Mininet(controller=RemoteController)

    info("*** Adding controller\n")
    net.addController("c0")

    info("*** Adding hosts\n")
    hosts = []
    for i in range(1, 5):
        hosts.append(
            net.addHost("h%s" % i, ip="10.0.0.%s" % i, mac="00:00:00:00:00:0%s" % i)
        )

    info("*** Adding switches\n")
    switches = []
    for i in range(1, n_switches + 1):
        switches.append(net.addSwitch("s%s" % i))

    info("*** Creating links\n")
    for i in range(n_switches - 1):
        net.addLink(switches[i], switches[i + 1])

    net.addLink(switches[0], hosts[0])
    net.addLink(switches[0], hosts[1])
    net.addLink(switches[-1], hosts[2])
    net.addLink(switches[-1], hosts[3])

    info("*** Starting network\n")
    net.start()

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network")
    net.stop()


def main():
    setLogLevel("info")

    n_switches = int(input("Enter number of switches: "))

    linear_topo(n_switches)


if __name__ == "__main__":
    main()
