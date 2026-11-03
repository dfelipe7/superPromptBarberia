import os
import shutil

BASE_DIR = os.path.dirname(__file__)
SECCIONES_DIR = os.path.join(BASE_DIR, 'secciones')
ROOT_DIR = os.path.join(BASE_DIR, '..')

BACKEND_DIR = os.path.abspath(os.path.join(ROOT_DIR, '..', 'Barberia-Backend'))
FRONTEND_DIR = os.path.abspath(os.path.join(ROOT_DIR, '..', 'Barberia-Frontend'))

# Destinos en superPromptBarberia
OUTPUT_MASTER = os.path.join(ROOT_DIR, 'SUPERPROMPT.md')
OUTPUT_BACKEND = os.path.join(ROOT_DIR, 'SUPERPROMPT_BACKEND.md')
OUTPUT_FRONTEND = os.path.join(ROOT_DIR, 'SUPERPROMPT_FRONTEND.md')

# Destinos en los respectivos repositorios
BACKEND_LOCAL_COPY = os.path.join(BACKEND_DIR, 'SUPERPROMPT_BACKEND.md')
FRONTEND_LOCAL_COPY = os.path.join(FRONTEND_DIR, 'SUPERPROMPT_FRONTEND.md')

SECCIONES_BACKEND = [
    '00-instrucciones-ia.md',
    '01-contexto-problema.md',
    '02-alcance.md',
    '03-roles-permisos.md',
    '04-stack-tecnologico.md',
    '05-arquitectura-patrones.md',
    '06-modelo-datos.md',
    '08-requisitos-no-funcionales.md',
    '09-api-contratos.md',
    '10-integraciones.md',
    '12-pruebas.md',
    '13-documentacion.md',
    '14-ia-responsable.md',
    '15-plan-ejecucion.md'
]

SECCIONES_FRONTEND = [
    '00-instrucciones-ia.md',
    '01-contexto-problema.md',
    '02-alcance.md',
    '03-roles-permisos.md',
    '04-stack-tecnologico.md',
    '05-arquitectura-patrones.md',
    '07-historias-usuario.md',
    '09-api-contratos.md',
    '11-ui-ux.md',
    '12-pruebas.md',
    '13-documentacion.md',
    '14-ia-responsable.md',
    '15-plan-ejecucion.md'
]

def compilar_archivo(titulo, subtitulo, archivos, ruta_destino):
    contenido = [
        f"# {titulo}\n",
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
        ruta = os.path.join(SECCIONES_DIR, arch)
        nombre_ancla = arch.replace('.md', '')
        if os.path.exists(ruta):
            with open(ruta, 'r', encoding='utf-8') as f:
                contenido.append(f"<a id=\"{nombre_ancla}\"></a>\n\n")
                contenido.append(f"<!-- ========================================================================= -->\n")
                contenido.append(f"<!-- SECCIÓN: {arch} -->\n")
                contenido.append(f"<!-- ========================================================================= -->\n\n")
                contenido.append(f.read().strip())
                contenido.append("\n\n---\n\n")
                
    with open(ruta_destino, 'w', encoding='utf-8') as f:
        f.writelines(contenido)
        
    print(f"[OK] Generado: {ruta_destino} ({len(archivos)} secciones)")

def main():
    if not os.path.exists(SECCIONES_DIR):
        print(f"❌ Error: El directorio no existe: {SECCIONES_DIR}")
        return

    todos = sorted([f for f in os.listdir(SECCIONES_DIR) if f.endswith('.md')])
    
    print("Compilando Superprompts...")
    # 1. Master Completo
    compilar_archivo(
        "SUPERPROMPT MAESTRO GLOBAL - KYRIOS BARBER SAAS",
        "Especificación maestra unificada (Full-Stack) compilada automáticamente a partir de superprompt/secciones/.",
        todos,
        OUTPUT_MASTER
    )
    
    # 2. Backend Especializado
    compilar_archivo(
        "SUPERPROMPT BACKEND - KYRIOS BARBER SAAS (NestJS + Prisma + MySQL)",
        "Especificación especializada para Backend, Base de Datos, Aislamiento de Inquilinos, Seguridad OWASP y Contratos de API.",
        SECCIONES_BACKEND,
        OUTPUT_BACKEND
    )
    
    # 3. Frontend Especializado
    compilar_archivo(
        "SUPERPROMPT FRONTEND - KYRIOS BARBER SAAS (React 19 + Vite + React Router)",
        "Especificación especializada para Frontend, Experiencia de Usuario (UI/UX), Enrutamiento /:slug, Theming Dinámico y Clientes HTTP.",
        SECCIONES_FRONTEND,
        OUTPUT_FRONTEND
    )
    
    # 4. Copiar a los repositorios respectivos si existen
    if os.path.exists(BACKEND_DIR):
        shutil.copyfile(OUTPUT_BACKEND, BACKEND_LOCAL_COPY)
        print(f"[OK] Copia sincronizada en: {BACKEND_LOCAL_COPY}")
        
    if os.path.exists(FRONTEND_DIR):
        shutil.copyfile(OUTPUT_FRONTEND, FRONTEND_LOCAL_COPY)
        print(f"[OK] Copia sincronizada en: {FRONTEND_LOCAL_COPY}")

if __name__ == '__main__':
    main()
