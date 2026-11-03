# 00. Instrucciones de Ejecución, Directivas de IA y Protocolo HITL

## 0.1 Objetivo General
Este documento establece las directrices normativas y técnicas para el desarrollo, auditoría y mantenimiento del sistema **Plataforma SaaS Multitenant para Barberías (Barber SaaS Platform)**, concebida como una solución agnóstica y multi-inquilino donde cualquier establecimiento de barbería puede operar de manera autónoma (utilizando a *Kyrios Barber* como caso de estudio e inquilino piloto inicial). Cualquier agente de Inteligencia Artificial (IA) o desarrollador de software que interactúe con este repositorio **DEBE** acatar estrictamente las reglas aquí descritas para garantizar la coherencia arquitectónica, la integridad de datos, el aislamiento multi-inquilino (*tenant isolation*) y el blindaje de seguridad.

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

### 0.4.1 Marco Conceptual y Fundamento Teórico
La técnica **Human-in-the-Loop (HITL)** o *humano en el bucle* es un enfoque de inteligencia artificial (IA) que combina el aprendizaje automático y los modelos de lenguaje con la **supervisión o intervención humana directa**. 

Su objetivo primordial es crear un **bucle de retroalimentación continuo (*continuous feedback loop*)**:
1. **Automatización y Propuesta (Modelo de IA):** El agente de IA realiza predicciones, genera código TypeScript, formula DTOs, propone esquemas de base de datos o automatiza procesos técnicos repetitivos.
2. **Supervisión y Refinamiento (Humano en el Bucle):** El desarrollador humano inspecciona, valida, corrige, refina y retroalimenta al modelo con ajustes sucesivos.
3. **Decisiones Finales en Momentos Críticos:** En aquellos puntos donde un error genera impacto irreversible (migraciones de base de datos, persistencia, seguridad, autenticación y despliegue a producción), la decisión final reside **exclusivamente en la persona humana**.

```
  ┌────────────────────────────────────────────────────────┐
  │         BUCLE DE RETROALIMENTACIÓN CONTINUO (HITL)     │
  └────────────────────────────────────────────────────────┘
              │                               ▲
  1. Propuesta de Código                      │ 2. Retroalimentación,
     y Automatización                         │    Pruebas y Corrección
              ▼                               │
  ┌──────────────────────┐        ┌──────────────────────┐
  │     AGENTE DE IA     │        │ DESARROLLADOR HUMANO │
  │   (Genera / Predice) │        │ (Supervisa / Refina) │
  └──────────────────────┘        └──────────────────────┘
              │
              ▼ [Llegada a un Momento Crítico]
  ┌──────────────────────────────────────────────────────┐
  │            COMPUERTAS DE APROBACIÓN HUMANA           │
  │  • Compuerta 1: Aprobación de Plan y Arquitectura    │
  │  • Compuerta 2: Auditoría de SQL de Migraciones      │
  │  • Compuerta 3: Verificación de Tests y Calidad      │
  │  • Compuerta 4: Aprobación de Push / Despliegue      │
  └──────────────────────────────────────────────────────┘
              │ [Solo si el Humano Autoriza]
              ▼
    [ Persistencia en BD / Despliegue a Producción ]
```

### 0.4.2 Las 5 Compuertas Mandatorias de Validación Humana
1. **Compuerta 1 (Plan & Arquitectura):** La IA **DEBE** plantear el diagnóstico y el plan de modificación antes de alterar código sustancial. El desarrollador valida el alcance.
2. **Compuerta 2 (Revisión de Código / Diff):** El humano audita línea por línea los cambios propuestos (`git diff`) para descartar regresiones o violaciones al aislamiento multi-inquilino.
3. **Compuerta 3 (Calidad & Tests):** Ningún cambio se considera terminado hasta que el humano ejecute y verifique las suites unitarias (`npm test`) y de compilación (`npm run build`).
4. **Compuerta 4 (Control de Migraciones SQL):** Ninguna migración de base de datos (`prisma migrate dev` o `prisma migrate deploy`) se ejecuta sin que el humano haya revisado y aprobado el archivo SQL generado (`migration.sql`). Se prohíbe `db push` destructivo.
5. **Compuerta 5 (Control de Red y Despliegue):** La IA **NO DEBE** ejecutar `git push`, interactuar con redes externas sin permiso, ni desplegar directamente a Railway/producción. Toda acción de publicación requiere autorización explícita del humano en la terminal.
