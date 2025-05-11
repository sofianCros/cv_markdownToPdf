# Affiche des barres de progression et des logs stylés avec rich
# Utilisable pour suivre plusieurs phases de traitement

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

console = Console()

class PhaseProgress:
    def __init__(self):
        self.progress = Progress(
            SpinnerColumn(),                             # Animation (⠙ ⠹ ⠼ ...)
            TextColumn("[bold cyan]{task.description}"), # Nom de la phase
            BarColumn(),                                 # Barre horizontale
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeElapsedColumn(),                         # Temps écoulé
            console=console,
            transient=False,
            auto_refresh=True
        )
        self.tasks = {}

    def start(self):
        self.progress.start()

    def stop(self):
        self.progress.stop()

    def add_phase(self, name, total):
        self.tasks[name] = self.progress.add_task(name, total=total)

    def advance(self, name, step=1):
        if name in self.tasks:
            self.progress.update(self.tasks[name], advance=step)

    def log(self, message, style="bold green"):
        console.log(f"[{style}]{message}[/]")
