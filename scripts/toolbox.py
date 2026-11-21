#!/usr/bin/env python3
"""Собрать каталог установленных инструментов для AI-агентов.

Источники:
  README.md                     — назначение и ссылка (разделы = роли);
  roles/*/defaults/*.yml        — реальные имена бинарников;
  report.json                   — факт установки и версия;
  vars/toolbox.yml              — домены, оверрайды, быстрая таблица.

Выход:
  toolbox.json                  — машиночитаемый каталог;
  docs/tools.md                 — индекс для агента;
  docs/tools/<domain>.md        — категории.

Скрипт ничего не устанавливает и не меняет систему: только читает файлы
репозитория и пишет каталог в XDG-каталоги пользователя.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - PyYAML приходит с Ansible
    sys.stderr.write("toolbox: нужен PyYAML (python3-yaml)\n")
    raise SystemExit(1)

SECTION_RE = re.compile(r"^###\s+(?P<name>.+?)\s*$")
BULLET_RE = re.compile(
    r"^- \[(?P<display>[^\]]+)\]\((?P<url>[^)]+)\)\s+—\s+(?P<desc>.+?)\s*$"
)
GITHUB_RE = re.compile(r"^https?://github\.com/(?P<repo>[^/]+/[^/#?]+)")
VERSION_RE = re.compile(
    r"\bv?\d+\.\d+(?:\.\d+)*(?:[-+][\w.]+)?\b"
)


def pick_version(output: str) -> str:
    """Достать номер версии из строки `--version`, если он там есть."""
    match = VERSION_RE.search(output)
    return match.group(0) if match else ""


def parse_readme(path: Path) -> list[dict]:
    """Вернуть пункты каталога README: раздел, имя, ссылка, описание."""
    entries: list[dict] = []
    section: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        heading = SECTION_RE.match(line)
        if heading:
            section = heading.group("name").strip()
            continue
        if line.startswith("## ") and not line.startswith("### "):
            section = None
            continue
        bullet = BULLET_RE.match(line)
        if bullet and section:
            entries.append(
                {
                    "section": section,
                    "display": bullet.group("display").strip(),
                    "url": bullet.group("url").strip(),
                    "purpose": bullet.group("desc").strip(),
                }
            )
    return entries


def walk_role(node, role: str, out: list[dict]) -> None:
    """Найти в defaults роли словари с name и источником установки."""
    if isinstance(node, dict):
        name = node.get("name")
        if isinstance(name, str) and name and (
            "repo" in node or "url" in node or "source" in node
        ):
            out.append(
                {
                    "name": name,
                    "repo": str(node.get("repo") or ""),
                    "role": role,
                }
            )
        for value in node.values():
            walk_role(value, role, out)
    elif isinstance(node, list):
        for value in node:
            walk_role(value, role, out)


def parse_roles(root: Path) -> tuple[dict, dict]:
    """Вернуть индексы: repo -> запись и имя -> запись."""
    by_repo: dict[str, dict] = {}
    by_name: dict[str, dict] = {}
    for defaults in sorted(root.glob("roles/*/defaults/*.yml")):
        role = defaults.parent.parent.name
        try:
            data = yaml.safe_load(defaults.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            sys.stderr.write(f"toolbox: {defaults}: {exc}\n")
            continue
        found: list[dict] = []
        walk_role(data, role, found)
        for item in found:
            if item["repo"]:
                by_repo.setdefault(item["repo"].lower(), item)
            by_name.setdefault(item["name"].lower(), item)
    return by_repo, by_name


def display_key(display: str) -> str:
    """Имя из README без markdown и уточнения в скобках."""
    text = display.replace("`", "").strip()
    text = re.sub(r"\s*\([^)]*\)\s*$", "", text).strip()
    return text


def load_report(path: Path) -> tuple[dict, set]:
    """Версии по имени бинарника и список установленных бинарников."""
    versions: dict[str, str] = {}
    installed: set[str] = set()
    if not path.exists():
        return versions, installed
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        sys.stderr.write(f"toolbox: {path}: {exc}\n")
        return versions, installed

    for tool in data.get("tools") or []:
        command = str(tool.get("command") or "")
        try:
            first = shlex.split(command)[0]
        except (ValueError, IndexError):
            first = command.split()[0] if command else ""
        binary = os.path.basename(first) if first else ""
        output = str(tool.get("output") or "").strip().splitlines()
        if binary and output:
            version = pick_version(output[0])
            if version:
                versions.setdefault(binary, version)
        if binary and tool.get("ok"):
            installed.add(binary)

    binaries = data.get("binaries")
    if isinstance(binaries, list):
        installed.update(item for item in binaries if isinstance(item, str))
    elif isinstance(binaries, dict):
        installed.update(value for value in binaries.values() if isinstance(value, str))
    return versions, installed


def build_catalog(
    entries: list[dict],
    root: Path,
    config: dict,
    report: Path,
) -> list[dict]:
    by_repo, by_name = parse_roles(root)
    versions, reported = load_report(report)

    domains = {item["id"]: item for item in config.get("toolbox_domains") or []}
    role_domains = config.get("toolbox_role_domains") or {}
    overrides = config.get("toolbox_overrides") or {}

    catalog: list[dict] = []
    seen: set[str] = set()
    for item in entries:
        repo_match = GITHUB_RE.match(item["url"])
        repo = repo_match.group("repo").lower() if repo_match else ""
        hit = by_repo.get(repo) if repo else None
        if hit is None:
            hit = by_name.get(display_key(item["display"]).lower())

        name = hit["name"] if hit else display_key(item["display"])
        role = hit["role"] if hit else item["section"]
        key = name.lower()

        override = overrides.get(key) or overrides.get(
            display_key(item["display"]).lower()
        ) or {}
        if override.get("skip"):
            continue

        binary = str(override.get("binary") or name)
        if name.lower() in seen:
            continue
        seen.add(name.lower())

        domain = str(override.get("domain") or role_domains.get(role) or "misc")
        domain_cfg = domains.get(domain, {"agent": True})
        agent = bool(override.get("agent", domain_cfg.get("agent", True)))

        path = shutil.which(binary)
        catalog.append(
            {
                "name": name,
                "binary": binary,
                "domain": domain,
                "role": role,
                "purpose": item["purpose"],
                "url": item["url"],
                "installed": bool(path) or binary in reported,
                "path": path or "",
                "version": versions.get(binary, ""),
                "agent": agent,
            }
        )

    catalog.sort(key=lambda row: (row["domain"], row["name"].lower()))
    return catalog


def commit_of(root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return "unknown"
    return result.stdout.strip() or "unknown"


def md_escape(text: str) -> str:
    return text.replace("|", r"\|").strip()


def render_index(
    config: dict,
    catalog: list[dict],
    domains: list[dict],
    meta: dict,
    outdir: Path,
) -> None:
    visible = [row for row in catalog if row["agent"]]
    counts = {domain["id"]: 0 for domain in domains}
    for row in visible:
        counts[row["domain"]] = counts.get(row["domain"], 0) + 1

    lines = [
        "# Инструменты на рабочей станции",
        "",
        f"Каталог собран плейбуком {meta['commit']} ({meta['generated_at']}).",
        "Руками не править: следующий прогон перезапишет файл.",
        "",
        "Полный машиночитаемый список:",
        "`~/.local/state/devops-playbook/toolbox.json`.",
        "Наличие проверяй через `command -v <binary>`, версия указана рядом.",
        "",
        "## Что использовать вместо дефолта",
        "",
        "| Задача | Инструмент | Вместо |",
        "| --- | --- | --- |",
    ]
    for row in config.get("toolbox_quick") or []:
        lines.append(
            "| {task} | {tool} | {instead} |".format(
                task=md_escape(str(row.get("task", ""))),
                tool=md_escape(str(row.get("tool", ""))),
                instead=md_escape(str(row.get("instead", ""))),
            )
        )

    lines += [
        "",
        "## Категории",
        "",
        "| Категория | Инструментов | Файл |",
        "| --- | --- | --- |",
    ]
    for domain in domains:
        if not domain.get("agent", True):
            continue
        count = counts.get(domain["id"], 0)
        if not count:
            continue
        lines.append(
            f"| {md_escape(domain['title'])} | {count} "
            f"| [tools/{domain['id']}.md](tools/{domain['id']}.md) |"
        )

    lines += [
        "",
        "## Запросы к каталогу",
        "",
        "```bash",
        "# по категории",
        "jq -r '.[] | select(.domain==\"observability\") "
        "| \"\\(.name) — \\(.purpose)\"' \\",
        "  ~/.local/state/devops-playbook/toolbox.json",
        "",
        "# поиск по назначению",
        "jq -r '.[] | select(.purpose|test(\"лог\"; \"i\")) "
        "| \"\\(.name) — \\(.purpose)\"' \\",
        "  ~/.local/state/devops-playbook/toolbox.json",
        "```",
        "",
    ]
    (outdir / "tools.md").write_text("\n".join(lines), encoding="utf-8")


def render_domains(
    catalog: list[dict],
    domains: list[dict],
    outdir: Path,
) -> None:
    tools_dir = outdir / "tools"
    tools_dir.mkdir(parents=True, exist_ok=True)
    for domain in domains:
        if not domain.get("agent", True):
            continue
        rows = [
            row
            for row in catalog
            if row["domain"] == domain["id"] and row["agent"]
        ]
        if not rows:
            continue
        lines = [
            f"# {domain['title']}",
            "",
            "[← Каталог](tools.md)",
            "",
            domain.get("description", ""),
            "",
        ]
        for row in rows:
            suffix = f" `{row['binary']}`"
            if row["version"]:
                suffix += f" · {row['version']}"
            lines.append(
                f"- [{row['name']}]({row['url']}) — {row['purpose']}{suffix}"
            )
        (tools_dir / f"{domain['id']}.md").write_text(
            "\n".join(lines) + "\n", encoding="utf-8"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="корень репозитория")
    parser.add_argument(
        "--vars",
        default="vars/toolbox.yml",
        help="файл с доменами и оверрайдами",
    )
    parser.add_argument(
        "--report",
        default="",
        help="report.json с версиями (пусто — не читать)",
    )
    parser.add_argument("--json", default="toolbox.json", help="куда писать JSON")
    parser.add_argument("--docs", default="docs", help="куда писать Markdown")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    config = yaml.safe_load((root / args.vars).read_text(encoding="utf-8")) or {}
    entries = parse_readme(root / "README.md")
    report = Path(args.report) if args.report else Path("/nonexistent")
    catalog = build_catalog(entries, root, config, report)

    meta = {
        "generated_at": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "commit": commit_of(root),
    }
    domains = config.get("toolbox_domains") or []
    payload = {
        "generated_at": meta["generated_at"],
        "playbook_commit": meta["commit"],
        "domains": domains,
        "tools": catalog,
    }

    json_path = Path(args.json)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    docs = Path(args.docs)
    docs.mkdir(parents=True, exist_ok=True)
    render_index(config, catalog, domains, meta, docs)
    render_domains(catalog, domains, docs)

    visible = [row for row in catalog if row["agent"]]
    counts: dict[str, int] = {}
    for row in visible:
        counts[row["domain"]] = counts.get(row["domain"], 0) + 1
    summary = ", ".join(f"{name}={count}" for name, count in sorted(counts.items()))
    missing = [row["name"] for row in visible if not row["installed"]]
    print(f"toolbox: {len(catalog)} записей, для агента {len(visible)} ({summary})")
    if missing:
        print(f"toolbox: не найдено бинарников: {len(missing)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
