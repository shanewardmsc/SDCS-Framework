PROGRAM Machine_Statistics
  VAR
    TotalDowntime_s AT %QW0 : INT := 0;
    TotalParts AT %QW1 : INT := 0;
    RejectedParts AT %QW2 : INT := 0;
    TotalRuntime_s AT %QW3 : INT := 0;
    GoodParts AT %QW4 : INT := 0;
    ProductVariant AT %QW5 : INT := 10;
    IdealCycleTime_s AT %MD0 : REAL := 2.0;
    PlannedProductionTime_REAL AT %MD1 : REAL := 3600.0;
    Availability AT %MD2 : REAL := 0.0;
    Performance AT %MD3 : REAL := 0.0;
    Quality AT %MD4 : REAL := 0.0;
    OEE AT %MD5 : REAL := 0.0;
    MachineRunning AT %QX0.0 : BOOL := FALSE;
    AlarmActive AT %QX0.1 : BOOL := FALSE;
  END_VAR
  VAR
    StartCycle : BOOL := FALSE;
    RejectDetected : BOOL := FALSE;
    StartCycleTimer : TON;
    RejectTimer : TON;
    CycleTimer_ms : TON;
    TickCounter : INT := 0;
    RandomValue : INT := 0;
    DowntimeTimer : TON;
    RuntimeTimer : TON;
    TON_Cycle : TIME := T#500ms;
    TON_Cycle_Preset : TIME := T#200ms;
    TON_Reject : TIME := T#200ms;
    TON_Runtime : TIME := T#1s;
    TON_Downtime : TIME := T#1s;
    MaxCycleTime_ms : TIME := T#1s;
    CycleCounter : INT := 0;
    RejectRate : REAL := 0.0;
    RejectedParts_REAL : REAL := 0.0;
    TotalParts_REAL : REAL := 0.0;
    GoodParts_REAL : REAL := 0.0;
    TotalRuntime_REAL : REAL := 0.0;
    Alarm_HighRejectRate : BOOL := FALSE;
    Alarm_CycleTimeExceeded : BOOL := FALSE;
  END_VAR

  TickCounter := TickCounter + 1;
  IF TickCounter MOD 10 = 0 THEN
      RandomValue := TickCounter MOD 7;
      IF RandomValue < 5 THEN
          StartCycleTimer(IN := TRUE, PT := TON_Cycle);
      END_IF;
  END_IF;

  (* Start cycle detection *)
  IF StartCycleTimer.Q THEN
      StartCycle := TRUE;
      StartCycleTimer(IN := FALSE);
  ELSE
      StartCycle := FALSE;
  END_IF;

  (* Trigger reject occasionally *)
  (*IF StartCycle THEN*)
  IF CycleCounter MOD 4 = 0 THEN
    RejectTimer(IN := TRUE, PT := TON_Reject);
  END_IF;
  (*    END_IF;*)


  IF RejectTimer.Q THEN
      RejectDetected := TRUE;
      RejectTimer(IN := FALSE);
  ELSE
      RejectDetected := FALSE;
  END_IF;

  (* Cycle process *)
  MachineRunning := StartCycle OR MachineRunning;

  IF StartCycle THEN
      CycleTimer_ms(IN := TRUE, PT := TON_CYCLE_PRESET);
  ELSE
      IF CycleTimer_ms.Q THEN
          CycleTimer_ms(IN := FALSE);
          CycleCounter := CycleCounter + 1;
          TotalParts := TotalParts + 1;

          IF NOT RejectDetected THEN
              GoodParts := GoodParts + 1;
          ELSE
              RejectedParts := RejectedParts + 1;
          END_IF;
      END_IF;
  END_IF;

  (* Runtime timer *)
  RuntimeTimer(IN := MachineRunning, PT := TON_Runtime);
  IF RuntimeTimer.Q THEN
      TotalRuntime_s := TotalRuntime_s + 1;
      RuntimeTimer(IN := FALSE);
  END_IF;

  (* Downtime timer *)
  DowntimeTimer(IN := NOT MachineRunning, PT := TON_Downtime);
  IF DowntimeTimer.Q THEN
      TotalDowntime_s := TotalDowntime_s + 1;
      DowntimeTimer(IN := FALSE);
  END_IF;

  (* Alarms *)
  IF TotalParts > 10 THEN
      RejectedParts_REAL := INT_TO_REAL(IN := RejectedParts);
      TotalParts_REAL := INT_TO_REAL(IN := TotalParts);

      RejectRate := RejectedParts_REAL / TotalParts_REAL;
      IF RejectRate > 0.2 THEN
          Alarm_HighRejectRate := TRUE;
      ELSE
          Alarm_HighRejectRate := FALSE;
      END_IF;
  END_IF;

  IF CycleTimer_ms.ET > MaxCycleTime_ms THEN
      Alarm_CycleTimeExceeded := TRUE;
  ELSE
      Alarm_CycleTimeExceeded := FALSE;
  END_IF;

  IF ALARM_HIGHREJECTRATE OR ALARM_CYCLETIMEEXCEEDED THEN
    ALARMACTIVE := TRUE;
  ELSE
    ALARMACTIVE := FALSE;
  END_IF;

  (* OEE Calculations *)
  IF TotalParts > 0 AND TotalRuntime_s > 0 THEN
      GoodParts_REAL := INT_TO_REAL(IN := GoodParts);

      TotalRuntime_REAL := INT_TO_REAL(IN := TotalRuntime_s);

      Quality := GoodParts_REAL / TotalParts_REAL;
      Performance := (IdealCycleTime_s * TotalParts_REAL) / TotalRuntime_REAL;
      Availability := TotalRuntime_REAL / PlannedProductionTime_REAL;
      OEE := Availability * Performance * Quality;
  END_IF;
