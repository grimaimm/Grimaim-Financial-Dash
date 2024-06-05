# -------------------------------------------------------------------------------------------------------------------

# Import modul-modul yang diperlukan
from models import db, User, Pengeluaran, Pemasukan, Kategori
from datetime import date, datetime, timedelta
from sqlalchemy.sql import func

# -------------------------------------------------------------------------------------------------------------------

# Fungsi Mendapatkan Total Pengeluaran dan Pemasukan Hari ini
def get_total_pengeluaran_pemasukan_hari_ini(user_id, date):
    total_pengeluaran_hari_ini = (
        Pengeluaran.query.filter(
            Pengeluaran.userID == user_id, Pengeluaran.tanggalPengeluaran == date
        )
        .with_entities(func.sum(Pengeluaran.jumlahPengeluaran))
        .scalar()
        or 0
    )

    total_pemasukan_hari_ini = (
        Pemasukan.query.filter(
            Pemasukan.userID == user_id, Pemasukan.tanggalPemasukan == date
        )
        .with_entities(func.sum(Pemasukan.jumlahPemasukan))
        .scalar()
        or 0
    )

    return total_pengeluaran_hari_ini, total_pemasukan_hari_ini


# -------------------------------------------------------------------------------------------------------------------

# Fungsi Mendapatkan Total Pengeluaran dan Pemasukan Minggu ini
def get_total_pengeluaran_pemasukan_mingguan(user_id, start_date, end_date):
    total_pengeluaran_mingguan = (
        Pengeluaran.query.filter(
            Pengeluaran.userID == user_id,
            Pengeluaran.tanggalPengeluaran.between(start_date, end_date),
        )
        .with_entities(func.sum(Pengeluaran.jumlahPengeluaran))
        .scalar()
        or 0
    )

    total_pemasukan_mingguan = (
        Pemasukan.query.filter(
            Pemasukan.userID == user_id,
            Pemasukan.tanggalPemasukan.between(start_date, end_date),
        )
        .with_entities(func.sum(Pemasukan.jumlahPemasukan))
        .scalar()
        or 0
    )

    return total_pengeluaran_mingguan, total_pemasukan_mingguan


# -------------------------------------------------------------------------------------------------------------------

# Fungsi Mendapatkan Total Pengeluaran dan Pemasukan Bulan ini
def get_total_pengeluaran_pemasukan_bulanan(user_id, year, month):
    first_day_of_month = date(year, month, 1)
    last_day_of_month = date(year, month + 1, 1) - timedelta(days=1)

    total_pengeluaran_bulanan = (
        Pengeluaran.query.filter(
            Pengeluaran.userID == user_id,
            Pengeluaran.tanggalPengeluaran.between(
                first_day_of_month, last_day_of_month
            ),
        )
        .with_entities(func.sum(Pengeluaran.jumlahPengeluaran))
        .scalar()
        or 0
    )

    total_pemasukan_bulanan = (
        Pemasukan.query.filter(
            Pemasukan.userID == user_id,
            Pemasukan.tanggalPemasukan.between(first_day_of_month, last_day_of_month),
        )
        .with_entities(func.sum(Pemasukan.jumlahPemasukan))
        .scalar()
        or 0
    )

    return total_pengeluaran_bulanan, total_pemasukan_bulanan


# -------------------------------------------------------------------------------------------------------------------

# Fungsi Mendapatkan Total Pengeluaran dan Pemasukan Tahun ini
def get_total_pengeluaran_pemasukan_tahunan(user_id, year):
    start_of_year = date(year, 1, 1)
    end_of_year = date(year, 12, 31)

    total_pengeluaran_tahunan = (
        Pengeluaran.query.filter(
            Pengeluaran.userID == user_id,
            Pengeluaran.tanggalPengeluaran >= start_of_year,
            Pengeluaran.tanggalPengeluaran <= end_of_year,
        )
        .with_entities(func.sum(Pengeluaran.jumlahPengeluaran))
        .scalar()
    )

    total_pemasukan_tahunan = (
        Pemasukan.query.filter(
            Pemasukan.userID == user_id,
            Pemasukan.tanggalPemasukan >= start_of_year,
            Pemasukan.tanggalPemasukan <= end_of_year,
        )
        .with_entities(func.sum(Pemasukan.jumlahPemasukan))
        .scalar()
    )

    return total_pengeluaran_tahunan or 0, total_pemasukan_tahunan or 0


# -------------------------------------------------------------------------------------------------------------------

# Fungsi Mendapatkan Total Pengeluaran dan Pemasukan USER
def get_total_transaksi(user_id):
    total_pemasukan = (
        Pemasukan.query.filter_by(userID=user_id)
        .with_entities(func.sum(Pemasukan.jumlahPemasukan))
        .scalar()
    )
    total_pengeluaran = (
        Pengeluaran.query.filter_by(userID=user_id)
        .with_entities(func.sum(Pengeluaran.jumlahPengeluaran))
        .scalar()
    )

    return total_pemasukan or 0, total_pengeluaran or 0


# -------------------------------------------------------------------------------------------------------------------

# Fungsi Mendapatkan Total Pengeluaran dan Pemasukan Tahun ini untuk di tampilkan di CHART.JS
def get_monthly_data(user_id, year):
    monthly_data = []

    for month in range(1, 13):
        start_date = f"{year}-{month:02d}-01"
        end_date = (
            (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=32))
            .replace(day=1)
            .strftime("%Y-%m-%d")
        )

        total_pengeluaran = (
            db.session.query(func.coalesce(func.sum(Pengeluaran.jumlahPengeluaran), 0))
            .filter(
                Pengeluaran.userID == user_id,
                Pengeluaran.tanggalPengeluaran.between(start_date, end_date),
            )
            .scalar()
        )

        total_pemasukan = (
            db.session.query(func.coalesce(func.sum(Pemasukan.jumlahPemasukan), 0))
            .filter(
                Pemasukan.userID == user_id,
                Pemasukan.tanggalPemasukan.between(start_date, end_date),
            )
            .scalar()
        )

        monthly_data.append(
            {
                "month": month,
                "total_pengeluaran": total_pengeluaran,
                "total_pemasukan": total_pemasukan,
            }
        )

    return monthly_data


# -------------------------------------------------------------------------------------------------------------------
