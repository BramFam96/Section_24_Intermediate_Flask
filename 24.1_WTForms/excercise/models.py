from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


def update_db(data):
  if type(data) is list:
    db.session.add_all(data);
    db.session.commit();
  else:
    db.session.add(data);
    db.session.commit();

def delete_data(data):
  db.session.delete(data);
  db.session.commit();


# MODELS GO BELOW!

dog_photo = 'https://images.pexels.com/photos/1805164/pexels-photo-1805164.jpeg?cs=srgb&dl=pexels-valeria-boltneva-1805164.jpg&fm=jpg'
cat_photo = 'https://images.pexels.com/photos/1741205/pexels-photo-1741205.jpeg?cs=srgb&dl=pexels-lina-kivaka-1741205.jpg&fm=jpg'
porc_photo = 'https://images.pexels.com/photos/2923830/pexels-photo-2923830.jpeg?cs=srgb&dl=pexels-egor-kamelev-2923830.jpg&fm=jpg'
class Pet(db.Model):
    """Pet Model"""

    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    species = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.Text)
    age = db.Column(db.Integer)
    notes = db.Column(db.Text)
    available = db.Column(db.Boolean, default = True)
    def photo(self):
        '''Picks default pictures based on species'''
        if self.photo_url:
            return self.photo_url            
        else:
            if self.species == 'dog': 
                return dog_photo;
            if self.species == 'cat':
                return cat_photo;
            else:
                return porc_photo;
    def check_status(self):
        '''Return adoption availability'''
        if self.available == True:
            return f'Available for Adoption'
        else: 
            return f'Currently unavailable'
        
    def __repr__(self):
        return f"<Pet {self.id}: {self.name}. {self.species} {self.available} >"


# class Employee(db.Model):
#     """Employee Model"""

#     __tablename__ = "employees"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.Text, nullable=False, unique=True)
#     state = db.Column(db.Text, nullable=False, default='CA')
#     dept_code = db.Column(db.Text, db.ForeignKey('departments.dept_code'))

#     # This is the magic line!
#     # Sets up a dept attribute on each instance of Employee.
#     # SQLA will populate it with data from the departments table automatically!
#     dept = db.relationship('Department', backref='employees')

#     assignments = db.relationship('EmployeeProject', backref='employee')

#     projects = db.relationship(
#         'Project', secondary="employees_projects", backref="employees")

#     def __repr__(self):
#         return f"<Employee {self.name} {self.state} {self.dept_code} >"


# class Project(db.Model):

#     __tablename__ = 'projects'

#     proj_code = db.Column(db.Text, primary_key=True)
#     proj_name = db.Column(db.Text, nullable=False, unique=True)

#     assignments = db.relationship('EmployeeProject', backref="project")


# class EmployeeProject(db.Model):

#     __tablename__ = 'employees_projects'

#     emp_id = db.Column(db.Integer, db.ForeignKey(
#         'employees.id'), primary_key=True)

#     proj_code = db.Column(db.Text, db.ForeignKey(
#         'projects.proj_code'), primary_key=True)

#     role = db.Column(db.Text)


# def get_directory():
#     all_emps = Employee.query.all()

#     for emp in all_emps:
#         if emp.dept is not None:
#             print(emp.name, emp.dept.dept_name, emp.dept.phone)
#         else:
#             print(emp.name)


# def get_directory_join():
#     directory = db.session.query(
#         Employee.name, Department.dept_name, Department.phone).join(Department).all()

#     for name, dept, phone in directory:
#         print(name, dept, phone)


# def get_directory_join_class():
#     directory = db.session.query(Employee, Department).join(Department).all()

#     for emp, dept in directory:
#         print(emp.name, dept.dept_name, dept.phone)


# def get_directory_all_join():
#     directory = db.session.query(
#         Employee.name, Department.dept_name, Department.phone).outerjoin(Department).all()

#     for name, dept, phone in directory:
#         print(name, dept, phone)
