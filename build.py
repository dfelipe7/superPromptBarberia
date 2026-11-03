import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

BACKEND_DIR = os.path.join(ROOT_DIR, 'backend')
BACKEND_SECCIONES = os.path.join(BACKEND_DIR, 'secciones')
BACKEND_OUTPUT = os.path.join(BACKEND_DIR, 'SUPERPROMPT_BACKEND.md')

FRONTEND_DIR = os.path.join(ROOT_DIR, 'frontend')
FRONTEND_SECCIONES = os.path.join(FRONTEND_DIR, 'secciones')
FRONTEND_OUTPUT = os.path.join(FRONTEND_DIR, 'SUPERPROMPT_FRONTEND.md')

MASTER_OUTPUT = os.path.join(ROOT_DIR, 'SUPERPROMPT.md')

def compilar_directorio(titulo, subtitulo, secciones_dir, salida):
    if not os.path.exists(secciones_dir):
        print(f"❌ Directorio no encontrado: {secciones_dir}")
        return

    archivos = sorted([f for f in os.listdir(secciones_dir) if f.endswith('.md')])
    
    contenido = [
        f"# {titulo}\n\n",
        f"> **{subtitulo}**\n\n",
        "> **ESTADO DE LA ESPECIFICACIÓN: ESPECIFICACIÓN VIVA (LIVING SPECIFICATION)**\n",
        "> Este documento representa con fidelidad milimétrica el estado del sistema hasta la fase actual y continúa evolucionando activamente a medida que se completan los hitos del roadmap y las siguientes fases de desarrollo.\n\n",
        "> - **🟢 Sprint 1 (Cimientos & Auth):** 100% Completado y Certificado.\n",
        "> - **🟢 Fase Multitenant Core & Temas:** 100% Completado, Migrado y Desplegado.\n",
        "> - **🟡 Sprint 2 (Citas, Horarios & OWASP):** ~85% Consolidado (En curso).\n",
        "> - **⚪ Sprint 3 (Pagos, Comisiones & Switcher):** Planificado / Backlog futuro incremental.\n\n",
        "## Índice de Contenidos\n\n"
    ]
    
    for arch in archivos:
        num = arch.split('-')[0]
        nombre_seccion = arch.replace('.md', '')
        partes = nombre_seccion.split('-')[1:]
        tit_sec = ' '.join(p.capitalize() for p in partes)
        contenido.append(f"- [{num}. {tit_sec}](#{nombre_seccion})\n")
        
    contenido.append("\n---\n\n")
    
    for arch in archivos:
        ruta = os.path.join(secciones_dir, arch)
        nombre_ancla = arch.replace('.md', '')
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido.append(f"<a id=\"{nombre_ancla}\"></a>\n\n")
            contenido.append(f"<!-- ========================================================================= -->\n")
            contenido.append(f"<!-- SECCIÓN: {arch} -->\n")
            contenido.append(f"<!-- ========================================================================= -->\n\n")
            contenido.append(f.read().strip())
            contenido.append("\n\n---\n\n")
            
    with open(salida, 'w', encoding='utf-8') as f:
        f.writelines(contenido)
        
    print(f"[OK] Generado: {salida} ({len(archivos)} secciones)")

def main():
    print("==================================================================")
    print("Compilando Superprompts Modulares en superPromptBarberia...")
    print("==================================================================")
    
    # 1. Backend
    compilar_directorio(
        "SUPERPROMPT BACKEND - KYRIOS BARBER SAAS",
        "Especificación especializada para Backend (NestJS 11 + Prisma ORM 7 + MySQL 8 + Seguridad OWASP).",
        BACKEND_SECCIONES,
        BACKEND_OUTPUT
    )
    
    # 2. Frontend
    compilar_directorio(
        "SUPERPROMPT FRONTEND - KYRIOS BARBER SAAS",
        "Especificación especializada para Frontend (React 19 + Vite 6 + React Router v7 + Temas Dinámicos).",
        FRONTEND_SECCIONES,
        FRONTEND_OUTPUT
    )
    
    # 3. Master unificado en la raíz
    legacy_secciones = os.path.join(ROOT_DIR, 'superprompt', 'secciones')
    if os.path.exists(legacy_secciones):
        compilar_directorio(
            "SUPERPROMPT MAESTRO GLOBAL - KYRIOS BARBER SAAS",
            "Especificación maestra unificada (Full-Stack) compilada a partir de las secciones base.",
            legacy_secciones,
            MASTER_OUTPUT
        )

if __name__ == '__main__':
    main()
