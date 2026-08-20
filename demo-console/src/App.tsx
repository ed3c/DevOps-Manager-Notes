import { useEffect, useMemo, useRef } from 'react'
import { useQuery } from '@tanstack/react-query'
import * as echarts from 'echarts'

type EvidenceState = 'PASS' | 'FAIL' | 'ABSENT' | 'NOT_IMPLEMENTED' | 'NOT_EXERCISED' | 'SKIPPED_BY_POLICY' | 'HUMAN_ADMIT_REQUIRED'
type EvidenceRecord = Record<string, unknown> & { id?: string; state?: EvidenceState; verdict?: EvidenceState; capability?: string; claim?: string }
type GapRecord = Record<string, unknown> & { id?: string; state?: EvidenceState; description?: string; requirement?: string }
type EvidenceIndex = {
  schemaVersion: string
  generatedFrom: string[]
  records: EvidenceRecord[]
  gaps: GapRecord[]
  publicClaimRules: string[]
}

const sections = [
  ['overview', 'Overview', ['platform', 'delivery', 'evidence']],
  ['model', 'Model Lifecycle', ['model', 'llm', 'eval', 'prompt']],
  ['delivery', 'Delivery', ['deploy', 'kubernetes', 'docker', 'ci']],
  ['reliability', 'Reliability', ['slo', 'load', 'latency', 'capacity', 'observability']],
  ['security', 'Security', ['security', 'policy', 'license', 'sbom', 'signature']],
  ['incident', 'Incident', ['failure', 'incident', 'rollback', 'recovery']],
  ['evidence', 'Evidence', ['evidence', 'audit', 'receipt']],
] as const

function stateOf(item: EvidenceRecord | GapRecord): EvidenceState {
  return (item.state ?? ('verdict' in item ? item.verdict : undefined) ?? 'ABSENT') as EvidenceState
}

function searchable(item: EvidenceRecord | GapRecord): string {
  return JSON.stringify(item).toLowerCase()
}

function EvidenceChart({ items }: { items: Array<EvidenceRecord | GapRecord> }) {
  const ref = useRef<HTMLDivElement>(null)
  const counts = useMemo(() => {
    const result = new Map<string, number>()
    for (const item of items) result.set(stateOf(item), (result.get(stateOf(item)) ?? 0) + 1)
    return [...result.entries()]
  }, [items])

  useEffect(() => {
    if (!ref.current) return
    const chart = echarts.init(ref.current, undefined, { renderer: 'svg' })
    chart.setOption({
      aria: { enabled: true, decal: { show: true } },
      tooltip: {},
      xAxis: { type: 'category', data: counts.map(([state]) => state), axisLabel: { rotate: 25 } },
      yAxis: { type: 'value', minInterval: 1 },
      series: [{ type: 'bar', data: counts.map(([, count]) => count) }],
    })
    const resize = () => chart.resize()
    window.addEventListener('resize', resize)
    return () => { window.removeEventListener('resize', resize); chart.dispose() }
  }, [counts])

  return <div className="chart" ref={ref} role="img" aria-label="Evidence states by count" />
}

function EvidenceList({ items }: { items: Array<EvidenceRecord | GapRecord> }) {
  if (items.length === 0) return <p className="empty">No canonical records match this surface yet. Absence is not converted to PASS.</p>
  return <div className="evidence-grid">
    {items.map((item, index) => {
      const id = String(item.id ?? ('requirement' in item ? item.requirement : '') ?? `record-${index}`)
      const description = String(('description' in item ? item.description : undefined) ?? ('claim' in item ? item.claim : undefined) ?? ('capability' in item ? item.capability : undefined) ?? id)
      const state = stateOf(item)
      return <article className="evidence-card" key={`${id}-${index}`}>
        <div className="card-head"><code>{id}</code><span className={`state state-${state.toLowerCase()}`}>{state}</span></div>
        <p>{description}</p>
        <details><summary>Canonical record</summary><pre>{JSON.stringify(item, null, 2)}</pre></details>
      </article>
    })}
  </div>
}

export function App() {
  const query = useQuery<EvidenceIndex>({
    queryKey: ['public-evidence-index'],
    queryFn: async () => {
      const response = await fetch('./evidence-index.json', { cache: 'no-store' })
      if (!response.ok) throw new Error(`evidence index HTTP ${response.status}`)
      return response.json() as Promise<EvidenceIndex>
    },
  })

  if (query.isPending) return <main id="main" className="shell"><h1>Manager Evidence Console</h1><p>Loading canonical public evidence…</p></main>
  if (query.isError) return <main id="main" className="shell"><h1>Manager Evidence Console</h1><p role="alert">Evidence index unavailable: {query.error.message}</p></main>

  const data = query.data
  const all = [...data.records, ...data.gaps]

  return <>
    <header className="hero">
      <p className="eyebrow">Public reviewer surface · evidence-first</p>
      <h1>Full Manager MVP Evidence Console</h1>
      <p>This UI renders canonical public registry data. A green UI cannot promote missing backend/runtime evidence.</p>
      <nav aria-label="Evidence views">{sections.map(([id, label]) => <a key={id} href={`#${id}`}>{label}</a>)}</nav>
    </header>
    <main id="main" className="shell">
      <section aria-labelledby="state-chart-title">
        <h2 id="state-chart-title">Current evidence state distribution</h2>
        <EvidenceChart items={all} />
      </section>
      {sections.map(([id, label, keywords]) => {
        const matching = id === 'overview' || id === 'evidence'
          ? all
          : all.filter(item => keywords.some(keyword => searchable(item).includes(keyword)))
        return <section id={id} key={id} aria-labelledby={`${id}-title`}>
          <div className="section-title"><h2 id={`${id}-title`}>{label}</h2><span>{matching.length} canonical records</span></div>
          <EvidenceList items={matching} />
        </section>
      })}
      <section aria-labelledby="rules-title" className="rules">
        <h2 id="rules-title">Public claim ceiling</h2>
        <ul>{data.publicClaimRules.map(rule => <li key={rule}>{rule}</li>)}</ul>
        <p className="provenance">Generated from: {data.generatedFrom.join(', ')} · schema {data.schemaVersion}</p>
      </section>
    </main>
  </>
}
