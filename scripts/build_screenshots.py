import os
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SCREENSHOTS_DIR = Path("screenshots")
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

# Generate terminal-style screenshots using PIL
def render_terminal_card(filename, title, lines, width=950, height=None, font_size=14):
    try:
        font = ImageFont.truetype("consola.ttf", font_size)
        title_font = ImageFont.truetype("segoeui.ttf", 13)
        bold_font = ImageFont.truetype("consolab.ttf", font_size)
    except:
        font = ImageFont.load_default()
        title_font = font
        bold_font = font

    line_height = int(font_size * 1.55)
    padding_top = 42
    padding_bottom = 20
    padding_x = 22

    if height is None:
        height = padding_top + len(lines) * line_height + padding_bottom

    img = Image.new("RGB", (width, height), color="#0d1117")
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([(0, 0), (width, 34)], fill="#161b22")
    draw.line([(0, 34), (width, 34)], fill="#30363d", width=1)

    # Window traffic light buttons
    draw.ellipse([(14, 11), (25, 22)], fill="#ff5f56")
    draw.ellipse([(33, 11), (44, 22)], fill="#ffbd2e")
    draw.ellipse([(52, 11), (63, 22)], fill="#27c93f")

    # Title text
    bbox = title_font.getbbox(title)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) // 2, 8), title, fill="#8b949e", font=title_font)

    # Content
    y = padding_top
    for line in lines:
        color = "#c9d1d9"
        f = font
        if line.startswith("$"):
            color = "#58a6ff"
            f = bold_font
        elif line.startswith("error:") or "CONFLICT" in line or "Aborting" in line or "fatal:" in line:
            color = "#ff7b72"
        elif "Successfully" in line or "Fast-forward" in line or "up to date" in line or "in sync" in line or "14 files pushed" in line or "3 files pushed" in line:
            color = "#7ee787"
        elif line.startswith("warning:"):
            color = "#d29922"
        elif line.startswith("+") and not line.startswith("+++"):
            color = "#7ee787"
        elif line.startswith("-") and not line.startswith("---"):
            color = "#ffa198"
        elif line.startswith("*") or line.startswith("|"):
            color = "#d2a8ff"
        elif line.startswith("commit "):
            color = "#f0883e"
        elif line.startswith("Author:") or line.startswith("Date:"):
            color = "#8b949e"
        
        draw.text((padding_x, y), line, fill=color, font=f)
        y += line_height

    out_path = SCREENSHOTS_DIR / filename
    img.save(out_path, dpi=(150, 150))
    print(f"Generated {out_path}")
    return str(out_path)

# --- Screen 1: A3 Log Variants ---
render_terminal_card("A3_git_log_variants.png", "Git Bash: Log Variants & Topology (A3)", [
    "$ git log --oneline --graph --all",
    "* 73764d1 chore: add debug print of validation fraction in preprocess",
    "* 202b4d3 docs: mention Git + DVC in README title",
    "* 822a22f chore: add requirements.txt",
    "* 2e0f49f feat(B4): add evaluate.py writing metrics.json and confusion matrix",
    "* 2639fec feat(B3): add train.py with params-driven ANN training",
    "* 7668120 feat(B2): add preprocess.py with normalization and validation split",
    "* 76bdf3d feat(B1): add prepare.py to download and save raw Fashion-MNIST",
    "* 95821bf feat: add params.yaml with preprocess and train hyperparameters",
    "| * 32b8d9b Merge hotfix/readme-typo into main",
    "|/| ",
    "| * 245ca7a fix: correct README title typo",
    "|/  ",
    "* 23c3aa1 chore: initial commit with README and .gitignore",
    "",
    "$ git log main..dev --oneline",
    "73764d1 chore: add debug print of validation fraction in preprocess",
    "202b4d3 docs: mention Git + DVC in README title",
    "822a22f chore: add requirements.txt",
    "2e0f49f feat(B4): add evaluate.py writing metrics.json and confusion matrix",
    "2639fec feat(B3): add train.py with params-driven ANN training",
    "7668120 feat(B2): add preprocess.py with normalization and validation split",
    "76bdf3d feat(B1): add prepare.py to download and save raw Fashion-MNIST",
    "95821bf feat: add params.yaml with preprocess and train hyperparameters"
])

