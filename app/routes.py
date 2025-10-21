from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database import mongo
from app import models
from app.core.comisiones_service import comisiones_service
from datetime import datetime
from bson.objectid import ObjectId 

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    vendedores = models.get_all_vendedores()
    
    selected_vendedor_id = request.form.get('vendedor_id')
    fecha_inicio_str = request.form.get('fecha_inicio') or datetime.now().replace(day=1).strftime('%Y-%m-%d')
    fecha_fin_str = request.form.get('fecha_fin') or datetime.now().strftime('%Y-%m-%d')

    resultados = None

    if request.method == 'POST':
        if not selected_vendedor_id or not fecha_inicio_str or not fecha_fin_str:
            flash('Por favor, selecciona un vendedor y las fechas.', 'danger')
        else:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d')
                
                resultados = comisiones_service.calcular_comisiones_vendedor(
                    selected_vendedor_id, fecha_inicio, fecha_fin
                )
            except Exception as e:
                flash(f'Error al calcular comisiones: {e}', 'danger')

    return render_template(
        'index.html',
        vendedores=vendedores,
        selected_vendedor_id=selected_vendedor_id,
        fecha_inicio=fecha_inicio_str,
        fecha_fin=fecha_fin_str,
        resultados=resultados
    )

@bp.route('/vendedores')
def list_vendedores():
    vendedores = models.get_all_vendedores()
    return render_template('vendedores/list.html', vendedores=vendedores)

@bp.route('/vendedores/new', methods=['GET', 'POST'])
def new_vendedor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        models.create_vendedor({'nombre': nombre, 'email': email})
        flash('Vendedor añadido exitosamente!', 'success')
        return redirect(url_for('main.list_vendedores'))
    return render_template('vendedores/form.html')

