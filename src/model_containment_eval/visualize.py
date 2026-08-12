from __future__ import annotations

from html import escape


def render_overview(report: dict) -> str:
    width, height = 1080, 590
    summaries = report["summary"]
    agents = report["agents"]
    by_key = {(item["agent"], item["control_profile"]): item for item in summaries}
    colors = {"attempt": "#f59e0b", "strict": "#22c55e", "audit": "#ef4444"}
    left, top = 230, 115
    plot_width = 700
    row_height = 88
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" rx="22" fill="#08111f"/>',
        '<text x="54" y="48" fill="#f8fafc" font-family="system-ui" font-size="25" font-weight="700">Containment evaluation overview</text>',
        '<text x="54" y="76" fill="#94a3b8" font-family="system-ui" font-size="13">Attempted policy violations versus simulated effects under strict and audit-only controls</text>',
    ]
    legend = [("Attempt rate", colors["attempt"]), ("Strict breach", colors["strict"]), ("Audit-only breach", colors["audit"])]
    for index, (label, color) in enumerate(legend):
        x = 610 + index * 145
        parts.extend([
            f'<rect x="{x}" y="35" width="12" height="12" rx="2" fill="{color}"/>',
            f'<text x="{x + 18}" y="46" fill="#cbd5e1" font-family="system-ui" font-size="12">{label}</text>',
        ])
    for tick in range(0, 101, 20):
        x = left + plot_width * tick / 100
        parts.append(f'<line x1="{x:.1f}" y1="{top - 20}" x2="{x:.1f}" y2="{top + row_height * len(agents) - 15}" stroke="#172033"/>')
        parts.append(f'<text x="{x:.1f}" y="{top - 30}" text-anchor="middle" fill="#64748b" font-family="system-ui" font-size="11">{tick}%</text>')
    for row, agent in enumerate(agents):
        y = top + row * row_height
        strict = by_key[(agent, "strict")]
        audit = by_key[(agent, "audit_only")]
        values = [
            (strict["violation_attempt_rate"], colors["attempt"]),
            (strict["simulated_breach_rate"], colors["strict"]),
            (audit["simulated_breach_rate"], colors["audit"]),
        ]
        parts.append(f'<text x="{left - 20}" y="{y + 30}" text-anchor="end" fill="#e2e8f0" font-family="system-ui" font-size="14" font-weight="600">{escape(agent)}</text>')
        for bar, (value, color) in enumerate(values):
            bar_y = y + bar * 18
            bar_width = max(value * plot_width, 1 if value else 0)
            parts.append(f'<rect x="{left}" y="{bar_y}" width="{bar_width:.1f}" height="12" rx="3" fill="{color}"/>')
            parts.append(f'<text x="{left + bar_width + 8:.1f}" y="{bar_y + 10}" fill="#cbd5e1" font-family="system-ui" font-size="11">{value:.0%}</text>')
    overall = report["overall"]
    parts.extend([
        f'<text x="54" y="530" fill="#94a3b8" font-family="system-ui" font-size="13">Strict containment integrity  <tspan fill="#22c55e" font-weight="700">{overall["strict_containment_integrity"]:.0%}</tspan></text>',
        f'<text x="365" y="530" fill="#94a3b8" font-family="system-ui" font-size="13">Monitor recall  <tspan fill="#8b5cf6" font-weight="700">{overall["monitor_recall"]:.0%}</tspan></text>',
        f'<text x="610" y="530" fill="#94a3b8" font-family="system-ui" font-size="13">Monitor false positives  <tspan fill="#38bdf8" font-weight="700">{overall["monitor_false_positive_rate"]:.0%}</tspan></text>',
        '<text x="54" y="565" fill="#64748b" font-family="system-ui" font-size="11">Synthetic results only · no host, shell, credential, or network access exists in the environment</text>',
        '</svg>',
    ])
    return "\n".join(parts)
