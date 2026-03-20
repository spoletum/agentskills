#!/usr/bin/env python3
"""Generate a new skill from template."""

import sys
import argparse
from pathlib import Path

SKILL_TEMPLATE = """---
name: {name}
description: {description}
metadata:
  author: {author}
  version: "1.0.0"
  created: "{date}"
---

# {title}

## Overview

Brief description of what this skill enables and why it matters.

## When to Use

- Trigger condition 1
- Trigger condition 2
- Specific scenarios where this applies

## Instructions

### Step 1: <First Action>

Description of what to do:

```bash
# Example command
command --option value
```

### Step 2: <Second Action>

Continue with next steps...

## Gotchas

- Non-obvious edge case 1 (environment-specific)
- Quirk 2 that defies normal assumptions
- Specific requirement or limitation

## Examples

### Example 1: <Common Scenario>

**Input**: User asks for...

**Process**:
1. Step one
2. Step two

**Output**:
```
Expected output format
```

### Example 2: <Edge Case>

**Input**: Unusual request...

**Handling**: How to handle it...

## Resources

- [Detailed Reference](references/REFERENCE.md) - Load when you need technical details
- [Template](assets/template.md) - Use for consistent output formatting
- `scripts/helper.py` - Helper script for complex operations
"""


def generate_skill(
    name: str, description: str, author: str = "", output_dir: str = "."
) -> Path:
    """Generate a new skill from template."""

    from datetime import datetime

    # Create directory
    skill_dir = Path(output_dir) / name
    skill_dir.mkdir(parents=True, exist_ok=True)

    # Create SKILL.md
    skill_md = skill_dir / "SKILL.md"
    title = name.replace("-", " ").title()

    content = SKILL_TEMPLATE.format(
        name=name,
        description=description,
        author=author or "unknown",
        date=datetime.now().strftime("%Y-%m-%d"),
        title=title,
    )

    skill_md.write_text(content)

    # Create empty directories
    (skill_dir / "scripts").mkdir(exist_ok=True)
    (skill_dir / "references").mkdir(exist_ok=True)
    (skill_dir / "assets").mkdir(exist_ok=True)

    print(f"✅ Created skill: {skill_dir}")
    print(f"   SKILL.md: {skill_md}")
    print(f"\nNext steps:")
    print(f"  1. Edit {skill_md}")
    print(f"  2. Add scripts to {skill_dir}/scripts/")
    print(f"  3. Add references to {skill_dir}/references/")
    print(f"  4. Validate: python validate_skill.py {skill_dir}")

    return skill_dir


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a new skill from template")
    parser.add_argument("name", help="Skill name (lowercase, hyphenated)")
    parser.add_argument("description", help="Skill description")
    parser.add_argument("--author", default="", help="Author name")
    parser.add_argument("--output", "-o", default=".", help="Output directory")

    args = parser.parse_args()

    generate_skill(args.name, args.description, args.author, args.output)
