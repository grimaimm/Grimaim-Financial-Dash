# -------------------------------------------------------------------------------------------------------------------

# Import modul-modul yang diperlukan
from models import db, User, Pengeluaran, Pemasukan, Kategori
from sqlalchemy import func
from flask_login import current_user

# -------------------------------------------------------------------------------------------------------------------

# Import modul-modul yang diperlukan
def get_unique_transaction_dates():
    unique_dates_pemasukan = (
        db.session.query(func.date(Pemasukan.tanggalPemasukan)).distinct().all()
    )
    unique_dates_pengeluaran = (
        db.session.query(func.date(Pengeluaran.tanggalPengeluaran)).distinct().all()
    )
    unique_dates = set(
        date[0] for date in unique_dates_pemasukan + unique_dates_pengeluaran
    )
    sorted_dates = sorted(unique_dates)
    return sorted_dates


# -------------------------------------------------------------------------------------------------------------------

# Fungsi untuk mendapatkan total pemasukan berdasarkan tanggal
def get_total_pemasukan_by_date(tanggal):
    pemasukan_by_date = Pemasukan.query.filter_by(
        tanggalPemasukan=tanggal, userID=current_user.userID
    ).all()
    return sum(item.jumlahPemasukan for item in pemasukan_by_date)


# -------------------------------------------------------------------------------------------------------------------

# Fungsi untuk mendapatkan total pengeluaran berdasarkan tanggal
def get_total_pengeluaran_by_date(tanggal):
    pengeluaran_by_date = Pengeluaran.query.filter_by(
        tanggalPengeluaran=tanggal, userID=current_user.userID
    ).all()
    return sum(item.jumlahPengeluaran for item in pengeluaran_by_date)


# -------------------------------------------------------------------------------------------------------------------

# Fungsi untuk mendapatkan semua Total Pengeluaran berdasarkan Kategori
def get_total_pengeluaran_by_kategori_semua(user_id):
    total_pengeluaran_by_kategori_semua = {}
    kategori_data = [
        "Biaya Tempat Tinggal",
        "Biaya Pendidikan",
        "Biaya Transportasi",
        "Biaya Kebutuhan Pribadi",
        "Biaya Kebutuhan Pangan",
        "Biaya Utilitas Rumah",
        "Biaya Utang Piutang",
        "Biaya Kesehatan",
        "Biaya Lainnya",
    ]
    for kategori_name in kategori_data:
        kategori = Kategori.query.filter_by(kategoriName=kategori_name).first()
        if kategori:
            kategori_id = kategori.kategoriID
            total_pengeluaran = (
                Pengeluaran.query.filter(
                    Pengeluaran.userID == user_id,
                    Pengeluaran.kategoriPengeluaran == kategori_id,
                )
                .with_entities(func.sum(Pengeluaran.jumlahPengeluaran))
                .scalar()
            )
            total_pengeluaran_by_kategori_semua[kategori_name] = total_pengeluaran or 0
    return total_pengeluaran_by_kategori_semua


# -------------------------------------------------------------------------------------------------------------------

# Fungsi untuk mendapatkan semua Total Pengeluaran Harian berdasarkan Kategori
def get_total_pengeluaran_by_kategori_harian(user_id, date=None):
    total_pengeluaran_by_kategori_harian = {}
    kategori_data = [
        "Biaya Tempat Tinggal",
        "Biaya Pendidikan",
        "Biaya Transportasi",
        "Biaya Kebutuhan Pribadi",
        "Biaya Kebutuhan Pangan",
        "Biaya Utilitas Rumah",
        "Biaya Utang Piutang",
        "Biaya Kesehatan",
        "Biaya Lainnya",
    ]
    for kategori_name in kategori_data:
        kategori = Kategori.query.filter_by(kategoriName=kategori_name).first()
        if kategori:
            kategori_id = kategori.kategoriID
            if date:
                total_pengeluaran = (
                    Pengeluaran.query.filter(
                        Pengeluaran.userID == user_id,
                        Pengeluaran.kategoriPengeluaran == kategori_id,
                        Pengeluaran.tanggalPengeluaran == date,
                    )
                    .with_entities(func.sum(Pengeluaran.jumlahPengeluaran))
                    .scalar()
                )
            else:
                total_pengeluaran = (
                    Pengeluaran.query.filter(
                        Pengeluaran.userID == user_id,
                        Pengeluaran.kategoriPengeluaran == kategori_id,
                    )
                    .with_entities(func.sum(Pengeluaran.jumlahPengeluaran))
                    .scalar()
                )
            total_pengeluaran_by_kategori_harian[kategori_name] = total_pengeluaran or 0
    return total_pengeluaran_by_kategori_harian


# -------------------------------------------------------------------------------------------------------------------

# Fungsi untuk mendapatkan semua Total Pengeluaran Mingguan berdasarkan Kategori
def get_total_pengeluaran_by_kategori_mingguan(user_id, start_date, end_date):
    total_pengeluaran_by_kategori_mingguan = {}
    kategori_data = [
        "Biaya Tempat Tinggal",
        "Biaya Pendidikan",
        "Biaya Transportasi",
        "Biaya Kebutuhan Pribadi",
        "Biaya Kebutuhan Pangan",
        "Biaya Utilitas Rumah",
        "Biaya Utang Piutang",
        "Biaya Kesehatan",
        "Biaya Lainnya",
    ]
    for kategori_name in kategori_data:
        kategori = Kategori.query.filter_by(kategoriName=kategori_name).first()
        if kategori:
            kategori_id = kategori.kategoriID
            total_pengeluaran = (
                Pengeluaran.query.filter(
                    Pengeluaran.userID == user_id,
                    Pengeluaran.kategoriPengeluaran == kategori_id,
                    Pengeluaran.tanggalPengeluaran.between(start_date, end_date),
                )
                .with_entities(func.sum(Pengeluaran.jumlahPengeluaran))
                .scalar()
            )
            total_pengeluaran_by_kategori_mingguan[kategori_name] = (
                total_pengeluaran or 0
            )
    return total_pengeluaran_by_kategori_mingguan


# -------------------------------------------------------------------------------------------------------------------

# Fungsi untuk mendapatkan semua Total Pengeluaran Bulanan berdasarkan Kategori
def get_total_pengeluaran_by_kategori_bulanan(user_id, start_date, end_date):
    total_pengeluaran_by_kategori_bulanan = {}
    kategori_data = [
        "Biaya Tempat Tinggal",
        "Biaya Pendidikan",
        "Biaya Transportasi",
        "Biaya Kebutuhan Pribadi",
        "Biaya Kebutuhan Pangan",
        "Biaya Utilitas Rumah",
        "Biaya Utang Piutang",
        "Biaya Kesehatan",
        "Biaya Lainnya",
    ]
    for kategori_name in kategori_data:
        kategori = Kategori.query.filter_by(kategoriName=kategori_name).first()
        if kategori:
            kategori_id = kategori.kategoriID
            total_pengeluaran = (
                Pengeluaran.query.filter(
                    Pengeluaran.userID == user_id,
                    Pengeluaran.kategoriPengeluaran == kategori_id,
                    Pengeluaran.tanggalPengeluaran.between(start_date, end_date),
                )
                .with_entities(func.sum(Pengeluaran.jumlahPengeluaran))
                .scalar()
            )
            total_pengeluaran_by_kategori_bulanan[kategori_name] = (
                total_pengeluaran or 0
            )
    return total_pengeluaran_by_kategori_bulanan


# -------------------------------------------------------------------------------------------------------------------
