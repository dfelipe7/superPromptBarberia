# 05. Arquitectura del Sistema y Patrones de Diseño Multitenant

## 5.1 Estilo Arquitectónico Global
La plataforma adopta una **Arquitectura Cliente-Servidor Desacoplada (Decoupled Client-Server Architecture)** con soporte nativo **Multi-Tenant (SaaS)** y comunicación sin estado (*stateless*) mediante API REST sobre HTTP/HTTPS:

```
[ Cliente Web (React 19 SPA) ]
  ├── Ruta: /:slug/... (Portal Sede)
  └── Ruta: /plataforma (Directorio SaaS)
              │
              ▼ (HTTPS / JSON / JWT + X-Negocio-Slug)
[ Middleware de Aislamiento de Inquilinos (Tenant Context) ]
              │
              ▼ (Contexto NegocioId inyectado en Request)
[ Capa de Controladores (REST Controllers) ]
              │
              ▼ (Guards, Pipes & Interceptors)
[ Capa de Servicios de Dominio (Business Services) ]
              │
              ▼ (Extensión de Prisma con Filtro Automático negocioId)
[ Capa de Repositorios (Data Access Layer) ]
              │
              ▼ (Claves Foráneas Compuestas)
[ Motor Prisma ORM 7 ➔ Base de Datos MySQL / MariaDB ]
```

## 5.2 Patrones de Diseño Aplicados en el Sistema

1. **Patrón de Aislamiento Multi-Inquilino (Tenant Isolation Pattern):**
   * **Resolución de Inquilino:** `NegocioContextoService` extrae el negocio a partir de la cabecera `X-Negocio-Slug` o el subdominio.
   * **Blindaje en ORM:** Las consultas a modelos tenant-scoped se filtran automáticamente por `negocioId`. No es posible que una barbería consulte ni altere registros de otra.
2. **Patrón Path-Prefix Multitenancy en Frontend:**
   * Las rutas del frontend se prefijan con el slug de la barbería (`/:slug/dashboard`, `/:slug/reservar`, `/:slug/catalogo`).
   * Axios extrae automáticamente el slug de la URL mediante `obtenerNegocioSlugActivo()` y lo envía en la cabecera `X-Negocio-Slug`.
   * **Aislamiento Estricto de Rutas Globales:** En las rutas raíz y de nivel de plataforma (`/`, `/plataforma`, `/explorar`), `obtenerNegocioSlugActivo()` **NUNCA** adopta un tenant residual de la sesión: limpia explícitamente `sessionStorage.removeItem('tab_negocio_slug')` y retorna `null`.
   * **Protección de Identidad de Marca Corporativa:** El componente `BrandLogo` soporta la directiva `forceKyrios`: en las páginas de plataforma (`LandingPlataformaPage`, `PlataformaHubPage`) se fuerza el renderizado exclusivo de los activos oficiales de Kyrios Platform (`logo-white.svg` / `logo-black.svg`) suprimiendo logotipos personalizados y nombres de tenants previos.
3. **Aislamiento de Sesiones por Pestaña (Tab Session Isolation) y Protección contra Storage Poisoning:**
   * Los tokens JWT y perfiles se almacenan con claves compuestas en almacenamiento de sesión: `token_barberia_<slug>` y `cliente_token_<slug>`.
   * Un usuario puede tener abiertas múltiples pestañas administrando sedes distintas simultáneamente sin colisión de estado.
   * **Mitigación de Browser Storage Poisoning (CWE):** Almacenar claves o valores en `localStorage` o `sessionStorage` exige validación estricta. Todo slug interpolado en una clave de almacenamiento **DEBE** sanitizarse validando contra la expresión regular `/^[a-z0-9-]+$/` y codificándose con `encodeURIComponent`. Los identificadores de temas y configuraciones **DEBEN** validarse obligatoriamente contra una lista blanca fija en memoria (`THEMES_ALLOWLIST`) antes de persistir, neutralizando cualquier intento de inyección desde URLs o respuestas de API no confiables.
4. **Patrón Repositorio (Repository Pattern):**
   * Desacopla la lógica de negocio pura de las consultas de persistencia a la base de datos (`reservas.repository.ts`, `usuarios.repository.ts`, `perfil-negocio.repository.ts`, etc.).
5. **Patrón Adaptador y Puertos (Ports & Adapters):**
   * En el módulo de horarios se implementó el puerto `ProveedorReservasActivas` (`proveedor-reservas-activas.port.ts`), desacoplando el cálculo de disponibilidad de la implementación física del módulo de reservas.
6. **Patrón Estrategia (Strategy Pattern):**
   * Utilizado en la validación de disponibilidad horaria mediante `ReglaDisponibilidadStrategy` y `ReservaActivaRule`. Cada restricción de horario (bloqueo por almuerzo, día de descanso, cita ocupada) se evalúa como una estrategia independiente.
