import argparse
import re
import time
import shutil
import os
import sys

# --- GIF DEPENDENCY CHECK ---
# We check this globally. If the user wants a GIF, we enforce these imports.
try:
    from PIL import Image, ImageDraw, ImageFont
    import imageio

    GIF_SUPPORT = True
except ImportError:
    GIF_SUPPORT = False


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

    # Mapping for the GIF generator (ANSI -> RGB Tuple)
    # Adjusted for high contrast on dark background
    RGB_MAP = {
        HEADER: (255, 0, 255),
        BLUE: (100, 180, 255),
        GREEN: (50, 255, 50),
        RED: (255, 80, 80),
        YELLOW: (255, 255, 0),
        CYAN: (0, 255, 255),
        WHITE: (255, 255, 255),
        ENDC: (220, 220, 220),  # Off-white for standard text
        BOLD: (255, 255, 255)
    }


class GifBuilder:
    def __init__(self, font_size=20):  # Increased font size for visibility
        self.frames = []
        self.font_size = font_size

        # specific list of common monospace fonts
        possible_fonts = [
            "consola.ttf", "Consolas.ttf",  # Windows
            "Menlo.ttc", "Monaco.ttf",  # Mac
            "DejaVuSansMono.ttf", "LiberationMono-Regular.ttf",  # Linux
            "arial.ttf"  # Fallback to non-mono if absolutely needed
        ]

        self.font = None
        for f in possible_fonts:
            try:
                self.font = ImageFont.truetype(f, font_size)
                # print(f"Loaded font: {f}") # Debug
                break
            except IOError:
                continue

        # Absolute fallback
        if self.font is None:
            print("Warning: No system font found. Using Pillow default (might be small).")
            self.font = ImageFont.load_default()

    def create_frame(self, text_lines):
        # 1. Calculate Image Size based on text content
        # We perform a dummy pass to measure width/height
        dummy_img = Image.new('RGB', (10, 10))
        dummy_draw = ImageDraw.Draw(dummy_img)

        max_width = 0
        total_height = 20  # padding
        line_height = int(self.font_size * 1.2)  # slightly more than font size

        clean_lines = []
        for line in text_lines:
            # Strip ANSI for measurement
            clean_text = re.sub(r'\x1b\[[0-9;]*m', '', line)
            clean_lines.append(clean_text)

            # Measure width
            bbox = dummy_draw.textbbox((0, 0), clean_text, font=self.font)
            width = bbox[2] - bbox[0]
            if width > max_width: max_width = width
            total_height += line_height

        img_width = max(800, int(max_width + 40))  # Min width 800 + padding
        img_height = max(400, total_height + 20)

        # 2. Draw actual frame
        img = Image.new('RGB', (img_width, img_height), color=(30, 30, 30))
        draw = ImageDraw.Draw(img)

        y = 20
        for line in text_lines:
            x = 20
            parts = re.split(r'(\x1b\[[0-9;]*m)', line)

            current_color = (220, 220, 220)  # Default

            for part in parts:
                if part.startswith('\033'):
                    if part in Colors.RGB_MAP:
                        current_color = Colors.RGB_MAP[part]
                    elif part == Colors.ENDC:
                        current_color = (220, 220, 220)
                else:
                    if part:
                        draw.text((x, y), part, font=self.font, fill=current_color)
                        bbox = draw.textbbox((x, y), part, font=self.font)
                        chunk_width = bbox[2] - bbox[0]
                        x += chunk_width
            y += line_height

        return img

    def add_frame(self, text_lines):
        self.frames.append(self.create_frame(text_lines))

    def save_gif(self, filename="visualization.gif", duration=0.1):
        if not self.frames:
            print("Error: No frames were captured for the GIF.")
            return

        print(f"\nProcessing {len(self.frames)} frames into GIF...")
        try:
            full_path = os.path.abspath(filename)
            imageio.mimsave(full_path, self.frames, duration=duration, loop=0)
            print(f"{Colors.GREEN}SUCCESS! GIF saved to:{Colors.ENDC}")
            print(f"{Colors.BLUE}{full_path}{Colors.ENDC}")
        except Exception as e:
            print(f"Failed to save GIF: {e}")


