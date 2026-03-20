---
name: skill-creator
description: Create new skills, agents, or commands following agentskills.io best practices. Use when asked to create a skill, agent, command, or when you need to package domain expertise into a reusable capability.
metadata:
  version: "1.0.0"
  author: spoletum
  type: meta-skill
---

# Skill Creator

Create well-structured, effective skills/agents/commands following the agentskills.io specification and best practices.

## When to Create What

**Create a SKILL** when:
- Packaging reusable domain expertise (e.g., "how to analyze PDFs")
- Capturing team conventions or workflows
- Extending agent capabilities for specific tasks

**Create an AGENT** when:
- Defining a specialized AI persona with multiple skills
- Setting up an autonomous system with specific goals
- Configuring model parameters and tool access

**Create a COMMAND** when:
- Defining a single, specific executable action
- Creating CLI shortcuts or automation scripts
- Wrapping complex operations into simple invocations

## Universal Principles (Apply to All)

### 1. Start with Real Expertise
- Extract from hands-on tasks you've completed
- Feed domain-specific context (APIs, schemas, gotchas)
- Don't rely on generic LLM knowledge

### 2. Progressive Disclosure Structure
```
Metadata (~100 tokens)     → Loaded at startup (name, description)
Instructions (<5000 tokens) → Loaded when activated (SKILL.md body)
Resources (on-demand)      → Loaded when referenced (scripts/, references/, assets/)
```

### 3. Calibrate Specificity
- **Be prescriptive** for fragile operations requiring exact sequences
- **Give freedom** when multiple approaches are valid
- **Provide defaults, not menus** - pick one primary approach, mention alternatives briefly

### 4. Include Gotchas
Document environment-specific facts that defy reasonable assumptions:
```markdown
## Gotchas
- The API returns 200 on `/health` even when DB is down - use `/ready` instead
- User IDs are `user_id` in DB but `uid` in auth service
```

## Creation Workflow

For each request, follow this sequence:

### Step 1: Understand Requirements
Ask clarifying questions:
- What domain/task is this for?
- What mistakes does the agent make without guidance?
- What are the specific tools/APIs involved?
- Are there project-specific conventions to capture?

### Step 2: Choose Output Type

| Type | File Structure | Use Case |
|------|---------------|----------|
| **Skill** | `skill-name/SKILL.md` + optional dirs | Reusable domain expertise |
| **Agent** | `agent-name/agent.json` or `SKILL.md` | Configured AI persona |
| **Command** | `command-name/command.json` or shell script | Single executable action |

### Step 3: Generate Content Following Format

#### SKILL.md Format
```markdown
---
name: <lowercase-hyphenated-name>
description: <What it does AND when to use it. Max 1024 chars.>
license: <optional>
compatibility: <optional - environment requirements>
metadata:
  author: <name>
  version: "1.0.0"
  <custom-keys>: <values>
---

# <Title>

## Overview
Brief description of what this enables.

## When to Use
Specific triggers that should activate this skill.

## Instructions
Step-by-step procedure. Be specific for fragile operations.

## Gotchas
- Non-obvious edge case 1
- Environment-specific fact 2

## Examples
### Example 1: <Scenario>
Input: ...
Output: ...

## Resources
- [Detailed Reference](references/REFERENCE.md)
- [Template](assets/template.md)
- `scripts/helper.py` - Helper script
```

#### Agent Format (JSON)
```json
{
  "name": "agent-name",
  "description": "What this agent does and when to use it",
  "version": "1.0.0",
  "skills": ["skill-1", "skill-2"],
  "commands": ["command-1"],
  "config": {
    "model": "claude-3-opus-20240229",
    "temperature": 0.7,
    "max_tokens": 4000
  },
  "system_prompt": "You are a specialized agent that...",
  "tools": ["Bash", "Read", "Write", "Edit"],
  "metadata": {
    "author": "",
    "created": "",
    "tags": []
  }
}
```

