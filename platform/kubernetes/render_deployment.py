#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def validate_image_ref(value: str) -> None:
    if "@sha256:" not in value:
        raise SystemExit("IMAGE_REF must be immutable and contain @sha256:")
    digest = value.rsplit("@sha256:", 1)[1]
    if len(digest) != 64:
        raise SystemExit("IMAGE_REF sha256 digest must contain 64 hex characters")
    int(digest, 16)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-ref", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--template", default=str(Path(__file__).with_name("deployment.yaml.tmpl")))
    args = parser.parse_args()
    validate_image_ref(args.image_ref)
    template = Path(args.template).read_text(encoding="utf-8")
    rendered = template.replace("${IMAGE_REF}", args.image_ref)
    if "${IMAGE_REF}" in rendered:
        raise SystemExit("unresolved IMAGE_REF placeholder")
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
