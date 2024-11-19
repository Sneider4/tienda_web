from datetime import datetime
from app import db
import pytz

# Definir la zona horaria de Colombia
zona_horaria_colombia = pytz.timezone('America/Bogota')

# Función para obtener la fecha de creación
def obtener_hora_creacion():
    return datetime.utcnow().astimezone(zona_horaria_colombia)

# Función para obtener la fecha de modificación
def obtener_hora_modificacion():
    return datetime.utcnow().astimezone(zona_horaria_colombia)



class DireccionCliente(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    calle = db.Column(db.String(100), nullable=False)
    barrio = db.Column(db.String(100), nullable=False)
    municipio = db.Column(db.String(50), nullable=False)
    departamento= db.Column(db.String(50), nullable=False)
    pais = db.Column(db.String(50), default="Colombia")
    informacion_adicional = db.Column(db.String(200), nullable=True)
    destinatario =  db.Column(db.String(50), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=obtener_hora_creacion)
    fecha_modificacion = db.Column(db.DateTime, default=obtener_hora_creacion, onupdate=obtener_hora_modificacion)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "calle": self.calle,
            "barrio": self.barrio,
            "municipio": self.municipio,
            "departamento": self.departamento,
            "pais": self.pais,
            "informacion_adicional": self.informacion_adicional,
            "destinatario": self.destinatario,
            "fecha_creacion": self.fecha_creacion,
            "fecha_modificacion": self.fecha_modificacion
        }