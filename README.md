# insight_graph_account_partner

Módulo de Odoo 17 que extiende [insight_graph](https://github.com/csrocha/odoo-insight-graph) agregando vistas de grafo para **contactos**, **facturas de cliente** y **productos**.

<video src="https://github.com/user-attachments/assets/68dbfcc8-ef49-4b89-ad4a-d1e57dadc44a" width="100%"></video>

## ¿Qué resuelve?

Permite navegar visualmente las relaciones entre contactos, facturas y productos sin salir de la pantalla, usando la vista **Grafo** integrada en los listados existentes de Odoo.

## Vistas incluidas

| Modelo | Menú | Forma del nodo |
|---|---|---|
| `res.partner` | Contactos / Clientes y Proveedores | Rectángulo redondeado |
| `account.move` | Contabilidad › Facturas de cliente | Rectángulo |
| `product.product` | (nodo destino desde facturas) | Diamante |

### Relaciones visualizadas

**Contacto (`res.partner`)**
- Empresa padre → contacto *(upstream)*
- Contactos hijos *(downstream)*
- Facturas emitidas *(downstream)*

**Factura (`account.move`)**
- Contacto asociado *(upstream)*
- Productos incluidos en las líneas *(downstream)*

## Requisitos

- Odoo 17.0
- Módulo [`insight_graph`](https://github.com/csrocha/odoo-insight-graph)
- Apps nativas: `account`, `contacts`

## Instalación

```bash
git clone https://github.com/csrocha/odoo-insight-graph-account-partner insight_graph_account_partner
```

O como submódulo de un proyecto existente:

```bash
git submodule add git@github.com:csrocha/odoo-insight-graph-account-partner.git addons/insight_graph_account_partner
```

## Datos de demo

Al activar los datos de demo se crean productos, contactos (compositores y cantantes latinoamericanos) y facturas de ejemplo listos para explorar el grafo desde el primer momento.

## Licencia

OPL-1 — ver [Odoo Proprietary License](https://www.odoo.com/documentation/17.0/legal/licenses.html#odoo-proprietary-license-v1-0).
