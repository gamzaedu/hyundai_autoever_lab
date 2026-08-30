import type { VehicleStatus } from '../types'

const STATUS_OPTIONS: VehicleStatus[] = ['DRIVING', 'IDLE', 'MAINTENANCE', 'OFFLINE']

interface Props {
  keyword: string
  onKeyword: (v: string) => void
  selected: VehicleStatus[]
  onToggle: (s: VehicleStatus) => void
  matched: number
}

export function FilterBar({ keyword, onKeyword, selected, onToggle, matched }: Props) {
  return (
    <div className="filter-bar">
      <input
        className="search-input"
        type="search"
        placeholder="차량번호 / 차종 / 담당부서 검색"
        value={keyword}
        onChange={(e) => onKeyword(e.target.value)}
      />
      <div className="chip-group">
        {STATUS_OPTIONS.map((s) => (
          <button
            key={s}
            type="button"
            className={'chip' + (selected.includes(s) ? ' chip--on' : '')}
            onClick={() => onToggle(s)}
          >
            {s}
          </button>
        ))}
      </div>
      <span className="matched-count">{matched}대 표시중</span>
    </div>
  )
}
