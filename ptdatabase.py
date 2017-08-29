from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Powertool(Base):
    __tablename__ = 'powertool'

    id = Column(Integer, primary_key=True)
    brand = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    powertool_item = relationship('PowertoolItem', cascade='all, delete-orphan')

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'brand': self.brand,
            'id': self.id,
        }


class PowertoolItem(Base):
    __tablename__ = 'powertool_item'

    model = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    category = Column(String(250))  
    powertool_id = Column(Integer, ForeignKey('powertool.id'))
    powertool = relationship(Powertool)    
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'model': self.model,
            'description': self.description,
            'id': self.id,
            'price': self.price,            
            'category': self.category,
        }


engine = create_engine('postgresql://catalog:password@localhost/catalog')  
Base.metadata.create_all(engine)

