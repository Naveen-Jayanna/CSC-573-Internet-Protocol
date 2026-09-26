# CSC 573 Internet Protocols

Networking assignments completed for CSC 573 at North Carolina State University. The repository combines protocol implementation, controlled experiments, network simulation, and packet analysis.

## Projects

### PA1: File transfer protocol comparison

Implemented file transfer clients and servers in Python and compared throughput across:

- HTTP/1.1
- HTTP/2
- gRPC
- BitTorrent

The experiments transferred files of several sizes over a local network, repeated each transfer, and recorded average throughput and standard deviation.

Each protocol directory contains its own execution notes. Experimental results and analysis are included in the assignment folder.

### PA2: TCP behavior in ns-3

Built an ns-3 simulation to compare DCTCP and TCP Cubic across a simple two-router topology. The experiment used configurable link parameters and captured results for analysis.

Environment used:

- Ubuntu 22.04
- ns-3.36.1
- C++

### PA3: Packet sniffer

Implemented a Python packet sniffer using raw sockets. The program samples network traffic for a configurable period and counts several protocol categories:

- IP
- TCP and UDP
- HTTP and HTTPS
- QUIC
- DNS
- ICMP

Results are written to CSV for later analysis.

## Repository structure

```text
PA1/  Protocol implementations and transfer experiments
PA2/  ns-3 TCP simulation
PA3/  Raw-socket packet sniffer
```

## Running the work

Setup differs by assignment. Read the local README before running a project.

For example, the packet sniffer runs on Linux with elevated privileges:

```bash
cd PA3/HW3
sudo python3 sniffer_njayann.py
```

The PA1 protocol implementations require Python 3 and protocol-specific packages such as `grpcio`, `h2`, or BitTorrent libraries. PA2 requires a compatible ns-3 installation.

## What I learned

- How application protocols affect transfer behavior and overhead
- How to design repeatable network measurements
- How congestion-control algorithms behave in a simulated topology
- How packet headers can be decoded directly from raw socket data
- How to separate implementation results from measurement noise

## Academic context

This repository contains completed coursework. Current students should follow their institution's academic integrity rules and should not submit this work as their own.

