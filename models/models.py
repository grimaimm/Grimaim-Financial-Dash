# models.py
# -------------------------------------------------------------------------------------------------------------------

# Import modul-modul yang diperlukan
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

DEFAULT_IMAGE = "default-image.jpg"


# -------------------------------------------------------------------------------------------------------------------

# Membuat Class User untuk Tabel User
class User(db.Model, UserMixin):
    userID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    fullname = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    userPicture = db.Column(db.String(1000), nullable=False, default=DEFAULT_IMAGE)

    def __init__(self, username, fullname, password, userPicture=None):
        self.username = username
        self.fullname = fullname
        self.password = password
        if userPicture is not None:
            self.userPicture = userPicture

    def get_id(self):
        return self.userID

    def __repr__(self):
        return f"<User {self.username}>"


# -------------------------------------------------------------------------------------------------------------------

# Membuat Class Pengeluaran untuk Tabel Pengeluaran
class Pengeluaran(db.Model):
    pengeluaranID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer, db.ForeignKey("user.userID"), nullable=False)
    tanggalPengeluaran = db.Column(db.Date, nullable=False)
    deskripsiPengeluaran = db.Column(db.String(255), nullable=False)
    kategoriPengeluaran = db.Column(
        db.Integer, db.ForeignKey("kategori.kategoriID"), nullable=False
    )
    jumlahPengeluaran = db.Column(db.Float, nullable=False)

    kategori = db.relationship("Kategori", backref="pengeluaran", lazy=True)

    def __repr__(self):
        return f"<Pengeluaran {self.pengeluaranID}>"


# -------------------------------------------------------------------------------------------------------------------

# Membuat Class Pemasukan untuk Tabel Pemasukan
class Pemasukan(db.Model):
    pemasukanID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer, db.ForeignKey("user.userID"), nullable=False)
    tanggalPemasukan = db.Column(db.Date, nullable=False)
    deskripsiPemasukan = db.Column(db.String(255), nullable=False)
    jumlahPemasukan = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Pemasukan {self.pemasukanID}>"


# -------------------------------------------------------------------------------------------------------------------

# Membuat Class Kategori untuk Tabel Kategori
class Kategori(db.Model):
    kategoriID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kategoriName = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Kategori {self.kategoriName}>"
