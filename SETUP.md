# Setup Guide

Step-by-step instructions for getting the AI Job Search framework running.

## 1. Prerequisites

### Claude Code

Install Claude Code (Anthropic's CLI for Claude):

```bash
npm install -g @anthropic-ai/claude-code
```

You'll need an Anthropic API key or a Claude Pro/Team subscription. See the [Claude Code docs](https://docs.anthropic.com/en/docs/claude-code) for details.

### Python

Python 3.10+ is required for the salary lookup tool. Check with:

```bash
python --version
```

On Windows, `py --version` is often the most reliable check if `python` is not on your PATH.

### Bun (for job search tools)

Optional. The `linkedin-search` CLI and any portal-specific CLIs you scaffold with `/add-portal` are written in TypeScript and run with Bun. For the Chinese market, `/scrape` uses WebSearch by default, so Bun is only needed if you add custom portal CLIs.

- macOS/Linux:

```bash
curl -fsSL https://bun.sh/install | bash
```

- Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -c "irm https://bun.sh/install.ps1 | iex"
```

If you prefer a package manager, `winget install Oven-sh.Bun` also works on Windows.

### LaTeX (for compiling CVs and cover letters)

Install a LaTeX distribution to compile the generated `.tex` files to PDF:

- **Windows:** [MiKTeX](https://miktex.org/download)
- **macOS:** [MacTeX](https://tug.org/mactex/)
- **Linux:** `sudo apt install texlive-full` or `sudo dnf install texlive-scheme-full`

The default CV compiles with `lualatex` (pdflatex often fails on modern MiKTeX installs with `fontawesome5` font-expansion errors). The default cover letter compiles with `xelatex` because `cover.cls` requires `fontspec`.

**Chinese templates** (`cv/chinese/main.tex`, `cover_letters/chinese/cover.tex`) use the `ctex` package and require `lualatex` or `xelatex`. pdflatex will fail. Make sure a Chinese font is available:
- **macOS:** MacTeX includes 苹方/华文 fonts.
- **Windows:** MiKTeX/TeX Live will use SimHei/SimSun.
- **Linux:** install `fonts-noto-cjk` (Noto Sans CJK SC).

If compilation fails with a CJK font error, edit the template to specify an installed font, e.g. `\setCJKmainfont{PingFang SC}` on macOS or `\setCJKmainfont{Noto Sans CJK SC}` on Linux.

### Optional: pdftotext (for the ATS check)

`/apply` runs an ATS parseability check on the compiled CV: it extracts the PDF's text layer and verifies contact details, reading order, and keyword coverage the way an applicant-tracking system sees them. This uses `pdftotext` from [poppler](https://poppler.freedesktop.org/), which is not part of TeX distributions:

- **macOS:** `brew install poppler`
- **Debian/Ubuntu:** `sudo apt install poppler-utils`
- **Windows:** `choco install poppler`

If `pdftotext` is missing, `/apply` skips the mechanical check with a warning and falls back to a visual keyword review — everything else works normally.

## 2. Fork and clone

```bash
gh repo fork cypggs/ai-job-search --clone
# or fork from the upstream MadsLorentzen/ai-job-search and merge Chinese changes manually
cd ai-job-search
```

Or manually: fork on GitHub, then clone your fork.

## 3. Install job search CLI dependencies (optional)

For the Chinese market, `/scrape` uses WebSearch by default. You only need to install CLI tools if you plan to use `linkedin-search` or scaffold a custom portal CLI with `/add-portal`.

Run these from the repository root if desired:

- PowerShell:

```powershell
Set-Location ".agents/skills/linkedin-search/cli"
bun install
Set-Location "..\..\.."
```

- Bash / zsh / Git Bash:
```bash
cd .agents/skills/linkedin-search/cli && bun install && cd ../../../..
```

For `linkedin-search` the install is optional: it has zero runtime dependencies and runs with plain `bun`; `bun install` only pulls TypeScript dev types.

If you want to add a portal-specific CLI for a Chinese job board that allows it, run `/add-portal` — it scaffolds the same CLI structure and test-runs a live query before registering. See the "Job search tools" section in the README.

## 4. Run the setup interview

Start Claude Code in the repository:

```bash
claude
```

Then run the onboarding:

```
/setup
```

Claude will offer three paths:

- **Path A (documents folder):** Add your CV, LinkedIn export, diplomas, references, or past applications under `documents/`. Claude reads and cross-references them before proposing profile updates. This is best when you have several source files.
- **Path B (single CV import):** Share one CV/resume by mentioning the file with `@` or pasting the text. Claude extracts it and asks follow-up questions for anything missing.
- **Path C (interview mode):** Answer structured interview questions section by section.

All three paths produce the same result: fully populated profile files.

### What gets populated

| File | Content |
|------|---------|
| `CLAUDE.md` | Your full candidate profile |
| `01-candidate-profile.md` | Structured education, experience, skills |
| `02-behavioral-profile.md` | Behavioral assessment |
| `04-job-evaluation.md` | Personalized skill match areas and career goals |
| `05-cv-templates.md` | Profile statement templates for your background |
| `07-interview-prep.md` | STAR examples from your experience |
| `cv/main_example.tex` | Your LaTeX CV with actual details |
| `cv/chinese/main.tex` | Chinese CV template with your details |
| `cover_letters/chinese/cover.tex` | Chinese cover letter template |
| `search-queries.md` | Job search queries for `/scrape` |

### Re-running setup

You can update specific sections later:

```
/setup --section skills
/setup --section experience
/setup --section search
```

The `--section search` option is especially useful as your priorities evolve. It re-runs the search configuration interview and suggests role types you may not have considered based on your full profile.

## 5. Optional: Set up salary benchmarking

If you have salary data (from a union, salary survey, Glassdoor, 脉脉, 看准网, or personal research):

1. **Option A:** Create `salary_data.json` manually in the repo root (see `tools/README_SALARY_TOOL.md` for the format)
2. **Option B:** Convert from Excel:
   ```bash
   pip install openpyxl
   python tools/convert_salary_excel.py path/to/salary-data.xlsx --source "My Salary Data 2025"
   ```

This creates `salary_data.json` which the `/apply` workflow uses for salary benchmarking. If you skip this step, salary lookup is simply omitted.

## 6. Test the workflow

Find a job posting you're interested in, then:

```
/apply https://www.zhipin.com/job/xxxxxxxx.html
```

Or paste the job description directly:

```
/apply [paste job posting text here]
```

For China-market postings, `/apply` generates Chinese CV and cover letter PDFs. For international postings, it uses the original English templates.

Claude will:
1. Evaluate the fit against your profile
2. Ask if you want to proceed
3. Draft a tailored CV and cover letter
4. Have a reviewer agent critique the drafts
5. Revise and present the final output

## 7. Compile your documents

After `/apply` creates the LaTeX files:

**International/English templates:**
```bash
# Bash / zsh / Git Bash
cd cv && lualatex main_<company>.tex && cd ..
cd cover_letters && xelatex cover_<company>_<role>.tex && cd ..
```

```powershell
# PowerShell
Set-Location cv; lualatex main_<company>.tex; Set-Location ..
Set-Location cover_letters; xelatex cover_<company>_<role>.tex; Set-Location ..
```

**Chinese templates:**
```bash
# Bash / zsh / Git Bash
cd cv/chinese && lualatex main_<company>.tex && cd ../..
cd cover_letters/chinese && xelatex cover_<company>_<role>.tex && cd ../..
```

```powershell
# PowerShell
Set-Location cv/chinese; lualatex main_<company>.tex; Set-Location ../..
Set-Location cover_letters/chinese; xelatex cover_<company>_<role>.tex; Set-Location ../..
```

These commands apply to the stock templates. If you'd rather use your own LaTeX template, run `/add-template` — it captures the template's compile engine, fonts, style rules, and page limit, test-compiles it, and wires it into `/apply`. See the "LaTeX templates" section in the README.

## Troubleshooting

### "salary_data.json not found"
This is expected if you haven't set up salary benchmarking. The `/apply` workflow skips this step automatically.

### Job search CLI tools not working
For the Chinese market, `/scrape` uses WebSearch by default and does not require portal CLIs. If you installed optional CLIs, make sure Bun is installed and you ran `bun install` in the CLI directory.

### LaTeX compilation errors
- Default CV: uses `lualatex` (pdflatex often fails on modern MiKTeX with `fontawesome5` font-expansion errors; lualatex handles the same sources cleanly)
- Default cover letter: uses `xelatex` (for custom fonts in `OpenFonts/fonts/`)
- Chinese CV/cover letter: use `ctex` and require `lualatex` or `xelatex`; pdflatex will fail
- Make sure your LaTeX distribution includes the `moderncv` and `ctex` packages

### Fonts not found in cover letter
The default cover letter template expects fonts in `cover_letters/OpenFonts/fonts/`. Make sure this directory exists and contains the Lato and Raleway font files.

For Chinese templates, if `ctex` cannot find a CJK font, specify a fontset in the document class or set `\setCJKmainfont` to an installed CJK font (see comments in the template).

### Stale `.claude/settings.local.json` from an older clone
Shared Claude Code permissions now live in `.claude/settings.json` (scoped to `bun run` and `python salary_lookup.py`). Earlier versions of this repo committed a broader `.claude/settings.local.json` that pre-approved `Bash(curl:*)`, `Bash(python:*)` and `Bash(bun:*)`. If you cloned before that change, git leaves the old file behind in your working copy, and its permissions still apply on top of `settings.json`. Delete it (or trim it to your own personal overrides):

```bash
rm .claude/settings.local.json
```
