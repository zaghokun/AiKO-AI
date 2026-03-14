Aku bakal rangkum perubahan terakhir secara jelas per file, fokus ke masalah utama yang tadi kita benerin: stabilitas render Live2D, centering, dan konflik DOM React vs canvas Pixi.

Read changed files in the active git repository

**Writeup Perubahan Terakhir (Frontend Chat + Live2D)**

Berikut yang baru saja diubah agar render karakter lebih stabil, center, dan tidak bentrok dengan React:

1. **Refactor layer karakter di halaman chat**
- File: page.tsx
- Update area karakter jadi floating style yang lebih besar dan lebih cocok dengan referensi Aethris.
- Posisi layer karakter diatur ulang ke center horizontal dengan top offset yang lebih konsisten.
- Ukuran viewport karakter dibesarkan agar full-body lebih mudah masuk frame.

2. **Refactor besar komponen Live2DCanvas**
- File: Live2DCanvas.tsx
- Tambah host canvas khusus (`canvasHostRef`) agar canvas Pixi dipasang di node terpisah.
- Hapus pola manipulasi root React yang berisiko (`innerHTML` di container utama).
- Mount/unmount canvas sekarang aman: child di-clear hanya pada host canvas, bukan root React.
- Resize logic dipindah ke root container supaya ukuran renderer selalu mengikuti viewport nyata.
- Auto-fit model diperbarui:
  - pakai bounds sumber yang immutable
  - hitung skala dari `usableWidth` dan `usableHeight`
  - center X dikunci
  - Y dikunci ke floor agar framing lebih stabil
- Animasi sway diperkecil agar tidak terlihat seperti drift posisi.

3. **Fix bug runtime yang ditarget**
- Error React DOM:
  - `Failed to execute 'removeChild' on 'Node': The node to be removed is not a child of this node.`
  - Teratasi dengan pemisahan node mount canvas dari node React children.
- Drift posisi saat refresh:
  - Dikurangi dengan relayout deterministic dan resize handling yang konsisten.
- Background hitam canvas:
  - tetap dipertahankan transparan melalui style dan opsi renderer.

4. **Status validasi**
- TypeScript error check: bersih untuk
  - Live2DCanvas.tsx
  - page.tsx

Kalau kamu mau, aku bisa lanjut bikin writeup versi “changelog commit” (format siap tempel ke PR/README) dalam 1 paragraf singkat + daftar fix.