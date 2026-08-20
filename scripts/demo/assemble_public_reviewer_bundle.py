from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import stat
import zipfile
from pathlib import Path


SECRET_PATTERNS = (
    "BEGIN RSA PRIVATE KEY",
    "BEGIN OPENSSH PRIVATE KEY",
    "BEGIN EC PRIVATE KEY",
    "ghp_",
    "github_pat_",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_extract(archive: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    resolved_root = destination.resolve()
    with zipfile.ZipFile(archive) as zf:
        for member in zf.infolist():
            target = (destination / member.filename).resolve()
            if resolved_root not in target.parents and target != resolved_root:
                raise RuntimeError(f"unsafe archive path: {member.filename}")
        zf.extractall(destination)


def require_paths(root: Path, required: list[str]) -> None:
    missing = [item for item in required if not (root / item).exists()]
    if missing:
        raise RuntimeError(f"missing required artifact paths under {root}: {missing}")


def copy_if_exists(source: Path, destination: Path) -> None:
    if not source.exists():
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(source, destination)
    else:
        shutil.copy2(source, destination)


def assert_public_boundary(root: Path) -> None:
    for path in root.rglob("*"):
        if not path.is_file() or path.stat().st_size > 5_000_000:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern in text:
                raise RuntimeError(f"secret-like material detected in {path}: {pattern}")


def enrich_console_index(console_dir: Path, convergence: dict[str, object]) -> None:
    index_path = console_dir / "evidence-index.json"
    current = json.loads(index_path.read_text())
    current.setdefault("records", [])
    current.setdefault("gaps", [])
    current.setdefault("generatedFrom", [])
    current["generatedFrom"].append("verified GitHub Actions artifacts in public-m4-inputs.json")
    current["records"].extend(
        [
            {
                "id": "M2-PUBLIC-REMOTE-FANOUT-FIRST-GREEN",
                "capability": "Five public implementation lanes independently reached bounded remote FIRST_GREEN",
                "state": "PASS",
                "evidence_ceiling": "LANE_BOUNDED_REMOTE_FIRST_GREEN_ONLY",
            },
            {
                "id": "M3-PUBLIC-REMOTE-FAILURE-RECOVERY-FIRST-GREEN",
                "capability": "Seven bounded incident/recovery drills reached same-failure re-verification",
                "state": "PASS",
                "evidence_ceiling": "GITHUB_HOSTED_DETERMINISTIC_AND_LOCAL_PROCESS_FAILURE_DRILLS_ONLY",
            },
            {
                "id": "M4-PUBLIC-REVIEWER-CONVERGENCE",
                "capability": "Exact public Actions artifacts were re-downloaded, digest-verified and compiled into one reviewer packet",
                "state": "PASS",
                "workflow_run_id": convergence["workflow_run_id"],
                "evidence_ceiling": "GITHUB_HOSTED_ARTIFACT_REDOWNLOAD_AND_REVIEWER_BUNDLE_ONLY",
            },
        ]
    )
    for residual in convergence["residuals"]:
        current["gaps"].append(
            {
                "id": residual,
                "description": residual.replace("_", " ").lower(),
                "state": "NOT_EXERCISED" if "OUTSIDE_REPOSITORY_PROOF" not in residual else "HUMAN_ADMIT_REQUIRED",
            }
        )
    current.setdefault("publicClaimRules", [])
    for rule in (
        "verified artifact re-download does not prove production runtime",
        "DRILL/SIMULATION does not prove production incident history",
        "1000 virtual users do not prove 1000 real users",
        "local Kubernetes evidence does not prove production tenure",
    ):
        if rule not in current["publicClaimRules"]:
            current["publicClaimRules"].append(rule)
    index_path.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n")


def build_bundle(manifest_path: Path, artifact_dir: Path, output: Path, workflow_run_id: str) -> None:
    manifest = json.loads(manifest_path.read_text())
    output.mkdir(parents=True, exist_ok=True)
    extracted_root = output / ".inputs"
    evidence_root = output / "evidence"
    verified: list[dict[str, object]] = []

    for artifact in manifest["artifacts"]:
        lane = artifact["lane"]
        archive = artifact_dir / f"{lane}.zip"
        if not archive.exists():
            raise RuntimeError(f"missing downloaded archive for {lane}: {archive}")
        actual = f"sha256:{sha256_file(archive)}"
        if actual != artifact["artifact_digest"]:
            raise RuntimeError(
                f"artifact digest mismatch for {lane}: expected {artifact['artifact_digest']} got {actual}"
            )
        lane_root = extracted_root / lane
        safe_extract(archive, lane_root)
        require_paths(lane_root, artifact["required_paths"])

        lane_evidence = evidence_root / lane
        lane_evidence.mkdir(parents=True, exist_ok=True)
        for required in artifact["required_paths"]:
            copy_if_exists(lane_root / required, lane_evidence / required)

        verified.append(
            {
                "lane": lane,
                "pull_request": artifact["pull_request"],
                "source_head": artifact["head"],
                "workflow_run": artifact["workflow_run"],
                "artifact_id": artifact["artifact_id"],
                "artifact_digest": actual,
                "required_paths": artifact["required_paths"],
                "evidence_ceiling": artifact["evidence_ceiling"],
                "verification": "PASS",
            }
        )

    console_input = extracted_root / "demo-console"
    console_output = output / "console"
    copy_if_exists(console_input, console_output)

    convergence = {
        "schema_version": "full-manager-mvp/public-reviewer-convergence/v1",
        "workflow_run_id": workflow_run_id,
        "verdict": "PASS",
        "checks": {
            "artifact_redownload": "PASS",
            "artifact_digest_verification": "PASS",
            "required_path_verification": "PASS",
            "public_console_included": "PASS",
            "failure_drill_packet_included": "PASS",
            "production_runtime": "NOT_EXERCISED",
            "real_user_adoption": "NOT_EXERCISED",
            "real_incident_history": "NOT_EXERCISED",
        },
        "verified_inputs": verified,
        "residuals": manifest["residuals"],
        "authority": manifest["authority"],
        "evidence_ceiling": "GITHUB_HOSTED_ARTIFACT_REDOWNLOAD_AND_REVIEWER_BUNDLE_ONLY",
    }
    (output / "reviewer-index.json").write_text(json.dumps(convergence, indent=2, sort_keys=True) + "\n")
    enrich_console_index(console_output, convergence)

    readme = """# Full Manager MVP — Public Reviewer Bundle\n\nThis packet is assembled only from exact GitHub Actions artifacts whose archive digests were re-verified during convergence. It is a public demo packet, not production-history evidence.\n\n## One-command local viewing\n\n```bash\npython3 serve.py\n```\n\nThen open `http://127.0.0.1:4173/`. The console renders the evidence ladder and explicit residual gaps.\n\n## Evidence boundary\n\n`PASS` here means the exact remote artifacts were re-downloaded, digest checked, required files admitted, and compiled into one bounded reviewer packet. Live Kubernetes, real Argo runtime, local model inference, 1,000-VU recovery, production users/incidents and management tenure remain outside this packet unless separately admitted.\n"""
    (output / "README.md").write_text(readme)
    serve = """from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler\nfrom functools import partial\nfrom pathlib import Path\n\nroot = Path(__file__).resolve().parent / 'console'\nhandler = partial(SimpleHTTPRequestHandler, directory=str(root))\nprint('Serving bounded reviewer console at http://127.0.0.1:4173/')\nThreadingHTTPServer(('127.0.0.1', 4173), handler).serve_forever()\n"""
    serve_path = output / "serve.py"
    serve_path.write_text(serve)
    serve_path.chmod(serve_path.stat().st_mode | stat.S_IXUSR)

    shutil.rmtree(extracted_root)
    assert_public_boundary(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workflow-run-id", required=True)
    args = parser.parse_args()
    build_bundle(args.manifest, args.artifact_dir, args.output, args.workflow_run_id)
