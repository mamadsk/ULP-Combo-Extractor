import os
import time
import re
import sys
import shutil
import collections
import statistics
import datetime

# --- NEON CYBERPUNK UI CONSTANTS ---
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"

# Neon Palette (TrueColor simulated with standard ANSI)
NEON_PINK   = "\033[95m"
NEON_CYAN   = "\033[96m"
NEON_BLUE   = "\033[94m"
NEON_GREEN  = "\033[92m"
NEON_YELLOW = "\033[93m"
NEON_RED    = "\033[91m"
WHITE       = "\033[97m"
GRAY        = "\033[90m"
BG_DARK     = "\033[40m"

# --- ICONS ---
ICON_MAIN    = f"{NEON_PINK}❖{RESET}"
ICON_ARROW   = f"{NEON_CYAN}➜{RESET}"
ICON_CHECK   = f"{NEON_GREEN}✔{RESET}"
ICON_CROSS   = f"{NEON_RED}✖{RESET}"
ICON_FOLDER  = f"{NEON_YELLOW}📂{RESET}"
ICON_FILE    = f"{NEON_BLUE}📄{RESET}"
ICON_STATS   = f"{NEON_PINK}📊{RESET}"
ICON_SECURE  = f"{NEON_GREEN}🔒{RESET}"
ICON_WEAK    = f"{NEON_RED}🔓{RESET}"
ICON_SPEED   = f"{NEON_YELLOW}⚡{RESET}"

# --- CONFIGURATION & PATTERNS ---
PERSIAN_ARABIC_PATTERN = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
WHITESPACE_PATTERN = re.compile(r'[\s\t\r\n]')
EMAIL_PATTERN = re.compile(r'^[\w\.-]+@([\w\.-]+\.\w+)$')
NUMERIC_PATTERN = re.compile(r'^\d+$')
ALPHA_PATTERN = re.compile(r'^[a-zA-Z]+$')

# Smart delimiter regex: matches :, ;, or |
DELIMITER_PATTERN = re.compile(r'[:;|]')

BAD_PHRASES_LIST = [
    'old or unknown version', 'notemmysbirthday', 'unknown version', 
    '██████', '██', '<br>', 'null', 'undefined', 'password', 'user:pass',
    'example', 'sample', 'test', 'username:password'
]
BAD_PHRASE_REGEX = re.compile('|'.join(map(re.escape, BAD_PHRASES_LIST)), re.IGNORECASE)

def get_terminal_width():
    try:
        return shutil.get_terminal_size().columns
    except:
        return 80

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_centered(text, width=None):
    if width is None:
        width = get_terminal_width()
    print(text.center(width))

def print_line(char="─", color=GRAY):
    print(f"{color}{char * get_terminal_width()}{RESET}")

def print_banner(text, color=NEON_CYAN):
    print_line("═", color)
    print_centered(f"{BOLD}{color}{text}{RESET}")
    print_line("═", color)

def logo():
    clear_screen()
    print("\n")
    print_centered(f"{NEON_PINK}██╗   ██╗██╗     ██████╗ {RESET}")
    print_centered(f"{NEON_PINK}██║   ██║██║     ██╔══██╗{RESET}")
    print_centered(f"{NEON_CYAN}██║   ██║██║     ██████╔╝{RESET}")
    print_centered(f"{NEON_CYAN}██║   ██║██║     ██╔═══╝ {RESET}")
    print_centered(f"{NEON_BLUE}╚██████╔╝███████╗██║     {RESET}")
    print_centered(f"{NEON_BLUE} ╚═════╝ ╚══════╝╚═╝     {RESET}")
    print("\n")
    print_centered(f"{BOLD}{WHITE}NEON EDITION v2{RESET}")
    print_centered(f"{DIM}Designed by {NEON_PINK}Mohammad SK{RESET}")
    print("\n")

def sizeof_fmt(num, suffix="B"):
    for unit in ['','K','M','G','T','P']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Y', suffix)

def format_time(seconds):
    if seconds < 60: return f"{int(seconds)}s"
    m, s = divmod(int(seconds), 60)
    return f"{m}m {s}s"

def has_invalid_chars(text):
    return bool(PERSIAN_ARABIC_PATTERN.search(text))

