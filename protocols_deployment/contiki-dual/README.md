Contiki dual
============================
![Contiki dual](contiki_dual.jpg)
This is a work in progress and one of our current goals, i.e., to enhance MINOS with the ability to operate "multi-stack" network protocols. In this attempt we have an adapted Contiki environment that supports a network stack with two routing algorithms: 
* RIME 
* IPv6

In the experiment we implement two network nodes that exchange messages using dynamically and interchangeably RIME and IPv6 messages.

### The example requires a LINUX machine with Java and Contiki. 

#### Execution Steps: 
* ```cd minos/protocols_deployment/contiki-dual/tools/cooja```
* ```ant run```
* Search and run the experiment in /tools/cooja/examples/dual-protocol/dualProtocols-RIME-IPv6.csc 

For more information contact Tryfon at theodorou@uom.edu.gr

For more information about Contiki, see the Contiki website:
[http://contiki-os.org](http://contiki-os.org)
