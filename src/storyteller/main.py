import sys
import subprocess
from pathlib import Path
import click
import importlib.metadata

# --- Project Imports ---
# Import constants and paths
from . import const
from . import paths

# --- GUI Imports ---
try:
    from storyteller.gui.main_window import MainWindow
    from PyQt6.QtWidgets import QApplication
    
    # Make qt_material optional
    try:
        import qt_material # type: ignore
        qt_material_available = True
    except ImportError:
        qt_material = None
        qt_material_available = False
        print("Warning: qt-material package not found. Using default PyQt styling.", file=sys.stderr)
except ImportError as e:
    # Print the original error for better debugging
    print(f"Warning: Could not import GUI components. GUI functionality might be limited. Error: {e}", file=sys.stderr)
    MainWindow = None
    QApplication = None
    qt_material = None
    qt_material_available = False

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
        if MainWindow is None or QApplication is None:
            click.echo("Error: Cannot run GUI, GUI components failed to load.", err=True)
            if 'build' not in sys.argv:
                sys.exit(1)
        else:
            ctx.invoke(run)

@cli.command()
def run():
    """Launches the StoryTeller GUI application."""
    if MainWindow is None or QApplication is None:
        click.echo("Error: Cannot run GUI, GUI components failed to load.", err=True)
        return
    
    # We can still run the app without qt_material

    click.echo("Launching StoryTeller GUI...")
    app = QApplication(sys.argv)

    # Apply the qt-material theme only if available
    if qt_material_available:
        try:
            qt_material.apply_stylesheet(app, theme='dark_blue.xml')  # Choose a dark theme
        except Exception as e:
            click.echo(f"Warning: Failed to apply qt-material theme. Using default style. Error: {e}", err=True)
    else:
        click.echo("Using default PyQt style (qt-material not installed).")

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

@cli.command()
def build():
    """Builds the StoryTeller application using PyInstaller."""
    click.echo("Starting PyInstaller build process...")

    # Use functions from paths module
    main_script_path = paths.get_main_script_path()
    build_dir = paths.get_build_dir()
    dist_dir = paths.get_dist_dir()

    if not main_script_path.exists():
        click.echo(f"Error: Main script not found at {main_script_path}", err=True)
        sys.exit(1)

    entry_point_script = str(main_script_path)

    command = [
        sys.executable,
        "-m", "PyInstaller",
        entry_point_script,
        "--name", const.APP_NAME,  # Use constant for app name
        "--distpath", str(dist_dir),  # Use path function result
        "--workpath", str(build_dir),  # Use path function result
        "--specpath", str(build_dir),  # Use path function result
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
            click.echo(f"Output located in: {dist_dir}")  # Use path variable
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
