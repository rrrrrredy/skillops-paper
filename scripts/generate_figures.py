from __future__ import annotations

import html
import importlib.util
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FIGURES_DIR = REPO_ROOT / "figures"


@dataclass(frozen=True)
class Node:
    node_id: str
    x: float
    y: float
    width: float
    height: float
    lines: tuple[str, ...]
    fill: str = "#f8fafc"


@dataclass(frozen=True)
class Arrow:
    source: str
    target: str


@dataclass(frozen=True)
class Diagram:
    title: str
    width: int
    height: int
    nodes: tuple[Node, ...]
    arrows: tuple[Arrow, ...]


PALETTE = {
    "background": "#ffffff",
    "stroke": "#0f172a",
    "primary": "#dbeafe",
    "secondary": "#ecfccb",
    "accent": "#fae8ff",
    "muted": "#f8fafc",
}


def has_matplotlib() -> bool:
    return importlib.util.find_spec("matplotlib") is not None


def node_center(node: Node) -> tuple[float, float]:
    return (node.x + node.width / 2, node.y + node.height / 2)


def arrow_points(source: Node, target: Node) -> tuple[tuple[float, float], tuple[float, float]]:
    sx, sy = node_center(source)
    tx, ty = node_center(target)
    dx = tx - sx
    dy = ty - sy

    if abs(dx) >= abs(dy):
        start = (source.x + source.width, sy) if dx >= 0 else (source.x, sy)
        end = (target.x, ty) if dx >= 0 else (target.x + target.width, ty)
    else:
        start = (sx, source.y + source.height) if dy >= 0 else (sx, source.y)
        end = (tx, target.y) if dy >= 0 else (tx, target.y + target.height)
    return start, end


def svg_line(x1: float, y1: float, x2: float, y2: float) -> str:
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        'stroke="#0f172a" stroke-width="2.5" marker-end="url(#arrowhead)" />'
    )


def wrap_text_line(line: str) -> str:
    return html.escape(line, quote=True)


def render_svg(diagram: Diagram, output_path: Path) -> None:
    nodes_by_id = {node.node_id: node for node in diagram.nodes}
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{diagram.width}" '
            f'height="{diagram.height}" viewBox="0 0 {diagram.width} {diagram.height}">'
        ),
        '<defs>',
        '<marker id="arrowhead" markerWidth="10" markerHeight="7" refX="8" refY="3.5" orient="auto">',
        '<polygon points="0 0, 10 3.5, 0 7" fill="#0f172a" />',
        "</marker>",
        "</defs>",
        f'<rect width="{diagram.width}" height="{diagram.height}" fill="{PALETTE["background"]}" />',
        (
            f'<text x="{diagram.width / 2:.1f}" y="34" text-anchor="middle" '
            'font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="700" '
            'fill="#0f172a">'
            f"{wrap_text_line(diagram.title)}</text>"
        ),
    ]

    for arrow in diagram.arrows:
        source = nodes_by_id[arrow.source]
        target = nodes_by_id[arrow.target]
        (x1, y1), (x2, y2) = arrow_points(source, target)
        parts.append(svg_line(x1, y1, x2, y2))

    for node in diagram.nodes:
        parts.append(
            (
                f'<rect x="{node.x:.1f}" y="{node.y:.1f}" width="{node.width:.1f}" '
                f'height="{node.height:.1f}" rx="18" ry="18" fill="{node.fill}" '
                'stroke="#0f172a" stroke-width="2.2" />'
            )
        )
        line_height = 20
        block_height = line_height * len(node.lines)
        start_y = node.y + (node.height - block_height) / 2 + 14
        for index, line in enumerate(node.lines):
            parts.append(
                (
                    f'<text x="{node.x + node.width / 2:.1f}" y="{start_y + index * line_height:.1f}" '
                    'text-anchor="middle" font-family="Arial, Helvetica, sans-serif" '
                    'font-size="16" font-weight="600" fill="#0f172a">'
                    f"{wrap_text_line(line)}</text>"
                )
            )

    parts.append("</svg>")
    output_path.write_text("\n".join(parts) + "\n", encoding="utf-8")


def render_matplotlib(diagram: Diagram, output_path: Path) -> None:
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

    figure, axis = plt.subplots(figsize=(diagram.width / 120, diagram.height / 120), dpi=120)
    figure.patch.set_facecolor(PALETTE["background"])
    axis.set_xlim(0, diagram.width)
    axis.set_ylim(diagram.height, 0)
    axis.axis("off")
    axis.text(
        diagram.width / 2,
        28,
        diagram.title,
        ha="center",
        va="center",
        fontsize=18,
        fontweight="bold",
        color=PALETTE["stroke"],
    )

    nodes_by_id = {node.node_id: node for node in diagram.nodes}
    for arrow in diagram.arrows:
        source = nodes_by_id[arrow.source]
        target = nodes_by_id[arrow.target]
        (x1, y1), (x2, y2) = arrow_points(source, target)
        axis.add_patch(
            FancyArrowPatch(
                (x1, y1),
                (x2, y2),
                arrowstyle="-|>",
                mutation_scale=18,
                linewidth=2.2,
                color=PALETTE["stroke"],
            )
        )

    for node in diagram.nodes:
        axis.add_patch(
            FancyBboxPatch(
                (node.x, node.y),
                node.width,
                node.height,
                boxstyle="round,pad=0.02,rounding_size=16",
                linewidth=2.0,
                edgecolor=PALETTE["stroke"],
                facecolor=node.fill,
            )
        )
        line_height = 18
        start_y = node.y + node.height / 2 - ((len(node.lines) - 1) * line_height / 2)
        for index, line in enumerate(node.lines):
            axis.text(
                node.x + node.width / 2,
                start_y + index * line_height,
                line,
                ha="center",
                va="center",
                fontsize=12,
                fontweight="semibold",
                color=PALETTE["stroke"],
            )

    figure.tight_layout(pad=0.5)
    figure.savefig(output_path, bbox_inches="tight", facecolor=figure.get_facecolor())
    plt.close(figure)


