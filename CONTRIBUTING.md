# Contributing

## Development Setup

1. Install Python 3.10+
2. Install ffmpeg and add it to PATH
3. Install deps:
   - `pip install -r requirements.txt`
4. Run:
   - `python run.py`

## Pull Request Checklist

- Keep changes focused (one purpose per PR).
- Test with at least:
  - one short audio file
  - one long file (chunk mode)
  - one video input if video output mode touched
- If UI changes, add screenshots.
- Update docs for any new setting or workflow.

## Performance and Stability Rules

- CPU-first stability matters for large files.
- Avoid high default values that increase heat/crash risk.
- Prefer adaptive behavior with safe fallbacks.

## Bug Reports

When reporting bugs, include:
- app version
- OS + CPU/GPU info
- relevant settings
- diagnostics JSON from UI
