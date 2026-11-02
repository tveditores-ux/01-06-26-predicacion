// EXPORTAR BIBLIOTECA DE SUNO
// 1) Abre https://suno.com/me con tu sesión iniciada.
// 2) Abre la consola del navegador (F12 → pestaña "Console").
// 3) Pega todo este código y presiona Enter.
// 4) Se descargará "suno_export.json" con todas tus canciones.
(async () => {
  const token = await window.Clerk.session.getToken();
  const all = [];
  for (let page = 0; page < 500; page++) {
    const r = await fetch(`https://studio-api.prod.suno.com/api/feed/v2?page=${page}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!r.ok) { console.warn("Parada en página", page, r.status); break; }
    const data = await r.json();
    const clips = Array.isArray(data) ? data : (data.clips || []);
    if (!clips.length) break;
    all.push(...clips);
    console.log(`Página ${page}: ${clips.length} (total ${all.length})`);
    await new Promise(res => setTimeout(res, 400));
  }
  const blob = new Blob([JSON.stringify(all, null, 2)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "suno_export.json";
  a.click();
  console.log(`Listo: ${all.length} canciones exportadas.`);
})();
