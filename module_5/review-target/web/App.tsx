import { useEffect, useState } from 'react'
import type {
  FleetSnapshot,
  SortDir,
  SortKey,
  Trip,
  TripsData,
  Vehicle,
  VehicleStatus,
} from './types'
import { KpiCards } from './components/KpiCards'
import { FilterBar } from './components/FilterBar'
import { VehicleTable } from './components/VehicleTable'
import { DetailPanel } from './components/DetailPanel'
import { formatDateTime } from './lib/format'

export default function App() {
  const [snapshot, setSnapshot] = useState<FleetSnapshot | null>(null)
  const [tripsData, setTripsData] = useState<TripsData | null>(null)
  const [keyword, setKeyword] = useState('')
  const [statuses, setStatuses] = useState<VehicleStatus[]>([])
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [sortKey, setSortKey] = useState<SortKey | null>(null)
  const [sortDir, setSortDir] = useState<SortDir>('asc')

  useEffect(() => {
    Promise.all([
      fetch('/data/vehicles.json').then((r) => r.json() as Promise<FleetSnapshot>),
      fetch('/data/trips.json').then((r) => r.json() as Promise<TripsData>),
    ]).then(([v, t]) => {
      setSnapshot(v)
      setTripsData(t)
    })
  }, [])

  const computeFiltered = (): Vehicle[] => {
    if (!snapshot) return []
    const kw = keyword.trim().toLowerCase()

    let rows = snapshot.vehicles.filter((v) => {
      const hitKeyword =
        kw === '' ||
        v.plate.toLowerCase().includes(kw) ||
        v.model.toLowerCase().includes(kw) ||
        v.owner_dept.toLowerCase().includes(kw)
      const hitStatus = statuses.length === 0 || statuses.includes(v.status)
      return hitKeyword && hitStatus
    })

    if (sortKey) {
      const dir = sortDir === 'asc' ? 1 : -1
      rows = [...rows].sort((a, b) => {
        if (sortKey === 'last_seen') {
          return (new Date(a.last_seen).getTime() - new Date(b.last_seen).getTime()) * dir
        }
        const av = a[sortKey] ?? -1
        const bv = b[sortKey] ?? -1
        return ((av as number) - (bv as number)) * dir
      })
    }
    return rows
  }

  const filtered = computeFiltered()

  const toggleStatus = (s: VehicleStatus) =>
    setStatuses((prev) => (prev.includes(s) ? prev.filter((x) => x !== s) : [...prev, s]))

  const handleSort = (k: SortKey) => {
    if (sortKey === k) setSortDir((d) => (d === 'asc' ? 'desc' : 'asc'))
    else {
      setSortKey(k)
      setSortDir('asc')
    }
  }

  if (!snapshot || !tripsData) {
    return <div className="loading">데이터 로딩중…</div>
  }

  const selected = filtered.find((v) => v.vehicle_id === selectedId) ?? null
  const trips: Trip[] = selected ? tripsData.trips[selected.vehicle_id] ?? [] : []

  return (
    <div className="app">
      <header className="app-head">
        <h1>커넥티드카 관제 콘솔</h1>
        <span className="as-of">기준시각 {formatDateTime(snapshot.as_of)}</span>
      </header>

      <KpiCards vehicles={filtered} asOf={snapshot.as_of} />

      <FilterBar
        keyword={keyword}
        onKeyword={setKeyword}
        selected={statuses}
        onToggle={toggleStatus}
        matched={filtered.length}
      />

      <div className="content">
        <VehicleTable
          vehicles={filtered}
          asOf={snapshot.as_of}
          selectedId={selectedId}
          onSelect={setSelectedId}
          sortKey={sortKey}
          sortDir={sortDir}
          onSort={handleSort}
        />
        <DetailPanel vehicle={selected} trips={trips} asOf={snapshot.as_of} />
      </div>
    </div>
  )
}
