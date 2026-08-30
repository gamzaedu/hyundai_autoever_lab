import type { SortDir, SortKey, Vehicle } from '../types'
import { evaluateAlarms, topSeverity } from '../lib/alarms'
import { formatDateTime, formatKm, formatPct, minutesSince } from '../lib/format'

interface Props {
  vehicles: Vehicle[]
  asOf: string
  selectedId: string | null
  onSelect: (id: string) => void
  sortKey: SortKey | null
  sortDir: SortDir
  onSort: (k: SortKey) => void
}

const COLUMNS: { key: SortKey | null; label: string }[] = [
  { key: null, label: '차량번호' },
  { key: null, label: '차종' },
  { key: null, label: '상태' },
  { key: 'soc_pct', label: 'SOC / 연료' },
  { key: 'odometer_km', label: '주행거리' },
  { key: 'last_seen', label: '최근 통신' },
  { key: null, label: '담당부서' },
  { key: null, label: '알람' },
]

export function VehicleTable({
  vehicles,
  asOf,
  selectedId,
  onSelect,
  sortKey,
  sortDir,
  onSort,
}: Props) {
  return (
    <div className="table-wrap">
      <table className="vehicle-table">
        <thead>
          <tr>
            {COLUMNS.map((c) => (
              <th
                key={c.label}
                className={c.key ? 'sortable' : undefined}
                onClick={() => c.key && onSort(c.key)}
              >
                {c.label}
                {c.key && sortKey === c.key ? (sortDir === 'asc' ? ' ▲' : ' ▼') : ''}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {vehicles.map((v) => {
            const alarms = evaluateAlarms(v, asOf)
            const sev = topSeverity(alarms)
            const stale = minutesSince(v.last_seen, asOf) > 30
            const lowSoc = v.soc_pct !== null && v.soc_pct < 15

            return (
              <tr
                key={v.vehicle_id}
                className={selectedId === v.vehicle_id ? 'row--selected' : undefined}
                onClick={() => onSelect(v.vehicle_id)}
              >
                <td className="mono">{v.plate}</td>
                <td>
                  {v.model}
                  <span className="ptr-tag">{v.powertrain}</span>
                </td>
                <td>
                  <span className={'status status--' + v.status.toLowerCase()}>{v.status}</span>
                </td>
                <td className={lowSoc ? 'soc soc--low' : 'soc'}>
                  {v.powertrain === 'ICE' ? formatPct(v.fuel_pct) : formatPct(v.soc_pct)}
                </td>
                <td className="num">{formatKm(v.odometer_km)}</td>
                <td className={stale ? 'stale' : undefined}>{formatDateTime(v.last_seen)}</td>
                <td>{v.owner_dept}</td>
                <td>
                  {sev && <span className={'badge badge--' + sev.toLowerCase()}>{alarms.length}</span>}
                </td>
              </tr>
            )
          })}
          {vehicles.length === 0 && (
            <tr>
              <td colSpan={COLUMNS.length} className="empty">
                조건에 맞는 차량이 없습니다.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
