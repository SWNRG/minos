/*
 * rpl-control.h
 * 
 * Copyright 2016 
 * Peter Ruckebusch (iMinds-UGent-IBCN) <peter.ruckebusch@intec.ugent.be>
 * Jo Van Damme (iMinds-UGent-IBCN) <jo.van.damme@intec.ugent.be>
 * 
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 * 
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 * 
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  
 * 02110-1301  USA.
 * 
 */

#include "rpl-control.h"

#if WISHFUL
  #include "param-repo.h"
  #include "wishful.h"
#endif

/*
 * Define the variables to replace the constants.
 * These must be defined even if WISHFUL is not defined in order for the protocols to work.
 */

uint8_t rpl_dio_interval_min = RPL_DIO_INTERVAL_MIN;
uint8_t rpl_dio_interval_doublings = RPL_DIO_INTERVAL_DOUBLINGS;
uint8_t rpl_dio_redundancy = RPL_DIO_REDUNDANCY;
uint8_t rpl_default_lifetime = RPL_DEFAULT_LIFETIME;

#if WISHFUL
	#define RPL_NUM_PARAMS 4

	/* Getter */
	void* 
	get_rpl_dio_interval_min(param_t* self)
	{
		return &rpl_dio_interval_min;
	}
	
	void* 
	get_rpl_dio_interval_doublings(param_t* self)
	{
		return &rpl_dio_interval_doublings;
	}

	void* 
	get_rpl_dio_redundancy(param_t* self)
	{
		return &rpl_dio_redundancy;
	}

	void* 
	get_rpl_default_lifetime(param_t* self)
	{
		return &rpl_default_lifetime;
	}


	/* Setter */
	error_t 
	set_rpl_dio_interval_min(param_t* self, void* new_value, const uint8_t new_value_len)
	{

		if (new_value_len != sizeof(uint8_t)){
	  		return EINVAL;
		}
		memcpy(&rpl_dio_interval_min, new_value, new_value_len);

		struct rpl_instance *instance, *end;
		for(instance = &instance_table[0], end = instance + RPL_MAX_INSTANCES;instance < end; ++instance){
	  		if(instance->used){
	    		memcpy(&instance->dio_intmin, new_value, new_value_len);
	  		}
		}

		return SUCCESS;
	}

	error_t 
	set_rpl_dio_interval_doublings(param_t* self, void* new_value, const uint8_t new_value_len)
	{

		if (new_value_len != sizeof(uint8_t)){
	  		return EINVAL;
		}
		memcpy(&rpl_dio_interval_doublings, new_value, new_value_len);

		struct rpl_instance *instance, *end;
		for(instance = &instance_table[0], end = instance + RPL_MAX_INSTANCES;instance < end; ++instance){
	  		if(instance->used){
	    		memcpy(&instance->dio_intdoubl, new_value, new_value_len);
	  		}
		}

		return SUCCESS;
	}

	error_t 
	set_rpl_dio_redundancy(param_t* self, void* new_value, const uint8_t new_value_len)
	{

		if (new_value_len != sizeof(uint8_t)){
	  		return EINVAL;
		}
		memcpy(&rpl_dio_redundancy, new_value, new_value_len);

		struct rpl_instance *instance, *end;
		for(instance = &instance_table[0], end = instance + RPL_MAX_INSTANCES;instance < end; ++instance){
	  		if(instance->used){
	    		memcpy(&instance->dio_redundancy, new_value, new_value_len);
	  		}
		}

		return SUCCESS;
	}

	error_t 
	set_rpl_default_lifetime(param_t* self, void* new_value, const uint8_t new_value_len)
	{

		if (new_value_len != sizeof(uint8_t)){
	  		return EINVAL;
		}
		memcpy(&rpl_default_lifetime, new_value, new_value_len);

		struct rpl_instance *instance, *end;
		for(instance = &instance_table[0], end = instance + RPL_MAX_INSTANCES;instance < end; ++instance){
	  		if(instance->used){
	    		memcpy(&instance->default_lifetime, new_value, new_value_len);
	  		}
		}

		return SUCCESS;
	}

	/*  Define parameter to add to the param-repo. */
	PARAMETER_UINT8(p_rpl_dio_interval_min, 99, get_rpl_dio_interval_min, set_rpl_dio_interval_min);
	PARAMETER_UINT8(p_rpl_dio_interval_doublings, 100, get_rpl_dio_interval_doublings, set_rpl_dio_interval_doublings);
	PARAMETER_UINT8(p_rpl_dio_redundancy, 101, get_rpl_dio_redundancy, set_rpl_dio_redundancy);
	PARAMETER_UINT8(p_rpl_default_lifetime, 102, get_rpl_default_lifetime, set_rpl_default_lifetime);

	void 
	wishul_rpl_init()
	{
		/* Add parameters to the default set or add the constructed set to the param-repo. */
		param_repo_add_parameter(&p_rpl_dio_interval_min);
		param_repo_add_parameter(&p_rpl_dio_interval_doublings);
		param_repo_add_parameter(&p_rpl_dio_redundancy);
		param_repo_add_parameter(&p_rpl_default_lifetime);
	}

#endif
