from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_from_directory
import os
from config import Config
from models import ProductoModel, InspeccionModel

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'dev-secret-key-change-in-production'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/formulario')
def formulario():
    productos = ProductoModel.get_all_productos()
    return render_template('formulario.html', productos=productos)

@app.route('/front1')
def front1():
    return render_template('front1.html')

@app.route('/front2')
def front2():
    return render_template('front2.html')

@app.route('/front3')
def front3():
    return render_template('front3.html')

@app.route('/descargar-documento')
def descargar_documento():
    directorio = os.path.join(app.root_path, 'static', 'documentos')
    return send_from_directory(directory=directorio, path='documento.pdf', as_attachment=True)

@app.route('/api/producto/<dun14>')
def obtener_producto(dun14):
    producto = ProductoModel.get_producto_by_dun14(dun14)
    if producto:
        return jsonify(producto)
    return jsonify({'error': 'Producto no encontrado'}), 404

@app.route('/guardar', methods=['POST'])
def guardar_inspeccion():
    try:
        datos_mapeados = InspeccionModel.mapear_datos_formulario(request.form)
        success, mensaje = InspeccionModel.guardar_inspeccion(datos_mapeados)
        
        if success:
            flash('✅ Inspección guardada correctamente', 'success')
        else:
            flash(f'❌ {mensaje}', 'error')
    except Exception as e:
        flash(f'❌ Error: {str(e)}', 'error')
    
    return redirect(url_for('formulario'))

@app.route('/api/test-connection')
def test_connection():
    try:
        productos = ProductoModel.get_all_productos()
        return jsonify({
            'status': 'success',
            'message': f'Productos encontrados: {len(productos)}'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