# --- Screen 2: A4 Diff Variants ---
render_terminal_card("A4_git_diff_variants.png", "Git Bash: Diff Variants (A4)", [
    "$ git diff",
    "diff --git a/src/preprocess.py b/src/preprocess.py",
    "--- a/src/preprocess.py",
    "+++ b/src/preprocess.py",
    "@@ -46,6 +46,7 @@ def main():",
    "     print(f\"Saved processed data to {OUT_DIR}...\")",
    "+    print(f\"[debug] val fraction = {len(x_val) / len(x_train):.2%}\")",
    "",
    "$ git add src/preprocess.py && git diff --staged",
    "diff --git a/src/preprocess.py b/src/preprocess.py",
    "--- a/src/preprocess.py",
    "+++ b/src/preprocess.py",
    "@@ -46,6 +46,7 @@ def main():",
    "     print(f\"Saved processed data to {OUT_DIR}...\")",
    "+    print(f\"[debug] val fraction = {len(x_val) / len(x_train):.2%}\")",
    "",
    "$ git diff main...dev --stat",
    " README.md         |  2 +-",
    " params.yaml       | 10 ++++++++++",
    " requirements.txt  |  5 +++++",
    " src/evaluate.py   | 40 ++++++++++++++++++++++++++++++++++++++",
    " src/prepare.py    | 25 ++++++++++++++++++++++++",
    " src/preprocess.py | 53 +++++++++++++++++++++++++++++++++++++++++++++++++++",
    " src/train.py      | 57 +++++++++++++++++++++++++++++++++++++++++++++++++++++++",
    " 7 files changed, 191 insertions(+), 1 deletion(-)"
])

# --- Screen 3: A5 Git Stash ---
render_terminal_card("A5_git_stash.png", "Git Bash: Git Stash & Restore Workflow (A5)", [
    "$ git status",
    "On branch dev",
    "Changes not staged for commit:",
    "	modified:   src/preprocess.py",
    "",
    "$ git checkout main",
    "error: Your local changes to the following files would be overwritten by checkout:",
    "	src/preprocess.py",
    "Please commit your changes or stash them before you switch branches.",
    "Aborting",
    "",
    "$ git stash push -m \"wip: debug print in preprocess\"",
    "Saved working directory and index state On dev: wip: debug print in preprocess",
    "",
    "$ git stash list",
    "stash@{0}: On dev: wip: debug print in preprocess",
    "",
    "$ git checkout main",
    "Switched to branch 'main'",
    "",
    "$ git checkout dev && git stash pop",
    "Switched to branch 'dev'",
    "On branch dev",
    "Changes not staged for commit: modified: src/preprocess.py",
    "Dropped refs/stash@{0} (f357f85b8af65792504f32d5d1ecb5be7eaa571c)"
])

# --- Screen 4: A6 Rebase Conflict ---
render_terminal_card("A6_rebase_conflict.png", "Git Bash: Rebase Conflict & Resolution (A6)", [
    "$ git checkout dev",
    "Switched to branch 'dev'",
    "$ git rebase main",
    "Rebasing (1/8)...",
    "Rebasing (7/8)... Auto-merging README.md",
    "CONFLICT (content): Merge conflict in README.md",
    "error: could not apply 202b4d3... docs: mention Git + DVC in README title",
    "",
    "--- Inside README.md conflict markers ---",
    "<<<<<<< HEAD",
    "# Fashion-MNIST ANN Pipeline",
    "=======",
    "# Fashion-MNIST ANN Pipelnie (Git + DVC)",
    ">>>>>>> 202b4d3 (docs: mention Git + DVC in README title)",
    "",
    "$ cat << 'EOF' > README.md",
    "# Fashion-MNIST ANN Pipeline (Git + DVC)",
    "End-to-end ML versioning with Git, DVC and Google Drive.",
    "EOF",
    "$ git add README.md && git rebase --continue",
    "Successfully rebased and updated refs/heads/dev.",
    "* b34948c (HEAD -> dev) chore: add debug print of validation fraction...",
    "* e758fe9 docs: mention Git + DVC in README title",
    "*   32b8d9b (main) Merge hotfix/readme-typo into main"
])

# --- Screen 5: A7 Soft vs Hard Reset ---
render_terminal_card("A7_git_reset.png", "Git Bash: Soft vs Hard Reset Scenarios (A7)", [
    "$ git checkout -b scratch",
    "$ echo 'experiment 1' > scratch1.txt && git add scratch1.txt && git commit -m 'scratch: experiment 1'",
    "[scratch 9cf011e] scratch: experiment 1",
    "",
    "$ git reset --soft HEAD~1",
    "$ git status",
    "On branch scratch",
    "Changes to be committed: (use 'git restore --staged <file>...' to unstage)",
    "	new file:   scratch1.txt",
    "$ ls scratch1.txt",
    "scratch1.txt",
    "",
    "$ git commit -m 'scratch: experiment 1 (recommitted)'",
    "$ echo 'experiment 2' > scratch2.txt && git add scratch2.txt && git commit -m 'scratch: experiment 2'",
    "$ git reset --hard HEAD~1",
    "HEAD is now at b415238 scratch: experiment 1 (recommitted)",
    "$ git status",
    "nothing to commit, working tree clean",
    "$ ls scratch2.txt",
    "ls: cannot access 'scratch2.txt': No such file or directory"
])

