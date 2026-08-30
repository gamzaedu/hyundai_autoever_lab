import type { Vehicle } from '../types'
import { countAlarmVehicles } from '../lib/alarms'

interface Props {
  vehicles: Vehicle[]
  asOf: string
}

export function KpiCards({ vehicles, asOf }: Props) {
  const total = vehicles.length
  const driving = vehicles.filter((v) => v.status === 'DRIVING').length

  const evs = vehicles.filter((v) => v.powertrain === 'EV' && v.soc_pct !== null)
  const avgSoc = evs.length === 0 ? 0 : evs.reduce((s, v) => s + (v.soc_pct as number), 0) / evs.length

  const alarmCount = countAlarmVehicles(vehicles, asOf)

  const cards = [
    { label: '총 대수', value: String(total), unit: '대' },
    { label: '운행중', value: String(driving), unit: '대' },
    { label: 'EV 평균 SOC', value: avgSoc.toFixed(1), unit: '%' },
    { label: '알람 차량', value: String(alarmCount), unit: '대', danger: alarmCount > 0 },
  ]

  return (
    <div className="kpi-row">
      {cards.map((c) => (
        <div key={c.label} className={'kpi-card' + (c.danger ? ' kpi-card--danger' : '')}>
          <span className="kpi-label">{c.label}</span>
          <span className="kpi-value">
            {c.value}
            <em>{c.unit}</em>
          </span>
        </div>
      ))}
    </div>
  )
}
