from pathlib import Path

INSTRUCTIONS_DIR = Path(__file__).parent / "instructions"

VALID_COMMANDS = ["help", "init", "mine", "backup", "status", "check", "wake-up", "diary", "palace", "kg", "closing-ritual"]


def run_instructions(command: str):
    command = command.lower().strip()

    if command not in VALID_COMMANDS:
        print(f"Unknown command: {command}")
        print(f"Valid commands: {', '.join(VALID_COMMANDS)}")
        raise SystemExit(1)

    instruction_file = INSTRUCTIONS_DIR / f"{command}.md"

    if not instruction_file.exists():
        print(f"Instruction file not found: {instruction_file}")
        raise SystemExit(1)

    print(instruction_file.read_text(encoding="utf-8"))
