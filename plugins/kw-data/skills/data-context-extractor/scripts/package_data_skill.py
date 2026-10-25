#!/usr/bin/env python3
"""
Package a generated data analysis skill into a distributable .skill file (zip format).

Usage:
    python package_data_skill.py <path/to/skill-folder> [output-directory]

Example:
    python package_data_skill.py /home/claude/acme-data-analyst
    python package_data_skill.py /home/claude/acme-data-analyst /tmp/outputs
"""

import os
import sys
import tempfile
import zipfile
from pathlib import Path


def validate_skill(skill_path: Path) -> tuple[bool, str]:
    """Basic validation of skill structure."""

    # Check SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "Missing SKILL.md"

    # Check SKILL.md has frontmatter
    content = skill_md.read_text()
    if not content.startswith("---"):
        return False, "SKILL.md missing YAML frontmatter"

    # Check for required frontmatter fields
    if "name:" not in content[:500]:
        return False, "SKILL.md missing 'name' in frontmatter"
    if "description:" not in content[:1000]:
        return False, "SKILL.md missing 'description' in frontmatter"

    # Check for placeholder text that wasn't filled in
    if "[PLACEHOLDER]" in content or "[COMPANY]" in content:
        return False, "SKILL.md contains unfilled placeholder text"

    return True, "Validation passed"


def package_skill(skill_path: str, output_dir: str | None = None) -> Path | None:
    """Package regular skill files without following links or including the output ZIP."""
    requested = Path(skill_path)
    if requested.is_symlink():
        print(f"Error: Skill folder is a symlink: {requested}")
        return None
    skill_root = requested.resolve()
    if not skill_root.is_dir():
        print(f"Error: Skill folder not found: {skill_root}")
        return None

    output_root = Path(output_dir).resolve() if output_dir else Path.cwd().resolve()
    skill_filename = output_root / f"{skill_root.name}.zip"
    if skill_filename.is_relative_to(skill_root):
        print(f"Error: Output ZIP cannot be inside the skill folder: {skill_filename}")
        return None

    files = []
    for item in sorted(skill_root.rglob('*')):
        if item.is_symlink() or not item.resolve().is_relative_to(skill_root):
            print(f"Error: Symlink or escaped path in skill folder: {item}")
            return None
        if not item.is_file():
            if item.is_dir():
                continue
            print(f"Error: Unsupported path in skill folder: {item}")
            return None
        relative = item.relative_to(skill_root)
        if any(part.startswith('.') or part == '__pycache__' for part in relative.parts):
            continue
        if item.name in {'.DS_Store', 'Thumbs.db'}:
            continue
        files.append(item)

    print("Validating skill...")
    valid, message = validate_skill(skill_root)
    if not valid:
        print(f"Validation failed: {message}")
        return None
    print(f"{message}\n")

    staged_zip = None
    try:
        output_root.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            dir=output_root, prefix=f".{skill_root.name}.", suffix=".zip.part", delete=False
        ) as staged:
            staged_zip = Path(staged.name)
        with zipfile.ZipFile(staged_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for item in files:
                arcname = item.relative_to(skill_root.parent)
                zipf.write(item, arcname)
                print(f"  Added: {arcname}")
        os.replace(staged_zip, skill_filename)
        print(f"\nSuccessfully packaged skill to: {skill_filename}")
        return skill_filename
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        print(f"Error creating zip file: {error}")
        return None
    finally:
        if staged_zip is not None:
            staged_zip.unlink(missing_ok=True)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"Packaging skill: {skill_path}")
    if output_dir:
        print(f"   Output directory: {output_dir}")
    print()

    result = package_skill(skill_path, output_dir)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
