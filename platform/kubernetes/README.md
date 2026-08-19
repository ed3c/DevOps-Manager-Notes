# Kubernetes contract

This directory is a **renderable local-substrate contract**, not proof that Kubernetes has executed.

`deployment.yaml.tmpl` refuses mutable image evidence at render time. Render with an immutable registry digest:

```bash
python3 platform/kubernetes/render_deployment.py \
  --image-ref 'registry.example/full-manager-mvp@sha256:<64-hex>' \
  --output /tmp/manager-demo-deployment.yaml
```

The deployment uses a `manager-demo-db` Secret containing key `database-url`; the Secret value is intentionally never committed.

Local kind/Kubernetes execution, database Secret creation, image distribution and post-deploy business verification are Local Handoff work. A Ready pod is not a business PASS.
