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

    # Default slow speed for human readability
    DELAY = 0.5

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
        # Using a specialized code to clear screen reduces flickering compared to os.system
        print("\033[H\033[J", end="")

    def render_frame(self, raw_ranges, merged_so_far, ingredients, checked_results, current_action_msg, scale_info):
        """
        Draws one complete frame of the animation.
        """
        self.clear_screen()
        min_val, max_val, scale, canvas_size = scale_info

        # Helper: Map real value to screen index
        def get_idx(val):
            return int((val - min_val) / scale)

        # Helper: Draw Bar (Optimized for Screen Width)
        def draw_bar(interval_list, char, color):
            line = [' '] * (canvas_size + 1)

            for start, end in interval_list:
                s_idx = get_idx(start)
                e_idx = get_idx(end)

                # Clamp to screen bounds to prevent crashes
                s_idx = max(0, min(s_idx, canvas_size))
                e_idx = max(0, min(e_idx, canvas_size))

                if s_idx == e_idx:
                    line[s_idx] = char
                else:
                    # Fill the range
                    for i in range(s_idx, e_idx + 1):
                        line[i] = char
            return f"{color}{''.join(line)}{Colors.ENDC}"

        print(f"{Colors.HEADER}=== REAL-TIME VISUALIZATION ==={Colors.ENDC}")
        print(f"File: {self.filename}")
        print(f"Range: {min_val} to {max_val} | Scale: 1 char = {scale:.2f} units")
        print("-" * 60)

        # 1. Axis
        axis_line = ['-'] * (canvas_size + 1)
        ticks = [min_val, min_val + (max_val - min_val) // 2, max_val]
        for t in ticks:
            i = get_idx(t)
            if 0 <= i <= canvas_size: axis_line[i] = '|'
        print(f"Axis    {min_val:<6} {''.join(axis_line)} {max_val}")

        # 2. Raw Intervals
        print(f"Raw     {' ':<6} {draw_bar(raw_ranges, '=', Colors.YELLOW)}")

        # 3. Merged Intervals (Animated Growth)
        print(f"Merged  {' ':<6} {draw_bar(merged_so_far, '█', Colors.GREEN)}")

        # 4. Ingredients (Animated Checks)
        ing_line = [' '] * (canvas_size + 1)

        # We process ingredients to show them on the timeline
        for ing_val, status in checked_results.items():
            idx = get_idx(ing_val)
            if 0 <= idx <= canvas_size:
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

        # --- AUTO-SPEED ADJUSTMENT ---
        total_ops = len(raw_ranges) + len(ingredients)
        if total_ops > 2000:
            self.DELAY = 0.0001  # "Matrix" mode for massive files
        elif total_ops > 200:
            self.DELAY = 0.005  # Fast mode
        elif total_ops > 50:
            self.DELAY = 0.05  # Brisk walk
        else:
            self.DELAY = 0.4  # Tutorial mode

        # --- SETUP SCALING ---
        all_points = [r[0] for r in raw_ranges] + [r[1] for r in raw_ranges] + ingredients
        min_val = min(all_points)
        max_val = max(all_points)
        data_span = max_val - min_val
        term_width = max(10, shutil.get_terminal_size().columns - 25)

        # Scale calculation: How many data units per 1 screen character
        scale = max(1.0, data_span / term_width)
        canvas_size = int((max_val - min_val) / scale)
        scale_info = (min_val, max_val, scale, canvas_size)

        # --- PHASE 1: ANIMATE MERGING ---
        raw_ranges.sort(key=lambda x: x[0])
        merged = []

        if raw_ranges:
            merged = [raw_ranges[0]]

            # Initial Frame
            self.render_frame(raw_ranges, merged, ingredients, {},
                              f"Initialized merge with {merged[0]}", scale_info)
            time.sleep(self.DELAY)

            for current_start, current_end in raw_ranges[1:]:
                last_start, last_end = merged[-1]

                # Check Overlap
                if current_start <= last_end:
                    new_end = max(last_end, current_end)
                    merged[-1] = (last_start, new_end)
                    msg = f"Merged [{current_start}-{current_end}] into current interval."
                else:
                    merged.append((current_start, current_end))
                    msg = f"New interval created at [{current_start}-{current_end}]."

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

            # Update frame
            msg = f"Checking ID {ing}... {status}"
            self.render_frame(raw_ranges, merged, ingredients, checked_results, msg, scale_info)
            time.sleep(self.DELAY)

        # --- FINAL SUMMARY ---
        msg = f"{Colors.GREEN}COMPLETE.{Colors.ENDC} Total Fresh: {fresh_count} / {len(ingredients)}"
        self.render_frame(raw_ranges, merged, ingredients, checked_results, msg, scale_info)
        return merged, fresh_count

    def part1(self):
        # We now run the animation for BOTH test and real input
        merged_intervals, count = self.animate()
        return count

    def part2(self):
        # We now run the animation for BOTH test and real input
        merged_intervals, _ = self.animate()

        freshness = 0
        for ranges_start, ranges_end in merged_intervals:
            freshness += ranges_end - ranges_start + 1
        return freshness


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solution file')
    parser.add_argument('-part', required=True, type=int, help='Part (1/2)')
    parser.add_argument('-test', required=True, type=str, help='Test mode (True/False)')
    args = parser.parse_args()

    # Convert string to boolean safely
    test_mode = True if args.test.lower() == 'true' else False

    solution = Solution(test=test_mode)
    result = solution.part1() if args.part == 1 else solution.part2()

    print(f"\nFinal Result: {result}")