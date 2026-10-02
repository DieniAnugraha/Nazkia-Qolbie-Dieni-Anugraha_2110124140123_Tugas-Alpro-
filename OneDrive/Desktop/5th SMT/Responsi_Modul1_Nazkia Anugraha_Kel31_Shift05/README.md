#REST API Peminjaman Buku Perpustakaan

Backend REST API sederhana untuk pencatatan peminjaman buku perpustakaan menggunakan Node.js, Express, dan Supabase.

##Identitas
- Nama: Nazkia Qolbie Dieni Anugraha
- NIM : 21120124140123
- Kelompok: 31
- Shift: 05

##Tech Stack
- Node.js
- Express.js
- Supabase (PostgreSQL)
- Vercel

##Struktur Tabel (loans)
- id (UUID, Primary Key)
- member_name (TEXT)
- book_title (TEXT)
- borrow_date (DATE)
- return_date (DATE)
- status (TEXT: Dipinjam / Dikembalikan / Terlambat)

##Cara Jalankan Lokal
1. Clone repo ini
2. Jalankan `npm install`
3. Buat file `.env` di root folder:
   ```env
   PORT=3000
   SUPABASE_URL=https://jqhxifnmkkzzcvczfvnn.supabase.co/rest/v1/
   SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpxaHhpZm5ta2t6emN2Y3pmdm5uIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTA5MzAzODEsImV4cCI6MjEwNjUwNjM4MX0.NXPfqi23aMbvDbOTsCTMcHDNEMoE_GKwRQ14h3KoClQ
