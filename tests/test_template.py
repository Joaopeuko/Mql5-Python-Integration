"""Tests for the template module that generates MT5 expert advisor template files."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Import the template functions directly for function-level testing
from mqpy.template import main


def test_template_generates_file_with_default_values() -> None:
    """Test that the template generates a file with default values."""
    # Create a temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    try:
        # Save current directory and move to temp directory
        original_dir = Path.cwd()
        os.chdir(temp_dir)

        # Run the main function directly
        sys.argv = ["template.py"]  # Reset sys.argv
        main()

        # Verify file was created with default name
        assert Path("demo.py").exists()

        # Check the content contains expected defaults
        with Path("demo.py").open(encoding="utf-8") as file:
            content = file.read()
            assert 'symbol="EURUSD"' in content
            assert "Moving Average Crossover" in content
            assert "short_window_size = 5" in content
            assert "long_window_size = 20" in content

    finally:
        # Clean up: restore original directory and remove temp directory
        os.chdir(original_dir)
        shutil.rmtree(temp_dir)


def test_template_generates_file_with_custom_values() -> None:
    """Test that the template generates a file with custom values."""
    # Create a temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    try:
        # Save current directory and move to temp directory
        original_dir = Path.cwd()
        os.chdir(temp_dir)

        # Set custom command line arguments
        sys.argv = ["template.py", "--file_name", "custom_strategy", "--symbol", "BTCUSD"]
        main()

        # Verify file was created with custom name
        assert Path("custom_strategy.py").exists()

        # Check the content contains the custom symbol
        with Path("custom_strategy.py").open(encoding="utf-8") as file:
            content = file.read()
            assert 'symbol="BTCUSD"' in content

    finally:
        # Clean up: restore original directory and remove temp directory
        os.chdir(original_dir)
        shutil.rmtree(temp_dir)


def test_template_overwrites_existing_file() -> None:
    """Test that the template overwrites an existing file."""
    # Create a temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    try:
        # Save current directory and move to temp directory
        original_dir = Path.cwd()
        os.chdir(temp_dir)

        # Create an existing file with known content
        Path("overwrite_test.py").write_text("ORIGINAL CONTENT THAT SHOULD BE REPLACED", encoding="utf-8")

        # Run the template generator with the same filename
        sys.argv = ["template.py", "--file_name", "overwrite_test", "--symbol", "EURUSD"]
        main()

        # Verify the file was overwritten
        with Path("overwrite_test.py").open(encoding="utf-8") as file:
            content = file.read()
            assert "ORIGINAL CONTENT THAT SHOULD BE REPLACED" not in content
            assert 'symbol="EURUSD"' in content
            assert "Moving Average Crossover" in content

    finally:
        # Clean up: restore original directory and remove temp directory
        os.chdir(original_dir)
        shutil.rmtree(temp_dir)


def test_template_runs_as_script() -> None:
    """Test that the template script can be run through Python."""
    # Create a temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    try:
        # Save current directory and move to temp directory
        original_dir = Path.cwd()
        os.chdir(temp_dir)

        # Run the template script using subprocess with custom parameters
        result = subprocess.run(  # noqa: S603
            [sys.executable, "-m", "mqpy.template", "--file_name", "script_test", "--symbol", "XAUUSD"],
            capture_output=True,
            text=True,
            check=True,
        )

        # Check that the process ran successfully
        assert result.returncode == 0

        # Verify file was created with the right name
        assert Path("script_test.py").exists()

        # Check the content contains the custom symbol
        with Path("script_test.py").open(encoding="utf-8") as file:
            content = file.read()
            assert 'symbol="XAUUSD"' in content

    finally:
        # Clean up: restore original directory and remove temp directory
        os.chdir(original_dir)
        shutil.rmtree(temp_dir)


def test_template_creates_valid_python_file() -> None:
    """Test that the generated template is valid Python code."""
    # Create a temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    try:
        # Save current directory and move to temp directory
        original_dir = Path.cwd()
        os.chdir(temp_dir)

        # Generate a template file
        sys.argv = ["template.py", "--file_name", "syntax_test"]
        main()

        # Try to compile the generated file to check for syntax errors
        with Path("syntax_test.py").open(encoding="utf-8") as file:
            content = file.read()

        # This will raise a SyntaxError if the code is not valid
        compile(content, "syntax_test.py", "exec")

    finally:
        # Clean up: restore original directory and remove temp directory
        os.chdir(original_dir)
        shutil.rmtree(temp_dir)


# CLI-specific tests
def test_cli_command_help() -> None:
    """Test that the CLI command --help option works correctly."""
    result = subprocess.run(  # noqa: S603
        [sys.executable, "-m", "mqpy.template", "--help"], capture_output=True, text=True, check=False
    )

    # Check that the command ran successfully
    assert result.returncode == 0

    # Check that the help output contains expected content
    assert "Generate MetaTrader 5 expert advisor templates" in result.stdout
    assert "--file_name" in result.stdout
    assert "--symbol" in result.stdout
    assert "--strategy" in result.stdout
    assert "moving_average" in result.stdout


def test_cli_different_strategies() -> None:
    """Test generating all different strategy types via CLI."""
    # Create a temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    try:
        # Save current directory and move to temp directory
        original_dir = Path.cwd()
        os.chdir(temp_dir)

        # Test each strategy type
        strategies = ["moving_average", "rsi", "macd", "bollinger"]

        for strategy in strategies:
            # Run the CLI command
            result = subprocess.run(  # noqa: S603
                [sys.executable, "-m", "mqpy.template", "--strategy", strategy, "--file_name", f"test_{strategy}"],
                capture_output=True,
                text=True,
                check=False,
            )

            # Check the command ran successfully
            assert result.returncode == 0

            # Verify file was created
            assert Path(f"test_{strategy}.py").exists()

            # Check strategy-specific content
            with Path(f"test_{strategy}.py").open(encoding="utf-8") as file:
                content = file.read()

                # Check for strategy-specific indicators
                if strategy == "moving_average":
                    assert "short_window_size = 5" in content
                    assert "long_window_size = 20" in content
                elif strategy == "rsi":
                    assert "rsi_period = 14" in content
                    assert "oversold_threshold = 30" in content
                    assert "calculate_rsi(" in content
                elif strategy == "macd":
                    assert "fast_period = 12" in content
                    assert "slow_period = 26" in content
                    assert "calculate_macd(" in content
                elif strategy == "bollinger":
                    assert "bb_period = 20" in content
                    assert "std_dev_multiplier = 2.0" in content
                    assert "calculate_bollinger_bands(" in content

    finally:
        # Clean up: restore original directory and remove temp directory
        os.chdir(original_dir)
        shutil.rmtree(temp_dir)


def test_cli_custom_directory() -> None:
    """Test that the --directory option works correctly."""
    # Create a temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    try:
        # Save current directory and move to temp directory
        original_dir = Path.cwd()
        os.chdir(temp_dir)

        # Create a subdirectory path that doesn't exist yet
        custom_dir = Path(temp_dir) / "custom_output_dir"

        # Run the CLI command with custom directory
        result = subprocess.run(  # noqa: S603
            [sys.executable, "-m", "mqpy.template", "--file_name", "dir_test", "--directory", str(custom_dir)],
            capture_output=True,
            text=True,
            check=False,
        )

        # Check the command ran successfully
        assert result.returncode == 0

        # Verify directory was created
        assert custom_dir.exists()

        # Verify file was created in the custom directory
        assert (custom_dir / "dir_test.py").exists()

    finally:
        # Clean up: restore original directory and remove temp directory
        os.chdir(original_dir)
        shutil.rmtree(temp_dir)


def test_cli_custom_parameters() -> None:
    """Test that the CLI command accepts custom trading parameters."""
    # Create a temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    try:
        # Save current directory and move to temp directory
        original_dir = Path.cwd()
        os.chdir(temp_dir)

        # Run the CLI command with custom parameters
        result = subprocess.run(  # noqa: S603
            [
                sys.executable,
                "-m",
                "mqpy.template",
                "--file_name",
                "params_test",
                "--symbol",
                "GBPJPY",
                "--magic_number",
                "12345",
                "--lot",
                "0.25",
                "--stop_loss",
                "30",
                "--take_profit",
                "60",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        # Check the command ran successfully
        assert result.returncode == 0

        # Verify file was created
        assert Path("params_test.py").exists()

        # Check custom parameters in the content
        with Path("params_test.py").open(encoding="utf-8") as file:
            content = file.read()
            assert 'symbol="GBPJPY"' in content
            assert "magic_number=12345" in content
            assert "lot=0.25" in content
            assert "stop_loss=30" in content
            assert "take_profit=60" in content

    finally:
        # Clean up: restore original directory and remove temp directory
        os.chdir(original_dir)
        shutil.rmtree(temp_dir)
