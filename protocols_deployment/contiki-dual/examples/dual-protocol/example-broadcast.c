/*
 * Copyright (c) 2007, Swedish Institute of Computer Science.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of the Institute nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE INSTITUTE AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE INSTITUTE OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 *
 * This file is part of the Contiki operating system.
 *
 */

/**
 * \file
 *         Testing the broadcast layer in Rime
 * \author
 *         Adam Dunkels <adam@sics.se>
 */

#include "contiki.h"

//#include "net/netstack.h"

#include "net/rime/rime.h"
#include "random.h"
//#include "dev/button-sensor.h"
//#include "dev/leds.h"
#include <stdio.h>

#include "lib/random.h"
#include "sys/ctimer.h"
#include "sys/etimer.h"
#include "net/ip/uip.h"
#include "net/ipv6/uip-ds6.h"

#include "simple-udp.h"

#include <string.h>

#define UDP_PORT 1234

#define SEND_INTERVAL		(20 * CLOCK_SECOND)
#define SEND_TIME		(random_rand() % (SEND_INTERVAL))

static struct simple_udp_connection broadcast_connection;

/*---------------------------------------------------------------------------*/
PROCESS(example_broadcast_process, "RIME Broadcast example");
PROCESS(broadcast_example_process, "IPv6 Broadcast example");
AUTOSTART_PROCESSES(&example_broadcast_process,&broadcast_example_process);
/*---------------------------------------------------------------------------*/
static void
broadcast_recv(struct broadcast_conn *c, const linkaddr_t *from)
{
  printf("<< RIME message received from %d.%d: '%s'\n",
         from->u8[0], from->u8[1], (char *)packetbuf_dataptr());
}
static const struct broadcast_callbacks broadcast_call = {broadcast_recv};
static struct broadcast_conn broadcast;
/*---------------------------------------------------------------------------*/

// ipv6 receiver code
static void
print_ipv6_addr(const uip_ipaddr_t *ip_addr) {
   int i;
   for (i = 0; i < 16; i++) {
       printf("%02x", ip_addr->u8[i]);
   }
}

static void
receiver(struct simple_udp_connection *c, 
         const uip_ipaddr_t *sender_addr,
         uint16_t sender_port,
         const uip_ipaddr_t *receiver_addr,
         uint16_t receiver_port,
         const uint8_t *data,
         uint16_t datalen)
{
    printf("<< IPv6 message received from [");
    print_ipv6_addr(sender_addr);
    printf("] Message: %s\n",data);
}

//static int stack = 0;


//RIME
PROCESS_THREAD(example_broadcast_process, ev, data)
{
  static struct etimer et;

  PROCESS_EXITHANDLER(broadcast_close(&broadcast);)

  PROCESS_BEGIN();
//printf("NETSTACK_CONF_WITH_RIME:%d",NETSTACK_CONF_WITH_RIME);
//printf("NEESTACK NAME:%s\n",NETSTACK_NETWORK.name);
  rime_driver.init();  //Befor broadcast OPEN
  broadcast_open(&broadcast, 129, &broadcast_call);


  while(1) {
//	stack = stack + 1;

//	printf("RIME stack: %d\n",stack);

	/* Delay 2-4 seconds */
	etimer_set(&et, CLOCK_SECOND * 4 + random_rand() % (CLOCK_SECOND * 4));

	PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&et));
 /*   if(stack==1){  
        rime_driver.init();
        rime_driver.input();
	broadcast_open(&broadcast, 129, &broadcast_call);
	printf("RIME INIT stack: %d\n",stack);
    } */

	packetbuf_copyfrom("RIME Hello", 11);
	broadcast_send(&broadcast);
	printf("RIME message sent =>\n");
  }

  PROCESS_END();
}

// ipv6 process

PROCESS_THREAD(broadcast_example_process, ev, data)
{
  static struct etimer periodic_timer;
  static struct etimer send_timer;
  uip_ipaddr_t addr;

  PROCESS_BEGIN();

//  printf("NEESTACK NAME:%s\n",NETSTACK_NETWORK.name);
  simple_udp_register(&broadcast_connection, UDP_PORT,
                      NULL, UDP_PORT,
                      receiver);
  sicslowpan_driver.init();

  etimer_set(&periodic_timer, SEND_INTERVAL);

  char msg[40];

  while(1) {
//	stack = stack + 1;
//	printf("IPV6 stsack: %d\n",stack);

	PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&periodic_timer));
	etimer_reset(&periodic_timer);
	etimer_set(&send_timer, SEND_TIME);

	PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&send_timer));

 /*   if(stack==20){  
        sicslowpan_driver.init();
        sicslowpan_driver.input();
        simple_udp_register(&broadcast_connection, UDP_PORT,
                      NULL, UDP_PORT,
                      receiver);
	printf("IPV6 INIT stack: %d\n",stack);
    } */

	uip_create_linklocal_allnodes_mcast(&addr);
	sprintf(msg, "ipv6 hello");

	printf("IPv6 message sent =>\n");
	simple_udp_sendto(&broadcast_connection, msg, strlen(msg), &addr);
  }

  PROCESS_END();
}

/*---------------------------------------------------------------------------*/
