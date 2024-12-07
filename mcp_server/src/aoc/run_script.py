import subprocess
import tempfile
import shutil
from pathlib import Path
import os
import uuid

DOCKERFILE_TEMPLATE = '''
FROM python:3.12-slim

# Install uv
RUN pip install uv

WORKDIR /aoc
COPY . /aoc/

# Set environment for Python
ENV PYTHONUNBUFFERED=1
'''

def run_script(script_path: str, timeout: int = 15) -> tuple[str, str]:
    """
    Run a Python script in a Docker container with network access.

    Args:
        script_path: Path to the script relative to AOC root
        timeout: Maximum execution time in seconds

    Returns:
        tuple[str, str]: (stdout, stderr)
    """
    aoc_root = Path("/Users/rictic/open/aoc2024")
    full_script_path = (aoc_root / script_path).resolve()

    # Validate path
    if not str(full_script_path).startswith(str(aoc_root)):
        raise ValueError(f"Script path must be within {aoc_root}")
    if full_script_path.suffix != '.py':
        raise ValueError("Script must be a Python file")

    # Convert the path to its location inside the container
    container_path = f"/aoc/{script_path}"

    # Create a temporary directory for Docker context
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Copy AOC directory contents, excluding unnecessary files
        def ignore_patterns(path, names):
            return [
                n for n in names
                if (n.startswith('.') and n != '.env') or  # Hidden files except .env
                n == '__pycache__' or    # Python cache
                n == '.venv' or          # Virtual environments
                n == 'node_modules' or   # Node.js modules
                n.endswith('.pyc')       # Compiled Python files
            ]

        shutil.copytree(
            aoc_root,
            temp_path / "aoc",
            ignore=ignore_patterns,
            dirs_exist_ok=True
        )

        # Create Dockerfile
        (temp_path / "aoc" / "Dockerfile").write_text(DOCKERFILE_TEMPLATE)

        # Generate unique container name
        container_name = f"aoc-runner-{uuid.uuid4().hex[:8]}"

        try:
            # Build Docker image
            subprocess.run(
                ["docker", "build", "-t", container_name, "./aoc"],
                cwd=temp_path,
                check=True,
                capture_output=True,
                text=True
            )

            # Run script in container using uv
            result = subprocess.run(
                [
                    "docker", "run",
                    "--name", container_name,
                    "--network", "host",  # Allow network access
                    "--rm",  # Remove container after execution
                    container_name,
                    "uv",
                    "--directory", "/aoc/mcp_server",
                    "run",
                    container_path
                ],
                timeout=timeout,
                capture_output=True,
                text=True
            )

            return result.stdout, result.stderr

        except subprocess.TimeoutExpired as e:
            # Clean up container if it's still running
            subprocess.run(["docker", "stop", container_name], capture_output=True)
            subprocess.run(["docker", "rm", container_name], capture_output=True)
            return (
                e.stdout.decode() if e.stdout else "",
                f"Script execution timed out after {timeout} seconds\n" +
                (e.stderr.decode() if e.stderr else "")
            )

        except subprocess.CalledProcessError as e:
            return (
                e.stdout,
                f"Error running script: {e.stderr}"
            )

        finally:
            # Clean up Docker image
            subprocess.run(["docker", "rmi", container_name], capture_output=True)

if __name__ == "__main__":
    # Test with day01/solve.py when run directly
    stdout, stderr = run_script("day01/solve.py")
    print("=== STDOUT ===")
    print(stdout)
    print("\n=== STDERR ===")
    print(stderr)
