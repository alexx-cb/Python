from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite:///zaidin_gym.db"

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def get_session():
    return SessionLocal()


def init_db():
    from Database.models import (UsuarioModel, SocioModel, SocioPremiumModel,
                                  MonitorModel, ActividadModel, VotoModel,
                                  SocioActividadModel, MonitorEspecialidadModel)
    Base.metadata.create_all(bind=engine)