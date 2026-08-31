import type { Alarm, Severity, Vehicle } from '../types'
import { minutesSince } from './format'

// 알람 판정 (PRD 5장 AL-01 ~ AL-03)
export function evaluateAlarms(v: Vehicle, asOf: string): Alarm[] {
  const list: Alarm[] = []

  // AL-01 배터리 부족
  if (v.powertrain === 'EV' && v.soc_pct !== null && v.soc_pct < 15) {
    list.push({
      vehicle_id: v.vehicle_id,
      code: 'AL-01',
      severity: 'CRITICAL',
      message: `배터리 부족 (${v.soc_pct}%)`,
    })
  }

  // AL-02 정비 필요
  if (v.status === 'MAINTENANCE' || v.dtc_codes.length > 0) {
    const detail = v.dtc_codes.length > 0 ? v.dtc_codes.join(', ') : '정비 입고 대상'
    list.push({
      vehicle_id: v.vehicle_id,
      code: 'AL-02',
      severity: 'WARNING',
      message: `정비 필요 (${detail})`,
    })
  }

  // AL-03 통신 두절
  if (minutesSince(v.last_seen, asOf) > 30) {
    list.push({
      vehicle_id: v.vehicle_id,
      code: 'AL-03',
      severity: 'CRITICAL',
      message: `통신 두절 (${Math.round(minutesSince(v.last_seen, asOf))}분 경과)`,
    })
  }

  return list
}

export function collectAlarms(vehicles: Vehicle[], asOf: string): Alarm[] {
  return vehicles.flatMap((v) => evaluateAlarms(v, asOf))
}

// KPI 용: 알람이 하나라도 있는 차량 수 (차량 기준 중복 제거)
export function countAlarmVehicles(vehicles: Vehicle[], asOf: string): number {
  return vehicles.filter((v) => evaluateAlarms(v, asOf).length > 0).length
}

export function topSeverity(alarms: Alarm[]): Severity | null {
  if (alarms.length === 0) return null
  return alarms.some((a) => a.severity === 'CRITICAL') ? 'CRITICAL' : 'WARNING'
}