@bp.route('/vendedores/edit/<id>', methods=['GET', 'POST'])
def edit_vendedor(id):
    vendedor = models.get_vendedor_by_id(id)
    if not vendedor:
        flash('Vendedor no encontrado.', 'danger')
        return redirect(url_for('main.list_vendedores'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        models.update_vendedor(id, {'nombre': nombre, 'email': email})
        flash('Vendedor actualizado exitosamente!', 'success')
        return redirect(url_for('main.list_vendedores'))
    return render_template('vendedores/form.html', vendedor=vendedor)

@bp.route('/vendedores/delete/<id>', methods=['POST'])
def delete_vendedor(id):
    models.delete_vendedor(id)
    flash('Vendedor eliminado exitosamente!', 'success')
    return redirect(url_for('main.list_vendedores'))

@bp.route('/ventas')
def list_ventas():
    ventas = models.get_all_ventas()
    ventas_con_nombres = []
    for venta in ventas:
        vendedor = models.get_vendedor_by_id(venta['vendedor_id'])
        venta['vendedor_nombre'] = vendedor['nombre'] if vendedor else 'Desconocido'
        ventas_con_nombres.append(venta)
    return render_template('ventas/list.html', ventas=ventas_con_nombres)

@bp.route('/ventas/new', methods=['GET', 'POST'])
def new_venta():
    vendedores = models.get_all_vendedores()
    if request.method == 'POST':
        vendedor_id = request.form['vendedor_id']
        monto = float(request.form['monto'])
        fecha_venta_str = request.form['fecha_venta']
        fecha_venta = datetime.strptime(fecha_venta_str, '%Y-%m-%d')
        
        models.create_venta({'vendedor_id': ObjectId(vendedor_id), 'monto': monto, 'fecha_venta': fecha_venta})
        flash('Venta añadida exitosamente!', 'success')
        return redirect(url_for('main.list_ventas'))
    return render_template('ventas/form.html', vendedores=vendedores)

@bp.route('/ventas/edit/<id>', methods=['GET', 'POST'])
def edit_venta(id):
    venta = mongo.db.ventas.find_one({'_id': ObjectId(id)})
    if not venta:
        flash('Venta no encontrada.', 'danger')
        return redirect(url_for('main.list_ventas'))

    vendedores = models.get_all_vendedores()

    if request.method == 'POST':
        vendedor_id = request.form['vendedor_id']
        monto = float(request.form['monto'])
        fecha_venta_str = request.form['fecha_venta']
        fecha_venta = datetime.strptime(fecha_venta_str, '%Y-%m-%d')
        
        models.update_venta(id, {'vendedor_id': ObjectId(vendedor_id), 'monto': monto, 'fecha_venta': fecha_venta})
        flash('Venta actualizada exitosamente!', 'success')
        return redirect(url_for('main.list_ventas'))
    
    venta['fecha_venta_str'] = venta['fecha_venta'].strftime('%Y-%m-%d')
    return render_template('ventas/form.html', venta=venta, vendedores=vendedores)

@bp.route('/ventas/delete/<id>', methods=['POST'])
def delete_venta(id):
    models.delete_venta(id)
    flash('Venta eliminada exitosamente!', 'success')
    return redirect(url_for('main.list_ventas'))


@bp.route('/reglas')
def list_reglas():
    reglas = models.get_all_reglas_comision()
    return render_template('reglas/list.html', reglas=reglas)

@bp.route('/reglas/new', methods=['GET', 'POST'])
def new_regla():
    if request.method == 'POST':
        nombre_regla = request.form['nombre_regla']
        umbral_ventas_min = float(request.form['umbral_ventas_min'])
        umbral_ventas_max = float(request.form['umbral_ventas_max'])
        porcentaje = float(request.form['porcentaje'])
        fecha_inicio_vigencia = datetime.strptime(request.form['fecha_inicio_vigencia'], '%Y-%m-%d')
        fecha_fin_vigencia = datetime.strptime(request.form['fecha_fin_vigencia'], '%Y-%m-%d')
        
        models.create_regla_comision({
            'nombre_regla': nombre_regla,
            'umbral_ventas_min': umbral_ventas_min,
            'umbral_ventas_max': umbral_ventas_max,
            'porcentaje': porcentaje,
            'fecha_inicio_vigencia': fecha_inicio_vigencia,
            'fecha_fin_vigencia': fecha_fin_vigencia
        })
        flash('Regla de comisión añadida exitosamente!', 'success')
        return redirect(url_for('main.list_reglas'))
    return render_template('reglas/form.html')

@bp.route('/reglas/edit/<id>', methods=['GET', 'POST'])
def edit_regla(id):
    regla = mongo.db.reglas_comision.find_one({'_id': ObjectId(id)})
    if not regla:
        flash('Regla de comisión no encontrada.', 'danger')
        return redirect(url_for('main.list_reglas'))

    if request.method == 'POST':
        nombre_regla = request.form['nombre_regla']
        umbral_ventas_min = float(request.form['umbral_ventas_min'])
        umbral_ventas_max = float(request.form['umbral_ventas_max'])
        porcentaje = float(request.form['porcentaje'])
        fecha_inicio_vigencia = datetime.strptime(request.form['fecha_inicio_vigencia'], '%Y-%m-%d')
        fecha_fin_vigencia = datetime.strptime(request.form['fecha_fin_vigencia'], '%Y-%m-%d')
        
        models.update_regla_comision(id, {
            'nombre_regla': nombre_regla,
            'umbral_ventas_min': umbral_ventas_min,
            'umbral_ventas_max': umbral_ventas_max,
            'porcentaje': porcentaje,
            'fecha_inicio_vigencia': fecha_inicio_vigencia,
            'fecha_fin_vigencia': fecha_fin_vigencia
        })
        flash('Regla de comisión actualizada exitosamente!', 'success')
        return redirect(url_for('main.list_reglas'))
    
    regla['fecha_inicio_vigencia_str'] = regla['fecha_inicio_vigencia'].strftime('%Y-%m-%d')
    regla['fecha_fin_vigencia_str'] = regla['fecha_fin_vigencia'].strftime('%Y-%m-%d')
    return render_template('reglas/form.html', regla=regla)

@bp.route('/reglas/delete/<id>', methods=['POST'])
def delete_regla(id):
    models.delete_regla(id)
    flash('Regla de comisión eliminada exitosamente!', 'success')
    return redirect(url_for('main.list_reglas'))