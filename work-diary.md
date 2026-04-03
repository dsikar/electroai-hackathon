# Work Diary

## 2026-03-26

- Added an EEAI-adapted starter prompt in `prompts/01-prompt-starter.md`.
- Added a root `.gitignore` entry for `tmp/`.
- Moved repository notes into `docs/notes.md`.
- Established this work diary to track repo changes and implementation decisions.

## 2026-03-27

- Added briefing, slide, and problem statement materials in `docs/`.
- Added research and planning prompts in `prompts/` for literature survey, software survey, gap analysis, and problem statement generation.
- Added survey and gap-analysis outputs in `reports/`, including standardised engineering software AI survey filenames.
- Prepared the repository for initial version control setup and remote push.
- Formatted `reports/03-gemini-report.md` into structured Markdown with headings, tables, and bullet lists.
- Actioned `prompts/04-gap-analysis-prompt.md`: produced `reports/04-claude-gap-analysis.md` synthesising all six survey reports into a four-tier landscape model with gap findings and hackathon recommendations.
- Actioned `prompts/05-problem-statement-prompt.md`: produced `docs/05-claude-problem-statement.md` with full problem statement, justification bullets, acceptable student directions, and scope guardrails.
- Actioned `prompts/06-short-problem-statement-prompt.md`: produced `docs/06-claude-short-problem-statement.md` with short (~200 word), ultra-short (3 sentence), and one-sentence versions.
## 2026-03-29

- Created `prompts/08-registration-page-prompt.md` to adapt the Clinical AI registration form for the ElectroAI Hackathon.
- Generated the ElectroAI Hackathon registration page content in `docs/electroai-hackathon-registration-page.md`, specifically tailored for Electrical Engineering students but open to all.
- Created a plain-text version of the registration page in `docs/electroai-hackathon-registration-page.txt` for direct use in online forms.
- Integrated the official registration link (`https://forms.gle/MaSj5SV3j6uy6H8x7`) into `README.md`, the registration Markdown page, and the plain-text copy.
- Updated the registration page eligibility to emphasize that while designed for EE students, all participants are welcome.
- Created `prompts/09-route-logistics-report-prompt.md`, a placeholder prompt for generating route logistics reports (resupply and public transport egress).

## 2026-04-02

- Expanded `README.md` with a detailed hybrid event schedule covering Tuesday to Friday sessions, the allnighter, room allocations, leads, Teams usage, and presentation timing.
- Rewrote the README success criteria and outputs/judging sections to match the ElectroAI Hackathon brief, including the IEEE-style paper requirement and clearer engineering-focused judging language.
- Cleaned up the README presentation by left-aligning the splash image, removing outdated wording, and aligning the embedded master-prompt success criteria with the main judging criteria.
- Copied judging rubric materials from the temporary Clinical AI Hackathon workspace into `judging/electroai-hackathon/`, including source criteria, source prompt, rendered HTML, and PDFs.
- Rebranded the main judging rubric for ElectroAI Hackathon, updated the date to `10 April 2026`, changed the listed judges to Dr Dave Muir, Leotis Buchanan, and TBA, and regenerated the printable PDF.
- Copied `hackathon-prize-vouchers.html` and `hackathon-prize-vouchers.pdf` into the repo root, rebranded them for ElectroAI Hackathon, replaced old winner-specific text with placeholders, updated presenter names, and regenerated the voucher PDF.
- Added a high-priority TODO item in `TODO.md` to create the Gemini CLI, Codex, and Claude Code install page for participants.
