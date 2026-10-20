# CHANGELOG

Formato basado en [Keep a Changelog](https://keepachangelog.com/es/1.1.0/).
Versionado: `17.0.MAYOR.MENOR.PARCHE`.

Cada entrada de version incluye el **prompt** que motivo los cambios
y las **discusiones de diseno** relevantes que influyeron en las decisiones,
para trazabilidad completa del razonamiento de agentes de IA.

---

## [17.0.1.0.3] - 2026-10-20

### Prompt

> Reordena la vista de insight_graph al final de la lista de vistas, para que no sea la vista por defecto.

### Discusión de diseño

- **Causa raíz**: `insight_graph` ya estaba al final del `view_mode`, pero `ir.actions.act_window._compute_views` arma `views` poniendo primero los `view_ids` (`ir.actions.act_window.view`) y recién después los modos del `view_mode` que no tienen registro. `account.action_move_out_invoice_type` no tiene `view_ids` en core, así que `act_view_account_move_insight_graph` (secuencia 99) era el único y quedaba primero: Facturas abría en el grafo. En contactos no pasa porque core ya define kanban/tree/form con secuencias 0-2.
- **Alternativa A**: agregar registros `act_window.view` para tree/kanban/form en la acción de facturas — descartada: más registros sobre una acción ajena, y fijar `view_id` duplicaría lo que core ya resuelve con `view_id` de la acción.
- **Alternativa B (elegida)**: eliminar el `act_window.view` de facturas y dejar `insight_graph` al final del `view_mode`; la vista se resuelve por tipo, ya que es la única `insight_graph` de `account.move`.
- **Además**: el override del `view_mode` usaba `list` en vez de `tree` y dejaba afuera `activity`. Con `list`, el `view_id` de core (`view_out_invoice_tree`, tipo `tree`) no coincidía con ningún modo y se perdía la lista específica de facturas. Se restaura el `view_mode` de core más `insight_graph`.

### Corregido

- `views/insight_graph_views.xml`: eliminado `act_view_account_move_insight_graph`; el `view_mode` de `account.action_move_out_invoice_type` pasa a `tree,kanban,form,activity,insight_graph`.

---

## [17.0.1.0.2] - 2026-10-03

### Prompt

> Sigue con los AGENTS.md
>
> (continuación de: "Arregla toda la documentación que haya quedado pendiente de sincronizar")

### Discusión de diseño

- **Línea de versión**: repetía la versión del manifest y quedaba atrasada en cada ship (55 de 58 addons la tenían desactualizada, varias en 17.0.1.0.0). Se reemplaza por una referencia a `__manifest__.py` en vez de corregir el número, para que no vuelva a desincronizarse.

### Cambiado

- `AGENTS.md`: la línea `**Version actual**` pasa a remitir a `__manifest__.py` en vez de repetir el número.

---

## [17.0.1.0.1] - 2026-07-16

### Modificado

- `AGENTS.md`: reorganizacion de `Update documentation` y sincronizacion de la
  referencia de seccion tras el reordenamiento.
- `DESIGN.md`: nuevo documento con arquitectura, vistas `insight_graph` por
  modelo, controladores, integracion con acciones existentes y decisiones de
  diseno del modulo.
- Merge de `develop` a `main` para el release de esta version.

## [17.0.1.0.0] - 2026-05-18

### Prompt

> Me gusta el patron de CHANGELOG.md para replicarlo en el resto de los modulos.
> Podrias agregarlo en AGENTS.md y agregar un CHANGELOG.md que empiece a partir
> de este cambio?
>
> Estoy hablando de los addons que son submodulos de fop-odoo, no otros.
>
> Unifica el formato de las versiones para que sigan el formato de los addons de Odoo.

### Discusion de diseno

- **Adopcion del patron CHANGELOG**: el modulo `fop_encuestas_portal` establecio
  la convencion de registrar en el CHANGELOG tanto el prompt como las discusiones
  de diseno (alternativas evaluadas, decisiones tomadas, motivos de descarte).
  Se replica aqui para mantener trazabilidad uniforme en todos los submodulos de `fop-odoo`.
- **AGENTS.md minimo con enlace a directrices base**: en lugar de duplicar las
  reglas generales de Observatorio PyME en cada addon, se mantiene un AGENTS.md
  local con el checklist especifico y un enlace al AGENTS.md canonico de `fop_odoo_theme`.


### Anadido

- `AGENTS.md`: directrices para agentes de IA con checklist pre-commit,
  incluyendo la obligacion de documentar discusiones de diseno en el CHANGELOG.
- `CHANGELOG.md`: este archivo. Primera entrada registrando la adopcion del
  patron de trazabilidad de cambios.
