# Submission checklist

Run these from the project root in Git Bash. Order matters.

## 0. One-time, if not done
```
cd /c/solumn
set -a; . .env; set +a            # load endpoint creds (never committed)
```

## 1. Reproducibility (optional but recommended)
```
bash scripts/pin_digests.sh       # pin base images to @sha256 (needs Docker)
bash scripts/pin_digests.sh --check
```

## 2. Verify everything still works
```
bash scripts/validate_all.sh      # offline: expect "ALL NINE PASSED"
bash scripts/oracle_check.sh      # under Harbor: expect 1 / 0 for all nine
```

## 3. Record the run environment
```
bash scripts/env_report.sh        # writes results/run_environment.txt
```

## 4. Commit and push
```
git add -A
git status                        # confirm .env, jobs/, jobs_iter/ are NOT listed
git commit -m "Final submission state"
git push
```

## 5. Build the archive
```
bash scripts/package_submission.sh
```
This creates `solumn_submission_final.zip` from the committed tree. It prints
"OK: no .env and no jobs/ output in the archive." If it prints DANGER, stop.

## 6. Submit
Upload `solumn_submission_final.zip` via the form:
https://forms.gle/sxVVi9scgn6up7CD9

## What's in the archive
- `environments/` — nine Harbor environments
- `results/` — baseline + iteration logs, grader-validation output, sample
  trajectories, run environment
- `scripts/` — validation, rollout, pinning, packaging helpers
- `report/` — 2-page overview (PDF + LaTeX)
- `QUALITY_BAR.md`, `README.md`

## After submitting
- Revoke the GitHub token that was pasted during setup
  (GitHub → Settings → Developer settings → Tokens → delete).
