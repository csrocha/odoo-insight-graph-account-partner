# DESIGN.md — insight_graph_account_partner

## 1. Propósito y Alcance

Módulo de demostración y caso de uso real del tipo de vista `insight_graph`.
Registra vistas de grafo para cuatro modelos del área contable/comercial:
`res.partner`, `account.move`, `product.product` y `product.template`.
Agrega el campo computado `product_ids` en `account.move` para exponer los
productos facturados como relación navegable en el grafo.

## 2. Arquitectura

```
insight_graph_account_partner/
├── models/
│   └── account_move.py          # Campo computado product_ids
├── views/
│   └── insight_graph_views.xml  # 4 vistas insight_graph + act_window updates
├── demo/
│   └── demo.xml                 # Partners, productos, facturas de ejemplo
└── __manifest__.py
```

**Dependencias:** `insight_graph`, `account`, `contacts`

## 3. Modelos Python

### AccountMove (hereda `account.move`)

**Campo:**
- `product_ids` (Many2many `product.product`, computed, non-stored)
  - Computa desde `invoice_line_ids.product_id`
  - Permite usar `product_ids` como `<link field>` en el arch del grafo

**Métodos:**

| Método | Descripción |
|--------|-------------|
| `_compute_product_ids()` | Extrae set de productos de líneas de factura |
| `_create_demo_invoices()` (model method) | Crea 7 facturas de demostración con productos y partners; tolerante a entornos sin plan de cuentas |

## 4. Controladores

Ninguno. Usa el controller genérico de `insight_graph`.

## 5. Vistas insight_graph (insight_graph_views.xml)

### 5.1 res.partner — Modo template HTML

```xml
<insight_graph>
    <node shape="roundrectangle" width="210" height="100">
        <div class="d-flex align-items-center h-100 gap-2 p-2 rounded"
             style="background:#e8f4fd;border:2px solid #4a9eda">
            <field name="image_128" type="image"
                   class="rounded-circle flex-shrink-0"
                   style="width:52px;height:52px;object-fit:cover"/>
            <div style="flex:1;min-width:0">
                <div class="fw-bold text-truncate" style="font-size:13px;color:#1a5276">
                    <field name="display_name" primary="true"/>
                </div>
                <div class="text-truncate" style="font-size:11px;color:#6c757d">
                    <field name="vat"/>
                </div>
            </div>
        </div>
    </node>
    <link field="parent_id" direction="upstream" model="res.partner"/>
    <link field="child_ids" direction="downstream" model="res.partner"/>
    <link field="invoice_ids" direction="downstream" model="account.move"/>
</insight_graph>
```

**Características:** Tarjeta con avatar circular (52×52), nombre en negrita, CUIT/VAT.
Navega hacia empresa padre, contactos hijos y facturas.

---

### 5.2 account.move — Modo campo simple con color de estado

```xml
<insight_graph>
    <node shape="diamond">
        <field name="name" primary="true"/>
        <field name="move_type"/>
        <field name="state" color="true"/>
        <field name="amount_total"/>
    </node>
    <link field="partner_id" direction="upstream" model="res.partner"/>
    <link field="product_ids" direction="downstream" model="product.product"/>
</insight_graph>
```

**Características:** Nodo diamante. `state` determina el color de fondo (colores
configurables via CSS vars). `amount_total` aparece en el tooltip. Navega hacia
el partner y hacia los productos facturados (via campo computado).

---

### 5.3 product.product — Modo template HTML con precio monetario

```xml
<insight_graph>
    <node shape="rectangle" width="210" height="100">
        <div class="d-flex align-items-center h-100 gap-2 p-2"
             style="background:#f0f4f8;border:2px solid #6c757d">
            <field name="image_128" type="image" class="flex-shrink-0"
                   style="width:52px;height:52px;object-fit:cover;border-radius:4px"/>
            <div style="flex:1;min-width:0">
                <div class="fw-bold text-truncate" style="font-size:13px;color:#2c3e50">
                    <field name="display_name" primary="true"/>
                </div>
                <div class="text-truncate" style="font-size:11px;color:#6c757d">
                    <field name="list_price" type="monetary" currency_field="currency_id"/>
                </div>
            </div>
        </div>
    </node>
    <link field="product_tmpl_id" direction="upstream" model="product.template"/>
</insight_graph>
```

