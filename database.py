from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Session, joinedload

engine = create_engine('postgresql+psycopg2://kirill:123321@localhost/postgres')
SessionLocal = sessionmaker(autoflush=False, bind=engine)
engine.connect()

Base = declarative_base()

class Products(Base):
    __tablename__ = 'Товары'
    code = Column(Integer, primary_key=True, nullable=False, unique=True)
    product_attribute = relationship('ProductAttributes')
    name_product = relationship('NameProducts')


class ProductAttributes(Base):
    __tablename__ = 'Атрибуты товара'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True ,unique=True)
    product_id = Column(Integer, ForeignKey('Товары.code'), nullable=False)
    attribute = Column(String(100), nullable=False)
    value = Column(String(100), nullable=False)

    __table_args__ = (
        UniqueConstraint('product_id', 'attribute', name='uix_product_id_attribute'),
    )


class NameProducts(Base):
    __tablename__ = 'Название продукта'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    product_id = Column(Integer, ForeignKey('Товары.code'), nullable=False)
    language = Column(String(50), nullable=False)
    name_product = Column(String(100), nullable=False)

    __table_args__ = (
        UniqueConstraint('product_id', 'language', name='uix_product_id_language'),
    )
