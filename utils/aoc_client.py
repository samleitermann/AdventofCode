import os 
import requests
import importlib.util
import pyperclip
import shutil

from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from bs4 import BeautifulSoup
from contextlib import contextmanager

console = Console()

@contextmanager
def pushd(path: Path):
    """Equivalent Python to temporarly `cd`"""
    old = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old)

class AocClient:
    BASE_URL = "https://adventofcode.com"
    SESSION_FILE = Path(".aoc_session")
    USER_AGENT = "AocClient/1.0 (+https://github.com/henriupton99/AdventOfCode)"

    def __init__(self, session_token: str):
        self.session = requests.Session()
        self.session.cookies.set("session", session_token)
        self.session.headers.update({
            "User-Agent": self.USER_AGENT,
            "X-AocClient": "AocClient-Python"
        })
        self.session_token = session_token

    # ===========================================================
    #                   LOGIN + TOKEN CACHE
    # ===========================================================
    @classmethod
    def load(cls):
        if cls.SESSION_FILE.exists():
            token = cls.SESSION_FILE.read_text().strip()
            return cls(token)

        console.print(Panel(
            "[bold cyan]AdventOfCode – first login[/bold cyan]\n"
            "Please input your session token (will be store/modifiable at file '.aoc_session' at any time).\n"
            "To get your session token : \n"
            "1. Go to AOC official website ([yellow]https://adventofcode.com/[/yellow]) and login to your personnal account \n"
            "2. Inspect the webpage using your browser (e.g Firefox, Google)\n"
            "3. Go to section 'Network', then refresh the page\n"
            "4. Check the first 'GET' item and the argument 'Cookie' (must be the pattern :[yellow]session=<your_session_token>[/yellow])",
            title="🔑 Session token"
        ))
        token = Prompt.ask("Session token", password=True)
        cls.SESSION_FILE.write_text(token)
        return cls(token)
    
    def collect_day(self, year: int, day: int,
                    template_solution="utils/solution.py"):
        """
        Collect day puzzle data :
        - README.md (puzzle)
        - test_input.txt (exemples)
        - real_input.txt
        - template solution
        """
        console.rule(f"[bold green]Collect Day {day} – {year}")

        dest_day = Path(f"problems/{year}/day_{day}")

        if dest_day.exists():
            raise FileExistsError(f"Directory {dest_day} already exists")

        dest_day.mkdir(parents=True)

        soup = self._fetch_puzzle_html(year, day)
        article = soup.find("article", class_="day-desc")

        # ---------------- README.md ----------------
        readme_path = dest_day / "README.md"
        self._write_readme(article, soup, readme_path)

        # ---------------- Test Input ----------------
        test_input_path = dest_day / "test_input.txt"
        self._extract_test_input(article, test_input_path)

        # ---------------- Real Input ----------------
        real_input_path = dest_day / "real_input.txt"
        self._fetch_real_input(year, day, real_input_path)

        # ---------------- Solution template ----------------
        shutil.copy(template_solution, dest_day / "solution.py")

        console.print("[bold green]✔ Collect done !\n")

    # ===========================================================
    #                     FETCH HTML & INPUTS
    # ===========================================================
    def _fetch_puzzle_html(self, year, day):
        url = f"{self.BASE_URL}/{year}/day/{day}"
        r = self.session.get(url)
        r.raise_for_status()
        return BeautifulSoup(r.text, "html.parser")

    def _fetch_real_input(self, year, day, dest):
        url = f"{self.BASE_URL}/{year}/day/{day}/input"
        r = self.session.get(url)
        if r.status_code == 400:
            raise RuntimeError("The session token is invalid. Please check the validity of your session token in the file '.aoc_session'")
        r.raise_for_status()
        dest.write_text(r.text.strip())
        console.print(f"[green]Real input →[/green] {dest}")

    # ===========================================================
    #                     README GENERATION
    # ===========================================================
    def _write_readme(self, article, soup, dest):
        title = soup.select_one(".day-desc h2")
        title = title.get_text(strip=True) if title else ""

        with dest.open("w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")

            for sec in article:
                if sec.name == "p":
                    f.write(sec.get_text() + "\n\n")
                elif sec.name == "pre":
                    f.write("```text\n")
                    f.write(sec.get_text().rstrip() + "\n")
                    f.write("```\n\n")

        console.print(f"[green]README →[/green] {dest}")

    # ===========================================================
    #                     TEST INPUT EXTRACTION
    # ===========================================================
    def _extract_test_input(self, article, dest):
        for p in article.find_all("p"):
            if "example" in p.get_text().lower():
                pre = p.find_next_sibling("pre")
                if pre:
                    dest.write_text(pre.get_text().strip())
                    console.print(f"[green]Test input →[/green] {dest}")
                    return

        console.print("[red] [WARNING] No test input found[/red]")

    def run_solution(self, year: int, day: int, part: int, test: bool,
                     copy_to_clipboard: bool = True):

        sol_dir = Path(f"problems/{year}/day_{day}")
        sol_file = "solution.py"

        full_path = sol_dir / sol_file
        if not full_path.exists():
            raise FileNotFoundError(f"{full_path} not found")

        # Move online to solution directory
        with pushd(sol_dir):
          
            spec = importlib.util.spec_from_file_location("solution", sol_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            Solution = module.Solution
            instance = Solution(test=test)

            result = instance.part1() if part == 1 else instance.part2()
        
        console.print(f"[bold yellow] Year :{year}\n Day :{day} \n Part :{part}[/bold yellow]")
        console.print(f"[bold yellow] Output : {result} [/bold yellow]")

        if copy_to_clipboard:
            try:
                pyperclip.copy(str(result))
                console.print("[green]Result copied in clipboard ✔[/green]")
            except Exception:
                console.print("[yellow]Clipboard not available[/yellow]")

        return result
