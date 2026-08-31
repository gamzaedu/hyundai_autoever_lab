export type Powertrain = 'EV' | 'HEV' | 'ICE'
export type VehicleStatus = 'DRIVING' | 'IDLE' | 'MAINTENANCE' | 'OFFLINE'

export interface Vehicle {
  vehicle_id: string
  plate: string
  model: string
  powertrain: Powertrain
  status: VehicleStatus
  soc_pct: number | null
  fuel_pct: number | null
  odometer_km: number
  last_seen: string
  location: { name: string; lat: number; lng: number }
  owner_dept: string
  dtc_codes: string[]
}

export interface Trip {
  started_at: string
  ended_at: string
  distance_km: number
  avg_speed_kph: number
  energy_kwh: number
}

export interface FleetSnapshot {
  as_of: string
  vehicles: Vehicle[]
}

export interface TripsData {
  as_of: string
  trips: Record<string, Trip[]>
}

export type AlarmCode = 'AL-01' | 'AL-02' | 'AL-03'
export type Severity = 'CRITICAL' | 'WARNING'

export interface Alarm {
  vehicle_id: string
  code: AlarmCode
  severity: Severity
  message: string
}

export type SortKey = 'soc_pct' | 'odometer_km' | 'last_seen'
export type SortDir = 'asc' | 'desc'
