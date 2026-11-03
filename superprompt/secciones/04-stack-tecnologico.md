# 04. Stack Tecnológico y Convenciones de Ingeniería

## 4.1 Tecnologías del Backend (API REST Multitenant)
* **Lenguaje:** TypeScript 5.7+ con compilación estricta (`strict: true`, `noImplicitAny: true`).
* **Framework:** NestJS 11.0 (Arquitectura orientada a módulos, controladores e inyección de dependencias).
* **ORM:** Prisma ORM 7.0 con extensiones de cliente personalizadas (`$extends`) para inyección automática de filtros de aislamiento por `negocioId`.
* **Motor de Base de Datos:** MariaDB 11.4 / MySQL 8.0 (Almacenamiento relacional compatible con transacciones ACID y claves compuestas foráneas).
* **Seguridad Perimetral:**
  * `helmet` v8.0.0 (Inyección de cabeceras de seguridad HTTP, CSP adaptado para iframes de mapas).
  * `@nestjs/throttler` v6.4.0 (Rate Limiting defensivo anti fuerza bruta).
  * `argon2` y `bcrypt` (Hashing criptográfico irreversible con salt para credenciales y tokens de gestión).
  * `@nestjs/jwt` (Generación y verificación de tokens de sesión HMAC-SHA256 con separación de roles de personal y clientes).
* **Observabilidad y Alertas:**
  * `nest-winston` + `winston-daily-rotate-file` (Registro rotativo en `audit.log`, `security.log` y `error.log`).
  * `@nestjs-modules/mailer` + `nodemailer` (Despacho de alertas SMTP a Google Gmail ante fallos 403 y 500).
* **Integraciones:**
  * `@whiskeysockets/baileys` (Integración con protocolo oficial WhatsApp Web con sesiones multi-tenant en disco).
  * `google-auth-library` (Validación criptográfica de tokens emitidos por Google Identity Services).

## 4.2 Tecnologías del Frontend (Cliente Web Multitenant)
* **Librería Core:** React 19.0 con TypeScript 5.8+.
* **Empaquetador y Servidor:** Vite 6.2 (Compilación modular basada en ESM y recarga rápida HMR) + Nginx en contenedor de producción.
* **Enrutamiento:** React Router DOM v7 (Manejo de rutas dinámicas prefijadas por sede `/:slug/...` y rutas globales `/plataforma`).
* **Manejo de Estado del Servidor:** TanStack Query v5 (Caché reactiva, invalidación automática tras mutaciones).
* **Clientes HTTP:**
  * `apiClient` (Axios 1.7): Interceptor con `Authorization: Bearer <token_barberia_slug>` y cabecera `X-Negocio-Slug: <slug>` para administración y catálogo.
  * `reservasApiClient` (Axios 1.7): Interceptor con `Authorization: Bearer <cliente_token_slug>` para el portal de clientes autenticados.
* **Estilos y Theming Dinámico:**
  * CSS Variables reactivas inyectadas por `TenantBrandContext` (`data-tenant-theme="clasico-azul" | "cyber-lime" | "oro-vip" | ...`).
  * Mapas embebidos con OpenStreetMap (filtro CSS Dark Mode) e integración a Google Maps.
* **Iconografía:** Lucide React.

## 4.3 Convenciones de Código y Estructura
1. **Nomenclatura de Archivos:** `kebab-case.tipo.ts` (Ej: `reservas.controller.ts`, `reservas.service.ts`, `reservas.repository.ts`).
2. **DTOs Obligatorios:** Toda petición POST, PUT o PATCH **DEBE** contar con su DTO de entrada tipado con decoradores de `class-validator` (`@IsString()`, `@IsInt()`, `@Min()`, `@IsEmail()`, etc.).
3. **Manejo de Respuestas:** El backend **DEBE** estructurar sus respuestas exitosas bajo un esquema JSON claro, y en caso de error **DEBE** responder con el formato estándar `{ statusCode, timestamp, path, message }` garantizado por el filtro global de excepciones.
