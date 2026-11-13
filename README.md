# Plataforma SaaS Multitenant para Barberías — Superprompt Modular

Repositorio oficial de especificación de ingeniería y prompts ejecutables para la **Plataforma SaaS Multitenant de Gestión para Barberías** (con *Kyrios Barber* como inquilino piloto inicial).

Este repositorio alberga la arquitectura viva (*Living Architecture Specification*) y los prompts modulares optimizados para ser interpretados por agentes de Inteligencia Artificial (IA) o desarrolladores para la construcción, auditoría y evolución del sistema.

---

## 📁 Estructura del Repositorio

El repositorio está desacoplado por dominios técnicos para evitar sobrecarga de contexto en los modelos de lenguaje:

```
superPromptBarberia/
│
├── backend/                                <- Prompts especializados para Backend
│   ├── SUPERPROMPT_BACKEND.md              <- Archivo compilado de Backend listo para IA
│   └── secciones/                          <- 12 prompts modulares de Backend
│       ├── 00-instrucciones-ia.md          <- Directivas estrictas + Protocolo HITL
│       ├── 01-contexto-alcance.md          <- Contexto SaaS y roadmap vivo
│       ├── 02-roles-permisos-rbac.md       <- Membresías por sede y matriz RACI
│       ├── 03-stack-tecnologico.md         <- NestJS 11, Prisma 7, MySQL 8, Helmet
│       ├── 04-arquitectura-patrones.md     <- Tenant Isolation, Middleware X-Negocio-Slug
│       ├── 05-modelo-datos.md              <- El schema.prisma literal de 650 líneas
│       ├── 06-seguridad-owasp-logs.md      <- Winston rotativo, Fail-Closed, OWASP 2025
│       ├── 07-contratos-api-dtos.md        <- Endpoints y DTOs JSON canónicos
│       ├── 08-integraciones.md             <- Baileys WhatsApp, SMTP Mailer, Google Auth
│       ├── 09-pruebas.md                   <- Mocks y pruebas unitarias con Jest
│       ├── 10-ia-responsable-hitl.md       <- Gobernanza y compuertas de decisión crítica
│       └── 11-plan-ejecucion-bootstrap.md  <- Bootstrapping paso a paso del backend y BD
│
├── frontend/                               <- Prompts especializados para Frontend
│   ├── SUPERPROMPT_FRONTEND.md             <- Archivo compilado de Frontend listo para IA
│   └── secciones/                          <- 11 prompts modulares de Frontend
│       ├── 00-instrucciones-ia.md          <- Directivas estrictas + Protocolo HITL
│       ├── 01-contexto-alcance.md          <- Contexto SaaS y roadmap vivo
│       ├── 02-roles-sesiones-frontend.md   <- Aislamiento de tokens por pestaña y slug
│       ├── 03-stack-tecnologico.md         <- React 19, Vite 6, React Router v7, Query v5
│       ├── 04-arquitectura-rutas-slugs.md  <- Enrutamiento /:slug y hub /plataforma
│       ├── 05-historias-usuario.md         <- Flujos de reserva cliente, barbero y admin
│       ├── 06-ui-ux-temas-mapas.md         <- Temas dinámicos (temaKey), OpenStreetMap dark
│       ├── 07-contratos-api-axios.md       <- Clientes Axios duales e interceptors
│       ├── 08-pruebas.md                   <- Testing de componentes con Vitest
│       ├── 09-ia-responsable-hitl.md       <- Gobernanza y compuertas de decisión crítica
│       └── 10-plan-ejecucion-bootstrap.md  <- Bootstrapping paso a paso del frontend
│
├── .github/workflows/                      <- CI/CD en GitHub Actions
│   └── superprompt.yml                     <- Validación automática de compilación
│
├── build.py                                <- Script maestro de compilación
├── README.md                               <- Guía del repositorio
└── SUPERPROMPT.md                          <- Documento Maestro Full-Stack consolidado
```

---

## 🛠️ Compilación Automática de los Prompts

Para recompilar los documentos maestros tras modificar cualquier sección en `backend/secciones/` o `frontend/secciones/`:

```bash
python build.py
```

El script genera automáticamente:
1. `backend/SUPERPROMPT_BACKEND.md` (12 secciones de Backend)
2. `frontend/SUPERPROMPT_FRONTEND.md` (11 secciones de Frontend)
3. `SUPERPROMPT.md` (Compilado Full-Stack maestro en la raíz)

---

## 🤖 Protocolo Human-in-the-Loop (HITL)

Todo el ciclo de ingeniería opera bajo supervisión humana continua:
* **El modelo de IA** predice, automatiza y formula propuestas de código, DTOs y migraciones.
* **El desarrollador humano** inspecciona diffs, ejecuta pruebas y retiene la autoridad exclusiva en las compuertas críticas (migraciones SQL, esquemas de BD, seguridad y despliegues).

---

## 📍 Conexión con los Repositorios del Proyecto y Documentación Normativa

Este repositorio (**`superPromptBarberia`**) es la especificación génesis para los agentes de IA. La implementación real, las pruebas de seguridad (**SAST, SCA, IAST, DAST**), los estándares internacionales de documentación (**OpenAPI 3.0, Arc42, ISO/IEC/IEEE 26514:2022, IEEE 1063 y TypeDoc**) y las reglas de validación de IA (**`AGENTS.md`**) están centralizados en:

| Repositorio / Centro Documental | Descripción | Enlace en GitHub |
| :--- | :--- | :--- |
| **📍 Hub Maestro de Documentación y Seguridad** | Punto de partida centralizado que reúne Arc42, OpenAPI 3.0, Manual ISO 26514, TypeDoc, Seguridad y Gobernanza IA. | [`Barberia-Backend/docs/README.md`](https://github.com/dfelipe7/Barberia-Backend/blob/feature/multitenant-core-fixes/docs/README.md) |
| **🗄️ Repositorio Backend (`Barberia-Backend`)** | API REST NestJS 11 + Prisma 7 + MariaDB + Workflows SAST, SCA, IAST (Datadog) y DAST (OWASP ZAP). | [`github.com/dfelipe7/Barberia-Backend`](https://github.com/dfelipe7/Barberia-Backend/tree/feature/multitenant-core-fixes) |
| **💻 Repositorio Frontend (`Barberia-Frontend`)** | Aplicación Web React 19 + Vite + TanStack Query + Workflows SAST y SCA. | [`github.com/dfelipe7/Barberia-Frontend`](https://github.com/dfelipe7/Barberia-Frontend/tree/feature/multitenant-core-fixes) |
| **📜 Reglas de Agentes IA (`AGENTS.md`)** | Reglamento *Human-in-the-Loop* (cero commits/push automáticos, bitácoras `.ai/sessions/` y hooks). | [`Backend/AGENTS.md`](https://github.com/dfelipe7/Barberia-Backend/blob/feature/multitenant-core-fixes/AGENTS.md) · [`Frontend/AGENTS.md`](https://github.com/dfelipe7/Barberia-Frontend/blob/feature/multitenant-core-fixes/AGENTS.md) |

