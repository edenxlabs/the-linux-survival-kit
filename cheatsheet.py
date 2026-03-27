#!/usr/bin/env python3
"""Generate a comprehensive The Linux Survival Kit  —  EdenX Labs PDF."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfgen import canvas as canv

# ── Colors ──────────────────────────────────────────────────────────
DARK_BG    = HexColor("#1e1e2e")   # dark section header bg
ACCENT     = HexColor("#89b4fa")   # blue accent
GREEN      = HexColor("#a6e3a1")   # green for commands
SURFACE    = HexColor("#f5f5f5")   # light gray row bg
BORDER     = HexColor("#cccccc")
TEXT_DARK  = HexColor("#1e1e2e")
TEXT_MED   = HexColor("#444444")
HEADER_BG  = HexColor("#2b2b3d")
CMD_BG     = HexColor("#f0f4ff")
WHITE      = white

# ── Page Setup ──────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4
MARGIN = 1.2 * cm

# ── Styles ──────────────────────────────────────────────────────────
style_section = ParagraphStyle(
    "SectionTitle", fontName="Helvetica-Bold", fontSize=13,
    textColor=WHITE, leading=18, spaceBefore=0, spaceAfter=0,
    alignment=TA_LEFT, leftIndent=4,
)
style_cmd = ParagraphStyle(
    "Cmd", fontName="Courier-Bold", fontSize=7.8, textColor=HexColor("#0a58ca"),
    leading=10.5, spaceBefore=0, spaceAfter=0,
)
style_desc = ParagraphStyle(
    "Desc", fontName="Helvetica", fontSize=7.8, textColor=TEXT_MED,
    leading=10.5, spaceBefore=0, spaceAfter=0,
)
style_subtitle = ParagraphStyle(
    "Subtitle", fontName="Helvetica-Bold", fontSize=8.5, textColor=TEXT_DARK,
    leading=12, spaceBefore=6, spaceAfter=2,
)

# ── Data ────────────────────────────────────────────────────────────
sections = [
    ("1 — NAVIGATION & DIRECTORY BASICS", [
        ("pwd", "Print current working directory"),
        ("cd /path/to/dir", "Change to specified directory"),
        ("cd ~  or  cd", "Go to your home directory"),
        ("cd ..", "Move up one directory level"),
        ("cd -", "Switch to the previous directory"),
        ("cd ~john", "Go to another users home directory (~user)"),
        ("cd ~john", "Go to user john's home directory"),
        (".", "Current directory (e.g., cp file.txt . copies here)"),
        ("/", "Filesystem root (e.g., ls / lists top-level dirs)"),
        ("ls", "List files in current directory"),
        ("ls -la", "List all files (incl. hidden) in long format"),
        ("ls -lhS", "List files sorted by size, human-readable"),
        ("ls -ltr", "List files sorted by modification time (oldest first)"),
        ("tree -L 2", "Show directory tree, 2 levels deep"),
        ("mkdir -p dir1/dir2", "Create nested directories in one step"),
        ("rmdir dir", "Remove an empty directory"),
    ]),

    ("2 — FILE OPERATIONS", [
        ("touch file.txt", "Create empty file or update its timestamp"),
        ("cp src dst", "Copy file src to dst"),
        ("cp -r srcdir/ dstdir/", "Copy directory recursively"),
        ("cp -a src dst", "Archive copy (preserves permissions, links, timestamps)"),
        ("mv old new", "Move or rename a file/directory"),
        ("rm file.txt", "Delete a file"),
        ("rm -rf dir/", "Force-delete directory and all contents (use carefully!)"),
        ("ln -s /path/to/target link", "Create a symbolic (soft) link"),
        ("ln /path/to/target link", "Create a hard link"),
        ("stat file.txt", "Display detailed file metadata (size, inode, times)"),
        ("file document.pdf", "Determine a file's type"),
    ]),

    ("3 — VIEWING & EDITING FILES", [
        ("cat file.txt", "Print entire file to terminal"),
        ("cat -n file.txt", "Print file with line numbers"),
        ("tac file.txt", "Print file in reverse (last line first)"),
        ("less file.txt", "Scroll through a file (q to quit, / to search)"),
        ("head -n 20 file.txt", "Show first 20 lines"),
        ("tail -n 20 file.txt", "Show last 20 lines"),
        ("tail -f /var/log/syslog", "Follow a log file in real time"),
        ("wc -l file.txt", "Count lines in a file"),
        ("wc -w file.txt", "Count words in a file"),
        ("diff file1 file2", "Show differences between two files"),
        ("nano file.txt", "Edit file with nano (beginner-friendly editor)"),
        ("vim file.txt", "Edit file with vim (powerful modal editor)"),
    ]),

    ("4 — SEARCH & FIND", [
        ("find / -name '*.log'", "Find all .log files starting from /"),
        ("find . -type f -mtime -7", "Files modified in last 7 days"),
        ("find . -type f -size +100M", "Files larger than 100 MB"),
        ("find . -name '*.tmp' -delete", "Find and delete all .tmp files"),
        ("find . -type f -exec chmod 644 {} \\;", "Run command on each found file"),
        ("locate filename", "Fast search using pre-built index (run updatedb first)"),
        ("which python3", "Show full path of an executable"),
        ("whereis gcc", "Locate binary, source, and man page for a program"),
        ("grep 'pattern' file.txt", "Search for pattern in file"),
        ("grep -rn 'TODO' src/", "Recursive search with line numbers"),
        ("grep -i 'error' log.txt", "Case-insensitive search"),
        ("grep -v 'debug' log.txt", "Show lines NOT matching pattern"),
        ("grep -c 'error' log.txt", "Count matching lines"),
        ("grep -E 'err|warn' log.txt", "Extended regex (OR pattern)"),
    ]),

    ("5 — USERS & GROUPS", [
        ("whoami", "Show current username"),
        ("id", "Show current user's UID, GID, and groups"),
        ("who", "Show who is currently logged in"),
        ("w", "Show logged-in users and their activity"),
        ("last", "Show recent login history"),
        ("sudo useradd -m -s /bin/bash john", "Create user john with home dir & bash shell"),
        ("sudo passwd john", "Set or change password for john"),
        ("sudo userdel -r john", "Delete user john and their home directory"),
        ("sudo usermod -aG docker john", "Add john to the docker group"),
        ("groups john", "List all groups john belongs to"),
        ("sudo groupadd devteam", "Create a new group"),
        ("su - john", "Switch to user john (with login shell)"),
        ("sudo -i", "Open a root shell"),
    ]),

    ("6 — FILE PERMISSIONS & OWNERSHIP", [
        ("chmod 755 script.sh", "Owner: rwx, Group: r-x, Others: r-x"),
        ("chmod 644 file.txt", "Owner: rw-, Group: r--, Others: r--"),
        ("chmod u+x script.sh", "Add execute permission for owner"),
        ("chmod g-w file.txt", "Remove write permission for group"),
        ("chmod -R 750 dir/", "Recursively set permissions on directory"),
        ("chmod a+r file.txt", "Give read permission to everyone"),
        ("chown user:group file.txt", "Change owner and group of a file"),
        ("chown -R user:group dir/", "Recursively change ownership"),
        ("chgrp www-data /var/www", "Change group ownership"),
        ("umask 022", "Set default permissions for new files (results in 644/755)"),
        ("getfacl file.txt", "View access control list (ACL) for a file"),
        ("setfacl -m u:john:rw file.txt", "Grant john read-write via ACL"),
    ]),

    ("7 — PROCESS MANAGEMENT", [
        ("ps aux", "Show all running processes with details"),
        ("ps aux | grep nginx", "Find processes matching 'nginx'"),
        ("top", "Live process viewer (q to quit)"),
        ("htop", "Interactive process viewer (better than top)"),
        ("kill PID", "Gracefully terminate process by PID"),
        ("kill -9 PID", "Force kill a process immediately"),
        ("killall processname", "Kill all processes by name"),
        ("pkill -f 'pattern'", "Kill processes matching a pattern"),
        ("pgrep -la nginx", "Find PIDs of processes matching nginx"),
        ("nohup command &amp;", "Run command in background, survives logout"),
        ("jobs", "List background/stopped jobs in current shell"),
        ("fg %1", "Bring job 1 to foreground"),
        ("bg %1", "Resume stopped job 1 in background"),
        ("Ctrl+Z  then  bg", "Suspend running process, then continue in background"),
        ("nice -n 10 command", "Run command with lower priority"),
        ("renice -n 5 -p PID", "Change priority of a running process"),
    ]),

    ("8 — SYSTEM INFORMATION", [
        ("uname -a", "Full system/kernel info"),
        ("uname -r", "Kernel version only"),
        ("hostname", "Show system hostname"),
        ("hostnamectl", "Detailed host and OS info (systemd)"),
        ("cat /etc/os-release", "Show distro name and version"),
        ("lsb_release -a", "Distribution-specific info (if installed)"),
        ("uptime", "System uptime and load averages"),
        ("date", "Current date and time"),
        ("timedatectl", "Time zone and NTP sync status"),
        ("cal", "Show this month's calendar"),
        ("dmesg | tail", "Recent kernel messages (hardware events, errors)"),
        ("journalctl -xe", "Recent systemd journal entries with explanations"),
    ]),

    ("9 — HARDWARE & PERFORMANCE", [
        ("lscpu", "CPU architecture details"),
        ("free -h", "Memory usage (human-readable)"),
        ("cat /proc/meminfo", "Detailed memory info"),
        ("lsblk", "List block devices (disks & partitions)"),
        ("lspci", "List PCI devices (GPU, NIC, etc.)"),
        ("lsusb", "List USB devices"),
        ("df -hT", "Disk space usage with filesystem type"),
        ("du -sh /path", "Total size of a directory"),
        ("du -h --max-depth=1 /home", "Size of each item in /home (1 level)"),
        ("ncdu /", "Interactive disk usage analyzer (ncurses-based)"),
        ("iostat -x 1", "Detailed disk I/O stats every 1 second"),
        ("vmstat 1", "Virtual memory stats every 1 second"),
        ("mpstat -P ALL 1", "Per-CPU utilization every 1 second"),
        ("sensors", "CPU/GPU temperatures (requires lm-sensors)"),
    ]),

    ("10 — NETWORKING", [
        ("ip addr show", "Show IP addresses of all interfaces"),
        ("ip route show", "Show routing table"),
        ("ip link set eth0 up", "Bring network interface up"),
        ("ss -tulnp", "Show listening TCP/UDP ports with process info"),
        ("ping -c 4 google.com", "Send 4 ICMP pings to test connectivity"),
        ("traceroute google.com", "Trace the network path to a host"),
        ("dig example.com", "DNS lookup for a domain"),
        ("nslookup example.com", "Simple DNS query"),
        ("host example.com", "DNS lookup (concise output)"),
        ("curl -I https://example.com", "Fetch HTTP headers only"),
        ("curl -O https://example.com/file", "Download a file"),
        ("wget https://example.com/file", "Download a file (with resume support)"),
        ("whois example.com", "WHOIS domain information"),
        ("nmap -sT localhost", "Scan open TCP ports on localhost"),
        ("iptables -L -n", "List firewall rules"),
        ("netstat -tulnp", "Show listening ports (legacy, use ss instead)"),
    ]),

    ("11 — SSH & REMOTE ACCESS", [
        ("ssh user@host", "Connect to remote host as user"),
        ("ssh -p 2222 user@host", "Connect on a custom port"),
        ("ssh -i ~/.ssh/key.pem user@host", "Connect using a specific private key"),
        ("ssh-keygen -t ed25519", "Generate a modern SSH key pair"),
        ("ssh-copy-id user@host", "Copy your public key to remote host"),
        ("scp file.txt user@host:/tmp/", "Copy local file to remote /tmp"),
        ("scp user@host:/var/log/app.log .", "Copy remote file to current dir"),
        ("scp -r dir/ user@host:/backup/", "Copy directory recursively to remote"),
        ("rsync -avz src/ user@host:/dst/", "Sync directory to remote with compression"),
        ("rsync -avz --delete src/ dst/", "Sync and delete extra files at destination"),
        ("ssh -L 8080:localhost:80 user@host", "Local port forwarding (tunnel)"),
        ("ssh -D 1080 user@host", "Dynamic SOCKS proxy through SSH"),
    ]),

    ("12 — ARCHIVES & COMPRESSION", [
        ("tar cf archive.tar dir/", "Create tar archive of dir/"),
        ("tar czf archive.tar.gz dir/", "Create gzip-compressed tar"),
        ("tar cjf archive.tar.bz2 dir/", "Create bzip2-compressed tar"),
        ("tar xf archive.tar", "Extract tar archive"),
        ("tar xzf archive.tar.gz", "Extract gzip-compressed tar"),
        ("tar xjf archive.tar.bz2", "Extract bzip2-compressed tar"),
        ("tar tzf archive.tar.gz", "List contents of a .tar.gz without extracting"),
        ("tar xzf archive.tar.gz -C /dst", "Extract to a specific directory"),
        ("zip -r archive.zip dir/", "Create a zip archive"),
        ("unzip archive.zip", "Extract a zip archive"),
        ("unzip -l archive.zip", "List contents of a zip file"),
        ("gzip file.txt", "Compress file (replaces original with file.txt.gz)"),
        ("gunzip file.txt.gz", "Decompress gzip file"),
        ("zcat file.txt.gz", "View compressed file without extracting"),
    ]),

    ("13 — PACKAGE MANAGEMENT", None),  # special: subsections
    ("__sub_Debian / Ubuntu (apt)", [
        ("sudo apt update", "Refresh package index from repositories"),
        ("sudo apt upgrade", "Upgrade all installed packages"),
        ("sudo apt install nginx", "Install a package"),
        ("sudo apt remove nginx", "Remove a package (keep config)"),
        ("sudo apt purge nginx", "Remove package and its config files"),
        ("sudo apt autoremove", "Remove unused dependency packages"),
        ("apt search keyword", "Search for packages by keyword"),
        ("apt show package", "Show package details"),
        ("dpkg -l", "List all installed packages"),
    ]),
    ("__sub_RHEL / Fedora (dnf/yum)", [
        ("sudo dnf install nginx", "Install a package"),
        ("sudo dnf remove nginx", "Remove a package"),
        ("sudo dnf update", "Update all packages"),
        ("dnf search keyword", "Search for packages"),
        ("dnf info package", "Show package info"),
        ("rpm -qa", "List all installed RPM packages"),
        ("rpm -ivh package.rpm", "Install a local RPM file"),
    ]),

    ("14 — SYSTEMD & SERVICES", [
        ("systemctl start nginx", "Start a service"),
        ("systemctl stop nginx", "Stop a service"),
        ("systemctl restart nginx", "Restart a service"),
        ("systemctl reload nginx", "Reload config without restarting"),
        ("systemctl status nginx", "Show service status and recent logs"),
        ("systemctl enable nginx", "Enable service to start at boot"),
        ("systemctl disable nginx", "Disable service from starting at boot"),
        ("systemctl is-active nginx", "Check if service is running"),
        ("systemctl list-units --type=service", "List all active services"),
        ("systemctl list-unit-files --state=enabled", "List enabled services"),
        ("journalctl -u nginx -f", "Follow logs for a specific service"),
        ("journalctl --since '1 hour ago'", "Show logs from last hour"),
        ("systemctl daemon-reload", "Reload systemd after editing unit files"),
    ]),

    ("15 — TEXT PROCESSING (POWER TOOLS)", [
        ("sort file.txt", "Sort lines alphabetically"),
        ("sort -n file.txt", "Sort lines numerically"),
        ("sort -u file.txt", "Sort and remove duplicates"),
        ("uniq", "Remove adjacent duplicate lines (use after sort)"),
        ("cut -d',' -f1,3 data.csv", "Extract columns 1 and 3 from CSV"),
        ("awk '{print $1, $3}' file.txt", "Print 1st and 3rd whitespace-delimited fields"),
        ("awk -F: '{print $1}' /etc/passwd", "Print all usernames from passwd"),
        ("sed 's/old/new/g' file.txt", "Replace all 'old' with 'new' (stdout)"),
        ("sed -i 's/old/new/g' file.txt", "Replace in-place (modifies the file)"),
        ("sed -n '10,20p' file.txt", "Print lines 10 through 20"),
        ("tr 'a-z' 'A-Z' &lt; file.txt", "Convert lowercase to uppercase"),
        ("tr -d '\\r' &lt; dos.txt &gt; unix.txt", "Remove Windows carriage returns"),
        ("paste file1 file2", "Merge lines of files side by side"),
        ("xargs", "Build and execute commands from stdin input"),
        ("command | tee output.txt", "Write output to file AND terminal"),
    ]),

    ("16 — REDIRECTION & PIPING", [
        ("command &gt; file.txt", "Redirect stdout to file (overwrite)"),
        ("command &gt;&gt; file.txt", "Append stdout to file"),
        ("command 2&gt; error.log", "Redirect stderr to file"),
        ("command &gt; out.txt 2&gt;&amp;1", "Redirect both stdout and stderr to file"),
        ("command &amp;&gt; all.log", "Shorthand: redirect stdout+stderr (bash)"),
        ("command1 | command2", "Pipe stdout of command1 into command2"),
        ("command1 |&amp; command2", "Pipe stdout and stderr into command2"),
        ("command &lt; input.txt", "Feed file contents as stdin"),
        ("cat &lt;&lt;EOF &gt; file.txt", "Here-document: write multi-line text to file"),
        ("diff &lt;(cmd1) &lt;(cmd2)", "Process substitution: compare output of two commands"),
    ]),

    ("17 — SHELL SHORTCUTS & TRICKS", [
        ("Ctrl+C", "Kill current foreground process"),
        ("Ctrl+Z", "Suspend current process (resume with fg or bg)"),
        ("Ctrl+D", "Send EOF / log out of current shell"),
        ("Ctrl+R", "Reverse search command history"),
        ("Ctrl+A / Ctrl+E", "Jump to beginning / end of line"),
        ("Ctrl+U / Ctrl+K", "Delete from cursor to start / end of line"),
        ("Ctrl+L", "Clear the terminal screen (same as clear)"),
        ("!!", "Repeat the last command"),
        ("!$", "Reuse the last argument of previous command"),
        ("sudo !!", "Re-run last command with sudo"),
        ("history | grep ssh", "Search command history for 'ssh'"),
        ("alias ll='ls -la'", "Create a shortcut alias"),
        ("echo $?", "Show exit code of last command (0 = success)"),
        ("command1 &amp;&amp; command2", "Run command2 only if command1 succeeds"),
        ("command1 || command2", "Run command2 only if command1 fails"),
    ]),

    ("18 — ENVIRONMENT & VARIABLES", [
        ("echo $PATH", "Show the executable search path"),
        ("echo $HOME", "Show home directory path"),
        ("export VAR='value'", "Set an environment variable for current session"),
        ("env", "List all environment variables"),
        ("printenv VAR", "Print value of a specific variable"),
        ("source ~/.bashrc", "Reload bash configuration"),
        ("echo 'export PATH=$PATH:/opt/bin' &gt;&gt; ~/.bashrc", "Permanently add to PATH"),
        ("unset VAR", "Remove an environment variable"),
    ]),

    ("19 — CRON & SCHEDULED TASKS", [
        ("crontab -l", "List your cron jobs"),
        ("crontab -e", "Edit your cron jobs"),
        ("crontab -r", "Remove all your cron jobs"),
        ("sudo crontab -u john -l", "List cron jobs for user john"),
        ("* * * * * command", "Cron: every minute"),
        ("0 * * * * command", "Cron: every hour at minute 0"),
        ("0 2 * * * command", "Cron: daily at 2:00 AM"),
        ("0 0 * * 0 command", "Cron: weekly on Sunday at midnight"),
        ("0 0 1 * * command", "Cron: first day of every month"),
        ("@reboot command", "Cron: run once at system startup"),
    ]),

    ("20 — SPECIAL FILES & DEVICES", [
        ("/dev/null", "Black hole — discards anything written to it"),
        ("/dev/zero", "Infinite stream of zero bytes (for creating blank files)"),
        ("/dev/urandom", "Infinite stream of random bytes"),
        ("/dev/stdin, /dev/stdout, /dev/stderr", "Symlinks to fd 0, 1, 2 of current process"),
        ("/proc/self/", "Info about the current process (PID, memory maps, etc.)"),
        ("/proc/cpuinfo, /proc/meminfo", "CPU and memory details exposed by kernel"),
        ("/etc/hosts", "Local DNS overrides — map hostnames to IPs"),
        ("/etc/resolv.conf", "DNS resolver configuration"),
        ("/etc/fstab", "Filesystem mount table (auto-mount at boot)"),
        ("/etc/crontab", "System-wide cron schedule"),
        ("/etc/passwd", "User account info (username, UID, home, shell)"),
        ("/etc/shadow", "Encrypted password hashes (root-only)"),
        ("/etc/sudoers", "Sudo privilege configuration (edit with visudo)"),
        ("/var/log/syslog or /var/log/messages", "Main system log"),
        ("/var/log/auth.log or /var/log/secure", "Authentication/login log"),
    ]),

    ("21 — REDIRECTION PATTERNS & FD TRICKS", [
        ("cmd > /dev/null 2>&1", "Silence ALL output (stdout + stderr to null)"),
        ("cmd &> /dev/null", "Same as above — bash shorthand"),
        ("cmd 2>/dev/null", "Silence errors only, keep normal output"),
        ("cmd 1>/dev/null", "Silence normal output only, keep errors"),
        ("cmd 2>&1 | grep error", "Pipe BOTH stdout and stderr into grep"),
        ("cmd |& grep error", "Same as above — bash shorthand"),
        ("cmd > out.log 2> err.log", "Send stdout and stderr to separate files"),
        ("cmd 3>&1 1>&2 2>&3", "Swap stdout and stderr"),
        ("exec 2> /tmp/script_errors.log", "Redirect all future stderr in a script to a file"),
        ("echo 'msg' >&2", "Write to stderr (useful inside scripts for status msgs)"),
        ("echo 'msg' > /dev/stderr", "Alternative: write to stderr via device path"),
        ("read line < /dev/stdin", "Explicitly read from stdin"),
        ("cat < /dev/null > empty.txt", "Create an empty file using special devices"),
        ("diff <(sort file1) <(sort file2)", "Compare sorted versions without temp files"),
        ("cmd | tee >(grep ERR > errs.txt)", "Tee output into a process substitution"),
    ]),

    ("22 — COMMAND CHAINING & PIPELINES", [
        ("cmd1 && cmd2", "Run cmd2 ONLY if cmd1 succeeds (exit code 0)"),
        ("cmd1 || cmd2", "Run cmd2 ONLY if cmd1 fails (exit code != 0)"),
        ("cmd1 ; cmd2", "Run cmd2 regardless of cmd1 result"),
        ("cmd1 | cmd2 | cmd3", "Chain: stdout of each feeds stdin of next"),
        ("cmd1 && cmd2 || cmd3", "If cmd1 succeeds run cmd2, else run cmd3"),
        ("(cmd1 ; cmd2) | cmd3", "Group commands, pipe combined output"),
        ("{ cmd1 ; cmd2 ; } > file", "Group without subshell, redirect together"),
        ("cmd1 | xargs cmd2", "Pass stdout lines of cmd1 as args to cmd2"),
        ("cmd1 | xargs -I {} cmd2 {}", "Place each line into {} placeholder"),
        ("cmd | head -1 | xargs -I {} sh -c 'echo {}'", "Chain: get first line, use in another cmd"),
        ("while read line; do echo $line; done < file", "Process file line by line in a loop"),
        ("cmd | while read line; do ...; done", "Process pipe output line by line"),
        ("for f in *.log; do echo $f; done", "Loop over matching files"),
    ]),

    ("23 — LIST, FILTER & TRANSFORM RECIPES", [
        ("ls -la | grep '.log'", "List files, filter to show only .log entries"),
        ("ls -lhS | head -20", "Top 20 largest files in current dir"),
        ("find . -name '*.py' | wc -l", "Count all Python files recursively"),
        ("find . -name '*.py' | xargs grep 'import'", "Search for 'import' in all .py files"),
        ("find . -type f -empty", "Find all empty files"),
        ("find . -mmin -30 -type f", "Files modified in last 30 minutes"),
        ("find . -name '*.bak' -exec rm {} +", "Delete all .bak files (efficient batch)"),
        ("cat file | sort | uniq -c | sort -rn", "Frequency count: sort, count dupes, rank"),
        ("cat file | tr ' ' '\\n' | sort | uniq -c | sort -rn", "Word frequency analysis"),
        ("cut -d: -f1 /etc/passwd | sort", "List all usernames, sorted"),
        ("awk -F: '$3 >= 1000 {print $1}' /etc/passwd", "List non-system users (UID >= 1000)"),
        ("du -sh */ | sort -rh | head -10", "Top 10 largest subdirectories"),
        ("ps aux --sort=-%mem | head -11", "Top 10 processes by memory usage"),
        ("ps aux --sort=-%cpu | head -11", "Top 10 processes by CPU usage"),
        ("dpkg -l | awk '/^ii/{print $2}' | wc -l", "Count installed packages (Debian)"),
    ]),

    ("24 — LOG ANALYSIS & FILTERING", [
        ("tail -f /var/log/syslog", "Follow system log in real time"),
        ("tail -f log | grep --line-buffered 'ERROR'", "Live-follow and filter for ERROR lines"),
        ("tail -1000 app.log | grep -i 'exception'", "Search last 1000 lines for exceptions"),
        ("grep -c 'ERROR' app.log", "Count total error occurrences"),
        ("grep -B2 -A5 'FATAL' app.log", "Show 2 lines before and 5 after each FATAL"),
        ("grep 'ERROR' app.log | awk '{print $1, $2}' | sort | uniq -c | sort -rn",
         "Rank error frequency by timestamp (date+time)"),
        ("awk '/2025-03-26/ && /ERROR/' app.log", "Errors on a specific date"),
        ("awk '$9 == 500' access.log", "Find HTTP 500 responses in nginx/apache log"),
        ("awk '$9 >= 400' access.log | wc -l", "Count all 4xx/5xx HTTP errors"),
        ("awk '{print $7}' access.log | sort | uniq -c | sort -rn | head -20",
         "Top 20 most requested URLs"),
        ("awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10",
         "Top 10 client IPs by request count"),
        ("awk '{sum+=$10} END {print sum/1024/1024 \" MB\"}' access.log",
         "Total bytes transferred (field 10 = bytes)"),
        ("journalctl -u nginx --since '2 hours ago' --no-pager",
         "Systemd: nginx logs from last 2 hours"),
        ("journalctl -p err -b", "All error-priority messages since last boot"),
        ("journalctl --disk-usage", "Check how much disk journal logs consume"),
        ("zgrep 'error' /var/log/syslog.2.gz", "Search inside gzipped rotated logs"),
    ]),

    ("25 — CURL, REQUESTS & API FILTERING", [
        ("curl -s https://api.example.com/data", "Silent GET request (no progress bar)"),
        ("curl -sS https://example.com", "Silent but show errors"),
        ("curl -s url | jq .", "GET JSON and pretty-print with jq"),
        ("curl -s url | jq '.results[].name'", "Extract 'name' from each item in results array"),
        ("curl -s url | jq '.[] | select(.status==\"active\")'",
         "Filter JSON array: only objects where status is active"),
        ("curl -s url | jq '[.[] | {name, email}]'",
         "Reshape: pick only name and email fields"),
        ("curl -s url | jq '.items | length'", "Count items in a JSON array"),
        ("curl -o output.json url", "Save response body to file"),
        ("curl -I url", "Fetch only HTTP response headers"),
        ("curl -s -o /dev/null -w '%{http_code}' url", "Get just the HTTP status code"),
        ("curl -s -o /dev/null -w '%{time_total}s' url", "Measure total request time"),
        ("curl -X POST -H 'Content-Type: application/json' -d '{\"key\":\"val\"}' url",
         "POST JSON data"),
        ("curl -u user:pass url", "Basic authentication"),
        ("curl -L url", "Follow redirects automatically"),
        ("curl -s url | grep -oP 'href=\"\\K[^\"]*'", "Extract all href links from HTML"),
        ("curl -w '\\nDNS: %{time_namelookup}s\\nConnect: %{time_connect}s\\nTotal: %{time_total}s\\n' -o /dev/null -s url",
         "Detailed timing breakdown of a request"),
    ]),

    ("26 — PRACTICAL ONE-LINER RECIPES", [
        ("find . -name '*.log' -mtime +30 -delete", "Delete log files older than 30 days"),
        ("find . -type f -name '*.jpg' | xargs -I{} cp {} /backup/", "Backup all JPGs found recursively"),
        ("tar czf backup-$(date +%F).tar.gz /etc/", "Timestamped backup of /etc"),
        ("grep -rl 'oldtext' . | xargs sed -i 's/oldtext/newtext/g'",
         "Find & replace text across all files recursively"),
        ("for f in *.txt; do mv \"$f\" \"${f%.txt}.md\"; done",
         "Batch rename: change .txt extension to .md"),
        ("find . -name '*.py' -exec wc -l {} + | tail -1",
         "Total lines of code in all Python files"),
        ("ss -tulnp | awk 'NR>1 {print $5}' | cut -d: -f2 | sort -un",
         "List all unique listening ports"),
        ("while ! ping -c1 host &>/dev/null; do sleep 1; done; echo 'Host is up!'",
         "Wait until a host comes online"),
        ("cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 32; echo",
         "Generate a random 32-char password"),
        ("history | awk '{print $2}' | sort | uniq -c | sort -rn | head -10",
         "Your top 10 most-used commands"),
        ("diff <(ssh host1 cat /etc/config) <(ssh host2 cat /etc/config)",
         "Compare a file across two remote servers"),
        ("comm -23 <(sort file1) <(sort file2)", "Lines in file1 but not in file2"),
        ("paste -sd+ numbers.txt | bc", "Sum all numbers in a file (one per line)"),
        ("awk '{s+=$1} END {print s}' numbers.txt", "Sum first column of a file"),
        ("netstat -an | awk '/ESTABLISHED/ {print $5}' | cut -d: -f1 | sort | uniq -c | sort -rn",
         "Rank remote IPs by number of active connections"),
        ("inotifywait -m -r /path -e modify | while read; do echo 'Changed!'; done",
         "Watch directory for file changes and react"),
    ]),

    ("27 — GLOBS, WILDCARDS & BRACE EXPANSION", [
        ("*", "Match any characters (ls *.log = all .log files)"),
        ("?", "Match exactly one character (file?.txt = file1.txt, fileA.txt)"),
        ("[abc]", "Match one of the listed characters (file[123].txt)"),
        ("[a-z]", "Match a character range ([0-9]* = starts with a digit)"),
        ("[!abc]  or  [^abc]", "Match any character NOT listed"),
        ("{a,b,c}", "Brace expansion (file.{txt,md,log} = 3 separate names)"),
        ("{1..10}", "Sequence expansion (echo {1..10} = 1 2 3 ... 10)"),
        ("{01..05}", "Zero-padded sequence (file{01..05}.txt)"),
        ("{a..z}", "Letter sequence expansion"),
        ("**", "Recursive glob (bash: shopt -s globstar first)"),
        ("cp file{,.bak}", "Expands to: cp file file.bak (quick backup trick)"),
        ("mkdir -p project/{src,lib,bin,docs}", "Create multiple dirs in one command"),
    ]),

    ("28 — HISTORY EXPANSION (ADVANCED)", [
        ("!!", "Repeat the last command (sudo !! is the classic use)"),
        ("!$", "Last argument of previous command"),
        ("!^", "First argument of previous command"),
        ("!*", "All arguments of previous command"),
        ("!n", "Run command number n from history (see with history)"),
        ("!-n", "Run the command n steps back (!-2 = 2 commands ago)"),
        ("!string", "Run last command that starts with 'string'"),
        ("!?string", "Run last command containing 'string' anywhere"),
        ("^old^new", "Repeat last command, replacing 'old' with 'new'"),
        ("!:gs/old/new", "Repeat last command, replace ALL occurrences"),
        ("$_", "Last argument of previous command (variable form of !$)"),
        ("fc", "Open last command in $EDITOR for editing, then run it"),
        ("history -c", "Clear command history for current session"),
        ("HISTSIZE=10000", "Set how many commands to keep in memory"),
        ("HISTCONTROL=ignoredups", "Don't save duplicate consecutive commands"),
    ]),

    ("29 — SPECIAL VARIABLES & PARAMETER EXPANSION", [
        ("$?", "Exit code of last command (0 = success, non-0 = error)"),
        ("$$", "PID of the current shell"),
        ("$!", "PID of the last background process"),
        ("$0", "Name of the current script or shell"),
        ("$1 .. $9", "Positional arguments passed to script/function"),
        ("$#", "Number of arguments passed to script/function"),
        ("$@", "All arguments as separate words (use in loops)"),
        ("$*", "All arguments as a single string"),
        ("${var:-default}", "Use 'default' if var is unset or empty"),
        ("${var:=default}", "Set var to 'default' if unset or empty"),
        ("${var:+alt}", "Use 'alt' only if var IS set (opposite of :-)"),
        ("${var:?'error msg'}", "Exit with error if var is unset"),
        ("${#var}", "Length of variable's value (char count)"),
        ("${var%pattern}", "Remove shortest suffix match (${f%.txt} = strip .txt)"),
        ("${var%%pattern}", "Remove longest suffix match (greedy)"),
        ("${var#pattern}", "Remove shortest prefix match"),
        ("${var##pattern}", "Remove longest prefix match (${path##*/} = basename)"),
        ("${var/old/new}", "Replace first occurrence of 'old' with 'new'"),
        ("${var//old/new}", "Replace ALL occurrences of 'old' with 'new'"),
        ("${var^}", "Uppercase first character"),
        ("${var^^}", "Uppercase entire string"),
        ("${var,}", "Lowercase first character"),
        ("${var,,}", "Lowercase entire string"),
    ]),

    ("30 — TEST CONDITIONS & CONDITIONALS", [
        ("[ condition ]", "Test command (spaces around brackets are required!)"),
        ("[[ condition ]]", "Enhanced bash test (supports regex, &&, ||, globbing)"),
        ("test condition", "Full command form of [ ] (identical behavior)"),
        ("-f file", "True if file exists and is a regular file"),
        ("-d dir", "True if directory exists"),
        ("-e path", "True if path exists (any type: file, dir, link)"),
        ("-s file", "True if file exists and is NOT empty"),
        ("-r / -w / -x file", "True if file is readable / writable / executable"),
        ("-L file", "True if file is a symbolic link"),
        ("-z \"$var\"", "True if string is empty (zero length)"),
        ("-n \"$var\"", "True if string is NOT empty"),
        ("\"$a\" = \"$b\"", "String equality (use == inside [[ ]])"),
        ("\"$a\" != \"$b\"", "String inequality"),
        ("$a -eq $b", "Numeric equal (-ne not equal, -gt -lt -ge -le)"),
        ("! condition", "Negate any test (! -f file = file does NOT exist)"),
        (": (colon)", "No-op / always true -- placeholder in if/while/functions"),
        (". script.sh  (dot)", "Same as 'source script.sh' -- runs script in current shell"),
    ]),

    ("31 — MISCELLANEOUS & USEFUL", [
        ("man command", "Open manual page for any command"),
        ("command --help", "Quick help / usage summary"),
        ("type command", "Show whether command is alias, builtin, or file"),
        ("watch -n 2 'command'", "Re-run command every 2 seconds and display output"),
        ("time command", "Measure how long a command takes to run"),
        ("yes | command", "Auto-answer 'yes' to prompts"),
        ("screen  or  tmux", "Terminal multiplexers (persistent sessions)"),
        ("lsof -i :80", "Show what process is using port 80"),
        ("dd if=/dev/zero of=test bs=1M count=100", "Create a 100 MB test file"),
        ("sha256sum file.txt", "Compute SHA-256 checksum"),
        ("md5sum file.txt", "Compute MD5 checksum"),
        ("base64 file.txt", "Encode file in base64"),
        ("date +%Y-%m-%d_%H%M%S", "Formatted timestamp (useful in scripts)"),
        ("column -t file.txt", "Format text into aligned columns"),
        ("script session.log", "Record entire terminal session to file"),
        ("strace -p PID", "Trace system calls of a running process"),
    ]),
]

# ── Helpers ─────────────────────────────────────────────────────────

def build_section_header(title):
    """Return a colored full-width section header as a Table."""
    p = Paragraph(title, style_section)
    tbl = Table([[p]], colWidths=[PAGE_W - 2*MARGIN])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HEADER_BG),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("ROUNDEDCORNERS", [4, 4, 4, 4]),
    ]))
    return tbl

def build_subsection_header(title):
    """Subsection label."""
    return Paragraph(f"<b>{title}</b>", style_subtitle)

def build_cmd_table(entries):
    """Return a Table of command/description rows."""
    col_cmd = (PAGE_W - 2*MARGIN) * 0.46
    col_desc = (PAGE_W - 2*MARGIN) * 0.54
    rows = []
    for cmd, desc in entries:
        rows.append([
            Paragraph(cmd.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"), style_cmd),
            Paragraph(desc, style_desc),
        ])
    tbl = Table(rows, colWidths=[col_cmd, col_desc])
    style_cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, -1), 8),
        ("LEFTPADDING", (1, 0), (1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, BORDER),
    ]
    # alternating row backgrounds
    for i in range(len(rows)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), CMD_BG))
    tbl.setStyle(TableStyle(style_cmds))
    return tbl


# ── Title Page Helper ───────────────────────────────────────────────

class TitlePageDocTemplate(SimpleDocTemplate):
    """Custom template that draws a title page on the first page."""
    def __init__(self, *args, **kwargs):
        self._title_text = kwargs.pop("title_text", "")
        self._subtitle_text = kwargs.pop("subtitle_text", "")
        super().__init__(*args, **kwargs)

def draw_header_footer(canvas, doc):
    """Draw footer on every page."""
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(TEXT_MED)
    canvas.drawCentredString(PAGE_W / 2, 12 * mm,
                              f"The Linux Survival Kit  —  EdenX Labs  —  Page {canvas.getPageNumber()}")
    # thin top accent line
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(1.5)
    canvas.line(MARGIN, PAGE_H - MARGIN + 4, PAGE_W - MARGIN, PAGE_H - MARGIN + 4)
    canvas.restoreState()


# ── Build Story ─────────────────────────────────────────────────────

def build_story():
    story = []

    # ── TITLE BLOCK ──
    title_style = ParagraphStyle(
        "MainTitle", fontName="Helvetica-Bold", fontSize=24,
        textColor=TEXT_DARK, leading=30, alignment=TA_CENTER,
        spaceBefore=20, spaceAfter=2,
    )
    subtitle_style = ParagraphStyle(
        "MainSub", fontName="Helvetica", fontSize=11,
        textColor=TEXT_MED, leading=16, alignment=TA_CENTER,
        spaceAfter=4,
    )
    story.append(Spacer(1, 14))
    story.append(Paragraph("EdenX Labs presents", ParagraphStyle(
        "Presents", fontName="Helvetica", fontSize=9,
        textColor=HexColor("#888888"), leading=14, alignment=TA_CENTER,
        spaceBefore=0, spaceAfter=6,
    )))
    story.append(Paragraph("THE LINUX", title_style))
    story.append(Paragraph("SURVIVAL KIT", ParagraphStyle(
        "MainTitle2", parent=title_style, fontSize=28, spaceBefore=0, spaceAfter=8,
        textColor=HexColor("#0a58ca"),
    )))
    story.append(Paragraph("Commands You Actually Use", subtitle_style))
    story.append(Paragraph("31 sections  •  420+ commands  •  Printable A4", ParagraphStyle(
        "MainSub2", parent=subtitle_style, fontSize=9, spaceAfter=20, textColor=HexColor("#888888"),
    )))

    # ── TABLE OF CONTENTS ──
    toc_title = ParagraphStyle(
        "TOCTitle", fontName="Helvetica-Bold", fontSize=12,
        textColor=TEXT_DARK, leading=18, spaceBefore=10, spaceAfter=6,
        alignment=TA_CENTER,
    )
    story.append(Paragraph("TABLE OF CONTENTS", toc_title))

    toc_entries = [s[0] for s in sections if not s[0].startswith("__sub")]
    # Build TOC as a 2-column table
    half = (len(toc_entries) + 1) // 2
    col1 = toc_entries[:half]
    col2 = toc_entries[half:]
    toc_style = ParagraphStyle(
        "TOCEntry", fontName="Helvetica", fontSize=7.5,
        textColor=TEXT_MED, leading=11.5,
    )
    toc_rows = []
    for i in range(max(len(col1), len(col2))):
        left = Paragraph(col1[i], toc_style) if i < len(col1) else ""
        right = Paragraph(col2[i], toc_style) if i < len(col2) else ""
        toc_rows.append([left, right])

    col_w = (PAGE_W - 2*MARGIN - 10) / 2
    toc_tbl = Table(toc_rows, colWidths=[col_w, col_w])
    toc_tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(toc_tbl)

    # Permission reference box
    story.append(Spacer(1, 10))
    perm_title = ParagraphStyle(
        "PermTitle", fontName="Helvetica-Bold", fontSize=9,
        textColor=TEXT_DARK, leading=13, alignment=TA_CENTER, spaceAfter=3,
    )
    perm_style = ParagraphStyle(
        "Perm", fontName="Courier", fontSize=7,
        textColor=TEXT_MED, leading=10, alignment=TA_CENTER,
    )
    story.append(Paragraph("QUICK REFERENCE: FILE PERMISSION NOTATION", perm_title))
    perm_text = (
        "-rwxrw-r--  =  File type(-) | User(rwx) | Group(rw-) | Others(r--)<br/>"
        "r=4  w=2  x=1  |  chmod 755 = rwxr-xr-x  |  chmod 644 = rw-r--r--<br/>"
        "u=user  g=group  o=others  a=all  |  + add  - remove  = set exact"
    )
    story.append(Paragraph(perm_text, perm_style))

    # Cron reference box
    story.append(Spacer(1, 8))
    story.append(Paragraph("QUICK REFERENCE: CRON SCHEDULE FORMAT", perm_title))
    cron_text = (
        "min(0-59)  hour(0-23)  day(1-31)  month(1-12)  weekday(0-7, Sun=0,7)<br/>"
        "  *          *           *          *             *         command<br/>"
        "Examples:  */5 * * * *  (every 5 min)  |  0 9 * * 1-5  (weekdays at 9 AM)"
    )
    story.append(Paragraph(cron_text, perm_style))

    # FD & Redirection reference box
    story.append(Spacer(1, 8))
    story.append(Paragraph("QUICK REFERENCE: FILE DESCRIPTORS &amp; REDIRECTION", perm_title))
    fd_text = (
        "fd 0 = stdin  |  fd 1 = stdout  |  fd 2 = stderr<br/>"
        "&gt;  overwrite  |  &gt;&gt;  append  |  &lt;  input from file  |  |  pipe stdout<br/>"
        "2&gt;&amp;1  stderr to stdout  |  &amp;&gt;  both to file  |  |&amp;  pipe both  |  &lt;()  process sub<br/>"
        "/dev/null = discard  |  /dev/zero = zeros  |  /dev/urandom = random bytes"
    )
    story.append(Paragraph(fd_text, perm_style))

    # Chaining operators reference box
    story.append(Spacer(1, 8))
    story.append(Paragraph("QUICK REFERENCE: CHAINING OPERATORS", perm_title))
    chain_text = (
        "A &amp;&amp; B  run B if A succeeds  |  A || B  run B if A fails  |  A ; B  run B always<br/>"
        "A | B  pipe A's stdout to B  |  A |&amp; B  pipe stdout+stderr<br/>"
        "$(cmd)  capture output  |  $?  last exit code (0=ok)  |  !!  repeat last cmd"
    )
    story.append(Paragraph(chain_text, perm_style))

    story.append(PageBreak())

    # ── SECTIONS ──
    first_section = True
    for title, entries in sections:
        if title.startswith("__sub_"):
            sub_label = title.replace("__sub_", "")
            story.append(build_subsection_header(sub_label))
            story.append(build_cmd_table(entries))
            story.append(Spacer(1, 4))
            continue

        if entries is None:
            top_sp = 6 if first_section else 10
            story.append(Spacer(1, top_sp))
            story.append(build_section_header(title))
            story.append(Spacer(1, 4))
            first_section = False
            continue

        top_sp = 6 if first_section else 10
        header = build_section_header(title)

        if len(entries) <= 8:
            table = build_cmd_table(entries)
            story.append(KeepTogether([
                Spacer(1, top_sp),
                header,
                Spacer(1, 4),
                table,
            ]))
        else:
            head_entries = entries[:2]
            tail_entries = entries[2:]
            head_table = build_cmd_table(head_entries)
            tail_table = build_cmd_table(tail_entries)
            story.append(KeepTogether([
                Spacer(1, top_sp),
                header,
                Spacer(1, 4),
                head_table,
            ]))
            story.append(tail_table)

        first_section = False

    return story


# ── Main ────────────────────────────────────────────────────────────
def main():
    output_path = "/home/claude/linux_cheatsheet.pdf"
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        topMargin=MARGIN + 4,
        bottomMargin=MARGIN + 6,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
    )
    story = build_story()
    doc.build(story, onFirstPage=draw_header_footer, onLaterPages=draw_header_footer)
    print(f"PDF created: {output_path}")


if __name__ == "__main__":
    main()
