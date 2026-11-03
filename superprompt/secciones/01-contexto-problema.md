# 01. Contexto Organizacional y Definición del Problema

## 1.1 Contexto de la Organización y Evolución a SaaS Multitenant
**Kyrios Barber** nació como una solución integral para **Kyrios Studio**, un prestigioso establecimiento comercial de barbería y cuidado estético masculino ubicado en la ciudad de Popayán, Colombia. La empresa presta servicios especializados de corte de cabello, arreglo de barba, tratamientos capilares y venta de productos cosméticos para caballeros, contando con un equipo de barberos profesionales que operan bajo un esquema de porcentaje de comisión por servicio prestado.

Debido al éxito operativo y a la necesidad de escalar el modelo a múltiples sedes y barberías aliadas, el sistema evolucionó hacia una **Plataforma SaaS Multitenant (Multi-Inquilino)**. Cada barbería o sede opera como un **Tenant autónomo** con su propia marca, catálogo de servicios, equipo de barberos, horarios, paleta de colores corporativa y base de clientes, compartiendo de manera segura una infraestructura cloud común con estricto aislamiento de datos.

## 1.2 Definición del Problema Central
Históricamente, la operación diaria de las barberías se ha gestionado de forma manual y fragmentada mediante cuadernos de apuntes físicos y conversaciones dispersas en aplicaciones de mensajería (WhatsApp personal de cada barbero). Este modelo genera fallas operativas críticas:

1. **Colisión de Citas y Agendamiento Solapado:**  
   Falta de sincronización en tiempo real entre los turnos solicitados por los clientes y la disponibilidad real de cada barbero, provocando sobreventa de horarios o clientes esperando más de 45 minutos.
2. **Elevada Tasa de Inasistencia Sin Aviso (*No-Show*):**  
   Al no contar con un sistema automatizado de recordatorios y confirmación previa de citas, entre un 20% y 30% de los turnos agendados terminaban en inasistencia, causando horas muertas y pérdidas económicas directas para los barberos.
3. **Opacidad en la Liquidación de Comisiones:**  
   Incertidumbre y fricción entre la administración y el personal técnico al final de la jornada por falta de un registro centralizado y trazable de qué servicios fueron efectivamente prestados por cada barbero en cada sede.
4. **Vulnerabilidad y Mezcla de Información en Sedes Múltiples:**  
   Riesgo de fuga o contaminación cruzada de datos de clientes, ingresos y configuraciones entre diferentes sucursales o franquicias al no contar con un aislamiento estricto por inquilino.

## 1.3 Solución Planteada
Diseñar, construir e implementar una plataforma web integral (*Kyrios Barber Platform*) con arquitectura cliente-servidor desacoplada y soporte nativo Multi-Tenant que automatice:
* El agendamiento autónomo de citas en línea por parte de los clientes (registrados o invitados) bajo la URL propia de cada barbería (`/:slug/reservar`).
* El control milimétrico de la disponibilidad, descansos y bloqueos de agenda de cada barbero por sede.
* El despacho automatizado de confirmaciones y recordatorios a través de WhatsApp (Baileys) con sesiones aisladas por negocio y correo electrónico.
* La administración multisede segura bajo el estándar internacional de ciberseguridad **OWASP Top 10: 2025**, permitiendo a dueños y administradores gestionar múltiples barberías con una única cuenta global sin colisión de sesiones.
