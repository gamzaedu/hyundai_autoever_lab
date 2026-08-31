// 시각 / 숫자 표기 유틸

export function minutesSince(iso: string, asOf: string): number {
  const t = new Date(iso).getTime()
  const base = new Date(asOf).getTime()
  return (base - t) / 60000
}

export function formatTime(iso: string): string {
  const d = new Date(iso)
  const hh = String(d.getHours()).padStart(2, '0')
  const mm = String(d.getMinutes()).padStart(2, '0')
  return `${hh}:${mm}`
}

export function formatDateTime(iso: string): string {
  const d = new Date(iso)
  const mo = String(d.getMonth() + 1).padStart(2, '0')
  const dy = String(d.getDate()).padStart(2, '0')
  return `${mo}/${dy} ${formatTime(iso)}`
}

export function formatKm(km: number): string {
  return km.toLocaleString('ko-KR') + ' km'
}

export function formatPct(v: number | null): string {
  return v === null ? '-' : v.toFixed(1) + '%'
}
