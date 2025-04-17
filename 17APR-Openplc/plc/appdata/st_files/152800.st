PROGRAM Machine_Statistics
  VAR
    CycleCounter AT %QW0 : INT := 0;
    GoodParts AT %QW1 : INT := 0;
    RejectedParts AT %QW2 : INT := 0;
    CycleTime_ms AT %QW3 : INT := 0;
    TotalRuntime_s AT %QW4 : INT := 0;
    MachineRunning AT %QX0.0 : BOOL := FALSE;
    StartCycle AT %QX0.1 : BOOL;
    RejectDetected AT %QX0.2 : BOOL;
  END_VAR
  VAR
    CycleTimer_ms : TON;
    RuntimeTimer : TON;
    StartCycleTimer : TON;
    RejectTimer : TON;
    TON_Cycle : TIME;
    TON_Reject : TIME;
    TON_ms : TIME;
    TON_Runtime : TIME;
  END_VAR


  StartCycleTimer(IN := TRUE, PT := TON_Cycle);
  IF StartCycleTimer.Q THEN
      StartCycle := TRUE;
      StartCycleTimer(IN := FALSE);  
  ELSE
      StartCycle := FALSE;
  END_IF;


  RejectTimer(IN := TRUE, PT := TON_Reject);
  IF RejectTimer.Q THEN
      RejectDetected := TRUE;
      RejectTimer(IN := FALSE);     
  ELSE
      RejectDetected := FALSE;
  END_IF;


  MachineRunning := StartCycle OR MachineRunning;
  IF StartCycle THEN
      CycleTimer_ms(IN := TRUE);
  ELSE
      IF CycleTimer_ms.Q THEN
          CycleTimer_ms(IN := FALSE);   
          CycleCounter := CycleCounter + 1;

          IF NOT RejectDetected THEN
              GoodParts := GoodParts + 1;
          ELSE
              RejectedParts := RejectedParts + 1;
          END_IF;
      END_IF;
  END_IF;


  RuntimeTimer(IN := MachineRunning, PT := TON_Runtime);
  IF RuntimeTimer.Q THEN
      TotalRuntime_s := TotalRuntime_s + 1;
      RuntimeTimer(IN := FALSE);
  END_IF;
END_PROGRAM


CONFIGURATION Config0

  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : Machine_Statistics;
  END_RESOURCE
END_CONFIGURATION

