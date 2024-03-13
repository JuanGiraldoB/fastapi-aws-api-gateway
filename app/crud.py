from sqlalchemy.orm import Session

from . import models, schemas

# User


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session):
    return db.query(models.User).all()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    user.password = user.password + "not_really_hashed"
    db_user = models.User(
        **user.model_dump(),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True

    return False


def put_user(db: Session, user_id: int, new_user: schemas.User) -> models.User:
    user = get_user(db, user_id)

    user.name = new_user.name
    user.email = new_user.email
    user.contact_info = new_user.contact_info

    db.commit()
    return user


def create_user_dog(db: Session, dog: schemas.DogCreate, user_id: int) -> models.Dog:
    db_dog = models.Dog(
        **dog.model_dump(),
        owner_id=user_id
    )

    db.add(db_dog)
    db.commit()
    db.refresh(db_dog)
    return db_dog


# Dog
def delete_dog(db: Session, dog_id: int):
    dog = db.query(models.Dog).filter(models.Dog.id == dog_id).first()
    if dog:
        db.delete(dog)
        db.commit()
        return True

    return False


def get_dog(db: Session, dog_id: int) -> models.Dog:
    return db.query(models.Dog).filter(models.Dog.id == dog_id).first()


def get_dogs(db: Session) -> list[models.Dog]:
    return db.query(models.Dog).all()


def put_dog(db: Session, dog_id: int, new_dog: schemas.Dog) -> models.Dog:
    dog = get_dog(db, dog_id)

    dog.breed = new_dog.breed
    dog.name = new_dog.name

    db.commit()
    return dog
