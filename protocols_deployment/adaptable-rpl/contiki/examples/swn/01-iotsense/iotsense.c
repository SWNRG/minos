/*
 * Copyright (c) 2012, Texas Instruments Incorporated - http://www.ti.com/
 * Copyright (c) 2015, Zolertia - http://www.zolertia.com
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
 *
 * 3. Neither the name of the copyright holder nor the names of its
 *    contributors may be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE
 * COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
 * STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
 * OF THE POSSIBILITY OF SUCH DAMAGE.
 */

/*---------------------------------------------------------------------------*/
#include "contiki.h"
#include "dev/adc-zoul.h"
#include "dev/zoul-sensors.h"
#include <stdio.h>
#include <stdint.h>
/*---------------------------------------------------------------------------*/
#define LOOP_PERIOD         8
#define LOOP_INTERVAL       (CLOCK_SECOND * LOOP_PERIOD)

/*---------------------------------------------------------------------------*/
static struct etimer et;
static uint16_t counter;
/*---------------------------------------------------------------------------*/
PROCESS(iotsens_process, "SWN NFVSDN HandsOn 1-1 process");
AUTOSTART_PROCESSES(&iotsens_process);

/*---------------------------------------------------------------------------*/
PROCESS_THREAD(iotsens_process, ev, data)
{
  PROCESS_BEGIN();

  counter = 0;

  /* Ports Configuration */
  adc_zoul.configure(SENSORS_HW_INIT, ZOUL_SENSORS_ADC_ALL);

  printf("SWN NFVSDN HandsOn 1-1 Contiki tutorial application\n");

  etimer_set(&et, LOOP_INTERVAL);

  while(1) {

    PROCESS_YIELD();

    if(ev == PROCESS_EVENT_TIMER) {

      printf("Measurement No: %04d - ", counter);

      printf("CPU Temperature = %02d.%02d ºC\n",
             cc2538_temp_sensor.value(CC2538_SENSORS_VALUE_TYPE_CONVERTED)/1000,
	     cc2538_temp_sensor.value(CC2538_SENSORS_VALUE_TYPE_CONVERTED)%1000);

      etimer_set(&et, LOOP_INTERVAL);

      counter++;

    } 
  }

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/