#### Command Format (JSON)
```json
{
  "name": "command-name",
  "description": "What this command does and when to use it",
  "version": "1.0.0",
  "command": "<base-command>",
  "arguments": [
    {
      "name": "arg1",
      "description": "Description",
      "required": true,
      "type": "string"
    }
  ],
  "options": {
    "--flag": {
      "description": "What this flag does",
      "type": "boolean",
      "default": false
    }
  },
  "help_text": "Full help documentation",
  "examples": [
    "command-name arg1 --flag"
  ],
  "metadata": {
    "author": "",
    "created": "",
    "tags": []
  }
}
```

### Step 4: Apply Content Best Practices

**DO:**
- Jump straight to specifics (omit "what is X" explanations)
- Include concrete examples with real inputs/outputs
- Add validation steps or checklists for multi-step workflows
- Reference external files for detailed content (progressive disclosure)
- Use code blocks for commands, templates, and examples

**DON'T:**
- Explain concepts the agent already knows
- Present multiple equal options without defaults
- Include every edge case in main file (move to references/)
- Write exhaustive documentation that competes for context

### Step 5: Create Supporting Files (if needed)

**scripts/** - Executable helpers:
```python
#!/usr/bin/env python3
"""Helper script for X. Handles edge case Y."""
# Self-contained or clearly document dependencies
# Include helpful error messages
```

**references/** - Detailed docs loaded on-demand:
```markdown
# Reference: <Topic>

Loaded when: <specific condition>

Detailed content here...
```

**assets/** - Templates and resources:
```markdown
<!-- assets/report-template.md -->
# Report Template

Use this structure for consistency...
```

## Validation Checklist

Before finalizing, verify:

- [ ] Name matches folder name, lowercase, hyphens only
- [ ] Description includes both "what" and "when to use"
- [ ] Under 500 lines / 5,000 tokens (main file)
- [ ] Gotchas section captures non-obvious issues
- [ ] Examples show realistic input/output
- [ ] Scripts are self-contained or dependencies documented
- [ ] No generic explanations of known concepts
- [ ] Clear default approach selected (not multiple equal options)

## Example: Creating a PDF Processing Skill

**User request**: "Create a skill for working with PDFs"

**Output**:

```markdown
---
name: pdf-processing
description: Extract text, fill forms, and merge PDFs. Use when working with PDF documents, extracting content, or modifying PDF files.
metadata:
  author: spoletum
  version: "1.0.0"
---

# PDF Processing

Process PDF documents efficiently with the right tools for each task.

## Quick Reference

| Task | Tool | Command |
|------|------|---------|
| Extract text | pdfplumber | `python scripts/extract_text.py <file>` |
| Fill forms | pdftk | `pdftk <input> fill_form <fdf> output <output>` |
| Merge PDFs | PyPDF2 | `python scripts/merge.py <files...>` |
| OCR (scanned) | pdf2image + pytesseract | See [OCR Guide](references/ocr.md) |

## Gotchas

- pdfplumber fails on encrypted PDFs - decrypt first with `qpdf --decrypt`
- Form field names often differ from displayed labels - use `scripts/list_fields.py` to see actual names
- Merging scanned + text PDFs can corrupt text layer - convert all to images first if mixing

## Text Extraction

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    text = "\n".join(page.extract_text() or "" for page in pdf.pages)
```

For scanned documents, use OCR instead: See [OCR Guide](references/ocr.md)

## Form Processing Workflow

Progress:
- [ ] Step 1: List form fields (`scripts/list_fields.py input.pdf`)
- [ ] Step 2: Create field mapping (edit `field_values.json`)
- [ ] Step 3: Validate mapping (`scripts/validate_fields.py`)
- [ ] Step 4: Fill form (`scripts/fill_form.py input.pdf field_values.json output.pdf`)
- [ ] Step 5: Verify output visually
```

## Current Request

Now apply this framework to create the requested skill/agent/command.
