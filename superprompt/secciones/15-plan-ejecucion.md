# 15. Plan de Ejecución, Hitos y Estado de Avance por Sprints

## 15.1 Resumen Consolidado de Hitos

```
[ Sprint 1: Cimientos & Auth ] ──────────────► ✅ 100% COMPLETADO (Certificado QA)
[ Fase Multitenant Core & Personalización ] ──► ✅ 100% COMPLETADO (Desplegado en Railway)
[ Sprint 2: Citas, Horarios & OWASP ] ────────► 🟡 ~85% EN PROGRESO (Estabilización & QA)
[ Sprint 3: Pagos, Comisiones & Switcher ] ───► ⚪ PLANIFICADO (Backlog Futuro)
```

---

## 15.2 Desglose del Plan por Fases

### 🟢 Sprint 1: Arquitectura Base, Autenticación y Personal (Completado)
* **Objetivo:** Establecer los cimientos del sistema y la gestión administrativa de la barbería.
* **Métricas Alcanzadas:**
  * 48 casos de prueba QA certificados con 100% de éxito.
  * Modelo RBAC operativo con Google OAuth 2.0 y JWT criptográfico.
  * CRUD completo de barberos con cálculo de comisiones y catálogo de servicios estéticos.
  * Pipeline CI/CD en GitHub Actions y despliegue inicial en Railway.
* **Estado:** **100% Entregado y Aprobado.**

---

### 🟢 Fase Multitenant Core, Aislamiento y Personalización de Marca (Completado)
* **Objetivo:** Transformar el sistema monotienda en una plataforma SaaS Multi-Inquilino integral.
* **Métricas Alcanzadas:**
  * Modelo relacional con `Negocio` y `PerfilNegocio`, filtrado automático en ORM mediante extensiones de Prisma por `negocioId`.
  * Membresías desacopladas de la persona global: `Administrador` y `Barbero` con llaves compuestas `@@unique([negocioId, usuarioId])`.
  * Aislamiento de sesiones en Frontend por ruta (`/:slug/...`) y por pestaña (`token_barberia_<slug>`, `cliente_token_<slug>`).
  * Módulo de personalización de marca con temas dinámicos (`temaKey` en BD, `data-tenant-theme` reactivo).
  * Georreferenciación completa: asistente GPS, extractor de coordenadas y radar dark mode con OpenStreetMap y Google Maps.
  * Directorio global SaaS (`/plataforma`) con onboarding atómico de nuevas barberías y Superadmins fundadores.
* **Estado:** **100% Entregado, Migrado en BD y Desplegado en Railway.**

---

### 🟡 Sprint 2: Agendamiento, Disponibilidad, WhatsApp y OWASP 2025 (Avance Actual)
* **Objetivo:** Automatizar el agendamiento de turnos, cálculo de disponibilidad y robustecer la seguridad integral.
* **Estado Actual de Entregables:**
  * **HE-04 (Reservas de Clientes):** Flujo de agendamiento cliente/invitado operativo, tokens de gestión y confirmaciones automáticas. En proceso: pruebas de concurrencia y validaciones de borde.
  * **HE-06 (Agenda de Barbero):** Consulta de turnos y cambio de estados operativo (`COMPLETADA`, `CANCELADA`, `NO_SHOW`).
  * **HE-08 (Disponibilidad y Horarios):** Cálculo de franjas de 60 min y bloqueos de agenda listo con principio *Fail-Closed*.
  * **WhatsApp Multi-Tenant:** Sesiones independientes de Baileys por barbería en disco (`storage/sessions/<negocioId>/`).
  * **Seguridad y Auditoría OWASP Top 10: 2025:** 100% blindado en código y probado con OWASP ZAP (22.866 ataques superados) y `npm audit` (0 vulnerabilidades).
* **Métrica Consolidada:** **Avance consolidado a ~85% global**.

---

### ⚪ Sprint 3: Pasarela de Pagos, Comisiones y Métricas (Próximos Pasos)
* **Objetivo:** Monetización digital, conmutación rápida de sedes y cierre de caja automatizado.
* **Backlog Priorizado:**
  * Conmutador rápido de sedes en Header (Branch Switcher) para alternar entre barberías en 1 clic.
  * Integración con pasarela de pagos en línea (Wompi / Bold) para anticipos de citas.
  * Módulo HE-09: Cierre financiero diario y liquidación automática de comisiones ganadas por barbero.
  * Módulo HE-10: Configuración de promociones y descuentos por día de la semana.
  * Dashboard gerencial con métricas de ingresos, retención de clientes y horas pico.

