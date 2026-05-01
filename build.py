import json
from pathlib import Path
from html import escape


def render_context(p: dict[str, str]) -> str:
    parts = []

    ctx = p.get("context")
    if ctx == "personal":
        parts.append("Developed out of personal interest")
    elif ctx == "course" and p.get("course"):
        parts.append(f"Developed for the EPFL course <i>{escape(p['course'])}</i>")
    elif ctx == "semester":
        parts.append("Developed as an EPFL robotics semester project")

    if p.get("lab"):
        parts.append(f", conducted in the lab <i>{escape(p['lab'])}</i>")
    elif p.get("association"):
        parts.append(
            f", conducted in the student-led association <i>{escape(p['association'])}</i>"
        )

    collaborators = p.get("collaborators")
    if collaborators:
        if len(collaborators) == 1:
            names = escape(collaborators[0])
        else:
            names = f"{", ".join(escape(x) for x in collaborators[:-1])} and {escape(collaborators[-1])}"
        parts.append(f", with {names}")

    return "".join(parts)


def render_links(p: dict[str, str]) -> str:
    items = []
    for key, label in [
        ("repository", "GitHub"),
        ("video", "Video"),
        ("website", "Website"),
    ]:
        href = p.get(key)
        if href:
            items.append(
                f'<a href="{escape(href, quote=True)}" target="_blank" rel="noopener">{label}</a>'
            )
    return " ".join(items)


def main() -> None:
    root = Path(__file__).parent
    html = (root / "index.template.html").read_text(encoding="utf-8")
    projects = json.loads((root / "projects.json").read_text(encoding="utf-8"))

    projects_html = [f"""
    <article class="project">
      <img class="image" src="{escape(p.get('image', ''), quote=True)}" alt="{escape(p.get('title', '') + ' image') if p.get('title') else ''}">
      <h2 class="title">{escape(p.get('title', ''))}</h2>
      <p class="description">{escape(p.get('description', ''))}</p>
      <div class="context">{render_context(p)}</div>
      <div class="bottom-container">
        <div class="date">{escape(p.get('date', ''))}</div>
        <div class="links">{render_links(p)}</div>
      </div>
    </article>
    """ for p in projects]

    html = html.replace("{{PROJECTS}}", "".join(projects_html))
    (root / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
