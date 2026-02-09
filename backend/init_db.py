from .database import engine, SessionLocal
from . import models, auth

def init_db():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(models.User).count() == 0:
        print("Creating initial admin user...")
        hashed_password = auth.get_password_hash("admin123")
        admin_user = models.User(
            username="admin",
            email="admin@cinema.local",
            hashed_password=hashed_password,
            user_type="ADMIN"
        )
        db.add(admin_user)
        db.commit()
        print("Admin user created: admin / admin123")
    db.close()

if __name__ == "__main__":
    init_db()