(*DBG:char md5[] = "9bd625652d7864cbe1dcf2e416e2dcd5";*)
(*DBG:/**)
(*DBG: * This file is part of OpenPLC Runtime*)
(*DBG: **)
(*DBG: * Copyright (C) 2023 Autonomy, GP Orcullo*)
(*DBG: * Based on the work by GP Orcullo on Beremiz for uC*)
(*DBG: **)
(*DBG: * This program is free software; you can redistribute it and/or*)
(*DBG: * modify it under the terms of the GNU General Public License*)
(*DBG: * as published by the Free Software Foundation; either version 2*)
(*DBG: * of the License, or (at your option) any later version.*)
(*DBG: **)
(*DBG: * This program is distributed in the hope that it will be useful,*)
(*DBG: * but WITHOUT ANY WARRANTY; without even the implied warranty of*)
(*DBG: * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the*)
(*DBG: * GNU General Public License for more details.*)
(*DBG: **)
(*DBG: * You should have received a copy of the GNU General Public License*)
(*DBG: * along with this program; If not, see <http://www.gnu.org/licenses/>.*)
(*DBG: **)
(*DBG: */*)
(*DBG:*)
(*DBG:#include <stdbool.h>*)
(*DBG:*)
(*DBG:#include "iec_types_all.h"*)
(*DBG:#include "POUS.h"*)
(*DBG:*)
(*DBG:#define SAME_ENDIANNESS      0*)
(*DBG:#define REVERSE_ENDIANNESS   1*)
(*DBG:*)
(*DBG:uint8_t endianness;*)
(*DBG:*)
(*DBG:*)
(*DBG:extern MACHINE_STATISTICS RES0__INSTANCE0;*)
(*DBG:*)
(*DBG:static const struct {*)
(*DBG:    void *ptr;*)
(*DBG:    __IEC_types_enum type;*)
(*DBG:} debug_vars[] = {*)
(*DBG:    {&(RES0__INSTANCE0.CYCLECOUNTER), INT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.GOODPARTS), INT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.REJECTEDPARTS), INT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.CYCLETIME_MS), INT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TOTALRUNTIME_S), INT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.MACHINERUNNING), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.STARTCYCLE), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.REJECTDETECTED), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.CYCLETIMER_MS.EN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.CYCLETIMER_MS.ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.CYCLETIMER_MS.IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.CYCLETIMER_MS.PT), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.CYCLETIMER_MS.Q), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.CYCLETIMER_MS.ET), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.CYCLETIMER_MS.STATE), SINT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.CYCLETIMER_MS.PREV_IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.CYCLETIMER_MS.CURRENT_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.CYCLETIMER_MS.START_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.RUNTIMETIMER.EN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.RUNTIMETIMER.ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.RUNTIMETIMER.IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.RUNTIMETIMER.PT), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.RUNTIMETIMER.Q), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.RUNTIMETIMER.ET), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.RUNTIMETIMER.STATE), SINT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.RUNTIMETIMER.PREV_IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.RUNTIMETIMER.CURRENT_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.RUNTIMETIMER.START_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.STARTCYCLETIMER.EN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.STARTCYCLETIMER.ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.STARTCYCLETIMER.IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.STARTCYCLETIMER.PT), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.STARTCYCLETIMER.Q), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.STARTCYCLETIMER.ET), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.STARTCYCLETIMER.STATE), SINT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.STARTCYCLETIMER.PREV_IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.STARTCYCLETIMER.CURRENT_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.STARTCYCLETIMER.START_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.REJECTTIMER.EN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.REJECTTIMER.ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.REJECTTIMER.IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.REJECTTIMER.PT), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.REJECTTIMER.Q), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.REJECTTIMER.ET), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.REJECTTIMER.STATE), SINT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.REJECTTIMER.PREV_IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.REJECTTIMER.CURRENT_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.REJECTTIMER.START_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TON_CYCLE), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TON_REJECT), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TON_MS), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TON_RUNTIME), TIME_ENUM},*)
(*DBG:};*)
(*DBG:*)
(*DBG:#define VAR_COUNT               52*)
(*DBG:*)
(*DBG:uint16_t get_var_count(void)*)
(*DBG:{*)
(*DBG:    return VAR_COUNT;*)
(*DBG:}*)
(*DBG:*)
(*DBG:size_t get_var_size(size_t idx)*)
(*DBG:{*)
(*DBG:    if (idx >= VAR_COUNT)*)
(*DBG:    {*)
(*DBG:        return 0;*)
(*DBG:    }*)
(*DBG:    switch (debug_vars[idx].type) {*)
(*DBG:    case TIME_ENUM:*)
(*DBG:        return sizeof(TIME);*)
(*DBG:    case BOOL_ENUM:*)
(*DBG:        return sizeof(BOOL);*)
(*DBG:    case INT_ENUM:*)
(*DBG:        return sizeof(INT);*)
(*DBG:    case SINT_ENUM:*)
(*DBG:        return sizeof(SINT);*)
(*DBG:    default:*)
(*DBG:        return 0;*)
(*DBG:    }*)
(*DBG:}*)
(*DBG:*)
(*DBG:void *get_var_addr(size_t idx)*)
(*DBG:{*)
(*DBG:    void *ptr = debug_vars[idx].ptr;*)
(*DBG:*)
(*DBG:    switch (debug_vars[idx].type) {*)
(*DBG:    case TIME_ENUM:*)
(*DBG:        return (void *)&((__IEC_TIME_t *) ptr)->value;*)
(*DBG:    case BOOL_ENUM:*)
(*DBG:        return (void *)&((__IEC_BOOL_t *) ptr)->value;*)
(*DBG:    case INT_ENUM:*)
(*DBG:        return (void *)&((__IEC_INT_t *) ptr)->value;*)
(*DBG:    case SINT_ENUM:*)
(*DBG:        return (void *)&((__IEC_SINT_t *) ptr)->value;*)
(*DBG:    default:*)
(*DBG:        return 0;*)
(*DBG:    }*)
(*DBG:}*)
(*DBG:*)
(*DBG:void force_var(size_t idx, bool forced, void *val)*)
(*DBG:{*)
(*DBG:    void *ptr = debug_vars[idx].ptr;*)
(*DBG:*)
(*DBG:    if (forced) {*)
(*DBG:        size_t var_size = get_var_size(idx);*)
(*DBG:        switch (debug_vars[idx].type) {*)
(*DBG:        case TIME_ENUM: {*)
(*DBG:            memcpy(&((__IEC_TIME_t *) ptr)->value, val, var_size);*)
(*DBG:            //((__IEC_TIME_t *) ptr)->value = *((TIME *) val);*)
(*DBG:            ((__IEC_TIME_t *) ptr)->flags |= __IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        }*)
(*DBG:        case BOOL_ENUM: {*)
(*DBG:            memcpy(&((__IEC_BOOL_t *) ptr)->value, val, var_size);*)
(*DBG:            //((__IEC_BOOL_t *) ptr)->value = *((BOOL *) val);*)
(*DBG:            ((__IEC_BOOL_t *) ptr)->flags |= __IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        }*)
(*DBG:        case INT_ENUM: {*)
(*DBG:            memcpy(&((__IEC_INT_t *) ptr)->value, val, var_size);*)
(*DBG:            //((__IEC_INT_t *) ptr)->value = *((INT *) val);*)
(*DBG:            ((__IEC_INT_t *) ptr)->flags |= __IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        }*)
(*DBG:        case SINT_ENUM: {*)
(*DBG:            memcpy(&((__IEC_SINT_t *) ptr)->value, val, var_size);*)
(*DBG:            //((__IEC_SINT_t *) ptr)->value = *((SINT *) val);*)
(*DBG:            ((__IEC_SINT_t *) ptr)->flags |= __IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        }*)
(*DBG:        default:*)
(*DBG:            break;*)
(*DBG:        }*)
(*DBG:    } else {*)
(*DBG:        switch (debug_vars[idx].type) {*)
(*DBG:        case TIME_ENUM:*)
(*DBG:            ((__IEC_TIME_t *) ptr)->flags &= ~__IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        case BOOL_ENUM:*)
(*DBG:            ((__IEC_BOOL_t *) ptr)->flags &= ~__IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        case INT_ENUM:*)
(*DBG:            ((__IEC_INT_t *) ptr)->flags &= ~__IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        case SINT_ENUM:*)
(*DBG:            ((__IEC_SINT_t *) ptr)->flags &= ~__IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        default:*)
(*DBG:            break;*)
(*DBG:        }*)
(*DBG:    }*)
(*DBG:}*)
(*DBG:*)
(*DBG:void swap_bytes(void *ptr, size_t size) *)
(*DBG:{*)
(*DBG:    uint8_t *bytePtr = (uint8_t *)ptr;*)
(*DBG:    size_t i;*)
(*DBG:    for (i = 0; i < size / 2; ++i) *)
(*DBG:    {*)
(*DBG:        uint8_t temp = bytePtr[i];*)
(*DBG:        bytePtr[i] = bytePtr[size - 1 - i];*)
(*DBG:        bytePtr[size - 1 - i] = temp;*)
(*DBG:    }*)
(*DBG:}*)
(*DBG:*)
(*DBG:void trace_reset(void)*)
(*DBG:{*)
(*DBG:    for (size_t i=0; i < VAR_COUNT; i++) *)
(*DBG:    {*)
(*DBG:        force_var(i, false, 0);*)
(*DBG:    }*)
(*DBG:}*)
(*DBG:*)
(*DBG:void set_trace(size_t idx, bool forced, void *val)*)
(*DBG:{*)
(*DBG:    if (idx >= 0 && idx < VAR_COUNT) *)
(*DBG:    {*)
(*DBG:        if (endianness == REVERSE_ENDIANNESS)*)
(*DBG:        {*)
(*DBG:            // Aaaaarghhhh... Stupid AVR is Big Endian.*)
(*DBG:            swap_bytes(val, get_var_size(idx));*)
(*DBG:        }*)
(*DBG:*)
(*DBG:        force_var(idx, forced, val);*)
(*DBG:    }*)
(*DBG:}*)
(*DBG:*)
(*DBG:void set_endianness(uint8_t value)*)
(*DBG:{*)
(*DBG:    if (value == SAME_ENDIANNESS || value == REVERSE_ENDIANNESS)*)
(*DBG:    {*)
(*DBG:        endianness = value;*)
(*DBG:    }*)
(*DBG:}*)
(*DBG:*)
