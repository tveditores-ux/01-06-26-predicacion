# Canciones de Suno

1. Abre https://suno.com/me (sesión iniciada), F12 → Console, pega `exportar_suno_consola.js`, Enter.
2. Se descarga `suno_export.json`. Súbelo aquí (o a esta carpeta).
3. `python3 organizar.py suno_export.json` crea `canciones/NNN-titulo-id/` con:
   - `info.md` — título, fecha, modelo, estilo, estilos excluidos, duración, enlaces, letra
   - `letra_prompt.txt` — la letra/prompt tal cual
   - `raw.json` — todos los datos originales de Suno
   un `indice.csv` con todas las canciones (abre en Excel/Sheets)
   y `reproductor.html`: ábrelo en el navegador para escuchar todas las canciones, buscar y ver letras.
