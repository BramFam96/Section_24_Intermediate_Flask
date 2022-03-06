from app import app
from models import db, Pet, update_db

db.drop_all()
db.create_all()

Pet.query.delete();

jack = Pet(name="Jackson", species='dog', age=2)
jane = Pet(name="Jane", species='dog', age=4)
floppy = Pet(name="Floppy", species='dog', age=1)

pets = [jack,jane,floppy]

update_db(pets)