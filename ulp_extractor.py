import os
import time
import re

# Color Styles
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"
WHITE = "\033[97m"

def has_persian_or_arabic(text):
    return bool(re.search(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]', text))

def is_badcombo(user, pw):
    if any(x in user for x in [' ', '\t', '\r', '\n']) or any(x in pw for x in [' ', '\t', '\r', '\n']):
        return True
    if has_persian_or_arabic(user) or has_persian_or_arabic(pw):
        return True
    if len(user) < 2 or len(pw) < 2:
        return True
    non_combo_phrases = [
        'old or unknown version', 'notemmysbirthday', 'unknown version', '██████', '██'
    ]
    if any(phrase in user.lower() or phrase in pw.lower() for phrase in non_combo_phrases):
        return True
    if pw.strip() == "":
        return True
    return False

def logo():
    print(f"""{CYAN}{BOLD}
╔══════════════════════════════════════════════════════════════════╗
║      {WHITE}ULP Combo Extractor{CYAN} — {MAGENTA}by Mohammad SK{CYAN}                        ║
╚══════════════════════════════════════════════════════════════════╝
{RESET}""")

def select_input_file():
    print(BLUE + "[1] Choose from txt files in this folder")
    print("[2] Enter a custom path or filename" + RESET)
    while True:
        sel = input(GREEN + "Select option [1/2]: " + RESET).strip()
        if sel == '1':
            txts = [f for f in os.listdir() if f.endswith('.txt')]
            if not txts:
                print(RED + "No .txt files found in this folder!" + RESET)
                continue
            for i, name in enumerate(txts, 1):
                print(f"{CYAN}{i}. {name}{RESET}")
            while True:
                try:
                    choice = int(input(GREEN + "Select input file [number]: " + RESET))
                    if 1 <= choice <= len(txts):
                        return txts[choice-1]
                except:
                    pass
                print(RED + "Invalid! Try again." + RESET)
        elif sel == '2':
            file = input(YELLOW + "Enter path or filename: " + RESET).strip('"\' ')
            if os.path.exists(file):
                return file
            else:
                print(RED + "File not found! Try again." + RESET)
        else:
            print(RED + "Only 1 or 2 are valid choices." + RESET)

def parse_ulp(line):
    parts = line.strip().split(':')
    if len(parts) < 2:
        return None, 'BAD'
    user = parts[-2]
    pw = ':'.join(parts[-1:])
    if is_badcombo(user, pw):
        return None, 'BAD'
    return f"{user}:{pw}", 'OK'

def sizeof_fmt(num, suffix="B"):
    for unit in ['','K','M','G','T','P']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Y', suffix)

def match_domain_filter(line, domain_filter):
    if not domain_filter:
        return True
    if domain_filter.lower() in line.lower():
        return True
    return False

def print_dashboard(stat):
    border = CYAN + "│" + RESET
    print(f"{CYAN}┌{'─'*52}┐{RESET}")
    print(f"{CYAN}│{WHITE} {'Extraction Summary':^50} {CYAN}│{RESET}")
    print(f"{CYAN}├{'─'*52}┤{RESET}")
    print(f"{border} {YELLOW}Input File    {RESET}: {stat['infile']}")
    print(f"{border} {YELLOW}Input Size    {RESET}: {stat['infile_size']}")
    print(f"{border} {YELLOW}Total Lines   {RESET}: {stat['total_lines']:,}")
    print(f"{border} {GREEN}Output File   {RESET}: {stat['outfile']}")
    print(f"{border} {GREEN}Output Size   {RESET}: {stat['outfile_size']}")
    print(f"{border} {BLUE}Unique Combos {RESET}: {stat['unique_combos']:,}")
    print(f"{border} {MAGENTA}Duplicates    {RESET}: {stat['duplicates']:,}")
    print(f"{border} {RED}Bad Chars     {RESET}: {stat['bad_charcount']:,}")
    print(f"{border} {CYAN}Time          {RESET}: {stat['elapsed']:.2f} s")
    print(f"{border} {CYAN}Speed         {RESET}: {stat['speed']:,} l/s")
    print(f"{CYAN}└{'─'*52}┘{RESET}")
    print(f"{GREEN}✔ Only valid combos are in your output file. -- Mohammad SK{RESET}")
    print(f"{YELLOW}📂 Output: {stat['outfile']}{RESET}\n")

def main():
    logo()
    infile = select_input_file()
    outfile = "converted_combo.txt"

    print(f"{CYAN}Selected: {infile}{RESET}")

    print(GREEN + "Example: .ir, ir./, netflix, .com, ... If you press Enter, all will be extracted." + RESET)
    domain_filter = input(YELLOW + "Domain/keyword filter (e.g. ir./ or .ir) [Enter=all]: " + RESET).strip()
    if domain_filter:
        print(GREEN + f"✔ Only lines containing: {domain_filter} will be processed." + RESET)
    else:
        print(GREEN + "✔ All valid combos will be extracted." + RESET)

    total_lines = sum(1 for _ in open(infile, encoding="utf-8"))
    infile_size = sizeof_fmt(os.path.getsize(infile))

    t0 = time.time()
    processed = 0
    valid_lines = 0
    unique_combos = set()
    duplicates = 0
    bad_charcount = 0

    speed_time = time.time()
    speed_count = 0

    with open(infile, "r", encoding="utf-8") as fin:
        for line in fin:
            raw = line.strip()
            if not raw or ':' not in raw:
                if raw:
                    bad_charcount += len(raw)
                continue

            if not match_domain_filter(raw, domain_filter):
                continue

            result, status = parse_ulp(raw)
            if status == 'OK':
                valid_lines += 1
                if result not in unique_combos:
                    unique_combos.add(result)
                else:
                    duplicates += 1
            else:
                bad_charcount += len(raw)
            processed += 1
            speed_count += 1
            if processed % 400 == 0 or processed == total_lines:
                elapsed = time.time() - speed_time
                liveline = int(speed_count / elapsed) if elapsed > 0 else speed_count
                print(f"{CYAN}  Processed: {processed}/{total_lines} | LiveLine: {liveline}/sec   {RESET}", end='\r')
                speed_time = time.time()
                speed_count = 0

    with open(outfile, "w", encoding="utf-8") as fout:
        for combo in unique_combos:
            fout.write(combo + "\n")

    t1 = time.time()
    outfile_size = sizeof_fmt(os.path.getsize(outfile))
    avg_speed = int(valid_lines / (t1-t0)) if (t1-t0) > 0 else valid_lines

    stat = {
        'infile': infile,
        'infile_size': infile_size,
        'total_lines': total_lines,
        'outfile': outfile,
        'outfile_size': outfile_size,
        'unique_combos': len(unique_combos),
        'duplicates': duplicates,
        'bad_charcount': bad_charcount,
        'elapsed': t1-t0,
        'speed': avg_speed
    }
    print_dashboard(stat)

if __name__ == "__main__":
    main()
