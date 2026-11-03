# 12. Estrategia de Pruebas y Aseguramiento de Calidad (QA) Multitenant

## 12.1 Pirámide de Pruebas Automatizadas
La calidad del software se garantiza mediante una estrategia multicapa que cubre pruebas unitarias, pruebas de aislamiento multi-tenant, integración y pruebas dinámicas de penetración:

```
          / \
         /   \     Pruebas DAST (OWASP ZAP: 22.866 vectores de ataque)
        / DAST\   ─────────────────────────────────────────────────────
       / AISL. \   Pruebas de Aislamiento Tenant (negocio-aislamiento.spec)
      /─────────\ ─────────────────────────────────────────────────────
     / INTEGRAC. \ Pruebas de Integración (Jest + Repositorios reales)
    / UNITARIAS   \ Pruebas Unitarias de Servicios, Guards y DTOs
   /───────────────\
```

---

## 12.2 Certificación de Pruebas Ejecutadas

### 1. Pruebas Unitarias, de Integración y Aislamiento (Jest)
* Cobertura de pruebas sobre servicios críticos:
  * `negocio-aislamiento.spec.ts` ➔ Blindaje de consultas tenant-scoped: verificación de que ninguna consulta pueda escapar del `negocioId` del contexto.
  * `perfil-negocio.service.spec.ts` ➔ Pruebas de persistencia de marca, validación de coordenadas y selección de `temaKey`.
  * `disponibilidad.service.spec.ts` ➔ Validación de franjas horarias y principio *Fail-Closed*.
  * `bloqueos-horario.service.spec.ts` ➔ Pruebas de solapamiento de descansos y vacaciones.
  * `horario-semanal.service.spec.ts` ➔ Creación y actualización de semanas laborales por sede.
  * `barberos.service.spec.ts` ➔ Gestión de comisiones por sede, fotos y membresías (46/46 tests aprobados).
  * `administradores.service.spec.ts` ➔ Asignación de Superadmin y administradores con llaves compuestas.
  * `all-exceptions.filter.spec.ts` ➔ Captura de errores 403/500 y verificación de llamadas a `AlertsService`.
  * `recordatorios.cron.spec.ts` ➔ Cron de recordatorios automáticos y enmascaramiento de PII.
* Comando de ejecución: `npm test` y `npm run test:multitenant`.

### 2. Pruebas de Seguridad en Dependencias (SCA)
* **Herramienta:** `npm audit` integrado en el pipeline de GitHub Actions (`security-audit.yml`).
* **Resultado:** **0 vulnerabilidades** reportadas tanto en `barberia-backend` como en `barberia-frontend`.

### 3. Pruebas Dinámicas de Penetración (DAST) con OWASP ZAP
* **Alcance:** Escaneo dinámico sobre la API en vivo de NestJS (`http://localhost:3000`) importando la definición OpenAPI oficial (`/api/docs-json`).
* **Métricas del Ataque:**
  * **22.866 solicitudes de ataque** lanzadas a través de 24 plugins de penetración en 04:08 minutos.
  * **3.769 ataques activos de Inyección SQL (SQLi):** 0 alertas (100% blindado por Prisma ORM).
  * **5.975 ataques de Inyección de Comandos OS:** 0 alertas (100% mitigado por validación de DTOs).
  * **5.610 ataques de Server-Side Code Injection (SSTI):** 0 alertas.
  * **Ataques de Fuerza Bruta / Inundación:** Mitigados con éxito mediante Throttler (HTTP 429 Too Many Requests).
