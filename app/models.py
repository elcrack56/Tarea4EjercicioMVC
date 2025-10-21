from bson.objectid import ObjectId
from app.database import mongo

def get_all_vendedores():
    return list(mongo.db.vendedores.find())

def get_vendedor_by_id(vendedor_id):
    return mongo.db.vendedores.find_one({'_id': ObjectId(vendedor_id)})

def create_vendedor(data):
    return mongo.db.vendedores.insert_one(data)

def update_vendedor(vendedor_id, data):
    return mongo.db.vendedores.update_one({'_id': ObjectId(vendedor_id)}, {'$set': data})

def delete_vendedor(vendedor_id):
    return mongo.db.vendedores.delete_one({'_id': ObjectId(vendedor_id)})

def get_all_ventas():
    return list(mongo.db.ventas.find())

def get_ventas_by_vendedor_and_date_range(vendedor_id, start_date, end_date):
    return list(mongo.db.ventas.find({
        'vendedor_id': ObjectId(vendedor_id),
        'fecha_venta': {
            '$gte': start_date, 
            '$lte': end_date   
        }
    }).sort('fecha_venta', 1))

def create_venta(data):
    return mongo.db.ventas.insert_one(data)

def update_venta(venta_id, data):
    return mongo.db.ventas.update_one({'_id': ObjectId(venta_id)}, {'$set': data})

def delete_venta(venta_id):
    return mongo.db.ventas.delete_one({'_id': ObjectId(venta_id)})

def get_all_reglas_comision():
    return list(mongo.db.reglas_comision.find())

def get_active_reglas_comision(current_date):
    return list(mongo.db.reglas_comision.find({
        'fecha_inicio_vigencia': {'$lte': current_date},
        'fecha_fin_vigencia': {'$gte': current_date}
    }))

def create_regla_comision(data):
    return mongo.db.reglas_comision.insert_one(data)

def update_regla_comision(regla_id, data):
    return mongo.db.reglas_comision.update_one({'_id': ObjectId(regla_id)}, {'$set': data})

def delete_regla_comision(regla_id):
    return mongo.db.reglas_comision.delete_one({'_id': ObjectId(regla_id)})