7. **Patrón Filtro Global de Excepciones (Exception Filter Pattern):**
   * Centralizado en `all-exceptions.filter.ts`. Intercepta cualquier excepción HTTP o fallo interno no capturado, homogeneizando el JSON de salida y disparando el subsistema de alertas SMTP de seguridad.
8. **Principio de Falla Cerrada (Fail-Closed):**
   * Si el proveedor de reservas o el contexto de negocio no responden o son inválidos, el sistema **DEBE** rechazar la consulta (con 403 o 503) en lugar de responder datos vacíos o franjas abiertas a ciegas.
9. **Patrón Máquina de Estados Finita:**
   * Gestiona el ciclo de vida de una cita:
     * `PENDIENTE` ➔ `CONFIRMADA`
     * `CONFIRMADA` ➔ `COMPLETADA`
     * `CONFIRMADA` ➔ `CANCELADA`
     * `CONFIRMADA` ➔ `NO_SHOW` (Inasistencia tras tolerancia)

---

## 5.3 Árbol Estructural Canónico del Repositorio

Cualquier IA o desarrollador que reconstruya el sistema **DEBE estructurar el código en las siguientes rutas y módulos**:

```
Barberia-Backend/
├── prisma/
│   ├── schema.prisma                  # Esquema Prisma canónico
│   └── migrations/                    # Historial de migraciones SQL versionadas
├── src/
│   ├── main.ts                        # Bootstrap NestJS con Helmet, Throttler, ValidationPipe
│   ├── app.module.ts                  # Registro raíz de módulos y middleware de inquilinos
│   ├── auth/                          # Autenticación JWT, Google OAuth, Guards y Decoradores
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   ├── guards/                    # JwtAuthGuard, RolesGuard
│   │   └── decorators/                # @Roles(), @CurrentUser()
│   ├── common/
│   │   ├── filters/                   # all-exceptions.filter.ts
│   │   ├── middleware/                # tenant-context.middleware.ts (resuelve X-Negocio-Slug)
│   │   └── guards/                    # tenant.guard.ts
│   ├── prisma/
│   │   ├── prisma.service.ts          # Conexión Prisma y extensiones de aislamiento
│   │   └── prisma.module.ts
│   └── modules/
│       ├── alerts/                    # Alertas SMTP de seguridad inmediata
│       ├── configuracion/             # Políticas operativas del tenant (cancelación, no-show)
│       ├── horarios/                  # Motor de disponibilidad, cálculo de slots de 60m
│       ├── negocios/                  # Directorio SaaS, onboarding POST /plataforma/negocios
│       ├── perfil-negocio/            # Identidad visual (temaKey), coordenadas GPS, logos
│       ├── reservas/                  # Agendamiento, máquina de estados, token de gestión
│       ├── servicios/                 # Catálogo de servicios por sede
│       ├── usuarios/                  # Personal (Administradores, Barberos, comisiones)
│       └── whatsapp/                  # Baileys WhatsApp multi-tenant en disco
└── test/                              # Suites e2e y pruebas de integración

Barberia-Frontend/
├── src/
│   ├── main.tsx                       # Bootstrap React 19 con QueryClient y BrowserRouter
│   ├── App.tsx                        # Rutas dinámicas /:slug, /plataforma, ErrorBoundary
│   ├── auth/
│   │   ├── context/AuthContext.tsx    # Sesión de personal administrativo y barbero
│   │   └── services/authService.ts
│   ├── config/
│   │   └── tenantTheme.ts             # Paletas de temas ('clasico-azul', 'cyber-lime', etc.)
│   ├── features/
│   │   ├── negocio/
│   │   │   ├── context/TenantBrandContext.tsx  # Inyección de tema visual (data-tenant-theme)
│   │   │   └── pages/ConfiguracionNegocioPage.tsx
│   │   ├── reservas/
│   │   │   ├── pages/ReservaClientePage.tsx    # Wizard público de reserva
│   │   │   ├── pages/ClientePortalPage.tsx     # Portal cliente autenticado
│   │   │   └── pages/ReservaGestionInvitadoPage.tsx # Gestión de cita vía token hash
│   │   ├── barberos/                  # Gestión de personal y comisiones
│   │   ├── servicios/                 # Gestión del catálogo de servicios
│   │   ├── horarios/                  # Gestión de matriz horaria y bloqueos
│   │   └── whatsapp/                  # Vinculación QR multi-tenant
│   ├── pages/
│   │   ├── Home/                      # Landing pública por barbería (/:slug)
│   │   │   └── components/LocationSection.tsx  # Mapa OpenStreetMap con modo oscuro y GPS
│   │   ├── Dashboard/                 # Panel administrativo por sede
│   │   ├── Plataforma/                # Hub global SaaS (/plataforma y /)
│   │   └── Login/                     # Inicio de sesión con Google SSO
│   └── shared/
│       ├── lib/http/axios.ts          # Clientes Axios duales (apiClient y reservasApiClient)
│       ├── layout/                    # MainLayout, Header, Sidebar
│       └── components/                # ProtectedRoute, ErrorBoundary
```
