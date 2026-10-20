# 08. Requisitos No Funcionales (RNF) y Seguridad OWASP 2025

## 8.1 Matriz de Blindaje OWASP Top 10: 2025

* **RNF-SEC-01 (A01: Broken Access Control):**  
  El sistema **DEBE** aplicar control de acceso con doble guardia: `ProtectedRoute` en React y `JwtAuthGuard` + `RolesGuard` en NestJS. La autorización granular a nivel de servicio **DEBE** validar la propiedad del recurso para evitar vulnerabilidades BOLA/IDOR.
* **RNF-SEC-02 (A02: Security Misconfiguration):**  
  El backend **DEBE** inicializarse con `helmet()` configurando cabeceras de seguridad estrictas (`X-Frame-Options: SAMEORIGIN`, `X-Content-Type-Options: nosniff`), CORS restringido a los dominios del frontend, y deshabilitación obligatoria del encabezado `X-Powered-By`.
* **RNF-SEC-03 (A03: Software Supply Chain Failures):**  
  Las dependencias del frontend y backend **DEBEN** mantenerse con `package-lock.json` inmutable y auditoría automatizada en CI/CD con `npm audit` exigiendo **0 vulnerabilidades de severidad alta o crítica**.
* **RNF-SEC-04 (A04: Cryptographic Failures):**  
  Las contraseñas **DEBEN** procesarse con hashing irreversible con salt (Argon2 / Bcrypt). Las sesiones **DEBEN** usar tokens JWT firmados con algoritmo HMAC-SHA256 y canal de transporte cifrado obligatorio mediante HTTPS/TLS.
* **RNF-SEC-05 (A05: Injection):**  
  El 100% de las consultas a la base de datos **DEBEN** realizarse a través de las funciones nativas parametrizadas de Prisma ORM, prohibiendo expresamente la concatenación de cadenas en SQL. El cliente React **DEBE** escapar automáticamente el árbol DOM contra Cross-Site Scripting (XSS).
* **RNF-SEC-06 (A06: Insecure Design):**  
  La arquitectura de agendamiento para clientes invitados **DEBE** desacoplarse del login administrativo mediante tokens temporales de gestión (`X-Reservation-Management-Token`).
* **RNF-SEC-07 (A07: Authentication Failures):**  
  La autenticación administrativa **DEBE** integrarse con el proveedor oficial Google OAuth 2.0 (SSO) y contar con Throttler / Rate Limiting configurado en 100 peticiones por minuto por IP para mitigar ataques de fuerza bruta o denegación de servicio.
* **RNF-SEC-08 (A08: Software or Data Integrity Failures):**  
  El módulo de subida de archivos (Multer) **DEBE** verificar el tipo MIME real inspeccionando los números mágicos del archivo binario y renombrarlo aleatoriamente mediante UUIDv4 para impedir la ejecución de scripts arbitrarios en el servidor.
* **RNF-SEC-09 (A09: Security Logging and Alerting):**  
  El sistema **DEBE** registrar los eventos de auditoría en 3 archivos físicos diarios (`audit.log`, `security.log`, `error.log`) mediante Winston y despachar alertas asíncronas por correo SMTP al Superadministrador ante errores 500 y violaciones de rol 403.
* **RNF-SEC-10 (A10: Mishandling of Exceptional Conditions):**  
  El servidor **DEBE** contar con un filtro global de excepciones que atrape cualquier error no previsto, devolviendo un mensaje genérico sin exponer trazas de código (*stack traces*) y aplicando el principio *Fail-Closed* en la disponibilidad.

---

## 8.2 Rendimiento y Eficiencia
* **RNF-PERF-01:** El cálculo y entrega del listado de disponibilidad horaria de un barbero **DEBE** responder en un tiempo inferior a **200 milisegundos** bajo condiciones normales de red.
* **RNF-PERF-02:** El frontend **DEBE** utilizar TanStack Query para mantener en caché las respuestas de catálogo de servicios y disponibilidad, invalidando datos únicamente cuando ocurra una mutación (creación o cancelación de cita).

---

## 8.3 Disponibilidad y Resiliencia
* **RNF-DISP-01:** La plataforma en la nube (Railway) **DEBE** mantener una tasa de disponibilidad del **99.9%** durante las horas comerciales de la barbería (08:00 a 20:00 hora de Colombia).
* **RNF-DISP-02:** La sesión de WhatsApp Baileys **DEBE** ponerse en modo reposo (*idle*) automáticamente si no hay actividad en 60 segundos para evitar saturación de memoria en el servidor.
