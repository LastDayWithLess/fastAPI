from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse
from database import *
from BaseModelClasses import *

try:
    Base.metadata.create_all(engine)
    print("Таблицы успешно созданы.")
except Exception as e:
    print(f"Ошибка при создании таблиц: {e}")

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/add_product")
def create_item(prod: ProductCreate, db: Session = Depends(get_db)):
    try:
        db_prod = Products(code=prod.code)
        db.add(db_prod)
        db.commit()
        db.refresh(db_prod)
        return db_prod
    
    except Exception:
        return {'except': 'Значение уже есть в базе!'}    

@app.post("/add_name_product")
def create_item(nem: NameProductCreate, db: Session = Depends(get_db)):
    try:
        db_nem = NameProducts(product_id=nem.product_id, language=nem.language, name_product=nem.name_product)
        db.add(db_nem)
        db.commit()
        db.refresh(db_nem)
        return db_nem
    
    except Exception:
        return {'except': 'Значение не уникально!'}
    
@app.post("/add_product_attribute")
def create_item(prod_atr: ProductAttributeCreate, db: Session = Depends(get_db)):
    try:
        db_prod_atr = ProductAttributes(product_id=prod_atr.product_id, attribute=prod_atr.attribute, value=prod_atr.value)
        db.add(db_prod_atr)
        db.commit()
        db.refresh(db_prod_atr)
        return db_prod_atr
    
    except Exception:
        return {'except': 'Значение не уникально!'}

@app.get("/get_products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Products).options(
        joinedload(Products.product_attribute),
        joinedload(Products.name_product)
    ).all()

    return products

@app.put('/change_product_attribute/{attribute}')
def put_product_attribute(attribute: str, value: str, db: Session = Depends(get_db)):
    try:
        db_prod_atr = db.query(ProductAttributes).filter(ProductAttributes.attribute == attribute).first()

        if db_prod_atr == None: 
            return JSONResponse(status_code=404, content={ "message": "Атрибут не найден"})
    
        db_prod_atr.value = value
        db.commit()
        db.refresh(db_prod_atr)

        return db_prod_atr
    except Exception as e:
        return {"error": str(e)}
    
@app.put('/deleete_attribute')
def deleete_attribute(attribute_id: int, db: Session = Depends(get_db)):
    try:
        db_prod_atr = db.query(ProductAttributes).filter(ProductAttributes.id == attribute_id).first()

        if db_prod_atr == None: 
            return JSONResponse(status_code=404, content={ "message": "Атрибут не найден"})
    
        db.delete(db_prod_atr)
        db.commit()

        return db_prod_atr
    except Exception as e:
        return {"error": str(e)}