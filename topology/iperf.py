from time import sleep
from linear_topo import linear_topo
from mininet.log import setLogLevel, info
from threading import Thread, Event


def start_server(server, port, stop):
    pid = server.cmd(f"iperf -s -p {port} > logs/server.log &")
    stop.wait()
    server.cmd(f"kill -SIGINT {pid}")


def main():
    setLogLevel("info")

    n_switches = int(input("Enter number of switches: "))
    n_server = int(input("Enter server host number: "))
    n_client = int(input("Enter client host number: "))
    port = int(input("Enter port: "))

    net = linear_topo(n_switches)

    info("*** Running Script\n")

    stop = Event()

    server = net.get(f"h{n_server}")
    thread = Thread(target=start_server, args=(server, port, stop))
    thread.start()

    client = net.get(f"h{n_client}")
    client.cmd(f"iperf -c {server.IP()} -p {port} -n 10 > logs/client.log &")
    sleep(2)
    stop.set()
    thread.join()

    info("*** Stopping network")
    net.stop()


def logs():
    with open("logs/server.log", "r") as f:
        logs = f.read()
        print(logs)

    with open("logs/client.log", "r") as f:
        logs = f.read()
        print(logs if logs != "" else "Client could not connect to server\n")


if __name__ == "__main__":
    main()
    logs()
