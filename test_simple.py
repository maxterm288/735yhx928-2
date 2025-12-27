# test_simple.py
import sys
sys.path.append('.')

from models import Database, ProductoModel

print("=" * 50)
print("TEST DE CONEXIÓN A POSTGRESQL AIVEN")
print("=" * 50)

# Test 1: Conexión a la base de datos
print("\n1. Probando conexión...")
conn = Database.get_connection()
if conn:
    print("✅ Conexión exitosa a PostgreSQL Aiven")
else:
    print("❌ Error de conexión")
    exit(1)

# Test 2: Obtener productos
print("\n2. Obteniendo productos de Hoja1...")
productos = ProductoModel.get_all_productos()
if productos:
    print(f"✅ Productos encontrados: {len(productos)}")
    print("\nPrimeros 3 productos:")
    for i, p in enumerate(productos[:3], 1):
        print(f"  {i}. {p['nombre_producto'][:50]}...")
        print(f"     DUN14: {p['dun14']}")
        print(f"     Código barras: {p['codigo_barra']}")
else:
    print("❌ No se encontraron productos")

# Test 3: Probar estructura de tabla Respuestas
try:
    print("\n3. Verificando estructura de Respuestas_de_formulario_1...")
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) as total_columnas 
        FROM information_schema.columns 
        WHERE table_name = 'respuestas_de_formulario_1'
    """)
    total_columnas = cur.fetchone()[0]
    print(f"✅ La tabla tiene {total_columnas} columnas")
    
    if total_columnas < 36:
        print(f"⚠️  Advertencia: Se esperaban 36 columnas, se encontraron {total_columnas}")
    
    cur.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'respuestas_de_formulario_1' 
        ORDER BY ordinal_position
        LIMIT 5
    """)
    primeras_columnas = cur.fetchall()
    print("\nPrimeras 5 columnas:")
    for col in primeras_columnas:
        print(f"  - {col[0]} ({col[1]})")
    
    cur.close()
    
except Exception as e:
    print(f"❌ Error al verificar estructura: {e}")

finally:
    if conn:
        conn.close()
        print("\n✅ Conexión cerrada correctamente")

print("\n" + "=" * 50)
print("TEST COMPLETADO")
print("=" * 50)
