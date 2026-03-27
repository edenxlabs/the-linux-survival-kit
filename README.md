# The Linux Survival Kit

**Commands You Actually Use** — A comprehensive, printable Linux command line cheat sheet by [EdenX Labs](https://www.edenxlabs.com).

![31 sections](https://img.shields.io/badge/sections-31-blue)
![420+ commands](https://img.shields.io/badge/commands-420%2B-green)
![Printable A4](https://img.shields.io/badge/format-A4%20PDF-red)
![License](https://img.shields.io/badge/license-MIT-yellow)

## What's Inside

This isn't another bloated reference manual. It's 420+ commands you'll actually reach for — organized into 31 sections, with practical examples and plain-English explanations.

Two formats included:

| Format | Pages | Best for |
|--------|-------|----------|
| **Portrait** | 13 pages | Reading on screen, single-page printing |
| **Landscape 2-column** | 8 pages | Desk reference, wall printing |

## Sections

| # | Section | # | Section |
|---|---------|---|---------|
| 1 | Navigation & Directory Basics | 17 | Shell Shortcuts & Tricks |
| 2 | File Operations | 18 | Environment & Variables |
| 3 | Viewing & Editing Files | 19 | Cron & Scheduled Tasks |
| 4 | Search & Find | 20 | Special Files & Devices |
| 5 | Users & Groups | 21 | Redirection Patterns & FD Tricks |
| 6 | File Permissions & Ownership | 22 | Command Chaining & Pipelines |
| 7 | Process Management | 23 | List, Filter & Transform Recipes |
| 8 | System Information | 24 | Log Analysis & Filtering |
| 9 | Hardware & Performance | 25 | Curl, Requests & API Filtering |
| 10 | Networking | 26 | Practical One-Liner Recipes |
| 11 | SSH & Remote Access | 27 | Globs, Wildcards & Brace Expansion |
| 12 | Archives & Compression | 28 | History Expansion |
| 13 | Package Management (apt & dnf) | 29 | Special Variables & Parameter Expansion |
| 14 | Systemd & Services | 30 | Test Conditions & Conditionals |
| 15 | Text Processing (Power Tools) | 31 | Miscellaneous & Useful |
| 16 | Redirection & Piping | | |

The title page includes quick-reference boxes for file permissions, cron syntax, file descriptors/redirection, and chaining operators.

## Download

Grab the PDFs directly:

- [**Portrait (13 pages)**](linux_cheatsheet.pdf)
- [**Landscape 2-column (8 pages)**](linux_cheatsheet_landscape.pdf)

## Generate from Source

Both PDFs are generated with Python and [ReportLab](https://www.reportlab.com/). No other dependencies.

```bash
pip install reportlab

# Portrait version
python3 cheatsheet.py

# Landscape 2-column version
python3 cheatsheet_landscape.py
```

Output files are written to the current directory.

## Highlights

Beyond the basics, this cheat sheet covers real-world patterns that most references skip:

**Redirection & file descriptors** — not just `>` and `|`, but `2>&1` ordering gotchas, swapping stdout/stderr, writing to stderr from scripts, process substitution with `<()`.

**Command chaining recipes** — piping `find` into `xargs` into `grep`, frequency counting with `sort | uniq -c | sort -rn`, line-by-line processing with `while read`.

**Log analysis** — live-filtering with `tail -f | grep --line-buffered`, awk-based HTTP status code parsing, ranking IPs and URLs from access logs, searching rotated gzipped logs with `zgrep`.

**API/curl patterns** — jq pipelines for filtering and reshaping JSON, timing breakdowns, extracting just the HTTP status code, and more.

**Shell internals** — parameter expansion (`${var%pattern}`, `${var:-default}`), brace expansion tricks, test conditions, history expansion beyond `!!`.

## Contributing

Found a typo? Missing your favorite command? PRs are welcome. The data lives in the `sections` list at the top of each script — just add a tuple of `("command", "description")` to the relevant section.

## License

MIT — print it, share it, put it on your wall.

---

*Built by [EdenX Labs](https://www.edenxlabs.com)*
