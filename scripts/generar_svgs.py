"""Genera los SVG animados del perfil (paleta azul) en assets/."""
import sys
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "assets"
SANS = "'Segoe UI', Inter, 'Helvetica Neue', Arial, sans-serif"
MONO = "Consolas, 'SFMono-Regular', Menlo, 'Courier New', monospace"

# Las animaciones usan fill-mode "backwards": sin soporte de animación se ve el estado final.
BASE_CSS = f"""
    .sans {{ font-family: {SANS}; }}
    .mono {{ font-family: {MONO}; }}
    .in {{ animation: up .7s ease-out backwards; }}
    @keyframes up {{ from {{ opacity: 0; transform: translateY(12px); }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
"""

GRAD = """
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#050E24"/>
      <stop offset="0.6" stop-color="#0B2A6B"/>
      <stop offset="1" stop-color="#1D4ED8"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#60A5FA"/>
      <stop offset="1" stop-color="#22D3EE"/>
    </linearGradient>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="#93C5FD" stroke-opacity="0.08"/>
    </pattern>"""


def svg(name, w, h, label, defs, css, body):
    doc = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">
  <defs>{GRAD}{defs}
    <clipPath id="frame"><rect width="{w}" height="{h}" rx="18"/></clipPath>
  </defs>
  <style>{BASE_CSS}{css}  </style>
  <g clip-path="url(#frame)">
    <rect width="{w}" height="{h}" fill="url(#bg)"/>
    <rect width="{w}" height="{h}" fill="url(#grid)"/>
{body}
  </g>
</svg>
"""
    (OUT / f"{name}.svg").write_text(doc, encoding="utf-8")


def delay(i, step=0.12, start=0.1):
    return f'style="animation-delay:{start + i * step:.2f}s"'


# ───────────────────────── Títulos de sección ─────────────────────────
SECTIONS = [
    ("sec-sobre-mi", "01", "Sobre mí"),
    ("sec-proyectos", "02", "Proyectos en producción"),
    ("sec-tecnologias", "03", "Tecnologías"),
    ("sec-como-trabajo", "04", "Cómo trabajo"),
    ("sec-repos", "05", "Repositorios públicos"),
]
for name, num, title in SECTIONS:
    svg(name, 1200, 72, title,
        defs="""
    <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.16"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>""",
        css="""
    .shine { animation: sweep 6s ease-in-out infinite; }
    @keyframes sweep { 0% { transform: translateX(-320px); } 45%, 100% { transform: translateX(1520px); } }
    .line { transform-box: fill-box; transform-origin: left; animation: grow 1.1s .3s cubic-bezier(.2,.8,.2,1) backwards; }
    @keyframes grow { from { transform: scaleX(0); } }
""",
        body=f"""    <rect class="shine" x="0" y="0" width="260" height="72" fill="url(#shine)" transform="translate(-320 0)"/>
    <rect x="0" y="0" width="6" height="72" fill="url(#accent)"/>
    <text class="mono in" x="34" y="46" fill="#22D3EE" font-size="22" font-weight="700">{num}</text>
    <text class="sans in" x="80" y="46" fill="#FFFFFF" font-size="27" font-weight="700" style="animation-delay:.1s">{escape(title)}</text>
    <rect class="line" x="{80 + len(title) * 15 + 30}" y="35" width="{1200 - (80 + len(title) * 15 + 30) - 40}" height="2" rx="1" fill="url(#accent)" opacity=".55"/>""")


# ───────────────────────── Sobre mí (tarjeta de código) ─────────────────────────
K, S, V, P = "#C4B5FD", "#7DD3FC", "#E0ECFF", "#94A3B8"  # keyword, string, var, puntuación
CODE = [
    [("class ", K), ("LuisAcuna", "#FDE68A"), (":", P)],
    [("    rol         ", V), ("= ", P), ('"Desarrollador Full Stack"', S)],
    [("    empresa     ", V), ("= ", P), ('"TradeFood"', S)],
    [("    ubicacion   ", V), ("= ", P), ('"Lima, Perú"', S)],
    [("    formacion   ", V), ("= ", P), ('"Ing. de TI y Sistemas · Universidad ESAN (Beca 18)"', S)],
    [("    construyo   ", V), ("= ", P), ("[", P), ('"plataformas web"', S), (", ", P), ('"apps de escritorio"', S), (", ", P), ('"apps Android"', S), ("]", P)],
    [("    me_ocupo_de ", V), ("= ", P), ("[", P), ('"base de datos"', S), (", ", P), ('"backend"', S), (", ", P), ('"frontend"', S), (", ", P), ('"despliegue"', S), ("]", P)],
]
lines = []
for i, parts in enumerate(CODE):
    y = 100 + i * 34
    spans = "".join(f'<tspan fill="{c}">{escape(t)}</tspan>' for t, c in parts)
    lines.append(f'    <text class="in" x="0" y="{y}" {delay(i, .18, .3)}><tspan x="56" fill="#475569">{i + 1}</tspan><tspan x="96" xml:space="preserve">{spans}</tspan></text>')
