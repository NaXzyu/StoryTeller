import sys
import subprocess
from pathlib import Path
import click
from PyQt6.QtWidgets import QApplication

try:
    from storyteller.gui.main_window import MainWindow
except ImportError:
    print("Warning: Could not import MainWindow. GUI functionality might be limited.", file=sys.stderr)
    MainWindow = None

@click.group(invoke_without_command=True)
@click.version_option(package_name='storyteller')
@click.pass_context
def cli(ctx):
    """
    StoryTeller: AI Dialogue Management System.

    Run without arguments or with the 'run' command to launch the GUI.
    Use the 'build' command to create a distributable package.
    """
    if ctx.invoked_subcommand is None:
        if MainWindow is None:
            click.echo("Error: Cannot run GUI, MainWindow component failed to load.", err=True)
            if 'build' not in sys.argv:
                sys.exit(1)
        else:
            ctx.invoke(run)

@cli.command()
def run():
    """Launches the StoryTeller GUI application (default action)."""
    if MainWindow is None:
        click.echo("Error: Cannot run GUI, MainWindow component failed to load.", err=True)
        sys.exit(1)
    click.echo("Launching StoryTeller GUI...")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

@cli.command()
def build():
    """Builds the StoryTeller application using PyInstaller."""
    click.echo("Starting PyInstaller build process...")

    script_dir = Path(__file__).parent
    main_script_path = script_dir / "main.py"
    project_root = script_dir.parent.parent
    build_dir = project_root / "build"  # Define build directory path

    if not main_script_path.exists():
        click.echo(f"Error: Main script not found at {main_script_path}", err=True)
        sys.exit(1)

    entry_point_script = str(main_script_path)

    # Ensure build directory exists for the spec file
    build_dir.mkdir(parents=True, exist_ok=True)

    command = [
        sys.executable,
        "-m", "PyInstaller",
        entry_point_script,
        "--name", "StoryTeller",
        "--distpath", str(project_root / "dist"),
        "--workpath", str(build_dir),  # Use build_dir for workpath
        "--specpath", str(build_dir),  # Use build_dir for specpath
        "--clean",
        "--noconfirm",
        "--windowed",  # Add this flag to hide the console window
    ]

    click.echo(f"Running command: {' '.join(command)}")

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            click.echo("PyInstaller build completed successfully.")
            click.echo(f"Output located in: {project_root / 'dist'}")
            click.echo("\n--- PyInstaller Output ---")
            click.echo(stdout)
            click.echo("--- End PyInstaller Output ---")
        else:
            click.echo(f"Error: PyInstaller build failed with return code {process.returncode}", err=True)
            click.echo("\n--- PyInstaller Error Output ---", err=True)
            click.echo(stderr, err=True)
            click.echo("--- End PyInstaller Error Output ---", err=True)
            sys.exit(process.returncode)

    except FileNotFoundError:
        click.echo("Error: PyInstaller command not found. Is PyInstaller installed in your environment?", err=True)
        click.echo("Install development dependencies: uv pip install -e .[dev]", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"An unexpected error occurred during build: {e}", err=True)
        sys.exit(1)

if __name__ == "__main__":
    cli()
