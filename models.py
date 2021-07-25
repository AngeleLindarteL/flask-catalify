from app import db

class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    descripcion = db.Column(db.String(2500), nullable=False)
    imglink = db.Column(db.String(3000), nullable=False)

    def __str__(self):
        return f'ID: {self.id} | Titulo: {self.title} | Descripcion: {self.descripcion} | imglink: {self.imglink}'