---

## 15.3 Guía de Replicación Paso a Paso (Bootstrapping para la IA)

Cualquier agente de IA o ingeniero que reciba este Superprompt **DEBE seguir este orden cronológico para reconstruir el sistema funcionalmente**:

### Paso 1: Configuración de Entornos y Archivos `.env`
**1. `Barberia-Backend/.env`:**
```env
PORT=3000
NODE_ENV=development
DATABASE_URL="mysql://root:password@localhost:3306/bd_barberia_multitenant_dev"
JWT_SECRET="kyrios-secret-key-32-chars-min-length-required"
JWT_EXPIRATION="8h"
GOOGLE_CLIENT_ID="your-google-client-id.apps.googleusercontent.com"
FRONTEND_URL="http://localhost:5173"
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USER="alertas@barberia.com"
SMTP_PASS="app-password-16-chars"
SMTP_FROM="Alertas Kyrios <alertas@barberia.com>"
```

**2. `Barberia-Frontend/.env`:**
```env
VITE_API_BASE_URL="http://localhost:3000"
VITE_GOOGLE_CLIENT_ID="your-google-client-id.apps.googleusercontent.com"
```

---

### Paso 2: Base de Datos y Prisma ORM
1. Iniciar contenedor de base de datos MySQL 8:
   ```bash
   docker run --name mysql-barberia -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=bd_barberia_multitenant_dev -p 3306:3306 -d mysql:8.0
   ```
2. Crear archivo `Barberia-Backend/prisma/schema.prisma` copiando exactamente el contenido de la **Sección 06**.
3. Generar el cliente de Prisma y correr la migración inicial:
   ```bash
   cd Barberia-Backend
   npm install
   npx prisma generate
   npx prisma migrate dev --name init_multitenant_schema
   ```

---

### Paso 3: Construcción del Backend NestJS
1. Configurar `main.ts` con seguridad perimetral:
   * `app.use(helmet({ contentSecurityPolicy: false }))` (o configurando CSP que permita OpenStreetMap y Google).
   * `app.useGlobalPipes(new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true }))`.
   * `app.useGlobalFilters(new AllExceptionsFilter(alertsService))`.
2. Registrar el middleware de tenant en `app.module.ts`:
   * Interceptar peticiones y resolver el tenant a partir de la cabecera `X-Negocio-Slug` o subdominio.
3. Crear los módulos en `src/modules/` según el árbol de la **Sección 05**, implementando los DTOs canónicos de la **Sección 09**.
4. Ejecutar pruebas unitarias para validar que el aislamiento y la lógica de citas funcionan:
   ```bash
   npm run test
   ```

---

### Paso 4: Construcción del Frontend React 19
1. Instalar dependencias core:
   ```bash
   cd ../Barberia-Frontend
   npm install react react-dom react-router-dom @tanstack/react-query axios lucide-react bootstrap
   ```
2. Crear `src/shared/lib/http/axios.ts` con los dos clientes:
   * `apiClient`: inyecta `Authorization: Bearer token_barberia_<slug>` y `X-Negocio-Slug: <slug>`.
   * `reservasApiClient`: inyecta `Authorization: Bearer cliente_token_<slug>`.
3. Crear `TenantBrandContext.tsx` que lea `temaKey` del perfil y fije el atributo `data-tenant-theme` en `document.documentElement`.
4. Configurar las rutas en `App.tsx`:
   * Raíz `/` y `/plataforma` ➔ Directorio global SaaS.
   * `/:slug` ➔ Landing de la sede con `LocationSection` (OpenStreetMap).
   * `/:slug/reservar` ➔ Wizard de agendamiento público.
   * `/:slug/dashboard` ➔ Panel administrativo protegido por membresía.

---

### Paso 5: Verificación End-to-End
1. Iniciar backend: `npm run start:dev` (puerto 3000).
2. Iniciar frontend: `npm run dev` (puerto 5173).
3. Entrar a `http://localhost:5173/plataforma`, crear una barbería de prueba (ej. `demo-barber`) y verificar que se pueda navegar a `http://localhost:5173/demo-barber` con su tema visual y mapa activos.