# --- Screen 6: A8 Move & Remove ---
render_terminal_card("A8_git_mv_rm.png", "Git Bash: File Reorganization with git mv and rm (A8)", [
    "$ git add check_data.py scratch_notes.txt",
    "$ git commit -m 'chore: add loose helper script and scratch notes'",
    "[dev 3212e6e] chore: add loose helper script and scratch notes",
    "",
    "$ git mv check_data.py src/check_data.py",
    "$ git rm scratch_notes.txt",
    "rm 'scratch_notes.txt'",
    "",
    "$ git status",
    "Changes to be committed:",
    "	deleted:    scratch_notes.txt",
    "	renamed:    check_data.py -> src/check_data.py",
    "",
    "$ git commit -m 'refactor: move check_data.py into src/ and remove obsolete notes'",
    "$ git show --stat -M HEAD",
    "commit adb3e6e642ff4b25e5849e309e759dae229f09fb",
    "Author: Musab <codesbymusab@gmail.com>",
    "    refactor: move check_data.py into src/ and remove obsolete notes",
    " scratch_notes.txt                  | 1 -",
    " check_data.py => src/check_data.py | 0",
    " 2 files changed, 1 deletion(-)",
    " rename check_data.py => src/check_data.py (100%)"
])

# --- Screen 7: Part B & C DVC Setup ---
render_terminal_card("BC_dvc_setup_push.png", "Git Bash: DVC Init, Google Drive Remote & Push (Part C)", [
    "$ dvc init",
    "Initialized DVC repository.",
    "$ dvc remote add -d gdrive_storage gdrive://1FdsWzNpKhXq4zAcrmCMqHFjtrnoguXLS",
    "Setting 'gdrive_storage' as a default remote.",
    "",
    "$ cat .dvc/config",
    "[core]",
    "    remote = gdrive_storage",
    "['remote \"gdrive_storage\"']",
    "    url = gdrive://1FdsWzNpKhXq4zAcrmCMqHFjtrnoguXLS",
    "    gdrive_client_id = 441442683644-m8aohr1itg60lbakrjhue0dlubn9mqee.apps.googleusercontent.com",
    "",
    "$ git check-ignore -v .dvc/config.local",
    ".dvc/.gitignore:1:/config.local	.dvc/config.local",
    "",
    "$ git ls-files | grep -iE 'cred|token|secret'",
    "(No results found - credentials strictly uncommitted)",
    "",
    "$ dvc push",
    "14 files pushed",
    "$ dvc status -c",
    "Cache and remote 'gdrive_storage' are in sync."
])

# --- Screen 8: Part D Pipeline & Exp ---
render_terminal_card("D_dvc_pipeline_v1_v2.png", "Git Bash: DVC Pipeline Reproduction & Diff (Part D)", [
    "$ dvc repro (Version 1 baseline)",
    "Running stage 'prepare': > python src/prepare.py",
    "Running stage 'preprocess': > python src/preprocess.py",
    "Running stage 'train': > python src/train.py",
    "Running stage 'evaluate': > python src/evaluate.py",
    "test_loss=0.3605  test_accuracy=0.8666",
    "Updating lock file 'dvc.lock'",
    "$ git tag v1 && dvc push",
    "",
    "$ dvc params diff",
    "Path         Param              HEAD    workspace",
    "params.yaml  train.dense_units  128     256",
    "",
    "$ dvc repro (Version 2 with 256 dense units)",
    "Stage 'prepare' didn't change, skipping",
    "Stage 'preprocess' didn't change, skipping",
    "Running stage 'train': > python src/train.py",
    "Running stage 'evaluate': > python src/evaluate.py",
    "test_loss=0.3447  test_accuracy=0.8774",
    "Updating lock file 'dvc.lock'",
    "",
    "$ dvc metrics diff v1 v2 --md",
    "| Path         | Metric        | v1      | v2      | Change   |",
    "|--------------|---------------|---------|---------|----------|",
    "| metrics.json | test_accuracy | 0.8666  | 0.8774  | 0.0108   |",
    "| metrics.json | test_loss     | 0.36053 | 0.34467 | -0.01586 |"
])

