#!/usr/bin/env python3
"""Generate available-skills.xml from skills/*/SKILL.md frontmatter.

Scans every skill directory, extracts name and description from the YAML
frontmatter, and writes an <available_skills> XML catalog at the repo root.

Usage:
    python scripts/generate-available-skills.py           # default: repo root
    python scripts/generate-available-skills.py /path      # custom base dir
"""

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.dom import minidom

_FRONTMATTER_RE = re.compile(
    r'^---[ \t]*\n(.*?)^---[ \t]*\n?', re.MULTILINE | re.DOTALL,
)


def _parse_yaml_value(raw: str) -> str:
    """Strip surrounding quotes from a YAML value."""
    raw = raw.strip()
    if (raw.startswith('"') and raw.endswith('"')) or (
        raw.startswith("'") and raw.endswith("'")
    ):
        return raw[1:-1]
    return raw


def _extract_frontmatter(text: str) -> dict[str, str]:
    """Minimal YAML frontmatter parser — extracts top-level scalar fields.

    Handles plain values, quoted strings, and YAML block scalars (>-, |-, >, |).
    """
    m = _FRONTMATTER_RE.search(text)
    if not m:
        return {}
    fields: dict[str, str] = {}
    lines = m.group(1).splitlines()
    i = 0
    while i < len(lines):
        # Check for block scalar indicator (>-, |-, >, |)
        block_match = re.match(r'^([a-zA-Z_-]+):\s*([>|]-?)\s*$', lines[i])
        if block_match:
            key = block_match.group(1)
            fold = block_match.group(2).startswith('>')
            # Collect indented continuation lines
            parts: list[str] = []
            i += 1
            while i < len(lines) and re.match(r'^[ \t]+', lines[i]):
                parts.append(lines[i].strip())
                i += 1
            fields[key] = ' '.join(parts) if fold else '\n'.join(parts)
            continue

        kv = re.match(r'^([a-zA-Z_-]+):\s+(.+)$', lines[i])
        if kv:
            fields[kv.group(1)] = _parse_yaml_value(kv.group(2))
        i += 1
    return fields


def collect_skills(base: Path) -> list[dict[str, str]]:
    """Return sorted list of {name, description, location} for each skill."""
    skills_dir = base / 'skills'
    if not skills_dir.is_dir():
        return []

    skills: list[dict[str, str]] = []
    for skill_path in sorted(skills_dir.iterdir()):
        skill_md = skill_path / 'SKILL.md'
        if not skill_md.is_file():
            continue
        fm = _extract_frontmatter(skill_md.read_text(encoding='utf-8'))
        name = fm.get('name', skill_path.name)
        description = fm.get('description', '')
        location = f'skills/{skill_path.name}/SKILL.md'
        skills.append({
            'name': name,
            'description': description,
            'location': location,
        })
    return skills


def build_xml(skills: list[dict[str, str]]) -> str:
    """Build <available_skills> XML string."""
    root = ET.Element('available_skills')
    for s in skills:
        skill_el = ET.SubElement(root, 'skill')
        ET.SubElement(skill_el, 'name').text = s['name']
        ET.SubElement(skill_el, 'description').text = s['description']
        ET.SubElement(skill_el, 'location').text = s['location']

    rough = ET.tostring(root, encoding='unicode', xml_declaration=False)
    parsed = minidom.parseString(rough)
    pretty = parsed.toprettyxml(indent='  ', encoding=None)
    # Remove the XML declaration line minidom adds
    lines = pretty.splitlines()
    if lines and lines[0].startswith('<?xml'):
        lines = lines[1:]
    # Remove blank lines between elements for cleaner output
    cleaned = '\n'.join(line for line in lines if line.strip())
    return cleaned + '\n'


def main() -> int:
    base = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    skills = collect_skills(base)

    if not skills:
        print('No skills found.', file=sys.stderr)
        return 1

    output = base / 'available-skills.xml'
    xml_content = build_xml(skills)
    output.write_text(xml_content, encoding='utf-8')
    print(f'Generated {output.name} with {len(skills)} skills.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