def is_bad_combo(user, pw):
    if len(user) < 3 or len(pw) < 2 or len(user) > 100: return True
    if BAD_PHRASE_REGEX.search(user) or BAD_PHRASE_REGEX.search(pw): return True
    if has_invalid_chars(user) or has_invalid_chars(pw): return True
    if WHITESPACE_PATTERN.search(user) or WHITESPACE_PATTERN.search(pw): return True
    return False

def analyze_password(pw):
    if NUMERIC_PATTERN.match(pw):
        return 'numeric'
    if ALPHA_PATTERN.match(pw):
        return 'alpha'
    return 'mixed'

def get_all_txt_files(path):
    file_list = []
    if os.path.isfile(path):
        return [path]
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".txt"):
                file_list.append(os.path.join(root, file))
    return file_list

def select_input_source():
    current_dir = os.getcwd()
    entries = os.listdir(current_dir)
    txt_files = [f for f in entries if f.endswith('.txt') and os.path.isfile(f)]
    
    print_banner("SELECT INPUT SOURCE", NEON_BLUE)
    print("\n")
    
    if txt_files:
        for i, name in enumerate(txt_files, 1):
            size = sizeof_fmt(os.path.getsize(name))
            idx_str = f"{NEON_CYAN}[{i:02d}]{RESET}"
            print(f"  {idx_str} {WHITE}{name:<40} {DIM}({size}){RESET}")
    else:
        print_centered(f"{ICON_CROSS} {GRAY}No text files found.{RESET}")
    
    print("\n")
    print(f"  {NEON_PINK}[?]{RESET} {GRAY}Enter number or path for Batch Mode{RESET}")
    print_line("-", GRAY)
    
    while True:
        choice = input(f" {ICON_ARROW} {NEON_YELLOW}INPUT > {RESET}").strip().strip('"\'')
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(txt_files):
                return [txt_files[idx-1]], False
        if os.path.exists(choice):
            if os.path.isfile(choice):
                return [choice], False
            elif os.path.isdir(choice):
                files = get_all_txt_files(choice)
                if files:
                    return files, True
                else:
                    print(f" {ICON_CROSS} {NEON_RED}Empty folder.{RESET}")
                    continue
        print(f" {ICON_CROSS} {NEON_RED}Invalid input.{RESET}")

def parse_line_smart(line):
    parts = DELIMITER_PATTERN.split(line.strip())
    if len(parts) == 2:
        return parts[0], parts[1]
    elif len(parts) > 2:
        return parts[-2], parts[-1]
    return None, None

def draw_hud(stats, progress, speed_mb, speed_lines, eta, total_files, current_file_idx):
    """Draws a Heads-Up Display (HUD) for processing."""
    lines_to_clear = 8
    sys.stdout.write(f"\033[{lines_to_clear}F") 
    
    width = get_terminal_width() - 4
    
    file_progress = f"File {current_file_idx}/{total_files}"
    print(f"  {NEON_BLUE}{BOLD}PROCESSING...{RESET} {GRAY}{file_progress:>20}{RESET}" + " " * 20)
    
    bar_width = width - 15
    filled = int(bar_width * progress)
    bar = f"{NEON_PINK}{'━' * filled}{GRAY}{'━' * (bar_width - filled)}{RESET}"
    print(f"  {bar} {NEON_CYAN}{int(progress*100):>3}%{RESET}")
    print("")

    c1 = f"{GRAY}Valid:{RESET} {NEON_GREEN}{stats['valid']:,}{RESET}"
    c2 = f"{GRAY}Dups:{RESET}  {NEON_YELLOW}{stats['duplicates']:,}{RESET}"
    c3 = f"{GRAY}Bad:{RESET}   {NEON_RED}{stats['bad']:,}{RESET}"
    
    gap = " " * 4
    row1 = f"  {c1:<25}{gap}{c2:<25}{gap}{c3:<25}"
    print(row1 + " " * 10)

    s1 = f"{GRAY}Speed:{RESET} {WHITE}{speed_mb:.1f} MB/s{RESET}"
    s2 = f"{GRAY}Rate:{RESET}  {WHITE}{speed_lines:,} L/s{RESET}"
    s3 = f"{GRAY}ETA:{RESET}   {NEON_CYAN}{eta}{RESET}"
    
    row2 = f"  {s1:<25}{gap}{s2:<25}{gap}{s3:<25}"
    print(row2 + " " * 10)
    
    print(f"  {GRAY}{'─' * width}{RESET}")
    print("")

