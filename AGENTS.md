# Agent guide: Lookbook Gallery for Shopify

Instructions for AI coding agents (Claude Code, Cursor, Codex, etc.) installing or customizing this section. Humans should start with [README.md](README.md).

## What this is

A single Shopify theme section, `sections/lookbook-gallery.liquid`. It renders a grid of "looks". Clicking a look opens a `<dialog>` with the look photo and its products, with inline quick add to cart. It is built to drop into **any** Online Store 2.0 theme without changes.

```
sections/lookbook-gallery.liquid   The product. Markup, CSS, JS and schema in one file.
demo/page.lookbook.json            Example page template (demo store handles and image filenames)
demo/products.csv                  27-product demo catalog for Products > Import
demo/build_products_csv.py         Generates products.csv
demo/look-images/                  9 look photos (Burst, free commercial use)
```

## Installing into a theme

With Shopify CLI, from the user's theme directory:

1. Copy `sections/lookbook-gallery.liquid` into the theme's `sections/` folder.
2. Create a page template. Minimal `templates/page.lookbook.json`:
   ```json
   {
     "sections": {
       "main": {
         "type": "lookbook-gallery",
         "blocks": {
           "look_1": { "type": "look", "settings": { "title": "Look 1", "products": ["product-handle-a", "product-handle-b"] } }
         },
         "block_order": ["look_1"],
         "settings": { "heading": "Lookbook" }
       }
     },
     "order": ["main"]
   }
   ```
   `products` takes product **handles**. `image` takes `shopify://shop_images/<filename>` and only works for files already uploaded to the store's **Content > Files**. You cannot upload Files with the CLI. Leave `image` out and the look falls back to its first product's image.
3. Push to an **unpublished** theme first: `shopify theme push --unpublished --theme "With lookbook"`, or `--only sections/lookbook-gallery.liquid --only templates/page.lookbook.json` against an existing theme ID.
4. Ask the human before pushing to the live theme (`--allow-live`).
5. The human creates the page: **Online Store > Pages > Add page**, Theme template `lookbook`.

The page template dropdown only lists templates from the **published** theme. If the user can't find `lookbook` there, the template is only in an unpublished theme.

## Hard rules when changing the section

These keep it portable. Breaking one usually works in the theme you're testing and fails in every other theme.

1. **Stay one file.** CSS goes in `{% stylesheet %}`, JS in `{% javascript %}`. No new files in `assets/` or `snippets/`. Note that `{% stylesheet %}` and `{% javascript %}` can't contain Liquid; pass values through CSS variables or `data-` attributes instead.
2. **No theme dependencies.** Don't use a theme's classes (`page-width`, `color-scheme-1`, `grid__item`), CSS variables (`--color-background`, `--font-body-family`) or JS (`publish()`, theme components) for core behavior. Theme-specific hooks are allowed only as optional extras, feature-detected, like the ones in `notifyTheme()`.
3. **Prefix everything.** Classes are `lbg__*` (BEM style) and modifiers `lbg--*`. Data attributes are `data-lbg-*`. CSS variables are `--lbg-*`. The custom element is `<lookbook-gallery>`. Many themes ship their own "lookbook" classes, so don't use bare `.lookbook`.
4. **Size text in `em`.** Themes set different root sizes (Dawn uses 62.5% so 1rem = 10px, Horizon uses 16px). `rem` breaks in one or the other. Use `px` only for fixed UI like icons, hit targets and borders.
5. **Colors come from the page.** Inside the popup use `var(--lbg-fg)` and `var(--lbg-bg)`. They resolve to the merchant's setting, otherwise the colors `detectColors()` reads from the page at runtime. Don't hard-code colors other than neutral overlays.
6. **Every visual choice a merchant might want to change is a setting.** Every shopper-facing string is a setting too (so merchants can translate it), passed to JS through a `data-label-*` attribute on the root element. The aria-labels (`Close`, `Previous look`, `Next look`) are the one exception so far.
7. **Guard the element definition**: `if (!customElements.get('lookbook-gallery'))`. The section can appear more than once on a page.

## How the file is laid out

Top to bottom:

1. **Liquid setup** (`{%- liquid -%}` block): turns settings into values, such as the aspect ratio strings, thumbnail width, max width and anchor prefix.
2. **Root element** `<lookbook-gallery>`: carries every layout setting as an inline CSS variable (`--lbg-cols-d`, `--lbg-ratio`, `--lbg-popup-w`, ...), and the cart URLs and labels as `data-*` attributes for JS. Behavior toggles are modifier classes (`lbg--hover-zoom`, `lbg--natural`, `lbg--cta-button`, `lbg--popup-image-right`).
3. **Grid**: one `<button data-lbg-open="{index}">` per block.
4. **Dialog**: **one** `<dialog class="lbg__dialog">` for the whole section, containing one `<article data-lbg-panel>` per look. Only one panel is visible at a time (`hidden` attribute). Each panel holds the image, arrows, text, product list and the bag bar.
5. **Product rows**: two variants, switched by the `product_action` setting.
   - `quick_add`: image and title link to the PDP. Below them are option chips (`fieldset[data-lbg-option]` > `button[data-lbg-chip]`), an add button (`[data-lbg-add]`), a status line and a `<script type="application/json" data-lbg-variants>` with `{id, available, options[], image?}` per variant.
   - `link`: the whole row is an `<a>` to the PDP.
6. **`{% stylesheet %}`**: mobile first. The dialog is a bottom sheet under 750px and a centered two-column modal at 750px and up. The grid switches columns at 750px and 990px.
7. **`{% javascript %}`**: the `LookbookGallery` class, described below.
8. **`{% schema %}`**: section settings, grouped under headers, plus one block type `look`.

