from linear_topo import linear_topo
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info


def main():
    setLogLevel("info")

    n_switches = int(input("Enter number of switches: "))

    net = linear_topo(n_switches)

    info("*** Running Script\n")
    net.pingAll()

    # info("*** Running CLI\n")
    # CLI(net)

    info("*** Stopping network")
    net.stop()


if __name__ == "__main__":
    main()
