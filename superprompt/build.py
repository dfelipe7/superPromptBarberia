import os

SECCIONES_DIR = os.path.join(os.path.dirname(__file__), 'secciones')
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), '..', 'SUPERPROMPT.md')

def compilar_superprompt():
    if not os.path.exists(SECCIONES_DIR):
        print(f"❌ Error: El directorio de secciones no existe: {SECCIONES_DIR}")
        return

    archivos = sorted([f for f in os.listdir(SECCIONES_DIR) if f.endswith('.md')])
    
    contenido_completo = [
        "# SUPERPROMPT - KYRIOS BARBER (KYRIOS STUDIO)\n",
        "> **Especificación maestra del sistema compilada automáticamente a partir de `prompt-master/superprompt/secciones/`. No editar directamente.**\n\n",
        "## Índice de Contenidos del Superprompt\n\n"
    ]
    
    # Generar índice interactivo con enlaces markdown
    for arch in archivos:
        num = arch.split('-')[0]
        nombre_seccion = arch.replace('.md', '')
        # Formatear título amigable
        partes = nombre_seccion.split('-')[1:]
        titulo = ' '.join(p.capitalize() for p in partes)
        contenido_completo.append(f"- [{num}. {titulo}](#{nombre_seccion})\n")
    
    contenido_completo.append("\n---\n\n")
    
    # Concatenar cada archivo en orden
    for arch in archivos:
        ruta = os.path.join(SECCIONES_DIR, arch)
        nombre_ancla = arch.replace('.md', '')
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido_completo.append(f"<a id=\"{nombre_ancla}\"></a>\n\n")
            contenido_completo.append(f"<!-- ========================================================================= -->\n")
            contenido_completo.append(f"<!-- SECCIÓN: {arch} -->\n")
            contenido_completo.append(f"<!-- ========================================================================= -->\n\n")
            contenido_completo.append(f.read().strip())
            contenido_completo.append("\n\n---\n\n")
            
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.writelines(contenido_completo)
        
    print(f"[OK] SUPERPROMPT.md generado exitosamente en: {OUTPUT_FILE}")
    print(f"[INFO] Secciones compiladas: {len(archivos)}")

if __name__ == '__main__':
    compilar_superprompt()
