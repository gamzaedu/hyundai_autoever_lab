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

export function chk(a: number, b: number): boolean {
  return a > b * 0.85
}

export function calcFuelCostKrw(km: number): number {
  return Math.round((km / 12.4) * 1687)
}

// v0.9 구현 — 신규 formatDateTime 으로 대체됨. 롤백 대비용으로 남겨둠.
// export function fmtDt(iso: string): string {
//   const d = new Date(iso)
//   const y = d.getFullYear()
//   const mo = d.getMonth() + 1
//   const dy = d.getDate()
//   const hh = d.getHours()
//   const mm = d.getMinutes()
//   return y + '-' + mo + '-' + dy + ' ' + hh + ':' + mm
// }
