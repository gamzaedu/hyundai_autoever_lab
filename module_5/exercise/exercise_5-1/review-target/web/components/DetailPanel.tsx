import type { Trip, Vehicle } from '../types'
import { evaluateAlarms } from '../lib/alarms'
import { formatDateTime, formatKm, formatPct } from '../lib/format'

interface Props {
  vehicle: Vehicle | null
  trips: Trip[]
  asOf: string
}

export function DetailPanel({ vehicle, trips, asOf }: Props) {
  if (!vehicle) {
    return (
      <aside className="detail detail--empty">
        <p>목록에서 차량을 선택하세요.</p>
      </aside>
    )
  }

  const alarms = evaluateAlarms(vehicle, asOf)
  const warnBattery = vehicle.soc_pct !== null && vehicle.soc_pct < 15

  return (
    <aside className="detail">
      <header className="detail-head">
        <h2>{vehicle.plate}</h2>
        <p>
          {vehicle.model} · {vehicle.powertrain} · {vehicle.status}
        </p>
      </header>

      <dl className="detail-grid">
        <div>
          <dt>SOC</dt>
          <dd className={warnBattery ? 'soc--low' : undefined}>{formatPct(vehicle.soc_pct)}</dd>
        </div>
        <div>
          <dt>연료</dt>
          <dd>{formatPct(vehicle.fuel_pct)}</dd>
        </div>
        <div>
          <dt>주행거리</dt>
          <dd>{formatKm(vehicle.odometer_km)}</dd>
        </div>
        <div>
          <dt>최근 통신</dt>
          <dd>{formatDateTime(vehicle.last_seen)}</dd>
        </div>
        <div>
          <dt>위치</dt>
          <dd>{vehicle.location.name}</dd>
        </div>
        <div>
          <dt>담당부서</dt>
          <dd>{vehicle.owner_dept}</dd>
        </div>
      </dl>

      <section>
        <h3>알람</h3>
        {alarms.length === 0 ? (
          <p className="muted">정상</p>
        ) : (
          <ul className="alarm-list">
            {alarms.map((a) => (
              <li key={a.code} className={'alarm alarm--' + a.severity.toLowerCase()}>
                <strong>{a.code}</strong> {a.message}
              </li>
            ))}
          </ul>
        )}
      </section>

      <section>
        <h3>최근 주행 이력</h3>
        <table className="trip-table">
          <thead>
            <tr>
              <th>출발</th>
              <th>도착</th>
              <th>거리</th>
              <th>평균속도</th>
            </tr>
          </thead>
          <tbody>
            {trips.slice(0, 5).map((t) => (
              <tr key={t.started_at}>
                <td>{formatDateTime(t.started_at)}</td>
                <td>{formatDateTime(t.ended_at)}</td>
                <td className="num">{t.distance_km} km</td>
                <td className="num">{t.avg_speed_kph} km/h</td>
              </tr>
            ))}
            {trips.length === 0 && (
              <tr>
                <td colSpan={4} className="empty">
                  주행 이력 없음
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </section>
    </aside>
  )
}
