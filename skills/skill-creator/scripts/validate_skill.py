#!/usr/bin/env python3
"""Validate a skill directory against agentskills.io specification."""

import sys
import re
import yaml
from pathlib import Path


def validate_skill(skill_path: str) -> bool:
    """Validate skill directory structure and SKILL.md content."""

    skill_dir = Path(skill_path)
    skill_md = skill_dir / "SKILL.md"

    errors = []
    warnings = []

    # Check directory exists
    if not skill_dir.exists():
        errors.append(f"Directory not found: {skill_path}")
        return False

    # Check SKILL.md exists
    if not skill_md.exists():
        errors.append(f"SKILL.md not found in {skill_path}")
        return False

    # Read SKILL.md
    content = skill_md.read_text()

    # Extract frontmatter
    if not content.startswith("---"):
        errors.append("SKILL.md must start with YAML frontmatter (---)")
        return False

    parts = content.split("---", 2)
    if len(parts) < 3:
        errors.append("Invalid frontmatter format")
        return False

    try:
        frontmatter = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML frontmatter: {e}")
        return False

    # Validate required fields
    if "name" not in frontmatter:
        errors.append("Missing required field: name")
    else:
        name = frontmatter["name"]
        # Validate name format
        if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name):
            errors.append(
                f"Invalid name '{name}': must be lowercase, alphanumeric with hyphens"
            )
        if len(name) > 64:
            errors.append(f"Name too long: {len(name)} chars (max 64)")
        if name != skill_dir.name:
            warnings.append(f"Name '{name}' doesn't match directory '{skill_dir.name}'")

    if "description" not in frontmatter:
        errors.append("Missing required field: description")
    else:
        desc = frontmatter["description"]
        if len(desc) > 1024:
            errors.append(f"Description too long: {len(desc)} chars (max 1024)")
        if len(desc) < 10:
            warnings.append(
                "Description seems very short - should explain what AND when to use"
            )

    # Check optional fields
    if "compatibility" in frontmatter:
        if len(frontmatter["compatibility"]) > 500:
            errors.append("compatibility field too long (max 500 chars)")

    # Check body content
    body = parts[2]
    body_lines = body.strip().split("\n")

    if len(body_lines) > 500:
        warnings.append(f"Body is {len(body_lines)} lines (recommended: <500)")

    # Check for gotchas section (recommended)
    if "## Gotchas" not in body and "## gotchas" not in body.lower():
        warnings.append(
            "No '## Gotchas' section found (recommended for non-obvious issues)"
        )

    # Check for examples (recommended)
    if "## Example" not in body:
        warnings.append("No examples section found (recommended)")

    # Check file references are valid
    ref_pattern = r"\[([^\]]+)\]\(([^)]+)\)"
    for match in re.finditer(ref_pattern, body):
        ref_path = match.group(2)
        if not ref_path.startswith(("http://", "https://", "#")):
            full_path = skill_dir / ref_path
            if not full_path.exists():
                errors.append(f"Referenced file not found: {ref_path}")

    # Report results
    if errors:
        print("❌ ERRORS:")
        for err in errors:
            print(f"  • {err}")

    if warnings:
        print("⚠️  WARNINGS:")
        for warn in warnings:
            print(f"  • {warn}")

    if not errors and not warnings:
        print("✅ Skill validation passed!")
        return True
    elif not errors:
        print("✅ Skill is valid (with warnings)")
        return True
    else:
        print("\n❌ Skill validation failed")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_skill.py <skill-directory>")
        sys.exit(1)

    success = validate_skill(sys.argv[1])
    sys.exit(0 if success else 1)
