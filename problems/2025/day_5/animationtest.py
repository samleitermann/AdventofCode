import argparse
import re
import time
import shutil
import os
import sys


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    WHITE = '\033[97m'


class Solution:
    filename_real_input = 'real_input.txt'
    filename_test_input = 'test_input.txt'

    # Animation Settings
    # DELAY: Seconds to wait between frames.
    # Decrease this (e.g., 0.01) if running on real_input.txt
    DELAY = 0.4

    @staticmethod
    def get_nums(string: str) -> list[int]:
        return list(map(int, re.findall(r'[-+]?\d+', string)))

    def __init__(self, test=False):
        self.filename = self.filename_test_input if test else self.filename_real_input
        try:
            with open(self.filename, 'r') as f:
                self.file = f.read()
            self.lines = self.file.splitlines()
        except FileNotFoundError:
            print(f"{Colors.RED}Error: File {self.filename} not found.{Colors.ENDC}")
            self.lines = []

    def parse_file(self):
        raw_ranges = []
        ingredients = []
        flag = False
        for line in self.lines:
            if line.strip() == '':
                flag = True
                continue
            if not flag:
                raw_ranges.append(line)
            if flag:
                ingredients.append(line)

        ranges = []
        for ran in raw_ranges:
            if '-' in ran:
                start, end = ran.split('-')
                ranges.append((int(start), int(end)))
        return ranges, ingredients

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def render_frame(self, raw_ranges, merged_so_far, ingredients, checked_results, current_action_msg, scale_info):
        """
        Draws one complete frame of the animation.
        """
        self.clear_screen()
        min_val, max_val, scale, canvas_size = scale_info

        # Helper: Map value to index
        def get_idx(val):
            return int((val - min_val) / scale)

        # Helper: Draw Bar
        def draw_bar(interval_list, char, color):
            line = [' '] * canvas_size
            for start, end in interval_list:
                s_idx = get_idx(start)
                e_idx = get_idx(end)
                if s_idx == e_idx:
                    line[s_idx] = char
                else:
                    for i in range(s_idx, e_idx + 1):
                        if i < len(line): line[i] = char
            return f"{color}{''.join(line)}{Colors.ENDC}"

        print(f"{Colors.HEADER}=== ALGORYTHMIC VISUALIZATION ==={Colors.ENDC}")
        print(f"Range: {min_val} to {max_val} | Scale: 1 char = {scale:.2f} units")
        print("-" * 60)

        # 1. Axis
        axis_line = ['-'] * canvas_size
        ticks = [min_val, min_val + (max_val - min_val) // 2, max_val]
        for t in ticks:
            i = get_idx(t)
            if i < len(axis_line): axis_line[i] = '|'
        print(f"Axis    {min_val:<6} {''.join(axis_line)} {max_val}")

        # 2. Raw Intervals
        print(f"Raw     {' ':<6} {draw_bar(raw_ranges, '=', Colors.YELLOW)}")

        # 3. Merged Intervals (Animated Growth)
        print(f"Merged  {' ':<6} {draw_bar(merged_so_far, '█', Colors.GREEN)}")

        # 4. Ingredients (Animated Checks)
        ing_line = [' '] * canvas_size
        for ing_val, status in checked_results.items():
            idx = get_idx(ing_val)
            if idx < len(ing_line):
                if status == 'FRESH':
                    ing_line[idx] = f"{Colors.GREEN}✓{Colors.ENDC}"
                elif status == 'SPOILED':
                    ing_line[idx] = f"{Colors.RED}✗{Colors.ENDC}"

        print(f"Check   {' ':<6} {''.join(ing_line)}")
        print("-" * 60)

        # 5. Live Log
        print(f"{Colors.BOLD}>> LOG:{Colors.ENDC} {current_action_msg}")

    def animate(self):
        raw_ranges, ingredients_str = self.parse_file()
        ingredients = [int(i) for i in ingredients_str]

        if not raw_ranges and not ingredients:
            print("No data.")
            return

        # --- SETUP SCALING ---
        all_points = [r[0] for r in raw_ranges] + [r[1] for r in raw_ranges] + ingredients
        min_val = min(all_points)
        max_val = max(all_points)
        data_span = max_val - min_val
        term_width = max(10, shutil.get_terminal_size().columns - 20)
        scale = max(1.0, data_span / term_width)
        canvas_size = int((max_val - min_val) / scale) + 2
        scale_info = (min_val, max_val, scale, canvas_size)

        # --- PHASE 1: ANIMATE MERGING ---
        raw_ranges.sort(key=lambda x: x[0])
        merged = []

        if raw_ranges:
            merged = [raw_ranges[0]]
            # Show initial state
            self.render_frame(raw_ranges, merged, ingredients, {},
                              f"Initialized merge with {merged[0]}", scale_info)
            time.sleep(self.DELAY)

            for current_start, current_end in raw_ranges[1:]:
                last_start, last_end = merged[-1]

                msg = f"Comparing [{current_start}-{current_end}] against merged tail [{last_start}-{last_end}]"
                self.render_frame(raw_ranges, merged, ingredients, {}, msg, scale_info)
                time.sleep(self.DELAY)

                if current_start <= last_end:
                    new_end = max(last_end, current_end)
                    merged[-1] = (last_start, new_end)
                    msg = f"{Colors.GREEN}OVERLAP!{Colors.ENDC} Extending tail to {new_end}"
                else:
                    merged.append((current_start, current_end))
                    msg = f"{Colors.YELLOW}NO OVERLAP.{Colors.ENDC} Starting new interval."

                self.render_frame(raw_ranges, merged, ingredients, {}, msg, scale_info)
                time.sleep(self.DELAY)

        # --- PHASE 2: ANIMATE CHECKING ---
        checked_results = {}  # {id: 'FRESH'/'SPOILED'}
        fresh_count = 0

        for ing in ingredients:
            is_fresh = False
            for m_start, m_end in merged:
                if m_start <= ing <= m_end:
                    is_fresh = True
                    break

            status = 'FRESH' if is_fresh else 'SPOILED'
            checked_results[ing] = status
            if is_fresh: fresh_count += 1

            color = Colors.GREEN if is_fresh else Colors.RED
            msg = f"Ingredient ID {Colors.WHITE}{ing}{Colors.ENDC}: {color}{status}{Colors.ENDC}"

            self.render_frame(raw_ranges, merged, ingredients, checked_results, msg, scale_info)
            time.sleep(self.DELAY)

        # --- FINAL SUMMARY ---
        msg = f"COMPLETE. Total Fresh: {fresh_count} / {len(ingredients)}"
        self.render_frame(raw_ranges, merged, ingredients, checked_results, msg, scale_info)
        return merged, fresh_count

    def part1(self):
        if self.filename == self.filename_test_input:
            # Run animation mode
            _, count = self.animate()
            return count
        else:
            # Standard fast mode for real input (unless you want to wait!)
            return self.standard_part1()

    def standard_part1(self):
        # Your original optimized logic for non-visual runs
        start = time.perf_counter()
        raw_ranges, ingredients_str = self.parse_file()
        ingredients = [int(i) for i in ingredients_str]

        # Logic to merge (copied for separation)
        raw_ranges.sort(key=lambda x: x[0])
        merged = [raw_ranges[0]]
        for cs, ce in raw_ranges[1:]:
            ls, le = merged[-1]
            if cs <= le:
                merged[-1] = (ls, max(le, ce))
            else:
                merged.append((cs, ce))

        fresh = 0
        for ing in ingredients:
            for ms, me in merged:
                if ms <= ing <= me:
                    fresh += 1
                    break
        end = time.perf_counter()
        print(f"Time: {end - start:0.6f}s")
        return fresh

    def part2(self):
        # For part 2, we can just run the same animation as it relies on the merge
        if self.filename == self.filename_test_input:
            merged_intervals, _ = self.animate()
        else:
            # Standard logic
            raw_ranges, _ = self.parse_file()
            raw_ranges.sort(key=lambda x: x[0])
            merged_intervals = [raw_ranges[0]]
            for cs, ce in raw_ranges[1:]:
                ls, le = merged_intervals[-1]
                if cs <= le:
                    merged_intervals[-1] = (ls, max(le, ce))
                else:
                    merged_intervals.append((cs, ce))

        freshness = 0
        for ranges_start, ranges_end in merged_intervals:
            freshness += ranges_end - ranges_start + 1
        return freshness


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solution file')
    parser.add_argument('-part', required=True, type=int, help='Part (1/2)')
    parser.add_argument('-test', required=True, type=str, help='Test mode (True/False)')
    args = parser.parse_args()

    test_mode = True if args.test.lower() == 'true' else False

    solution = Solution(test=test_mode)

    # If running real input, warn user about animation
    if not test_mode:
        print("Running in fast mode (No Animation for Real Input).")
        result = solution.part1() if args.part == 1 else solution.part2()
    else:
        result = solution.part1() if args.part == 1 else solution.part2()

    print(f"\nFinal Result: {result}")