def lifecycle_diagram() -> Diagram:
    labels = [
        ("design", ("design",), PALETTE["primary"]),
        ("lint", ("lint",), PALETTE["secondary"]),
        ("scan", ("security", "scan"), PALETTE["accent"]),
        ("inject", ("runtime", "injection"), PALETTE["primary"]),
        ("execute", ("execution",), PALETTE["secondary"]),
        ("audit", ("self-audit",), PALETTE["accent"]),
        ("update", ("update or", "forgetting"), PALETTE["primary"]),
    ]
    nodes = []
    start_x = 26
    y = 92
    width = 170
    height = 88
    gap = 18
    for index, (node_id, lines, fill) in enumerate(labels):
        nodes.append(Node(node_id, start_x + index * (width + gap), y, width, height, lines, fill))
    arrows = tuple(Arrow(labels[index][0], labels[index + 1][0]) for index in range(len(labels) - 1))
    return Diagram(
        title="SkillOps Lifecycle",
        width=1360,
        height=250,
        nodes=tuple(nodes),
        arrows=arrows,
    )


def skill_anatomy_diagram() -> Diagram:
    nodes = (
        Node("metadata", 70, 80, 220, 88, ("metadata",), PALETTE["primary"]),
        Node("trigger", 70, 200, 220, 88, ("trigger", "contract"), PALETTE["secondary"]),
        Node("instructions", 70, 320, 220, 88, ("instructions",), PALETTE["accent"]),
        Node("center", 440, 185, 320, 120, ("skill package", "SKILL.md + repo contract"), PALETTE["muted"]),
        Node("context", 910, 80, 220, 88, ("context", "boundary"), PALETTE["primary"]),
        Node("constraints", 910, 200, 220, 88, ("execution", "constraints"), PALETTE["secondary"]),
        Node("memory", 910, 320, 220, 88, ("memory", "interface"), PALETTE["accent"]),
        Node("tests", 360, 410, 180, 76, ("tests",), PALETTE["secondary"]),
        Node("security", 560, 410, 180, 76, ("security", "checks"), PALETTE["accent"]),
        Node("failure", 760, 410, 180, 76, ("failure", "modes"), PALETTE["primary"]),
    )
    arrows = (
        Arrow("metadata", "center"),
        Arrow("trigger", "center"),
        Arrow("instructions", "center"),
        Arrow("context", "center"),
        Arrow("constraints", "center"),
        Arrow("memory", "center"),
        Arrow("tests", "center"),
        Arrow("security", "center"),
        Arrow("failure", "center"),
    )
    return Diagram(
        title="Skill Anatomy",
        width=1200,
        height=540,
        nodes=nodes,
        arrows=arrows,
    )


def evaluation_pipeline_diagram() -> Diagram:
    labels = [
        ("inventory", ("artifact", "inventory"), PALETTE["primary"]),
        ("cases", ("manual", "benchmark cases"), PALETTE["secondary"]),
        ("scripts", ("scripts",), PALETTE["accent"]),
        ("tables", ("result tables",), PALETTE["primary"]),
        ("interpret", ("cautious", "interpretation"), PALETTE["secondary"]),
    ]
    nodes = []
    start_x = 70
    y = 105
    width = 200
    height = 96
    gap = 28
    for index, (node_id, lines, fill) in enumerate(labels):
        nodes.append(Node(node_id, start_x + index * (width + gap), y, width, height, lines, fill))
    arrows = tuple(Arrow(labels[index][0], labels[index + 1][0]) for index in range(len(labels) - 1))
    return Diagram(
        title="Evaluation Pipeline",
        width=1250,
        height=280,
        nodes=tuple(nodes),
        arrows=arrows,
    )


def diagram_specs() -> list[tuple[str, Diagram]]:
    return [
        ("skillops_lifecycle", lifecycle_diagram()),
        ("skill_anatomy", skill_anatomy_diagram()),
        ("evaluation_pipeline", evaluation_pipeline_diagram()),
    ]


def main() -> dict[str, object]:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    use_matplotlib = has_matplotlib()
    suffix = ".png" if use_matplotlib else ".svg"
    outputs = []
    for stem, diagram in diagram_specs():
        output_path = FIGURES_DIR / f"{stem}{suffix}"
        if use_matplotlib:
            render_matplotlib(diagram, output_path)
        else:
            render_svg(diagram, output_path)
        outputs.append(str(output_path))

    backend = "matplotlib" if use_matplotlib else "svg"
    print(f"Generated figures using {backend}:")
    for output in outputs:
        print(output)
    return {"outputs": outputs, "backend": backend}


if __name__ == "__main__":
    main()
