# 13. Documentación Técnica, Artefactos y Entregables

## 13.1 Catálogo de Documentación del Repositorio
El proyecto cuenta con un acervo formal de documentación técnica estructurada que respalda cada decisión arquitectónica y criterio de evaluación:

1. **Especificación Interactiva Swagger / OpenAPI:**
   * Archivo vivo expuesto en `/api/docs` con schemas tipados de DTOs, códigos de respuesta HTTP, cabecera `X-Negocio-Slug` y decoradores de autenticación Bearer.
2. **Documentación Multitenant Oficial:**
   * `CAMBIOS_PLATAFORMA_MULTITENANT.md` ➔ Registro exhaustivo de la evolución de arquitectura monotienda a SaaS multitenant, llaves compuestas y aislamiento de sesiones por pestaña.
   * `CONTRATOS_API_MULTITENANT.md` ➔ Matriz de endpoints por rol, cabeceras requeridas y códigos de error por tenant.
3. **Documentos de Seguridad y Ciberseguridad (OWASP):**
   * `DICCIONARIO_DETALLADO_ALERTAS_OWASP_ZAP.docx` ➔ Análisis técnico y justificación de falsos positivos de los escaneos de penetración.
   * `OWASP_Top_10_2025_Auditoria_Barberia.docx` ➔ Mapeo detallado de los 10 riesgos del estándar oficial contra las líneas de código fuente.
   * `PRUEBAS_Y_VECTORES_DE_ATAQUE_OWASP_ZAP.docx` ➔ Evidencia de los 22.866 vectores de ataque ejecutados con ZAP.
4. **Modelado y Procesos de Negocio:**
   * `BPMN_AS_IS_Kyrios_Studio.drawio` ➔ Diagrama BPMN del proceso operativo y flujo de clientes.
   * `EntidadRelacionBarberia.drawio` ➔ Diagrama entidad-relación del modelo de datos normalizado con llaves compuestas.
   * `Matriz RACI por Roles del Sistema.xlsx` ➔ Asignación formal de responsabilidades por rol y sede.
   * `HE_HU.xlsx` ➔ Backlog maestro consolidado de Épicas e Historias de Usuario con sus criterios de aceptación.
5. **Guías Operativas:**
   * `GUIA_WHATSAPP_BAILEYS.md` ➔ Manual de vinculación, sesiones multi-tenant en disco y resolución de problemas del bot de mensajería.
