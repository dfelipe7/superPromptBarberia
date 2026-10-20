# 01. Contexto Organizacional y Definición del Problema

## 1.1 Contexto de la Organización
**Kyrios Studio** es un establecimiento comercial de barbería y cuidado estético masculino ubicado en la ciudad de Popayán, Colombia. La empresa presta servicios especializados de corte de cabello, arreglo de barba, tratamientos capilares y venta de productos cosméticos para caballeros, contando con un equipo de barberos profesionales que operan bajo un esquema de porcentaje de comisión por servicio prestado.

## 1.2 Definición del Problema Central
Históricamente, la operación diaria de la barbería se ha gestionado de forma manual y fragmentada mediante cuadernos de apuntes físicos y conversaciones dispersas en aplicaciones de mensajería (WhatsApp personal de cada barbero). Este modelo ha generado fallas operativas críticas:

1. **Colisión de Citas y Agendamiento Solapado:**  
   Falta de sincronización en tiempo real entre los turnos solicitados por los clientes y la disponibilidad real de cada barbero, provocando sobreventa de horarios o clientes esperando más de 45 minutos.
2. **Elevada Tasa de Inasistencia Sin Aviso (*No-Show*):**  
   Al no contar con un sistema automatizado de recordatorios y confirmación previa de citas, entre un 20% y 30% de los turnos agendados terminaban en inasistencia, causando horas muertas y pérdidas económicas directas para los barberos.
3. **Opacidad en la Liquidación de Comisiones:**  
   Incertidumbre y fricción entre la administración y el personal técnico al final de la jornada por falta de un registro centralizado y trazable de qué servicios fueron efectivamente prestados por cada barbero.
4. **Vulnerabilidad en la Gestión de la Información:**  
   Inexistencia de controles de acceso digital, almacenamiento inseguro de contactos de clientes y carencia de políticas de auditoría informática.

## 1.3 Solución Planteada
Diseñar, construir e implementar una plataforma web integral (*Kyrios Barber*) con arquitectura cliente-servidor desacoplada que automatice:
* El agendamiento autónomo de citas en línea por parte de los clientes (registrados o invitados).
* El control milimétrico de la disponibilidad, descansos y bloqueos de agenda de cada barbero.
* El despacho automatizado de confirmaciones y recordatorios a través de WhatsApp (Baileys) y correo electrónico.
* La administración segura de usuarios bajo el estándar internacional de ciberseguridad **OWASP Top 10: 2025**.
