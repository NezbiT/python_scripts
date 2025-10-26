from pathlib import Path
import json
from typing import List, Dict, Any

FILE_PATH = Path("test.json")
OUTPUT_PATH = Path("proccess_users.json")


def load_json_data(file_path: Path) -> List[Dict[str, Any]] | None:
    """Carga datos desde un archivo JSON.

    Args:
        file_path: Ruta al archivo JSON.

    Returns:
        Lista de documentos o None si hay un error.
    """
    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        print(f"✅ Cargado: {len(data)} registros")
        return data
    except FileNotFoundError:
        print(f"❌ Error: No se encontró '{file_path}'")
        return None
    except json.JSONDecodeError:
        print(f"❌ Error: '{file_path}' no es un JSON válido")
        return None


def process_users_with_phone(data: List[Dict[str, Any]]) -> tuple[List[Dict[str, Any]], List[str]]:
    """Procesa documentos con teléfono, actualizando nombres y rangos de edad.

    Args:
        data: Lista de documentos JSON.

    Returns:
        Tupla con lista de documentos con teléfono (modificados si name u over18 lo requieren) y lista de rangos válidos asignados.
    """
    users_with_phone = []
    valid_ranges_assigned = []

    for doc in data or []:
        if doc.get("phone") is not None:
            # Copiar documento para no modificar el original
            modified_doc = doc.copy()
            # Cambiar name a 'No nombre' si es un string vacío
            if modified_doc.get("name") == "":
                modified_doc["name"] = "No nombre"
            # Procesar over18
            over18 = modified_doc.get("over18")
            age_range = None
            if over18 == "Yes":
                age_range = "55+"
            elif over18 is not None:
                try:
                    age = int(over18)
                    if 17 < age < 26:
                        age_range = "18-25"
                    elif 25 < age < 36:
                        age_range = "26-35"
                    elif 35 < age < 46:
                        age_range = "36-45"
                    elif 45 < age < 56:
                        age_range = "46-55"
                    elif age >= 56 and age < 99:
                        age_range = "55+"
                except (ValueError, TypeError):
                    # No asignar si no es numérico ni "Yes"
                    pass

            if age_range:
                modified_doc["ageRange"] = age_range
                print(f"AgeRange asignado: {age_range}")
                valid_ranges_assigned.append(age_range)
            # Eliminar over18 (opcional)
            modified_doc.pop("over18", None)
            users_with_phone.append(modified_doc)  # Añadir solo una vez

    return users_with_phone, valid_ranges_assigned


def save_results(users_with_phone: List[Dict[str, Any]], output_path: Path) -> None:
    """Guarda los documentos con teléfono en un archivo JSON.

    Args:
        users_with_phone: Lista de documentos con teléfono.
        output_path: Ruta del archivo de salida.
    """
    with output_path.open("w", encoding="utf-8") as outfile:
        json.dump(users_with_phone, outfile, ensure_ascii=False, indent=4)
    print(f"✅ Guardado: {len(users_with_phone)} documentos en '{output_path}'")


def main():
    """Procesa el archivo JSON y guarda documentos con teléfono."""
    data = load_json_data(FILE_PATH)
    if not data:
        return

    users_with_phone, valid_ranges_assigned = process_users_with_phone(data)

    print(f"📱 Documentos con teléfono: {len(users_with_phone)}")
    print(f"🎯 Rangos válidos asignados: {valid_ranges_assigned}")
    if users_with_phone:
        print("\nPrimeros 5 documentos con teléfono:")
        for i, user in enumerate(users_with_phone[:5], 1):
            print(f"{i}. {user}")

    if users_with_phone:
        save_results(users_with_phone, OUTPUT_PATH)
    else:
        print("⚠️ No se encontraron documentos con teléfono")


if __name__ == "__main__":
    main()