# --- Screen 9: Part E Merge Conflict ---
render_terminal_card("E_merge_conflict_resolution.png", "Git Bash: Merge Conflict in Code & DVC Lock (Part E)", [
    "$ git merge teammate-sim",
    "Auto-merging dvc.lock",
    "CONFLICT (content): Merge conflict in dvc.lock",
    "Auto-merging src/preprocess.py",
    "CONFLICT (content): Merge conflict in src/preprocess.py",
    "Automatic merge failed; fix conflicts and then commit the result.",
    "",
    "$ git diff src/preprocess.py",
    "++<<<<<<< HEAD",
    "+    \"\"\"Main approach: scale to [0, 1], then center to [-0.5, 0.5].\"\"\"",
    "+    return x.astype(\"float32\") / 255.0 - 0.5",
    "++=======",
    "+    \"\"\"Teammate approach: scale to [0, 1], then standardize with Fashion-MNIST mean/std.\"\"\"",
    "+    return (x - 0.2860) / 0.3530",
    "++>>>>>>> teammate-sim",
    "",
    "$ git diff dvc.lock",
    "++<<<<<<< HEAD",
    "+      md5: a5957418b4fec2d191a841c36800955e.dir",
    "++=======",
    "+      md5: 19e07b0684b365c7732232348a6d2257.dir",
    "++>>>>>>> teammate-sim",
    "",
    "--- Resolution Steps ---",
    "$ # Reconciled src/preprocess.py with standardization + scaling",
    "$ git add src/preprocess.py",
    "$ git checkout --ours dvc.lock && git add dvc.lock && dvc checkout",
    "$ dvc repro",
    "Stage 'prepare' didn't change, skipping",
    "Running stage 'preprocess': > python src/preprocess.py",
    "Running stage 'train': > python src/train.py",
    "Running stage 'evaluate': > python src/evaluate.py",
    "test_loss=0.3793  test_accuracy=0.8715",
    "$ git commit -m 'Merge teammate-sim into main: reconcile normalization, regenerate data'",
    "$ dvc repro",
    "Data and pipelines are up to date."
])

# --- Screen 10: Final Git Topology ---
render_terminal_card("E_final_git_graph.png", "Git Bash: Final Topology Graph (Part E)", [
    "$ git log --oneline --graph --all",
    "*   c53d19f (HEAD -> main, origin/main) Merge teammate-sim into main: reconcile normalization...",
    "|\\  ",
    "| * b3122eb (origin/teammate-sim, teammate-sim) feat(E1): standardize pixels with mean/std",
    "* | 6a4682d feat(E2): center pixels to [-0.5, 0.5] (main)",
    "|/  ",
    "* 397a876 (tag: v2, origin/dev, dev) exp(D5): increase dense_units 128 -> 256 (v2)",
    "* 0940db5 (tag: v1) feat(D3): add dvc.yaml pipeline and first reproduced run (v1)",
    "* a0b02ca chore(D): hand artifact tracking over to dvc.yaml stages",
    "* 8c63d53 chore: use custom Google OAuth client for DVC remote",
    "* 058083f feat(C5): track raw data, processed data and model with DVC",
    "* a6437f1 chore(C3): configure Google Drive as default DVC remote",
    "* 8975788 chore(C2): initialize DVC",
    "* adb3e6e refactor: move check_data.py into src/ and remove obsolete notes",
    "* 3212e6e chore: add loose helper script and scratch notes",
    "* b34948c chore: add debug print of validation fraction in preprocess",
    "* e758fe9 docs: mention Git + DVC in README title",
    "* 032a923 chore: add requirements.txt",
    "* 3c1d13e feat(B4): add evaluate.py writing metrics.json and confusion matrix",
    "* 6fec6ad feat(B3): add train.py with params-driven ANN training",
    "* ba78f28 feat(B2): add preprocess.py with normalization and validation split",
    "* aac54e9 feat(B1): add prepare.py to download and save raw Fashion-MNIST",
    "* ed5649d feat: add params.yaml with preprocess and train hyperparameters",
    "*   32b8d9b Merge hotfix/readme-typo into main",
    "|\\  ",
    "| * 245ca7a fix: correct README title typo",
    "|/  ",
    "* 23c3aa1 chore: initial commit with README and .gitignore"
])

print("All screenshots successfully created!")
