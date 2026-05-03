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

    def run_cmd(self, cmd):
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout.strip()
        except Exception as e:
            return str(e)

    def build_database(self):
        """Fetches all installed packages and their details via pacman."""
        console.print("[bold yellow]Scanning installed packages... This may take a moment...[/bold yellow]")
        
        # Get list of all explicitly and implicitly installed packages
        installed_pkgs = self.run_cmd("pacman -Qq").split('\n')
        
        data = {}
        for pkg in installed_pkgs:
            if not pkg: continue
            # Get detailed info for each package
            info_raw = self.run_cmd(f"pacman -Qi {pkg}")
            details = {}
            for line in info_raw.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    details[key.strip()] = value.strip()
            
            data[pkg] = {
                "name": pkg,
                "desc": details.get("Description", "No description"),
                "deps": details.get("Depends On", "None"),
                "version": details.get("Version", "Unknown")
            }
        
        self.packages = data
        with open(CACHE_FILE, 'w') as f:
            json.dump(data, f)
        console.print("[bold green]Database built successfully![/bold green]")

    def load_database(self):
        """Loads data from cache to avoid running pacman -Qi 1000+ times every launch."""
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f:
                self.packages = json.load(f)
            return True
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

    console.print(Panel.fit("📦 [bold cyan]CachyOS Package & Dependency Explorer[/bold cyan]\n[small]Search installed packages, descriptions, and dependencies[/small]"))

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