def process_files(file_list, is_batch, outfile_base, domain_filter):
    total_size_bytes = sum(os.path.getsize(f) for f in file_list)
    total_files_count = len(file_list)
    
    clear_screen()
    print_banner("SYSTEM ACTIVE", NEON_GREEN)
    print("\n")
    
    print("\n" * 8)

    unique_combos = set()
    pass_stats = {'numeric': 0, 'alpha': 0, 'mixed': 0, 'lengths': []}
    
    stats = {
        'processed_lines': 0, 'valid': 0, 'duplicates': 0, 'bad': 0, 
        'filtered': 0, 'email_type': 0, 'user_type': 0
    }
    
    domain_counter = collections.Counter()
    
    start_time = time.time()
    speed_time = start_time
    speed_counter = 0
    speed_bytes = 0
    processed_bytes = 0
    
    file_idx = 0

    for current_file in file_list:
        file_idx += 1
        try:
            with open(current_file, "r", encoding="utf-8", errors="ignore") as fin:
                for line in fin:
                    line_len = len(line)
                    processed_bytes += line_len
                    speed_bytes += line_len
                    stats['processed_lines'] += 1
                    speed_counter += 1
                    
                    raw = line.strip()
                    if not raw or not DELIMITER_PATTERN.search(raw):
                        stats['bad'] += 1
                        continue
                    if domain_filter and domain_filter.lower() not in raw.lower():
                        stats['filtered'] += 1
                        continue

                    user, pw = parse_line_smart(raw)
                    if not user or not pw or is_bad_combo(user, pw):
                        stats['bad'] += 1
                        continue

                    combo = f"{user}:{pw}"
                    if combo not in unique_combos:
                        unique_combos.add(combo)
                        stats['valid'] += 1
                        
                        ptype = analyze_password(pw)
                        pass_stats[ptype] += 1
                        pass_stats['lengths'].append(len(pw))
                        
                        match = EMAIL_PATTERN.match(user)
                        if match:
                            stats['email_type'] += 1
                            domain = match.group(1).lower()
                            domain_counter[domain] += 1
                        else:
                            stats['user_type'] += 1
                    else:
                        stats['duplicates'] += 1

                    if stats['processed_lines'] % 5000 == 0:
                        cur_time = time.time()
                        if cur_time - speed_time >= 0.2:
                            time_diff = cur_time - speed_time
                            current_speed_lines = int(speed_counter / time_diff)
                            current_speed_mb = (speed_bytes / time_diff) / (1024 * 1024)
                            
                            percent = processed_bytes / total_size_bytes if total_size_bytes > 0 else 0
                            eta = format_time((total_size_bytes - processed_bytes)/(speed_bytes/time_diff)) if speed_bytes > 0 else '...'
                            
                            draw_hud(stats, percent, current_speed_mb, current_speed_lines, eta, total_files_count, file_idx)
                            
                            speed_time = cur_time
                            speed_counter = 0
                            speed_bytes = 0
        except:
            continue

    # Final HUD update (100%)
    draw_hud(stats, 1.0, 0.0, 0, "0s", total_files_count, file_idx)

    # --- SAVE PHASE ---
    print(f"\n  {ICON_MAIN} {NEON_YELLOW}Optimizing & Saving Data...{RESET}")
    
    sorted_combos = sorted(unique_combos)
    created_files = []
    
    main_out = f"{outfile_base}.txt"
    with open(main_out, "w", encoding="utf-8") as fout:
        for combo in sorted_combos:
            fout.write(combo + "\n")
    created_files.append(main_out)
    
    # NOTE: Automatic domain saving removed from here.
    # We now return sorted_combos to allow optional saving later.

    avg_pass = int(statistics.mean(pass_stats['lengths'])) if pass_stats['lengths'] else 0
    return stats, start_time, domain_counter, pass_stats, avg_pass, created_files, sorted_combos

