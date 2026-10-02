const express = require('express');
const { createClient } = require('@supabase/supabase-js');
const cors = require('cors');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_ANON_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

// Root Endpoint
app.get('/', (req, res) => {
  res.status(200).json({
    message: 'REST API Peminjaman Buku Perpustakaan - Praktikum PPB 2026',
    author: 'Nazkia Anugraha - Kelompok 31 - Shift 05',
    endpoints: {
      getAllOrFilterLoans: 'GET /loans (atau /loans?status=Terlambat)',
      createLoan: 'POST /loans',
      updateLoan: 'PUT /loans/:id',
      deleteLoan: 'DELETE /loans/:id'
    }
  });
});

// READ (Get All & Filter Query /loans?status=...)
app.get('/loans', async (req, res) => {
  try {
    let query = supabase.from('loans').select('*');
    const { status } = req.query;
    if (status) {
      query = query.eq('status', status);
    }
    const { data, error } = await query;
    if (error) throw error;
    res.status(200).json({
      success: true,
      message: 'Berhasil mengambil data peminjaman buku',
      count: data.length,
      data
    });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
});

// CREATE (Insert data peminjaman baru)
app.post('/loans', async (req, res) => {
  try {
    const { member_name, book_title, borrow_date, return_date, status } = req.body;
    if (!member_name || !book_title || !borrow_date || !return_date || !status) {
      return res.status(400).json({
        success: false,
        message: 'Semua field (member_name, book_title, borrow_date, return_date, status) wajib diisi!'
      });
    }
    const { data, error } = await supabase
      .from('loans')
      .insert([{ member_name, book_title, borrow_date, return_date, status }])
      .select();

    if (error) throw error;
    res.status(201).json({
      success: true,
      message: 'Data peminjaman berhasil ditambahkan',
      data: data[0]
    });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
});

// UPDATE (Mengubah data berdasarkan ID)
app.put('/loans/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { member_name, book_title, borrow_date, return_date, status } = req.body;
    const { data, error } = await supabase
      .from('loans')
      .update({ member_name, book_title, borrow_date, return_date, status })
      .eq('id', id)
      .select();

    if (error) throw error;
    if (!data || data.length === 0) {
      return res.status(404).json({ success: false, message: 'Data peminjaman tidak ditemukan' });
    }
    res.status(200).json({
      success: true,
      message: 'Data peminjaman berhasil diperbarui',
      data: data[0]
    });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
});

// DELETE (Menghapus data berdasarkan ID)
app.delete('/loans/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { data, error } = await supabase
      .from('loans')
      .delete()
      .eq('id', id)
      .select();

    if (error) throw error;
    if (!data || data.length === 0) {
      return res.status(404).json({ success: false, message: 'Data peminjaman tidak ditemukan' });
    }
    res.status(200).json({
      success: true,
      message: 'Data peminjaman berhasil dihapus',
      data: data[0]
    });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
});

app.listen(port, () => {
  console.log(`Server berjalan di port ${port}`);
});