### JavaScript (`LookbookGallery`)

| Method | Job |
|---|---|
| `connectedCallback` / `disconnectedCallback` | Wire and unwire listeners. Opening a look from the URL hash happens here too |
| `detectColors` | Walks up from the element to find the first non-transparent background, sets `--lbg-auto-bg` and `--lbg-auto-fg` |
| `onClick` | One delegated handler for open, chip, add, close, prev and next, plus backdrop clicks |
| `open(index)` / `step(delta)` / `close()` / `onClosed()` | Show a panel, sync the URL hash with `history.replaceState`, lock page scroll, restore focus on close |
| `openFromHash` | Opens the panel whose `data-anchor` matches `location.hash` (deep links like `#look-3`) |
| `selectBlock` | Theme editor: opens the look the merchant selected |
| `variantsFor` / `selectionFor` / `selectChip` / `syncProduct` | Variant picking. `syncProduct` crosses out values with no in-stock variant given the other chosen options, and sets the add button label, `disabled` and `data-variant-id` |
| `addToCart` | See below |
| `fetchCart` / `toStandardCart` | Read `/cart.js` and convert it to the Shopify standard-events cart shape |
| `notifyTheme` | Tells the theme the cart changed. **Add support for more themes here** |
| `refreshBag` / `showBag` | The "N in your bag · View bag" bar |

### Cart flow (`addToCart`)

1. Create a promise and dispatch `shopify:cart:lines-update` (`action: 'add'`, `context: 'dialog'`, `lines` with a `gid://shopify/ProductVariant/{id}` merchandise ID, `promise`) **from the add button**, not from `document`. Themes on Shopify's standard events (Horizon) update their cart icon and cart drawer from that promise. Because the event starts inside an open modal dialog, Horizon's cart drawer waits for the lookbook to close before auto-opening. Dispatching from `document` would open the drawer on top of the popup.
2. `POST {routes.cart_add_url}.js` with `{ items: [{ id, quantity: 1 }], sections: 'cart-icon-bubble' }`.
3. `GET /cart.js`, resolve the promise with `{ cart: toStandardCart(cart), detail: { itemCount } }`. On failure, reject it and show the error in `[data-lbg-status]`.
4. `notifyTheme()`: swaps in the re-rendered `#cart-icon-bubble` (Dawn family), calls `window.publish('cart-update', ...)` if the theme defines it (Dawn pub/sub), then dispatches `lookbook:cart:added` on `document` with `{ variantId, cart }`.

To support another theme's cart drawer or icon, add a feature-detected branch to `notifyTheme()`. Find what the theme's own product form does after adding to cart (search its assets for `cart/add` or its add-to-cart handler) and repeat that. Don't remove the existing branches.

## Common changes

- **New setting:** add it to `{% schema %}` under the right header. Read it through `s.<id>` (`assign s = section.settings`). For layout values, add a `--lbg-*` variable on the root element and use it in the CSS. For JS, add a `data-*` attribute on the root element.
- **New shopper-facing text:** schema `text` setting with a default. Render it in Liquid, or pass it as `data-label-*` and read it with `this.dataset.label*`.
- **Popup layout:** desktop rules are in the `@media screen and (min-width: 750px)` block (`.lbg__panel:not([hidden])` is the two-column grid). Mobile is everything outside the media queries.
- **Product row content:** edit the `quick_add` branch and the `link` branch in the product loop. Both exist, so change both if the change applies to both.
- **Quantity picker, "add whole look", hotspots on the photo:** not built yet. Keep new controls inside the panel, use the `lbg__` prefix, route adds through `addToCart` (or a sibling that reuses its event dispatch and `notifyTheme`) so every theme keeps syncing.

## Gotchas

- The sticky bag bar (`.lbg__bag`) uses negative margins and a negative `bottom` that exactly cancel the panel body's padding. If you change `.lbg__panel-body` padding, change `.lbg__bag` to match, or the bar floats above the popup's bottom edge with content showing underneath.
- `image_picker` values must be files in the store's Files. `product_list` is capped at `limit: 25` here (Shopify allows up to 50).
- Section JS and CSS are bundled by Shopify. After adding the section in the theme editor, a merchant may need to save and refresh before the popup works in the preview.
- `{% javascript %}` runs once per page, not once per section. Per-instance state lives on the element.
- Test hash deep links by loading `/pages/<handle>#look-2` directly, not only by clicking.

## Before you hand back

1. **Schema is valid JSON:**
   ```bash
   python3 -c "import re,json;s=open('sections/lookbook-gallery.liquid').read();json.loads(re.search(r'{% schema %}(.*?){% endschema %}',s,re.S).group(1));print('ok')"
   ```
2. **JS parses:**
   ```bash
   python3 -c "import re;s=open('sections/lookbook-gallery.liquid').read();open('/tmp/lbg.js','w').write(re.search(r'{% javascript %}(.*?){% endjavascript %}',s,re.S).group(1))" && node --check /tmp/lbg.js
   ```
3. **Theme check passes**, run inside a full theme (it needs `locales/` and `config/`): copy the section into a pulled theme and run `shopify theme check`. Only look at offenses for `lookbook-gallery.liquid`, because themes ship with their own.
4. **Manual test on a dev store:** grid renders, popup opens and closes (button, Esc, backdrop), arrows cycle, `#look-2` opens on load, chips cross out sold-out values, add to cart updates the header count, bag bar sits flush at the bottom, mobile bottom sheet scrolls. If it's a Dawn-family theme, check the cart bubble too.
5. **Keep the docs in sync:** new settings or behavior go in README.md (for merchants) and this file (for agents).
