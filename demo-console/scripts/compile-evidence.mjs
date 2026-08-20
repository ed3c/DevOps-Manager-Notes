import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import YAML from 'yaml'

const here = path.dirname(fileURLToPath(import.meta.url))
const consoleRoot = path.resolve(here, '..')
const repoRoot = path.resolve(consoleRoot, '..')

const evidence = YAML.parse(fs.readFileSync(path.join(repoRoot, 'registry/evidence.yaml'), 'utf8')) ?? {}
const gaps = YAML.parse(fs.readFileSync(path.join(repoRoot, 'registry/gaps.yaml'), 'utf8')) ?? {}

const records = Array.isArray(evidence.records) ? evidence.records : []
const gapRecords = Array.isArray(gaps.gaps) ? gaps.gaps : []
const allowedStates = new Set([
  'PASS', 'FAIL', 'ABSENT', 'NOT_IMPLEMENTED', 'NOT_EXERCISED',
  'SKIPPED_BY_POLICY', 'HUMAN_ADMIT_REQUIRED',
])

for (const record of records) {
  const state = record.state ?? record.verdict ?? record.evidence_state
  if (state && !allowedStates.has(state)) {
    throw new Error(`unknown evidence state in canonical registry: ${state}`)
  }
}
for (const gap of gapRecords) {
  if (gap.state && !allowedStates.has(gap.state)) {
    throw new Error(`unknown gap state in canonical registry: ${gap.state}`)
  }
}

const output = {
  schemaVersion: 'full-manager-mvp/public-evidence-index/v1',
  generatedFrom: ['registry/evidence.yaml', 'registry/gaps.yaml'],
  evidenceLadder: evidence.ladder ?? {},
  records,
  gaps: gapRecords,
  publicClaimRules: [
    'UI state cannot promote backend evidence state',
    'virtual users do not prove real adoption',
    'DRILL/SIMULATION does not prove production incident history',
    'local or CI runtime does not prove production tenure',
  ],
}

const publicDir = path.join(consoleRoot, 'public')
fs.mkdirSync(publicDir, { recursive: true })
fs.writeFileSync(path.join(publicDir, 'evidence-index.json'), `${JSON.stringify(output, null, 2)}\n`)