END_PROGRAM


CONFIGURATION Config0

  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : Machine_Statistics;
  END_RESOURCE
END_CONFIGURATION

(*DBG:char md5[] = "ac38cd3c0fe6ae9e21f5e6fc5278a8e4";*)
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
(*DBG:    {&(RES0__INSTANCE0.TOTALDOWNTIME_S), INT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TOTALPARTS), INT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.REJECTEDPARTS), INT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TOTALRUNTIME_S), INT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.GOODPARTS), INT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.PRODUCTVARIANT), INT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.IDEALCYCLETIME_S), REAL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.PLANNEDPRODUCTIONTIME_REAL), REAL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.AVAILABILITY), REAL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.PERFORMANCE), REAL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.QUALITY), REAL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.OEE), REAL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.MACHINERUNNING), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.ALARMACTIVE), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.STARTCYCLE), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.REJECTDETECTED), BOOL_ENUM},*)
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
(*DBG:    {&(RES0__INSTANCE0.TICKCOUNTER), INT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.RANDOMVALUE), INT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.DOWNTIMETIMER.EN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.DOWNTIMETIMER.ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.DOWNTIMETIMER.IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.DOWNTIMETIMER.PT), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.DOWNTIMETIMER.Q), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.DOWNTIMETIMER.ET), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.DOWNTIMETIMER.STATE), SINT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.DOWNTIMETIMER.PREV_IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.DOWNTIMETIMER.CURRENT_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.DOWNTIMETIMER.START_TIME), TIME_ENUM},*)
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
(*DBG:    {&(RES0__INSTANCE0.TON_CYCLE), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TON_CYCLE_PRESET), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TON_REJECT), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TON_RUNTIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TON_DOWNTIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.MAXCYCLETIME_MS), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.CYCLECOUNTER), INT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.REJECTRATE), REAL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.REJECTEDPARTS_REAL), REAL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TOTALPARTS_REAL), REAL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.GOODPARTS_REAL), REAL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TOTALRUNTIME_REAL), REAL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.ALARM_HIGHREJECTRATE), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.ALARM_CYCLETIMEEXCEEDED), BOOL_ENUM},*)
(*DBG:};*)
(*DBG:*)
(*DBG:#define VAR_COUNT               82*)
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
(*DBG:    case SINT_ENUM:*)
(*DBG:        return sizeof(SINT);*)
(*DBG:    case BOOL_ENUM:*)
(*DBG:        return sizeof(BOOL);*)
(*DBG:    case REAL_ENUM:*)
(*DBG:        return sizeof(REAL);*)
(*DBG:    case TIME_ENUM:*)
(*DBG:        return sizeof(TIME);*)
(*DBG:    case INT_ENUM:*)
(*DBG:        return sizeof(INT);*)
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
(*DBG:    case SINT_ENUM:*)
(*DBG:        return (void *)&((__IEC_SINT_t *) ptr)->value;*)
(*DBG:    case BOOL_ENUM:*)
(*DBG:        return (void *)&((__IEC_BOOL_t *) ptr)->value;*)
(*DBG:    case REAL_ENUM:*)
(*DBG:        return (void *)&((__IEC_REAL_t *) ptr)->value;*)
(*DBG:    case TIME_ENUM:*)
(*DBG:        return (void *)&((__IEC_TIME_t *) ptr)->value;*)
(*DBG:    case INT_ENUM:*)
(*DBG:        return (void *)&((__IEC_INT_t *) ptr)->value;*)
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
(*DBG:        case SINT_ENUM: {*)
(*DBG:            memcpy(&((__IEC_SINT_t *) ptr)->value, val, var_size);*)
(*DBG:            //((__IEC_SINT_t *) ptr)->value = *((SINT *) val);*)
(*DBG:            ((__IEC_SINT_t *) ptr)->flags |= __IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        }*)
(*DBG:        case BOOL_ENUM: {*)
(*DBG:            memcpy(&((__IEC_BOOL_t *) ptr)->value, val, var_size);*)
(*DBG:            //((__IEC_BOOL_t *) ptr)->value = *((BOOL *) val);*)
(*DBG:            ((__IEC_BOOL_t *) ptr)->flags |= __IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        }*)
(*DBG:        case REAL_ENUM: {*)
(*DBG:            memcpy(&((__IEC_REAL_t *) ptr)->value, val, var_size);*)
(*DBG:            //((__IEC_REAL_t *) ptr)->value = *((REAL *) val);*)
(*DBG:            ((__IEC_REAL_t *) ptr)->flags |= __IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        }*)
(*DBG:        case TIME_ENUM: {*)
(*DBG:            memcpy(&((__IEC_TIME_t *) ptr)->value, val, var_size);*)
(*DBG:            //((__IEC_TIME_t *) ptr)->value = *((TIME *) val);*)
(*DBG:            ((__IEC_TIME_t *) ptr)->flags |= __IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        }*)
(*DBG:        case INT_ENUM: {*)
(*DBG:            memcpy(&((__IEC_INT_t *) ptr)->value, val, var_size);*)
(*DBG:            //((__IEC_INT_t *) ptr)->value = *((INT *) val);*)
(*DBG:            ((__IEC_INT_t *) ptr)->flags |= __IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        }*)
(*DBG:        default:*)
(*DBG:            break;*)
(*DBG:        }*)
(*DBG:    } else {*)
(*DBG:        switch (debug_vars[idx].type) {*)
(*DBG:        case SINT_ENUM:*)
(*DBG:            ((__IEC_SINT_t *) ptr)->flags &= ~__IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        case BOOL_ENUM:*)
(*DBG:            ((__IEC_BOOL_t *) ptr)->flags &= ~__IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        case REAL_ENUM:*)
(*DBG:            ((__IEC_REAL_t *) ptr)->flags &= ~__IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        case TIME_ENUM:*)
(*DBG:            ((__IEC_TIME_t *) ptr)->flags &= ~__IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        case INT_ENUM:*)
(*DBG:            ((__IEC_INT_t *) ptr)->flags &= ~__IEC_FORCE_FLAG;*)
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