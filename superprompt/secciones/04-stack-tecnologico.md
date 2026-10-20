# 04. Stack Tecnológico y Convenciones de Ingeniería

## 4.1 Tecnologías del Backend (API REST)
* **Lenguaje:** TypeScript 5.7+ con compilación estricta (`strict: true`, `noImplicitAny: true`).
* **Framework:** NestJS 11.0 (Arquitectura orientada a módulos, controladores e inyección de dependencias).
* **ORM:** Prisma ORM 7.0 (Mapeo relacional seguro con consultas parametrizadas internamente).
* **Motor de Base de Datos:** MariaDB 11.4 / MySQL 8.0 (Almacenamiento relacional compatible con transacciones ACID).
* **Seguridad Perimetral:**
  * `helmet` v8.0.0 (Inyección de cabeceras de seguridad HTTP).
  * `@nestjs/throttler` v6.4.0 (Rate Limiting defensivo anti fuerza bruta).
  * `argon2` y `bcrypt` (Hashing criptográfico irreversible con salt para credenciales).
  * `@nestjs/jwt` (Generación y verificación de tokens de sesión HMAC-SHA256).
* **Observabilidad y Alertas:**
  * `nest-winston` + `winston-daily-rotate-file` (Registro rotativo en `audit.log`, `security.log` y `error.log`).
  * `@nestjs-modules/mailer` + `nodemailer` (Despacho de alertas SMTP a Google Gmail ante fallos 403 y 500).
* **Integraciones:**
  * `@whiskeysockets/baileys` (Integración con protocolo oficial WhatsApp Web para notificaciones).
  * `google-auth-library` (Validación criptográfica de tokens emitidos por Google Identity Services).

## 4.2 Tecnologías del Frontend (Cliente Web)
* **Librería Core:** React 19.0 con TypeScript 5.8+.
* **Empaquetador y Servidor Local:** Vite 6.2 (Compilación modular basada en ESM y recarga rápida HMR).
* **Enrutamiento:** React Router DOM v7 (Manejo de rutas declarativas con control de acceso RBAC).
* **Manejo de Estado del Servidor:** TanStack Query v5 (Caché reactiva, invalidación automática tras mutaciones y resiliencia de datos).
* **Cliente HTTP:** Axios 1.7 con interceptores de solicitud (inyección automática del encabezado `Authorization: Bearer <token>`) y respuesta (manejo centralizado de 401/403).
* **Estilos:** Vanilla CSS / Tailwind CSS con sistema editorial de diseño en Modo Oscuro (*Dark Mode*) y micro-animaciones en CSS puro.
* **Componentes UI e Íconos:** Lucide React (Iconografía consistente y minimalista).

## 4.3 Convenciones de Código y Estructura
1. **Nomenclatura de Archivos:** `kebab-case.tipo.ts` (Ej: `reservas.controller.ts`, `reservas.service.ts`, `reservas.repository.ts`).
2. **DTOs Obligatorios:** Toda petición POST, PUT o PATCH **DEBE** contar con su DTO de entrada tipado con decoradores de `class-validator` (`@IsString()`, `@IsInt()`, `@Min()`, `@IsEmail()`, etc.).
3. **Manejo de Respuestas:** El backend **DEBE** estructurar sus respuestas exitosas bajo un esquema JSON claro, y en caso de error **DEBE** responder con el formato estándar `{ statusCode, timestamp, path, message }` garantizado por el filtro global de excepciones.
