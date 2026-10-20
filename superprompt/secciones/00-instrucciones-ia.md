# 00. Instrucciones de Ejecución y Directivas para Inteligencia Artificial

## 0.1 Objetivo General
Este documento establece las directrices normativas y técnicas para el desarrollo, auditoría y mantenimiento del sistema **Kyrios Barber (Kyrios Studio)**. Cualquier agente de Inteligencia Artificial (IA) o desarrollador de software que interactúe con este repositorio **DEBE** acatar estrictamente las reglas aquí descritas para garantizar la coherencia arquitectónica, la integridad de datos y el blindaje de seguridad.

## 0.2 Terminología Normativa (RFC 2119)
* **DEBE / OBLIGATORIO (SHALL / MUST):** Indica una exigencia absoluta del sistema de ingeniería.
* **NO DEBE (MUST NOT):** Indica una prohibición absoluta por motivos de seguridad o integridad arquitectónica.
* **DEBERÍA / RECOMENDADO (SHOULD):** Indica una práctica aconsejable que solo puede omitirse con justificación técnica explícita.
* **PUEDE / OPCIONAL (MAY):** Indica una característica potestativa según los requerimientos de la fase.

## 0.3 Directivas Estrictas de Codificación
1. **TypeScript Estricto:**
   * Tanto en Backend (NestJS) como en Frontend (React 19), el código **DEBE** tener tipado estricto.
   * **PROHIBICIÓN:** **NO DEBE** utilizarse el tipo `any` bajo ninguna circunstancia. Toda estructura de datos debe contar con su correspondiente `interface`, `type` o `DTO`.
2. **Arquitectura y Modularidad en NestJS:**
   * Cada módulo **DEBE** encapsular sus controladores, servicios y repositorios.
   * La lógica de acceso a datos **DEBE** aislarse en clases de repositorio que consuman `PrismaService`, evitando invocar el cliente de base de datos directamente desde los controladores.
   * La validación de entrada **DEBE** ejecutarse a través de `ValidationPipe` global con `{ whitelist: true, forbidNonWhitelisted: true, transform: true }`.
3. **Persistencia y Esquema Prisma:**
   * Ningún cambio en la base de datos **DEBE** realizarse manualmente o mediante consultas arbitrarias.
   * Todo ajuste estructural de base de datos **DEBE** ejecutarse mediante migraciones versionadas de Prisma (`npx prisma migrate dev`).
4. **Seguridad Defensiva y Principio Fail-Closed:**
   * En caso de duda, falta de datos o inconsistencia en la verificación de reservas o disponibilidad horaria, el sistema **DEBE** "fallar cerrado" (`fail-closed`), rechazando la operación con el código HTTP correspondiente (403, 409 o 503) para evitar ventas duplicadas o accesos no autorizados.
5. **Preservación de Pruebas y Evidencias:**
   * Todo cambio en la lógica de negocio **DEBE** respaldarse con pruebas unitarias (`*.spec.ts`) ejecutadas satisfactoriamente mediante `npm run test`.
