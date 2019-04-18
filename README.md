# MINOS: A Multi-protocol Software Defined Networking Platform for the Internet of Things

![MINOS Architecture](/MINOSArchitecturev4.jpg)

MINOS is suitable to accomodate many different protocols.
Two of them are included, both in the relevalt folders inside protocols_deployment/. We also include a work in progress in dual-stack (contiki dual-stack) using a contiki version.

* CORAL-SDN, Readme file [here](/protocols_deployment/CORAL-SDN_dataplane/readme.md)
CORAL-SDN is an OpenFlow-like protocol. CORAL-SDN decouples complexity from the network protocol and ofﬂoads it to network control software deployed at the surrounding ﬁxed infrastructure. It supports dynamic deployment and configuration of SDN enabled topology and flow control mechanisms. Moreover, applies network control using [two novel topology control algorithms](https://www.researchgate.net/publication/321736253_Software_defined_topology_control_strategies_for_the_Internet_of_Things) and two flow establishment and forwarding techniques that can be combined and adjusted on-demand. Reference paper [here](https://www.researchgate.net/publication/321741443_CORAL-SDN_A_software-defined_networking_solution_for_the_Internet_of_Things)
* Adaptable-RPL, Readme file [here](/protocols_deployment/adaptable-rpl/readme.md)
The Adaptable-RPL is a standard contiki-RPL with modifications in order to provide handlers to MINOS to adapt RPL parameters in real time. These parameters are Imin, Idouble, effecting the tricle algorithm, responsible for neighbors solicitiation, which affects the performance of mobile nodes. Other parameters include the frequency of UDP messages sending (aka communication data), and dynamic change of Objective Function, described in submitted works.
* Contiki with Dual Stack, Readme file [here](/protocols_deployment/contiki-dual/README.md)

