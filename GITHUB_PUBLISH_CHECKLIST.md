# GitHub Publish Checklist

Date: 2026-02-08  
Project root: `/Users/michaelaliegertova/Desktop/Codex_review_Jirka/single_ev_droplet_calculator`

## 1. Final pre-publish checks

```bash
cd /Users/michaelaliegertova/Desktop/Codex_review_Jirka/single_ev_droplet_calculator
PYTHONPATH=. python3 -m unittest discover -s tests -v
PYTHONPATH=. python3 -m single_ev_droplet_calculator.cli compare --lambda-a 0.10 --lambda-b 0.20
```

## 2. Set repository metadata

1. Update `CITATION.cff`:
- replace `repository-code` with your real GitHub URL.
2. Optionally set author/team details in `pyproject.toml`.

## 3. Create GitHub repo and push

```bash
cd /Users/michaelaliegertova/Desktop/Codex_review_Jirka/single_ev_droplet_calculator
git init
git add .
git commit -m "Initial release: single-EV droplet occupancy calculator"
git branch -M main
git remote add origin https://github.com/<ORG_OR_USER>/single-ev-droplet-calculator.git
git push -u origin main
```

## 4. Suggested release tag

```bash
git tag v0.1.0
git push origin v0.1.0
```

## 5. Manuscript integration

- In the manuscript data-availability section, replace local path reference with GitHub URL and release tag/commit hash.
- Optional: archive the release on Zenodo and cite DOI in the manuscript.

