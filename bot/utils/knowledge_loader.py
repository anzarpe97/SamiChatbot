import json
import os

def load_knowledge():
    """
    Carga el archivo knowledge.json y retorna su contenido como un string formateado
    para ser incluido en el prompt del sistema.
    """
    knowledge_path = os.path.join(os.getcwd(), 'knowledge.json')
    
    if not os.path.exists(knowledge_path):
        return ""

    try:
        with open(knowledge_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Convertimos el diccionario en un formato legible para la IA
        knowledge_text = "Información importante sobre Anderson (Andi):\n"
        
        for category, items in data.items():
            knowledge_text += f"\n- {category.replace('_', ' ').capitalize()}:\n"
            for key, value in items.items():
                # Reemplazar guiones bajos por espacios para mejor lectura
                clean_key = key.replace('_', ' ')
                knowledge_text += f"  * {clean_key}: {value}\n"
                
        return knowledge_text
    except Exception as e:
        print(f"Error cargando el conocimiento: {e}")
        return ""
