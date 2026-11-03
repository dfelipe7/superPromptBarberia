# 00. Instrucciones de Ejecución, Directivas de IA y Protocolo HITL

## 0.1 Objetivo General
Este documento establece las directrices normativas y técnicas para el desarrollo, auditoría y mantenimiento del sistema **Kyrios Barber Platform (SaaS Multitenant)**. Cualquier agente de Inteligencia Artificial (IA) o desarrollador de software que interactúe con este repositorio **DEBE** acatar estrictamente las reglas aquí descritas para garantizar la coherencia arquitectónica, la integridad de datos, el aislamiento multi-inquilino (*tenant isolation*) y el blindaje de seguridad.

## 0.2 Terminología Normativa (RFC 2119)
* **DEBE / OBLIGATORIO (SHALL / MUST):** Indica una exigencia absoluta del sistema de ingeniería.
* **NO DEBE (MUST NOT):** Indica una prohibición absoluta por motivos de seguridad o integridad arquitectónica.
* **DEBERÍA / RECOMENDADO (SHOULD):** Indica una práctica aconsejable que solo puede omitirse con justificación técnica explícita.
* **PUEDE / OPCIONAL (MAY):** Indica una característica potestativa según los requerimientos de la fase.

## 0.3 Directivas Estrictas de Codificación
1. **TypeScript Estricto:**
   * Tanto en Backend (NestJS 11) como en Frontend (React 19), el código **DEBE** tener tipado estricto.
   * **PROHIBICIÓN:** **NO DEBE** utilizarse el tipo `any` bajo ninguna circunstancia. Toda estructura de datos debe contar con su correspondiente `interface`, `type` o `DTO`.
2. **Arquitectura y Aislamiento Multi-Tenant en NestJS:**
   * Cada módulo **DEBE** encapsular sus controladores, servicios y repositorios.
   * Toda consulta a modelos de ámbito de inquilino (*tenant-scoped*) **DEBE** estar acotada obligatoriamente por el `negocioId` del contexto de la petición (`X-Negocio-Slug` o subdominio), garantizado por el middleware de aislamiento y extensiones de Prisma.
   * La validación de entrada **DEBE** ejecutarse a través de `ValidationPipe` global con `{ whitelist: true, forbidNonWhitelisted: true, transform: true }`.
3. **Persistencia y Esquema Prisma:**
   * Ningún cambio en la base de datos **DEBE** realizarse manualmente o mediante consultas arbitrarias.
   * Todo ajuste estructural de base de datos **DEBE** ejecutarse mediante migraciones versionadas de Prisma (`npx prisma migrate dev` / `prisma migrate deploy`). Se prohíbe el uso de comandos destructivos como `db push` en producción.
4. **Seguridad Defensiva y Principio Fail-Closed:**
   * En caso de duda, falta de contexto de negocio, o inconsistencia en la verificación de reservas o disponibilidad horaria, el sistema **DEBE** "fallar cerrado" (`fail-closed`), rechazando la operación con el código HTTP correspondiente (403, 404, 409 o 503).
5. **Preservación de Pruebas y Evidencias:**
   * Todo cambio en la lógica de negocio **DEBE** respaldarse con pruebas unitarias (`*.spec.ts`) ejecutadas satisfactoriamente mediante `npm run test`.

---

## 0.4 Protocolo Operativo Human-in-the-Loop (HITL)

El desarrollo del sistema opera bajo un modelo obligatorio de **Human-in-the-Loop (HITL)**. La IA actúa como un copiloto de ingeniería que propone, formula y refactoriza código, pero **el desarrollador humano es el único con autoridad para autorizar y ejecutar acciones críticas**:

```
[ Desarrollador Humano ] ──► Solicita requerimiento y aprueba plan inicial
           │
           ▼
[ Agente de IA ] ──────────► Propone cambios de código, DTOs y pruebas unitarias
           │
           ▼
[ Compuerta 1: Revisión ] ──► Humano audita el diff (`git diff`) y autoriza aplicación
           │
           ▼
[ Compuerta 2: Calidad ] ───► Humano ejecuta compilación y tests (`npm test`, `npm run build`)
           │
           ▼
[ Compuerta 3: BD/Prisma ] ─► Humano revisa SQL de migración y ejecuta `prisma migrate deploy`
           │
           ▼
[ Compuerta 4: Deploy ] ────► Humano autoriza `git push`, merge a `master` y paso a producción
```

### Reglas de Ejecución HITL para la IA:
1. **Propuesta Previa (Plan Gate):** La IA **DEBE** explicar qué archivos va a modificar y por qué antes de realizar cambios masivos.
2. **Prohibición de Despliegue Autónomo:** La IA **NO DEBE** ejecutar despliegues directos a producción sin que el humano haya verificado previamente el resultado en local o staging.
3. **Control Criptográfico y de Migraciones:** Las migraciones de base de datos requieren siempre que el humano revise el archivo `migration.sql` y ejecute explícitamente el comando de migración en la base de datos real.
4. **Entorno Aislado (Sandbox):** Toda ejecución de comandos que interactúe con redes externas o servicios en la nube requiere la aprobación explícita del desarrollador humano en la terminal.
