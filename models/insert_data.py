# from app import db, Kategori
from models import db
from models import Kategori

def insert_data_function():
    # Check if data already exists in Kategori table
    if not Kategori.query.first():
        kategori_data = ["Biaya Tempat Tinggal", "Biaya Pendidikan", "Biaya Transportasi", "Biaya Kebutuhan Pribadi", "Biaya Kebutuhan Pangan", "Biaya Utilitas Rumah", "Biaya Utang Piutang", "Biaya Kesehatan", "Biaya Lainnya"]
        for name in kategori_data:
            new_kategori = Kategori(kategoriName=name)
            db.session.add(new_kategori)

    # Commit the changes
    db.session.commit()