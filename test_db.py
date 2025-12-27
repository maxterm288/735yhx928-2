# test_db.py
from models import Database, ProductoModel

def test_connection():
    print("Probando conexión a la base de datos...")
    
    # Probar conexión
    conn = Database.get_connection()
    if conn:
        print("✅ Conexión exitosa a PostgreSQL Aiven")
        
        # Probar obtener productos
        productos = ProductoModel.get_all_productos()
        print(f"✅ Productos encontrados: {len(productos)}")
        
        # Probar estructura de tabla Respuestas
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'respuestas_de_formulario_1' 
                ORDER BY ordinal_position
            """)
            columnas = cur.fetchall()
            print(f"\n✅ Estructura de Respuestas_de_formulario_1 ({len(columnas)} columnas):")
            for i, col in enumerate(columnas, 1):
                print(f"  Column_{i}: {col[0]} ({col[1]})")
            
            cur.close()
        except Exception as e:
            print(f"❌ Error al leer estructura: {e}")
        
        conn.close()
    else:
        print("❌ Error de conexión")

if __name__ == "__main__":
    test_connection() 
