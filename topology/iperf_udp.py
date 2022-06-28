from linear_topo import linear_topo
from mininet.cli import CLI
from mininet.log import setLogLevel, info


def main():
    setLogLevel("info")

    n_switches = int(input("Enter number of switches: "))
    n_server = int(input("Enter server host number: "))
    n_client = int(input("Enter client host number: "))
    port = int(input("Enter port: "))

    net = linear_topo(n_switches)

    info("*** Running Script\n")

    server = net.get(f'h{n_server}')
    print(server.cmd(f'iperf -s -p {port} -u >logs/server.log &'))

    client = net.get(f'h{n_client}')
    print(client.cmd(
        f'iperf -c {server.IP()} -p {port} -n 10 -u >logs/client.log &'))

    # info("*** Running CLI\n")
    # CLI(net)

    info("*** Stopping network")
    net.stop()


if __name__ == "__main__":
    main()