class Solution:
    filename_real_input = 'real_input.txt'
    filename_test_input = 'test_input.txt'
    DELAY = 0.5

    @staticmethod
    def get_nums(string: str) -> list[int]:
        return list(map(int, re.findall(r'[-+]?\d+', string)))

    def __init__(self, test=False, make_gif=False):
        self.filename = self.filename_test_input if test else self.filename_real_input
        self.make_gif = make_gif

        # STRICT DEPENDENCY CHECK
        if self.make_gif:
            if not GIF_SUPPORT:
                print(f"\n{Colors.RED}CRITICAL ERROR: GIF Requested but libraries missing.{Colors.ENDC}")
                print("Please run: pip install pillow imageio")
                sys.exit(1)
            print("Initializing GIF Builder...")
            self.gif_builder = GifBuilder()
        else:
            self.gif_builder = None

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
        print("\033[H\033[J", end="")

    def render_frame(self, raw_ranges, merged_so_far, ingredients, checked_results, current_action_msg, scale_info):
        self.clear_screen()
        min_val, max_val, scale, canvas_size = scale_info

        output_buffer = []

        def get_idx(val):
            return int((val - min_val) / scale)

        def draw_bar(interval_list, char, color):
            line = [' '] * (canvas_size + 1)
            for start, end in interval_list:
                s_idx = get_idx(start)
                e_idx = get_idx(end)
                s_idx = max(0, min(s_idx, canvas_size))
                e_idx = max(0, min(e_idx, canvas_size))
                if s_idx == e_idx:
                    line[s_idx] = char
                else:
                    for i in range(s_idx, e_idx + 1):
                        line[i] = char
            return f"{color}{''.join(line)}{Colors.ENDC}"

        # --- Build Output ---
        output_buffer.append(f"{Colors.HEADER}=== VISUALIZATION ==={Colors.ENDC}")
        output_buffer.append(f"Range: {min_val} to {max_val} | Scale: 1 char = {scale:.2f} units")
        output_buffer.append("-" * 60)

        # Axis
        axis_line = ['-'] * (canvas_size + 1)
        ticks = [min_val, min_val + (max_val - min_val) // 2, max_val]
        for t in ticks:
            i = get_idx(t)
            if 0 <= i <= canvas_size: axis_line[i] = '|'
        output_buffer.append(f"Axis    {min_val:<6} {''.join(axis_line)} {max_val}")

        # Data Lines
        output_buffer.append(f"Raw     {' ':<6} {draw_bar(raw_ranges, '=', Colors.YELLOW)}")
        output_buffer.append(f"Merged  {' ':<6} {draw_bar(merged_so_far, '█', Colors.GREEN)}")

        # Check Line
        ing_line = [' '] * (canvas_size + 1)
        for ing_val, status in checked_results.items():
            idx = get_idx(ing_val)
            if 0 <= idx <= canvas_size:
                if status == 'FRESH':
                    ing_line[idx] = f"{Colors.GREEN}✓{Colors.ENDC}"
                elif status == 'SPOILED':
                    ing_line[idx] = f"{Colors.RED}✗{Colors.ENDC}"
        output_buffer.append(f"Check   {' ':<6} {''.join(ing_line)}")
        output_buffer.append("-" * 60)

        # Log
        # We strip colors for the log message in the gif just to keep it clean,
        # or we can keep them if we want multi-colored logs
        output_buffer.append(f"{Colors.BOLD}LOG:{Colors.ENDC} {current_action_msg}")

        # 1. Print to Terminal
        for line in output_buffer:
            print(line)

        # 2. Add to GIF
        if self.make_gif and self.gif_builder:
            self.gif_builder.add_frame(output_buffer)

    def animate(self):
        raw_ranges, ingredients_str = self.parse_file()
        ingredients = [int(i) for i in ingredients_str]

        if not raw_ranges and not ingredients:
            return

        # Auto-speed
        total_ops = len(raw_ranges) + len(ingredients)
        if total_ops > 2000:
            self.DELAY = 0.0001
        elif total_ops > 200:
            self.DELAY = 0.005
        elif total_ops > 50:
            self.DELAY = 0.05
        else:
            self.DELAY = 0.4

        # Scaling
        all_points = [r[0] for r in raw_ranges] + [r[1] for r in raw_ranges] + ingredients
        min_val = min(all_points)
        max_val = max(all_points)
        data_span = max_val - min_val
        term_width = max(10, shutil.get_terminal_size().columns - 25)
        scale = max(1.0, data_span / term_width)
        canvas_size = int((max_val - min_val) / scale)
        scale_info = (min_val, max_val, scale, canvas_size)

        # Merge Phase
        raw_ranges.sort(key=lambda x: x[0])
        merged = [raw_ranges[0]]
        self.render_frame(raw_ranges, merged, ingredients, {}, "Start", scale_info)
        time.sleep(self.DELAY)

        if len(raw_ranges) > 1:
            for current_start, current_end in raw_ranges[1:]:
                last_start, last_end = merged[-1]
                if current_start <= last_end:
                    merged[-1] = (last_start, max(last_end, current_end))
                    msg = "Merging Interval..."
                else:
                    merged.append((current_start, current_end))
                    msg = "New Interval..."

                self.render_frame(raw_ranges, merged, ingredients, {}, msg, scale_info)
                time.sleep(self.DELAY)

        # Check Phase
        checked_results = {}
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

            self.render_frame(raw_ranges, merged, ingredients, checked_results, f"Checking {ing} -> {status}",
                              scale_info)
            time.sleep(self.DELAY)

        # Done
        msg = f"COMPLETE. Fresh: {fresh_count}"
        self.render_frame(raw_ranges, merged, ingredients, checked_results, msg, scale_info)

        # SAVE GIF
        if self.make_gif and self.gif_builder:
            # Enforce minimum delay for GIF visibility (0.1s)
            gif_delay = max(0.1, self.DELAY)
            self.gif_builder.save_gif(duration=gif_delay)

        return fresh_count

    def part1(self):
        return self.animate()

    def part2(self):
        self.animate()
        return "Done (See GIF)"


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solution file')
    parser.add_argument('-part', required=True, type=int, help='Part (1/2)')
    parser.add_argument('-test', required=True, type=str, help='Test mode (True/False)')
    parser.add_argument('-gif', required=False, type=str, default='False', help='Create GIF (True/False)')

    args = parser.parse_args()
    test_mode = True if args.test.lower() == 'true' else False
    gif_mode = True if args.gif.lower() == 'true' else False

    solution = Solution(test=test_mode, make_gif=gif_mode)
    result = solution.part1() if args.part == 1 else solution.part2()

    if not gif_mode:
        print(f"\nFinal Result: {result}")