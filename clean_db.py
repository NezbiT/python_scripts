import json

file_path = 'new.json'

def open_file():
    """Carga los datos desde un archivo JSON."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        print(f"✅ Archivo JSON cargado con éxito. Se encontraron {len(data)} registros.")
        return data
    except FileNotFoundError:
        print(f"❌ Error: El archivo '{file_path}' no fue encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"❌ Error: El archivo '{file_path}' no contiene un JSON válido.")
        return None

def find_users_with_phone():
    """
    Procesa todos los documentos, identifica aquellos sin el campo 'phone' 
    y los guarda en una lista.
    """
    all_documents = open_file()
    
    # 1. Inicializar la lista (arreglo) para guardar los documentos sin nombre
    new_id = []
    
    if all_documents:
        for document in all_documents:
            # Intentar obtener el nombre. Si no existe, .get() devuelve None.
            phone = document.get('phone')

            # 2. Comprobar la condición
            if phone is None:
                print('Empty User')
                # 3. Si no tiene nombre, añadir el documento COMPLETO a la lista
            else:
                new_id.append(document)

            
            # Opcional: También puedes imprimir un seguimiento mientras procesas
                # oid = document.get('_id', {}).get('$oid', 'ID no disponible')
                # print(f"Procesando ID: {oid}")

    print("-" * 50)
    print(f"Proceso finalizado.")
    print(f"Total de usuarios con datos: {len(new_id)}")
    print("-" * 50)
    
    # Devolver la lista con los documentos filtrados
    return new_id


# # --- Ejecutar el script ---
if __name__ == "__main__":
    users_list = find_users_with_phone()
    
    # Ejemplo de cómo ver el contenido de la nueva lista
    if users_list:
        print("\nPrimeros 5 documentos con phone number:")
        # Imprimir los primeros 5 elementos de la lista para verificación
        for i, user in enumerate(users_list[:5]):
            print(f"{i+1}. Documento: {user}")
            
        # Opcional: Guardar esta nueva lista en un archivo JSON
        with open('good_users.json', 'w', encoding='utf-8') as outfile:
            json.dump(users_list, outfile, ensure_ascii=False, indent=4)
        print(f"\nLista de {len(users_list)} documentos sin nombre guardada en 'good_users.json'")