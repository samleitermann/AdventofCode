import argparse
import re
import time
import shutil
import os
import sys

# --- DEPENDENCY CHECK ---
try:
    from PIL import Image, ImageDraw, ImageFont
    import imageio
    import numpy as np

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

    RGB_MAP = {
        HEADER: (255, 0, 255),
        BLUE: (80, 200, 255),
        GREEN: (0, 255, 100),
        RED: (255, 50, 80),
        YELLOW: (255, 255, 0),
        CYAN: (0, 255, 255),
        WHITE: (255, 255, 255),
        ENDC: (240, 240, 240),
        BOLD: (255, 255, 255)
    }


class GifBuilder:
    def __init__(self, font_size=20):
        self.frames = []
        self.font_size = font_size
        self.width = 1200
        self.height = 800

        possible_fonts = ["consola.ttf", "Consolas.ttf", "Menlo.ttc", "Monaco.ttf", "arial.ttf"]
        self.font = None
        for f in possible_fonts:
            try:
                self.font = ImageFont.truetype(f, font_size)
                break
            except IOError:
                continue
        if self.font is None: self.font = ImageFont.load_default()

    def add_title_frame(self, title_text, sub_text, duration_seconds, fps_delay):
        """
        Adds multiple copies of the title frame.
        Includes 'Pixel Jitter' to prevent GIF optimizers from collapsing frames.
        """
        base_img = Image.new('RGB', (self.width, self.height), color=(20, 20, 20))
        draw = ImageDraw.Draw(base_img)

        # Title
        w_title = draw.textlength(title_text, font=self.font)
        x_title = (self.width - w_title) // 2
        y_title = (self.height // 2) - 40
        draw.text((x_title, y_title), title_text, font=self.font, fill=(255, 50, 50))

        # Subtitle
        w_sub = draw.textlength(sub_text, font=self.font)
        x_sub = (self.width - w_sub) // 2
        y_sub = y_title + 40
        draw.text((x_sub, y_sub), sub_text, font=self.font, fill=(0, 255, 255))

        # Border
        draw.rectangle([10, 10, self.width - 10, self.height - 10], outline=(255, 255, 0), width=3)

        # Calculate needed frames
        frame_count = int(duration_seconds / fps_delay)
        print(
            f"[{Colors.CYAN}DEBUG{Colors.ENDC}] Generating {frame_count} title frames (Target: {duration_seconds}s @ {fps_delay}s/frame)")

        # --- PIXEL JITTER FIX ---
        for i in range(frame_count):
            frame_copy = base_img.copy()
            # Toggle the very first pixel between two nearly identical colors
            # This forces the encoder to treat every frame as unique.
            jitter_color = (20, 20, 20) if i % 2 == 0 else (21, 21, 21)
            frame_copy.putpixel((0, 0), jitter_color)
            self.frames.append(frame_copy)

    def create_frame(self, text_lines):
        img = Image.new('RGB', (self.width, self.height), color=(20, 20, 20))
        draw = ImageDraw.Draw(img)

        line_height = int(self.font_size * 1.2)
        y = 20
        for line in text_lines:
            x = 30
            if y > self.height - 20: break

            parts = re.split(r'(\x1b\[[0-9;]*m)', line)
            curr_color = (240, 240, 240)

            for part in parts:
                if part.startswith('\033'):
                    if part in Colors.RGB_MAP:
                        curr_color = Colors.RGB_MAP[part]
                    elif part == Colors.ENDC:
                        curr_color = (240, 240, 240)
                elif part:
                    draw.text((x, y), part, font=self.font, fill=curr_color)
                    x += draw.textlength(part, font=self.font)
            y += line_height
        return img

    def add_frame(self, text_lines):
        self.frames.append(self.create_frame(text_lines))

    def save_gif(self, filename="visualization.gif", duration=0.1):
        if not self.frames: return
        abs_path = os.path.abspath(filename)
        print(f"Saving {len(self.frames)} frames to {abs_path}...")
        try:
            # We use the subrectangles=True option which sometimes helps with alignment,
            # but sticking to standard params with distinct frames is best.
            imageio.mimsave(filename, self.frames, duration=duration, loop=0)
            print(f"{Colors.GREEN}GIF Saved Successfully.{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}GIF Save Failed: {e}{Colors.ENDC}")


class Solution:
    filename_real_input = 'real_input.txt'
    filename_test_input = 'test_input.txt'

    @staticmethod
    def get_nums(string: str) -> list[int]:
        return list(map(int, re.findall(r'[-+]?\d+', string)))

    def __init__(self, test=False, make_gif=False):
        self.filename = self.filename_test_input if test else self.filename_real_input
        self.make_gif = make_gif

        if self.make_gif:
            if not GIF_SUPPORT:
                print(f"{Colors.RED}Error: Install 'pillow' and 'imageio' for GIFs{Colors.ENDC}")
                sys.exit(1)
            self.gif_builder = GifBuilder()
        else:
            self.gif_builder = None

        try:
            with open(self.filename, 'r') as f:
                self.file = f.read()
            self.lines = self.file.splitlines()
        except FileNotFoundError:
            self.lines = []

    def parse_file(self):
        raw, ing = [], []
        flag = False
        for line in self.lines:
            if line.strip() == '': flag = True; continue
            if not flag:
                raw.append(line)
            else:
                ing.append(line)
        ranges = []
        for r in raw:
            if '-' in r:
                s, e = r.split('-')
                ranges.append((int(s), int(e)))
        return ranges, ing

    def fmt_num(self, n):
        return f"{n:.3e}"

    def clear_screen(self):
        print("\033[H\033[J", end="")

    def start_screen_wait(self, duration=5):
        self.clear_screen()
        try:
            cols, rows = shutil.get_terminal_size()
        except:
            cols, rows = 80, 24

        print("\n" * (rows // 2 - 4))
        print(f"{Colors.RED}##################################################{Colors.ENDC}".center(cols + 9))
        print(
            f"{Colors.RED}#{Colors.ENDC}       {Colors.YELLOW}ELF INVENTORY SYSTEM - ADVENT OF CODE{Colors.ENDC}      {Colors.RED}#{Colors.ENDC}".center(
                cols + 35))
        print(
            f"{Colors.RED}#{Colors.ENDC}         {Colors.CYAN}TOP SECRET // CLEARANCE LEVEL 5{Colors.ENDC}        {Colors.RED}#{Colors.ENDC}".center(
                cols + 35))
        print(f"{Colors.RED}##################################################{Colors.ENDC}".center(cols + 9))
        print(f"\n(Initializing... Wait {duration}s)".center(cols))
        time.sleep(duration)

    def render_frame(self, raw_ranges, merged, ingredients, checked, log_msg, scale_info):
        self.clear_screen()
        min_val, max_val, scale, canvas_size = scale_info

        buf = []
        buf.append(f"{Colors.HEADER}=== ELF INVENTORY SYSTEM ==={Colors.ENDC}")
        buf.append(f"Range: {self.fmt_num(min_val)} to {self.fmt_num(max_val)}")
        buf.append(f"Scale: 1 char = {scale:.2f} units")
        buf.append(f"{Colors.BLUE}" + "-" * 70 + f"{Colors.ENDC}")

        def get_idx(val):
            return int((val - min_val) / scale)

        def draw_bar(intervals, char, color):
            line = [' '] * (canvas_size + 1)
            for s, e in intervals:
                si, ei = max(0, min(get_idx(s), canvas_size)), max(0, min(get_idx(e), canvas_size))
                if si == ei:
                    line[si] = char
                else:
                    for i in range(si, ei + 1): line[i] = char
            return f"{color}{''.join(line)}{Colors.ENDC}"

        axis_chars = ['-'] * (canvas_size + 1)
        t1, t2, t3 = min_val, min_val + (max_val - min_val) // 2, max_val
        i1, i2, i3 = get_idx(t1), get_idx(t2), get_idx(t3)
        for i in [i1, i2, i3]:
            if 0 <= i <= canvas_size: axis_chars[i] = '|'

        buf.append(f"Axis    {''.join(axis_chars)}")
        buf.append(f"        {t1:.1e} ... {t2:.1e} ... {t3:.1e}")
        buf.append(f"Raw     {draw_bar(raw_ranges, '=', Colors.YELLOW)}")
        buf.append(f"Merged  {draw_bar(merged, '█', Colors.GREEN)}")

        ing_line = [' '] * (canvas_size + 1)
        for val, stat in checked.items():
            idx = get_idx(val)
            if 0 <= idx <= canvas_size:
                ing_line[idx] = f"{Colors.GREEN}✓{Colors.ENDC}" if stat == 'FRESH' else f"{Colors.RED}✗{Colors.ENDC}"

        buf.append(f"Check   {''.join(ing_line)}")
        buf.append(f"{Colors.BLUE}" + "-" * 70 + f"{Colors.ENDC}")
        buf.append(f"{Colors.BOLD}LOG:{Colors.ENDC} {log_msg}")

        for l in buf: print(l)
        if self.make_gif and self.gif_builder:
            self.gif_builder.add_frame(buf)

    def animate(self):
        raw, ing_str = self.parse_file()
        ing = [int(i) for i in ing_str]
        if not raw and not ing: return

        # --- DETERMINE GIF SPEED ---
        # If 'ops' is low, 'delay' is 0.4. If high, 'delay' is 0.05.
        # We clamp GIF speed to 0.1s minimum so it doesn't break players
        ops = len(raw) + len(ing)
        delay = 0.0001 if ops > 2000 else (0.05 if ops > 50 else 0.4)
        gif_delay = max(0.1, delay)

        # --- 1. START SCREEN (5 Seconds) ---
        self.start_screen_wait(5)

        if self.make_gif and self.gif_builder:
            self.gif_builder.add_title_frame(
                "Elf Inventory System - Advent of Code",
                "TOP SECRET // CLEARANCE LEVEL 5",
                duration_seconds=5.0,
                fps_delay=gif_delay
            )

        # --- PREPARE DATA ---
        all_p = [r[0] for r in raw] + [r[1] for r in raw] + ing
        min_v, max_v = min(all_p), max(all_p)
        width = max(10, shutil.get_terminal_size().columns - 20)
        scale = max(1.0, (max_v - min_v) / width)
        c_size = int((max_v - min_v) / scale)
        s_info = (min_v, max_v, scale, c_size)

        # --- ANIMATION LOOP ---
        raw.sort(key=lambda x: x[0])
        merged = [raw[0]]
        self.render_frame(raw, merged, ing, {}, "Initializing...", s_info)

        if len(raw) > 1:
            for cs, ce in raw[1:]:
                ls, le = merged[-1]
                if cs <= le:
                    merged[-1] = (ls, max(le, ce))
                    msg = f"Merging {self.fmt_num(cs)}..."
                else:
                    merged.append((cs, ce))
                    msg = f"New Range {self.fmt_num(cs)}..."
                self.render_frame(raw, merged, ing, {}, msg, s_info)
                time.sleep(delay)

        checked = {}
        count = 0
        for i in ing:
            is_f = any(ms <= i <= me for ms, me in merged)
            stat = 'FRESH' if is_f else 'SPOILED'
            checked[i] = stat
            if is_f: count += 1
            self.render_frame(raw, merged, ing, checked, f"ID {self.fmt_num(i)}: {stat}", s_info)
            time.sleep(delay)

        self.render_frame(raw, merged, ing, checked, f"{Colors.GREEN}DONE. Fresh: {count}{Colors.ENDC}", s_info)

        # --- 2. END SCREEN (5 Seconds) ---
        time.sleep(5)  # Terminal Wait

        if self.make_gif and self.gif_builder and self.gif_builder.frames:
            # Repeat the FINAL frame 50 times (with jitter)
            last_frame = self.gif_builder.frames[-1]
            frames_needed = int(5.0 / gif_delay)

            print(f"[{Colors.CYAN}DEBUG{Colors.ENDC}] Generating {frames_needed} end frames...")

            for i in range(frames_needed):
                f_copy = last_frame.copy()
                # Pixel Jitter here too
                jitter_color = (20, 20, 20) if i % 2 == 0 else (21, 21, 21)
                f_copy.putpixel((0, 0), jitter_color)
                self.gif_builder.frames.append(f_copy)

            self.gif_builder.save_gif(duration=gif_delay)

        return count

    def part1(self):
        return self.animate()

    def part2(self):
        self.animate(); return "Done"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-part', type=int, required=True)
    parser.add_argument('-test', type=str, required=True)
    parser.add_argument('-gif', type=str, default='False')
    args = parser.parse_args()

    t_mode = args.test.lower() == 'true'
    g_mode = args.gif.lower() == 'true'

    sol = Solution(test=t_mode, make_gif=g_mode)
    res = sol.part1() if args.part == 1 else sol.part2()
    if not g_mode: print(res)