#include <fstream>
#include <string>
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/ipv4-global-routing-helper.h"
#include "ns3/netanim-module.h"
#include "ns3/flow-monitor-module.h"

using namespace ns3;
NS_LOG_COMPONENT_DEFINE("IP_PA2");

NodeContainer nodes, sender, dest, router, s1tor1, s2tor1, r1tor2, r2tod1, r2tod2;
NetDeviceContainer s1linkr1, s2linkr1,r1linkr2, r2linkd1, r2linkd2;
Ipv4InterfaceContainer i_s1tor1, i_s2tor1, i_r1tor2, i_r2tod1, i_r2tod2;
Address d1_IP, d2_IP;
Ipv4AddressHelper address;
PointToPointHelper pointToPoint;
InternetStackHelper internet;
double flow_time = 60.0;
int d1_port = 8331, d2_port = 8331;
uint maxBytes = 50 * 1024 * 1024;       // 50MB data being sent

const int THROUGHPUT = 0;
const int FTIME = 1;

/* Calculate the metrics for all the experiments using FlowIDs and writing it into a CSV file.
We get 48 Flows in total after running all the 5 experiments. We extract the stats for corresponding FlowIDs for each experiment to calculate the metrics. The following represents the FlowIDs corresponding to each experiment:

Experiment 1: 1 3 5 (S1 -> D1)

Experiment 2: 7 11 15 (S1 -> D1)
              8 12 16 (S2 -> D2)

Experiment 3: 19 21 23 (S1 -> D1)

Experiment 4: 25 29 33 (S1 -> D1)
              26 30 34 (S2 -> D2)

Experiment 5: 37 41 45 (S1 -> D1)
              38 42 46 (S2 -> D2)  

*/

/* Calculating the standard deviation */
double getStdDev(std::vector<double>  arr, double mean)
{
    double sdv = 0.0;
    for(int i=0; i<3; ++i)
        sdv += pow(arr[i]-mean, 2);

    return sqrt(sdv / 3);
}

void calculateMetrics(std::map<FlowId, FlowMonitor::FlowStats> stats,int type, int flow_id, int exp_no, int metric){
    std::ofstream file;
    file.open("tcp_njayann.csv", std::ios::out | std::ios::app);
    std::vector<double> tputs1, tputs2, ftime1, ftime2;
    double curr_throughput = 0, time_taken = 0;
    double sum1 = 0, sum2 = 0, fsum1 = 0, fsum2 = 0;
    for(int i=0; i<3; i++){
        FlowMonitor::FlowStats fs = stats[flow_id];
        time_taken = fs.timeLastRxPacket.GetSeconds()-fs.timeFirstTxPacket.GetSeconds();
        curr_throughput = fs.rxBytes*8.0/time_taken/(1024*1024);
        tputs1.push_back(curr_throughput);
        ftime1.push_back(time_taken);
        fsum1 += time_taken;
        sum1 += curr_throughput;
        if(type){
            FlowMonitor::FlowStats fs = stats[flow_id + 1];
            time_taken = fs.timeLastRxPacket.GetSeconds()-fs.timeFirstTxPacket.GetSeconds();
            curr_throughput = fs.rxBytes*8.0/time_taken/(1024*1024);
            ftime2.push_back(time_taken);
            tputs2.push_back(curr_throughput);
            sum2 += curr_throughput;
            fsum2 += time_taken;
            flow_id += 2; 
        }
        flow_id += 2;
    }
    if(!type && metric == THROUGHPUT){
        file << "th_" << exp_no << "," << tputs1[0] << "," << tputs1[1] << "," << tputs1[2] << "," << (double)sum1/3 << "," << getStdDev(tputs1, (double)sum1/3) << "," << "Mbps,,,,,,\n" ;
    }
    else if(!type && metric == FTIME){
        file << "afct_" << exp_no << "," << ftime1[0] << "," << ftime1[1] << "," << ftime1[2] << "," << (double)fsum1/3 << "," << getStdDev(ftime1, (double)fsum1/3) << "," << "sec,,,,,,\n" ;
    }
    else if(type && metric == THROUGHPUT){
        file << "th_" << exp_no << "," << tputs1[0] << "," << tputs1[1] << "," << tputs1[2] << "," << (double)sum1/3 << "," << getStdDev(tputs1, (double)sum1/3) << "," << "Mbps," << tputs2[0] << "," << tputs2[1] << "," << tputs2[2] << "," << (double)sum2/3 << "," << getStdDev(tputs2, (double)sum2/3) << "," << "Mbps\n" ;
    }
    else if(type && metric == FTIME){
        file << "afct_" << exp_no << "," << ftime1[0] << "," << ftime1[1] << "," << ftime1[2] << "," << (double)fsum1/3 << "," << getStdDev(ftime1, (double)fsum1/3) << "," << "sec," << ftime2[0] << "," << ftime2[1] << "," << ftime2[2] << "," << (double)fsum2/3 << "," << getStdDev(ftime2, (double)fsum2/3) << "," << "sec\n" ;
    }
    file.close();
}


/* Send maxBytes data from Source to Destination for different TCP versions */
void data_transfer(Ptr<Node> src, Ptr<Node> dest, Address sinkAddress, uint16_t sinkPort, std::string tcp_version, double start_time, double end_time)
{
    if(tcp_version.compare("TcpBic")){
        Config::SetDefault("ns3::TcpL4Protocol::SocketType", TypeIdValue(TcpBic::GetTypeId()));
    }
    else if(tcp_version.compare("TcpDctcp")){
        Config::SetDefault("ns3::TcpL4Protocol::SocketType", TypeIdValue(TcpDctcp::GetTypeId()));
    }

    BulkSendHelper sourceHelper("ns3::TcpSocketFactory", sinkAddress);
    sourceHelper.SetAttribute("MaxBytes", UintegerValue(maxBytes));
   
    PacketSinkHelper packetSinkHelper("ns3::TcpSocketFactory", InetSocketAddress(Ipv4Address::GetAny(), sinkPort));
    ApplicationContainer dest_container = packetSinkHelper.Install(dest);
    ApplicationContainer source_container = sourceHelper.Install(src);

    dest_container.Start(Seconds(start_time));
    dest_container.Stop(Seconds(end_time));
   
    source_container.Start(Seconds(start_time));
    source_container.Stop(Seconds(end_time));
}

