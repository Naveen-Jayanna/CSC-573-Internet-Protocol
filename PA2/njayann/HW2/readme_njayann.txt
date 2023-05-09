Environment Setup:

    NS3 version: ns-3.36.1 
    OS Used: Ubuntu 22.04 LTS

    Installation of NS3 (ns-3.36.1)

    Step 1:  Prerequisites

    $ sudo apt update
    $ sudo apt install g++ python3 python3-dev pkg-config sqlite3 cmake python3-setuptools git qtbase5-dev qtchooser qt5-qmake qtbase5-dev-tools gir1.2-goocanvas-2.0 python3-gi python3-gi-cairo python3-pygraphviz gir1.2-gtk-3.0 ipython3 openmpi-bin openmpi-common openmpi-doc libopenmpi-dev autoconf cvs bzr unrar gsl-bin libgsl-dev libgslcblas0 wireshark tcpdump sqlite sqlite3 libsqlite3-dev  libxml2 libxml2-dev libc6-dev libc6-dev-i386 libclang-dev llvm-dev automake python3-pip libxml2 libxml2-dev libboost-all-dev 

    Step 2 : Download ns-allinone-3.36.1.tar.bz2 from the website nsnam.org. 

    https://www.nsnam.org/releases/ns-all... 

    Step 3 : Unzip the above file content to the home folder
    
    $ tar jxvf ns-allinone-3.36.1.tar.bz2 
    
    Step 4: Build and run 

    $ cd ns-allinone-3.36.1/ 
    $ ./build.py --enable-examples --enable-tests

Execution:

    Once the installation is done, you can run the tcp analysis experiment. To run the experiment, you need to copy 
    the file tcp_njayann.cc to the scratch folder and execute the file as shown below 
    
    $ cd ns-3.36.1/
    $ ./ns3 run scratch/tcp_njayann 

Experiment parameters:

    Delay: 5 milliseconds
    Data Transferred: 50 MB
    Link bandwidth : 1 Gbps
    TCP types used: DCTCP and TCP Cubic
    
    Network Topology:

    s1 ----               ---- d1
           -             -
            r1---------r2
           -             -
    s2 ----               ---- d2


