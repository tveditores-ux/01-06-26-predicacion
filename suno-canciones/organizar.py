"""Convierte suno_export.json en una carpeta por canción.
Uso: python3 organizar.py suno_export.json
"""
import csv, json, re, sys, unicodedata
from pathlib import Path

def slug(s):
    s = unicodedata.normalize("NFKD", s or "sin-titulo").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()[:60] or "sin-titulo"

src = Path(sys.argv[1] if len(sys.argv) > 1 else "suno_export.json")
clips = json.loads(src.read_text(encoding="utf-8"))
out = Path(__file__).parent / "canciones"
out.mkdir(exist_ok=True)
clips.sort(key=lambda c: c.get("created_at") or "")
rows = []
for i, c in enumerate(clips, 1):
    m = c.get("metadata") or {}
    info = {
        "titulo": c.get("title") or "(sin título)",
        "id": c.get("id"),
        "fecha": c.get("created_at"),
        "modelo": c.get("model_name") or c.get("major_model_version"),
        "estilo_tags": m.get("tags"),
        "estilos_excluidos": m.get("negative_tags"),
        "descripcion_prompt": m.get("gpt_description_prompt"),
        "duracion_seg": m.get("duration"),
        "tipo": m.get("type"),
        "publica": c.get("is_public"),
        "reproducciones": c.get("play_count"),
        "likes": c.get("upvote_count"),
        "url": f"https://suno.com/song/{c.get('id')}",
        "audio": c.get("audio_url"),
        "video": c.get("video_url"),
        "portada": c.get("image_large_url") or c.get("image_url"),
    }
    letra = m.get("prompt") or ""
    d = out / f"{i:03d}-{slug(info['titulo'])}-{(c.get('id') or '')[:8]}"
    d.mkdir(exist_ok=True)
    (d / "letra_prompt.txt").write_text(letra, encoding="utf-8")
    (d / "raw.json").write_text(json.dumps(c, ensure_ascii=False, indent=2), encoding="utf-8")
    md = [f"# {info['titulo']}", ""]
    md += [f"- **{k.replace('_', ' ').capitalize()}:** {v}" for k, v in info.items() if k != "titulo" and v not in (None, "")]
    md += ["", "## Estilo (prompt de estilo)", "", info["estilo_tags"] or "—"]
    if info["descripcion_prompt"]:
        md += ["", "## Descripción (modo simple)", "", info["descripcion_prompt"]]
    md += ["", "## Letra / prompt", "", "```", letra, "```"]
    (d / "info.md").write_text("\n".join(md), encoding="utf-8")
    rows.append({"n": i, "carpeta": d.name, **info})
with open(out.parent / "indice.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else ["n"])
    w.writeheader(); w.writerows(rows)
print(f"{len(rows)} canciones organizadas en {out}")
