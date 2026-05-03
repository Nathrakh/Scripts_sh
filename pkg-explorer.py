import subprocess
import sys
import json
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

CACHE_FILE = os.path.expanduser("~/.cache/pkg-explorer-data.json")

class PkgExplorer:
    def __init__(self):
        self.packages = {}

    def run_cmd(self, cmd_list):
        """Runs a command from a list to avoid shell overhead and argument limits."""
        try:
            result = subprocess.run(cmd_list, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except Exception as e:
            return ""

    def build_database(self):
        """Fetches all installed packages and their details via pacman in one go."""
        console.print("[bold yellow]Scanning installed packages...[/bold yellow]")
        
        # Get list of all installed packages
        try:
            installed_pkgs_raw = subprocess.run(["pacman", "-Qq"], capture_output=True, text=True, check=True).stdout.strip()
            installed_pkgs = [pkg for pkg in installed_pkgs_raw.split('\n') if pkg]
        except Exception as e:
            console.print(f"[bold red]Failed to get package list: {e}[/bold red]")
            return

        # Fetch info for ALL packages in a SINGLE subprocess call
        # Passing the list directly avoids shell string limits
        info_raw = self.run_cmd(["pacman", "-Qi"] + installed_pkgs)
        
        data = {}
        # pacman -Qi separates packages with double newlines
        blocks = info_raw.split('\n\n')
        
        for block in blocks:
            if not block.strip():
                continue
                
            details = {}
            for line in block.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    details[key.strip()] = value.strip()
            
            if "Name" in details:
                pkg_name = details["Name"]
                data[pkg_name] = {
                    "name": pkg_name,
                    "desc": details.get("Description", "No description"),
                    "deps": details.get("Depends On", "None"),
                    "version": details.get("Version", "Unknown")
                }
        
        self.packages = data
        
        # Ensure cache directory exists
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        
        with open(CACHE_FILE, 'w') as f:
            json.dump(data, f)
        console.print("[bold green]Database built successfully![/bold green]")

    def load_database(self):
        """Loads data from cache to avoid rebuilding every launch."""
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, 'r') as f:
                    self.packages = json.load(f)
                return True
            except json.JSONDecodeError:
                return False
        return False

    def search(self, keyword):
        """Search across names, descriptions and dependencies."""
        keyword = keyword.lower()
        results = []
        for pkg_name, info in self.packages.items():
            if (keyword in pkg_name.lower() or 
                keyword in info['desc'].lower() or 
                keyword in info['deps'].lower()):
                results.append(info)
        return results

    def display_results(self, results):
        if not results:
            console.print("[bold red]No packages found matching that keyword.[/bold red]")
            return

        table = Table(title=f"Search Results ({len(results)} found)")
        table.add_column("Package", style="cyan", no_wrap=True)
        table.add_column("Version", style="magenta")
        table.add_column("Description", style="green")
        table.add_column("Dependencies", style="yellow")

        for res in results:
            # Truncate long dependency lists for readability
            deps = res['deps']
            if len(deps) > 60:
                deps = deps[:57] + "..."
            
            table.add_row(res['name'], res['version'], res['desc'], deps)

        console.print(table)


def main():
    explorer = PkgExplorer()
    
    if not explorer.load_database():
        explorer.build_database()

    console.print(Panel.fit("📦 [bold cyan]Arch Package & Dependency Explorer[/bold cyan]\n[small]Search installed packages, descriptions, and dependencies[/small]"))

    while True:
        choice = Prompt.ask(
            "\n[bold white]Enter keyword to search (or 'r' to refresh, 'q' to quit)[/bold white]", 
            default=""
        )

        if choice.lower() == 'q':
            break
        elif choice.lower() == 'r':
            explorer.build_database()
            continue
        elif choice == "":
            continue
        else:
            results = explorer.search(choice)
            explorer.display_results(results)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Exiting...[/yellow]")
        sys.exit(0)