**Características:** Tarjeta con imagen del producto, nombre y precio formateado con
símbolo de moneda. Navega hacia la plantilla del producto.

---

### 5.4 product.template — Nodo octágono simple

```xml
<insight_graph>
    <node shape="octagon">
        <field name="display_name" primary="true"/>
        <field name="categ_id"/>
    </node>
</insight_graph>
```

**Características:** Nodo octágono (hoja del grafo). Muestra nombre y categoría en tooltip.
Sin links de salida: es el extremo final de la jerarquía del grafo.

## 6. Integración con Acciones Existentes

El módulo extiende (append) las acciones de ventana existentes para agregar el modo
`insight_graph` con secuencia 99 (al final de la lista):

| Acción | Modos resultantes |
|--------|-------------------|
| `base.action_partner_form` | kanban, tree, form, **insight_graph** |
| `contacts.action_contacts` | kanban, tree, form, activity, **insight_graph** |
| `account.action_move_out_invoice_type` | list, kanban, form, **insight_graph** |

## 7. Datos de Demostración (demo/demo.xml)

**Categoría de producto:** "Instrumentos Musicales"

**Productos:**
- Guitarra Fender Stratocaster (precio: 1500.0, tipo: servicio)
- Micrófono Shure SM58 (precio: 250.0, tipo: servicio)

**Partners (compositores/intérpretes latinoamericanos):**
- Astor Piazzolla (AR)
- Alberto Ginastera (AR)
- Atahualpa Yupanqui (AR)
- Agustín Lara (MX)
- Mercedes Sosa (AR)
- Lila Downs (MX)
- Alfredo Zitarrosa (UY)

**Facturas (vía `_create_demo_invoices()`):**

| Partner | Productos | Fecha |
|---------|-----------|-------|
| Astor Piazzolla | Guitarra | 2024-01-15 |
| Alberto Ginastera | Guitarra | 2024-01-22 |
| Agustín Lara | Guitarra | 2024-02-10 |
| Atahualpa Yupanqui | Guitarra | 2024-02-28 |
| Mercedes Sosa | Micrófono | 2024-03-15 |
| Lila Downs | Micrófono | 2024-03-22 |
| Alfredo Zitarrosa | Guitarra + Micrófono | 2024-04-05 |

Las facturas se crean via método Python en lugar de XML para tolerar entornos
sin plan de cuentas configurado.

## 8. Grafo resultante (estructura de demostración)

```
product.template (Instrumentos Musicales)
    ▲
    │ product_tmpl_id
product.product (Guitarra)    product.product (Micrófono)
    ▲                               ▲
    │ product_ids (computed)        │ product_ids (computed)
account.move (Fact. Piazzolla) ...  account.move (Fact. Zitarrosa) [ambas]
    │                               │
    │ partner_id                    │ partner_id
    ▼                               ▼
res.partner (Piazzolla)         res.partner (Zitarrosa)
    │ parent_id (si hay empresa matriz)
    ▼
res.partner (empresa)
```

## 9. Decisiones de Diseño

**`product_ids` como campo computado no almacenado:**
`account.move.invoice_line_ids` ya tiene los productos; exponer `product_ids` como
Many2many computado permite usarlo como `<link field>` en el arch sin alterar el
esquema de la base de datos.

**Demo data con partners latinoamericanos:**
Datos reconocibles culturalmente para el equipo de Observatorio PyME (Argentina,
México, Uruguay), ilustran correctamente la jerarquía partner → factura → producto.

**Facturas creadas via método Python:**
`ir.config_parameter` y el plan de cuentas pueden no estar configurados en ambientes
de testing. El método `_create_demo_invoices()` maneja estas condiciones de contorno.

**Secuencia 99 en act_window views:**
Se agrega al final de los modos existentes para no alterar el modo de vista por defecto
de las acciones estándar de Odoo.

**Cuatro shapes diferentes por modelo:**
`roundrectangle` (partner), `diamond` (factura), `rectangle` (producto),
`octagon` (template) — diferenciación visual inmediata del tipo de nodo sin
necesidad de leer la etiqueta.
