# 12. Estrategia de Pruebas y Aseguramiento de Calidad (QA)

## 12.1 Pirámide de Pruebas Automatizadas
La calidad del software se garantiza mediante una estrategia multicapa que cubre pruebas unitarias, de integración y pruebas dinámicas de penetración:

```
          / \
         /   \     Pruebas DAST (OWASP ZAP: 22.866 vectores)
        / DAST\   ─────────────────────────────────────────────
       /───────\   Pruebas de Integración (Jest + Repositorios reales)
      / INTEGR. \ ─────────────────────────────────────────────
     / UNITARIAS \ Pruebas Unitarias de Servicios y Controladores
    /─────────────\
```

---

## 12.2 Certificación de Pruebas Ejecutadas

### 1. Pruebas Unitarias y de Integración (Jest)
* **Resultado Oficial Verificado:** **65 Suites de Pruebas Aprobadas (65/65, 100%)** y **751 Casos de Prueba Ejecutados Satisfactoriamente (751/751, 100% éxito)**.
* Cobertura de pruebas sobre servicios críticos:
  * `disponibilidad.service.spec.ts` ➔ Validación de franjas horarias y principio *Fail-Closed*.
  * `bloqueos-horario.service.spec.ts` ➔ Pruebas de solapamiento de descansos y vacaciones.
  * `horario-semanal.service.spec.ts` ➔ Creación y actualización de semanas laborales.
  * `all-exceptions.filter.spec.ts` ➔ Captura de errores 403 y 500 y verificación de llamadas a `AlertsService`.
  * `alerts.service.spec.ts` ➔ Despacho de correos electrónicos vía Nodemailer.
  * `reservas-invitado-gestion.spec.ts` ➔ Validación de tokens de gestión efímeros.
  * `recordatorios.cron.spec.ts` ➔ Cron de recordatorios automáticos y enmascaramiento de PII.
* Comando de ejecución: `npm test` y `npm run test:cov`.

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
* **Alertas Analizadas:** Las advertencias reportadas por ZAP corresponden a **falsos positivos** propios del servidor de desarrollo local de Vite (`?v=...`) o scripts dinámicos de Google OAuth, sin impacto en producción.