/* Creating the required Dumbbell topology */
void create_topology(uint16_t d1_port, uint16_t d2_port){

    sender.Create(2);
    dest.Create(2);
    router.Create(2);
   
    s1tor1 = NodeContainer(sender.Get(0), router.Get(0));
    s2tor1 = NodeContainer(sender.Get(1), router.Get(0));
    r1tor2 = NodeContainer(router.Get(0), router.Get(1));
    r2tod2 = NodeContainer(router.Get(1), dest.Get(1));
    r2tod1 = NodeContainer(router.Get(1), dest.Get(0));

    pointToPoint.SetDeviceAttribute("DataRate", StringValue("1Gbps"));
    pointToPoint.SetChannelAttribute("Delay", StringValue("5ms"));

    internet.Install(sender);
    internet.Install(dest);
    internet.Install(router);

    s1linkr1 = pointToPoint.Install(s1tor1);
    s2linkr1 = pointToPoint.Install(s2tor1);
    r1linkr2 = pointToPoint.Install(r1tor2);
    r2linkd1 = pointToPoint.Install(r2tod1);
    r2linkd2 = pointToPoint.Install(r2tod2);

    address.SetBase("10.1.1.0", "255.255.255.0");
    i_s1tor1 = address.Assign(s1linkr1);
    address.SetBase("10.1.2.0", "255.255.255.0");
    i_s2tor1 = address.Assign(s2linkr1);
    address.SetBase("10.1.3.0", "255.255.255.0");
    i_r1tor2 = address.Assign(r1linkr2);
    address.SetBase("10.1.4.0", "255.255.255.0");
    i_r2tod1 = address.Assign(r2linkd1);
    address.SetBase("10.1.5.0", "255.255.255.0");
    i_r2tod2 = address.Assign(r2linkd2);

    Ipv4GlobalRoutingHelper::PopulateRoutingTables();

    d1_IP = InetSocketAddress(i_r2tod1.GetAddress(1), d1_port);
    d2_IP = InetSocketAddress(i_r2tod2.GetAddress(1), d2_port);
}

/* Run experiments based on type of TCP */
void run_experiment(int exp_no,int runs, double start_time){
    for(int i=0; i<runs; i++, start_time += flow_time){
        switch(exp_no){
            case 1: data_transfer(sender.Get(0), dest.Get(0), d1_IP, d1_port, "TcpBic", start_time, start_time+flow_time);
                    break;
            case 2: data_transfer(sender.Get(0), dest.Get(0), d1_IP, d1_port, "TcpBic", start_time, start_time+flow_time);
                    data_transfer(sender.Get(1), dest.Get(1), d2_IP, d2_port, "TcpBic", start_time, start_time+flow_time);
                    break;
            case 3: data_transfer(sender.Get(0), dest.Get(0), d1_IP, d1_port, "TcpDctcp", start_time, start_time+flow_time);
                    break;
            case 4: data_transfer(sender.Get(0), dest.Get(0), d1_IP, d1_port, "TcpDctcp", start_time, start_time+flow_time);
                    data_transfer(sender.Get(1), dest.Get(1), d2_IP, d2_port, "TcpDctcp", start_time, start_time+flow_time);
                    break;
            case 5: data_transfer(sender.Get(0), dest.Get(0), d1_IP, d1_port, "TcpBic", start_time, start_time+flow_time);
                    data_transfer(sender.Get(1), dest.Get(1), d2_IP, d2_port, "TcpDctcp", start_time, start_time+flow_time);
                    break;
        }
    }
}
int main(int argc, char *argv[])
{
    Time::SetResolution(Time::NS);
    create_topology(8331, 8331);

    for(int i=1; i<=5; i++){
        run_experiment(i, 3, (i-1)*180);
    }

    FlowMonitorHelper flowmon;
    Ptr<FlowMonitor> monitor = flowmon.InstallAll();

    Simulator::Stop(Seconds(1500.));
    Simulator::Run();
    Simulator::Destroy();

    monitor->CheckForLostPackets();

    Ptr<Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier>(flowmon.GetClassifier());
    std::map<FlowId, FlowMonitor::FlowStats> stats = monitor->GetFlowStats();

    std::ofstream file;
    file.open("tcp_njayann.csv", std::ios::out | std::ios::trunc);
    file << "exp,r1_s1,r2_s1,r3_s1,avg_s1,std_s1,unit_s1,r1_s2,r2_s2,r3_s2,avg_s2,std_s2,unit_s2\n";
    file.close();

    std::vector<int> type_arr {0, 1, 0, 1, 1};
    std::vector<int> flow_arr {1, 7, 19, 25, 37};

    /* Calculating and inserting throughput into the CSV */
    for(int i=0; i<5; i++){
        calculateMetrics(stats, type_arr[i], flow_arr[i], i+1, THROUGHPUT);
    }

    /* Calculating and inserting Avg Flow Completion Time into the CSV */
    for(int i=0; i<5; i++){
        calculateMetrics(stats, type_arr[i], flow_arr[i], i+1, FTIME);
    }

    monitor->SerializeToXmlFile("IP_PA2.flowmon", true, true);
    return 0;
}


