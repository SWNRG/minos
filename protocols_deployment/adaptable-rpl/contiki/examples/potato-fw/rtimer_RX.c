/*
 * Copyright (c) 2015, Zolertia
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
 *         Potato RX
 * \author
 *         Aitor Mejias <amejias@zolertia.com>
 */

#include "contiki.h"
#include "cpu.h"
#include "sys/etimer.h"
#include "sys/rtimer.h"
#include "dev/scb.h"
#include "dev/leds.h"
#include "dev/uart.h"
#include "dev/button-sensor.h"
#include "dev/remote-sensors.h"
#include "dev/watchdog.h"
#include "dev/serial-line.h"
#include "dev/sys-ctrl.h"
#include "net/rime/broadcast.h"
#include "dev/antenna-sw.h"
#include "dev/tmp102.h"
#include "dev/radio.h"
#include "net/netstack.h"
#include "dev/cc2538-rf.h"
#include "lpm.h"
#include "reg.h"
#include "serial-ubidots.h"
#include <stdio.h>
#include <stdint.h>

#define  PERIOD_T     3 * RTIMER_SECOND
#define assert_wfi() do { asm("wfi"::); } while(0)
#define LOOP_INTERVAL       (CLOCK_SECOND)
#define BROADCAST_CHANNEL   129

static struct etimer et;
static struct rtimer my_timer;
static struct rtimer my_timer2;

void
send_to_ubidots(const char *api, const char *id, uint16_t *val)
{
  uint8_t i;
  unsigned char buf[6];
  printf("\r\n%s", api);
  printf("\t%s", id);
  for (i=0; i<UBIDOTS_MSG_16B_NUM; i++) {
    snprintf(buf, 6, "%04d", val[i]);
    printf("\t%s", buf);
  }
  printf("\r\n");
}


static void periodic_rtimer(struct rtimer *rt, void* ptr);

static uint16_t counter;

/*---------------------------------------------------------------------------*/
PROCESS(rtime_process_rx, "Realtimer RX");
AUTOSTART_PROCESSES(&rtime_process_rx);

static void
broadcast_recv(struct broadcast_conn *c, const linkaddr_t *from)
{
  int16_t bufRssi;
  leds_on(LEDS_BLUE);
  leds_toggle(LEDS_GREEN);
  bufRssi = packetbuf_attr(PACKETBUF_ATTR_RSSI);
//  printf("Received Packet\n");

  printf("*** Received %u bytes from %u:%u: '0x%04x',RSSI: %d LQI: %d\n", packetbuf_datalen(),
         from->u8[0], from->u8[1], *(uint16_t *)packetbuf_dataptr(),
         bufRssi, packetbuf_attr(PACKETBUF_ATTR_LINK_QUALITY));
  leds_off(LEDS_BLUE);
}

static const struct broadcast_callbacks bc_rx = { broadcast_recv };
static struct broadcast_conn bc;

static void
select_32_mhz_xosc(void)
{
  /*First, make sure there is no ongoing clock source change */
  while((REG(SYS_CTRL_CLOCK_STA) & SYS_CTRL_CLOCK_STA_SOURCE_CHANGE) != 0);
  /* Turn on the 32 MHz XOSC and source the system clock on it. */
  REG(SYS_CTRL_CLOCK_CTRL) &= ~SYS_CTRL_CLOCK_CTRL_OSC;
  /* Wait for the switch to take place */
  while((REG(SYS_CTRL_CLOCK_STA) & SYS_CTRL_CLOCK_STA_OSC) != 0);
  /* Power down the unused oscillator. */
  REG(SYS_CTRL_CLOCK_CTRL) |= SYS_CTRL_CLOCK_CTRL_OSC_PD;
}
/*---------------------------------------------------------------------------*/
static void
select_16_mhz_rcosc(void)
{
  /* Power up both oscillators in order to speed up the transition to the 32-MHz
   * XOSC after wake up.*/
  REG(SYS_CTRL_CLOCK_CTRL) &= ~SYS_CTRL_CLOCK_CTRL_OSC_PD;
  /*First, make sure there is no ongoing clock source change */
  while((REG(SYS_CTRL_CLOCK_STA) & SYS_CTRL_CLOCK_STA_SOURCE_CHANGE) != 0);
  /* Set the System Clock to use the 16MHz RC OSC */
  REG(SYS_CTRL_CLOCK_CTRL) |= SYS_CTRL_CLOCK_CTRL_OSC;
  /* Wait till it's happened */
  while((REG(SYS_CTRL_CLOCK_STA) & SYS_CTRL_CLOCK_STA_OSC) == 0);
}


static void ledOff(struct rtimer *rt, void* ptr){
  uint8_t ret;
  rtimer_clock_t time_now = RTIMER_NOW();

  leds_off(LEDS_RED);

  // Leave to minimum low power
  ret = rtimer_set(&my_timer, time_now + PERIOD_T, 1,
         (void (*)(struct rtimer *, void *))periodic_rtimer, NULL);

  select_16_mhz_rcosc();

  REG(SCB_SYSCTRL) |= SCB_SYSCTRL_SLEEPDEEP;
  REG(SYS_CTRL_PMCTL) = SYS_CTRL_PMCTL_PM2;

}

static void periodic_rtimer(struct rtimer *rt, void* ptr){
  uint8_t ret;
  select_32_mhz_xosc();
  rtimer_clock_t time_now = RTIMER_NOW();
  counter++;
  leds_on(LEDS_RED);

  ret = rtimer_set(&my_timer2, time_now + (RTIMER_SECOND/10), 1,
         (void (*)(struct rtimer *, void *))ledOff, NULL);
}

/*---------------------------------------------------------------------------*/
PROCESS_THREAD(rtime_process_rx, ev, data)
{

  PROCESS_BEGIN();

  counter = 0;

  // Select antenna external
  antenna_sw_select(ANTENNA_SW_SELECT_EXTERNAL);

  // Open and configure Port
  broadcast_open(&bc, BROADCAST_CHANNEL, &bc_rx);

  printf("rtimer_RX Starting...\n");

  while(1){
    PROCESS_YIELD();
  }
  PROCESS_END();  
}
/*---------------------------------------------------------------------------*/