last_len = sum(len(t) for t, _ in CODE[-1])
svg("sobre-mi", 1200, 380, "Sobre mí: Desarrollador Full Stack en TradeFood, Lima, Perú. Ingeniería de TI y Sistemas en la Universidad ESAN con Beca 18. Construyo plataformas web, apps de escritorio y apps Android.",
    defs="",
    css="""
    .code text { font-size: 20px; }
    .cursor { animation: blink 1s steps(1) infinite; }
    @keyframes blink { 50% { opacity: 0; } }
""",
    body=f"""    <rect x="0" y="0" width="1200" height="52" fill="#050E24" fill-opacity=".55"/>
    <circle cx="34" cy="26" r="7" fill="#F87171"/><circle cx="58" cy="26" r="7" fill="#FBBF24"/><circle cx="82" cy="26" r="7" fill="#34D399"/>
    <text class="mono" x="600" y="32" fill="#93C5FD" font-size="16" text-anchor="middle">luis_acuna.py</text>
    <g class="mono code">
{chr(10).join(lines)}
    </g>
    <rect class="cursor mono" x="{96 + last_len * 11 + 4}" y="{100 + 6 * 34 - 18}" width="11" height="22" fill="#22D3EE"/>
    <text class="mono" x="56" y="{100 + 7 * 34 + 12}" fill="#64748B" font-size="17"># contacto: linkedin.com/in/luis-acuna-dev · luisacudev@gmail.com</text>""")


# ───────────────────────── Cómo trabajo ─────────────────────────
ICONS = {
    "db": '<ellipse cx="0" cy="-9" rx="13" ry="5"/><path d="M-13 -9v18c0 2.8 5.8 5 13 5s13-2.2 13-5v-18M-13 0c0 2.8 5.8 5 13 5s13-2.2 13-5"/>',
    "test": '<path d="M-12 1l8 8 16-17"/>',
    "deploy": '<path d="M0 12V-12M-10 -2L0 -12L10 -2"/><path d="M-14 15H14"/>',
    "ai": '<path d="M0 -14C1.5 -4 4 -1.5 14 0C4 1.5 1.5 4 0 14C-1.5 4 -4 1.5 -14 0C-4 -1.5 -1.5 -4 0 -14Z"/>',
}
CARDS = [
    ("db", "Datos primero", ["Diseño la base de datos de cada sistema y", "versiono sus cambios con migraciones (Alembic)."]),
    ("test", "Pruebas automatizadas", ["Escribo pruebas con Pytest y Vitest y las", "ejecuto en integración continua (GitHub Actions)."]),
    ("deploy", "Despliegue propio", ["Despliego con Docker, Nginx y systemd en", "servidores Ubuntu, con respaldos automáticos."]),
    ("ai", "IA como apoyo", ["Uso agentes de IA (Claude Code, Codex) para", "agilizar el desarrollo, la revisión y las pruebas."]),
]
cards = []
for i, (icon, title, text) in enumerate(CARDS):
    cx, cy = 30 + (i % 2) * 580, 30 + (i // 2) * 150
    cards.append(f"""    <g class="in sans" {delay(i, .15, .1)}>
      <rect x="{cx}" y="{cy}" width="560" height="130" rx="14" fill="#050E24" fill-opacity=".45" stroke="#3B82F6" stroke-opacity=".45"/>
      <circle class="halo" cx="{cx + 52}" cy="{cy + 65}" r="30" fill="url(#accent)" fill-opacity=".14" stroke="url(#accent)" stroke-width="1.5" style="animation-delay:{i * .6:.1f}s"/>
      <g transform="translate({cx + 52} {cy + 65})" fill="none" stroke="#7DD3FC" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</g>
      <text x="{cx + 104}" y="{cy + 50}" fill="#FFFFFF" font-size="22" font-weight="700">{title}</text>
      <text fill="#C7D7F5" font-size="17"><tspan x="{cx + 104}" y="{cy + 80}">{escape(text[0])}</tspan><tspan x="{cx + 104}" y="{cy + 104}">{escape(text[1])}</tspan></text>
    </g>""")
svg("como-trabajo", 1200, 340, "Cómo trabajo: datos primero con migraciones Alembic; pruebas automatizadas con Pytest, Vitest y GitHub Actions; despliegue con Docker, Nginx y systemd en Ubuntu; IA como apoyo con Claude Code y Codex.",
    defs="",
    css="""
    .halo { transform-box: fill-box; transform-origin: center; animation: breathe 3s ease-in-out infinite; }
    @keyframes breathe { 50% { transform: scale(1.12); } }
""",
    body="\n".join(cards))


# ───────────────────────── Pie ─────────────────────────
def wave(amp, y, period=600, width=1800):
    d = f"M0 {y}"
    for x in range(0, width, period):
        d += f" C{x + period * .25} {y - amp} {x + period * .25} {y - amp} {x + period * .5} {y} S{x + period * .75} {y + amp} {x + period} {y}"
    return d + f" V200 H0 Z"


svg("footer", 1200, 190, "¿Tienes un proyecto en mente? Escríbeme a luisacudev@gmail.com",
    defs="",
    css="""
    .w1 { animation: slide 12s linear infinite; }
    .w2 { animation: slide 8s linear infinite reverse; }
    @keyframes slide { to { transform: translateX(-600px); } }
""",
    body=f"""    <path class="w1" d="{wave(14, 140)}" fill="#1D4ED8" fill-opacity=".55"/>
    <g transform="translate(-300 0)"><path class="w2" d="{wave(10, 156)}" fill="#3B82F6" fill-opacity=".45"/></g>
    <g class="sans" text-anchor="middle">
      <text class="in" x="600" y="64" fill="#FFFFFF" font-size="28" font-weight="700">¿Tienes un proyecto en mente?</text>
      <text class="in" x="600" y="100" fill="#93C5FD" font-size="19" style="animation-delay:.2s">Escríbeme a luisacudev@gmail.com</text>
    </g>""")

print("ok:", sorted(p.name for p in OUT.glob("*.svg")))
