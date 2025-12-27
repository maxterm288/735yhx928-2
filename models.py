import psycopg2
from config import Config
from datetime import datetime

class Database:
    @staticmethod
    def get_connection():
        try:
            conn = psycopg2.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                database=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                sslmode=Config.DB_SSLMODE
            )
            return conn
        except Exception as e:
            print(f"Error de conexión: {e}")
            return None

class ProductoModel:
    @staticmethod
    def get_all_productos():
        conn = Database.get_connection()
        if not conn:
            return []
        
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT 
                    Column_1 as nombre_producto,
                    Column_2 as dun14,
                    Column_3 as codigo_barra,
                    Column_4 as conteo_hojas,
                    Column_5 as peso_rollo,
                    Column_6 as micro_corte,
                    Column_7 as altura
                FROM Hoja1 
                WHERE Column_1 NOT LIKE 'A: Producto' 
                AND Column_1 != ''
                ORDER BY Column_1
            """)
            
            productos = []
            for row in cur.fetchall():
                productos.append({
                    'nombre_producto': row[0],
                    'dun14': row[1],
                    'codigo_barra': row[2],
                    'conteo_hojas': row[3],
                    'peso_rollo': row[4],
                    'micro_corte': row[5],
                    'altura': row[6]
                })
            
            cur.close()
            return productos
            
        except Exception as e:
            print(f"Error al obtener productos: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def get_producto_by_dun14(dun14):
        conn = Database.get_connection()
        if not conn:
            return None
        
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT 
                    Column_1 as nombre_producto,
                    Column_2 as dun14,
                    Column_3 as codigo_barra,
                    Column_4 as conteo_hojas,
                    Column_5 as peso_rollo,
                    Column_6 as micro_corte,
                    Column_7 as altura
                FROM Hoja1 
                WHERE Column_2 = %s
            """, (dun14,))
            
            row = cur.fetchone()
            cur.close()
            
            if row:
                return {
                    'nombre_producto': row[0],
                    'dun14': row[1],
                    'codigo_barra': row[2],
                    'conteo_hojas': row[3],
                    'peso_rollo': row[4],
                    'micro_corte': row[5],
                    'altura': row[6]
                }
            return None
            
        except Exception as e:
            print(f"Error al obtener producto: {e}")
            return None
        finally:
            if conn:
                conn.close()

class InspeccionModel:
    @staticmethod
    def mapear_datos_formulario(form_data):
        defectos = {
            'fardos_flojos': int(form_data.get('fardos_flojos', 0) or 0),
            'sellos_debiles': int(form_data.get('sellos_debiles', 0) or 0),
            'fardos_rotos': int(form_data.get('fardos_rotos', 0) or 0),
            'hojas_suel': int(form_data.get('fardos_con_rollos_con_hojas_sueltas', 0) or 0),
            'rollos_suc': int(form_data.get('fardos_con_rollos_sucios', 0) or 0),
            'rollos_gol': int(form_data.get('fardos_con_rollos_golpeados', 0) or 0),
            'tipo_gal': int(form_data.get('fardos_con_rollo_tipo_galleta', 0) or 0),
            'var_altura': int(form_data.get('fardos_con_rollos_con_variacion_altura', 0) or 0),
            'mal_corte': int(form_data.get('fardos_con_rollo_con_mal_corte', 0) or 0),
            'mala_trans': int(form_data.get('fardos_con_rollos_con_mala_transferencia', 0) or 0),
            'marcados': int(form_data.get('fardos_con_rollo_marcados', 0) or 0),
            'rasgados': int(form_data.get('fardos_con_rollos_rasgados', 0) or 0),
            'mala_impre': int(form_data.get('fardos_con_mala_impresion', 0) or 0)
        }
        
        total_defectos = sum(defectos.values())
        total_inspeccionados = int(form_data.get('total_inspeccionados', 0) or 0)
        
        calidad_impresion = form_data.get('calidad_impresion', '')
        resultado = 'ACEP'
        if calidad_impresion == 'rechazada' or total_defectos > 0:
            resultado = 'RECH'
        
        puntua = 100
        if total_inspeccionados > 0 and total_defectos > 0:
            porcentaje_aceptado = ((total_inspeccionados - total_defectos) / total_inspeccionados) * 100
            puntua = round(porcentaje_aceptado, 2)
        
        return {
            'column_1': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'column_2': form_data.get('producto', ''),
            'column_3': form_data.get('factura', ''),
            'column_4': form_data.get('fecha_fabricacion', ''),
            'column_5': form_data.get('fecha_inspeccion', ''),
            'column_6': form_data.get('transportista', ''),
            'column_7': form_data.get('referencia', ''),
            'column_8': form_data.get('dun14', ''),
            'column_9': form_data.get('codigo_barra', ''),
            'column_10': form_data.get('carga_asignada', ''),
            'column_11': form_data.get('cliente', ''),
            'column_12': form_data.get('calidad_impresion', ''),
            'column_13': form_data.get('conteo_hojas', ''),
            'column_14': form_data.get('peso_rollo', ''),
            'column_15': form_data.get('micro_corte', ''),
            'column_16': form_data.get('altura', ''),
            'column_17': str(defectos['fardos_flojos']),
            'column_18': str(defectos['sellos_debiles']),
            'column_19': str(defectos['fardos_rotos']),
            'column_20': str(defectos['hojas_suel']),
            'column_21': str(defectos['rollos_suc']),
            'column_22': str(defectos['rollos_gol']),
            'column_23': str(defectos['tipo_gal']),
            'column_24': str(defectos['var_altura']),
            'column_25': str(defectos['mal_corte']),
            'column_26': str(defectos['mala_trans']),
            'column_27': str(defectos['marcados']),
            'column_28': str(defectos['rasgados']),
            'column_29': str(defectos['mala_impre']),
            'column_30': form_data.get('otros_defectos', ''),
            'column_31': str(total_inspeccionados),
            'column_32': form_data.get('observaciones', ''),
            'column_33': form_data.get('inspector', ''),
            'column_34': str(puntua),
            'column_35': str(total_defectos),
            'column_36': resultado
        }
    
    @staticmethod
    def guardar_inspeccion(datos_mapeados):
        conn = Database.get_connection()
        if not conn:
            return False, "Error de conexión"
        
        try:
            cur = conn.cursor()
            valores = []
            for i in range(1, 37):
                valores.append(datos_mapeados.get(f'column_{i}', ''))
            
            placeholders = ', '.join(['%s'] * 36)
            columnas = ', '.join([f'Column_{i}' for i in range(1, 37)])
            
            query = f"INSERT INTO Respuestas_de_formulario_1 ({columnas}) VALUES ({placeholders})"
            cur.execute(query, valores)
            conn.commit()
            cur.close()
            
            return True, "Inspección guardada"
            
        except Exception as e:
            conn.rollback()
            return False, f"Error: {str(e)}"
        finally:
            if conn:
                conn.close()