def ask_and_save_domains(outfile_base, sorted_combos, domain_counter):
    # Get top domains with at least 1 hit (or set a small threshold like 10)
    top_domains_data = domain_counter.most_common(5)
    target_domains = [d for d, c in top_domains_data if c > 0]
    
    if not target_domains:
        return

    print("\n")
    print_line("-", GRAY)
    print(f"  {ICON_FOLDER} {NEON_PINK}TOP DOMAINS DETECTED:{RESET}")
    for d, c in top_domains_data:
        if c > 0:
            print(f"    {NEON_CYAN}➜{RESET} {WHITE}{d:<20}{RESET} {DIM}({c:,}){RESET}")
    
    print("\n")
    q = input(f"  {NEON_YELLOW}[?] Extract these domains into separate files? (y/n) > {RESET}").strip().lower()
    
    if q.startswith('y'):
        print(f"\n  {ICON_MAIN} {NEON_BLUE}Partitioning Domains...{RESET}")
        domain_files = {d: open(f"{outfile_base}_{d.replace('.', '_')}.txt", "w", encoding="utf-8") for d in target_domains}
        
        for combo in sorted_combos:
            user_part = combo.split(':')[0]
            match = EMAIL_PATTERN.match(user_part)
            if match:
                dom = match.group(1).lower()
                if dom in domain_files:
                    domain_files[dom].write(combo + "\n")
        
        for f in domain_files.values():
            f.close()
            print(f"    {ICON_FILE} {WHITE}Saved: {f.name}{RESET}")
        
        print(f"\n  {ICON_CHECK} {NEON_GREEN}Domain extraction complete.{RESET}")
    else:
        print(f"\n  {ICON_CROSS} {GRAY}Skipped domain extraction.{RESET}")

def final_report(stats, start_time, created_files, domain_counter, pass_stats, avg_pass):
    elapsed = time.time() - start_time
    clear_screen()
    print_banner("MISSION COMPLETE", NEON_GREEN)
    print("\n")
    
    print(f"  {NEON_CYAN}{BOLD}PERFORMANCE METRICS{RESET}")
    print(f"  {GRAY}Total Time:{RESET} {WHITE}{format_time(elapsed)}{RESET}")
    print(f"  {GRAY}Valid Hits:{RESET} {NEON_GREEN}{stats['valid']:,}{RESET}")
    print(f"  {GRAY}Discarded :{RESET} {NEON_RED}{stats['duplicates'] + stats['bad']:,}{RESET}")
    print_line(".", GRAY)
    
    print(f"  {NEON_PINK}{BOLD}SECURITY ANALYTICS{RESET}")
    total = stats['valid'] if stats['valid'] > 0 else 1
    print(f"  {GRAY}Avg Pass Len :{RESET} {WHITE}{avg_pass}{RESET}")
    print(f"  {GRAY}Numeric Only :{RESET} {NEON_YELLOW}{pass_stats['numeric']:,}{RESET} {DIM}({int(pass_stats['numeric']/total*100)}%){RESET}")
    print(f"  {GRAY}Complex/Mixed:{RESET} {NEON_BLUE}{pass_stats['mixed']:,}{RESET} {DIM}({int(pass_stats['mixed']/total*100)}%){RESET}")
    print_line(".", GRAY)

    if domain_counter:
        print(f"  {NEON_CYAN}{BOLD}TOP DOMAINS{RESET}")
        for d, c in domain_counter.most_common(5):
             print(f"  {NEON_CYAN}➜{RESET} {WHITE}{d:<20}{RESET} {GRAY}{c:,}{RESET}")
        print_line(".", GRAY)

    print(f"  {NEON_GREEN}{BOLD}OUTPUT FILES{RESET}")
    for fname in created_files:
        print(f"  {ICON_FILE} {WHITE}{fname}{RESET}")

    print("\n\n")
    print_centered(f"{NEON_PINK}Mohammad SK {GRAY}///{RESET} {NEON_CYAN}NEON EDITION v2{RESET}")
    print("\n")

def main():
    logo()
    file_list, is_batch = select_input_source()
    
    if is_batch:
        folder_name = os.path.basename(os.path.normpath(os.path.dirname(file_list[0])))
        outfile_base = f"BatchResult_{folder_name}"
    else:
        base_name = os.path.basename(file_list[0]).rsplit('.', 1)[0]
        outfile_base = f"{base_name}_extracted"
    
    print_line("-", GRAY)
    domain_filter = input(f" {ICON_MAIN} {NEON_YELLOW}FILTER KEYWORD (Optional) > {RESET}").strip()
    
    stats, start, domain_counter, pass_stats, avg_pass, files, sorted_combos = process_files(file_list, is_batch, outfile_base, domain_filter)
    final_report(stats, start, files, domain_counter, pass_stats, avg_pass)
    
    # New interactive step
    ask_and_save_domains(outfile_base, sorted_combos, domain_counter)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n {ICON_CROSS} {NEON_RED}System Halted.{RESET}")
