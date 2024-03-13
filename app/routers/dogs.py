from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..dependencies import get_db
from .. import schemas
from .. import crud

router = APIRouter(
    prefix="/dogs",
    tags=["dogs"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.Dog])
def read_dogs(db: Session = Depends(get_db)):
    dogs = crud.get_dogs(db)
    print("dogs:", dogs)
    return dogs


@router.get("/{dog_id}", response_model=schemas.Dog)
def get_dog_by_id(dog_id: int, db: Session = Depends(get_db)):
    dogs = crud.get_dog(db, dog_id)
    return dogs


@router.post("/{user_id}/dogs/", response_model=schemas.Dog)
def create_dog_for_user(
    user_id: int, dog: schemas.DogCreate, db: Session = Depends(get_db)
):
    return crud.create_user_dog(db=db, dog=dog, user_id=user_id)


@router.put("/{dog_id}", response_model=schemas.Dog)
def update_dog(dog_id: int, dog: schemas.DogBase, db: Session = Depends(get_db)):
    dog = crud.put_dog(db, dog_id, dog)
    return dog


@router.delete("/{dog_id}")
def delete_dog(dog_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_dog(db, dog_id)

    if deleted:
        return {"detail": "Dog deleted"}

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Dog does not exist")
