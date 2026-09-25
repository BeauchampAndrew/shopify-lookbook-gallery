# Lookbook Gallery for Shopify

A shoppable lookbook section for any Shopify theme. Shoppers click a look, see every product in it, pick a size and add to cart without leaving the page.

It's one file. No app, no monthly fee, no code knowledge needed to install it.

**Using Claude Code, Cursor or another AI coding tool?** Point it at this repo and tell it what you want, like "install this in my theme" or "make the popup image go on the right and add a quantity picker". [AGENTS.md](AGENTS.md) tells it how the section works and how to change it without breaking it in other themes.

## What it does

- Grid of look photos. Clicking one opens a popup with the photo and every product in that look.
- **Quick add:** shoppers choose a size and add to cart right in the popup, then keep browsing other looks. Out-of-stock sizes are crossed out.
- Arrows (and keyboard arrow keys) to move between looks.
- Every look has its own link, like `yourstore.com/pages/lookbook#look-3`. Use these in emails and ads to open a specific look.
- Matches your theme's fonts, colors and headings automatically.
- Works on mobile. The popup slides up from the bottom of the screen.
- Everything is adjustable in the theme editor: columns, image shape, spacing, popup size, colors, labels and more.

## Install it (about 5 minutes, no coding)

You need a Shopify theme that supports sections on every page ("Online Store 2.0"). Every free Shopify theme made since 2021 does, including Horizon and Dawn.

**Tip:** do this on a copy of your theme first. In **Online Store > Themes**, click **...** next to your theme and choose **Duplicate**. Try it there, then publish the copy when you're happy.

### Step 1: Add the section file

1. Open [`sections/lookbook-gallery.liquid`](sections/lookbook-gallery.liquid) here on GitHub and click the **Copy raw file** button (the two-squares icon at the top right of the file).
2. In your Shopify admin, go to **Online Store > Themes**. Next to your theme, click **...** then **Edit code**.
3. In the file list on the left, find the **Sections** folder and click **Add a new section**.
4. Name it `lookbook-gallery` and pick **Liquid** if it asks.
5. Delete everything in the new file, paste what you copied, and click **Save**.

### Step 2: Make a lookbook page

1. Go to **Online Store > Themes** and click **Customize**.
2. In the dropdown at the top of the screen, choose **Pages**, then **Create template**. Name it `lookbook` and click **Create template**.
3. In the left sidebar, click **Add section** and choose **Lookbook gallery**. You can remove the page's default sections if you don't want them.
4. Click **Save**.
5. Go to **Online Store > Pages > Add page**. Give it a title (like "Lookbook"), set **Theme template** to `lookbook`, and save.

Your lookbook is live at `yourstore.com/pages/lookbook` (or whatever you named the page).

### Step 3: Add your looks

In the theme editor, open the Lookbook gallery section. Each **Look** is a block. For each one:

- **Look photo:** upload the outfit photo.
- **Products in this look:** pick the products shoppers can buy.
- **Title, subtitle, description:** optional. Shown in the popup.

Click **Add Look** for more. Drag looks to reorder them. When you select a look in the editor, its popup opens so you can see what you're editing.

## Link straight to a look

Each look has a link that opens its popup when the page loads:

```
yourstore.com/pages/lookbook#look-1
yourstore.com/pages/lookbook#look-2
```

Great for "Look of the Week" emails. To use your own names (like `#summer-linen`), fill in **Custom link anchor** on the look.

## Settings

Everything lives in the theme editor. The main ones:

| Group | What you can change |
|---|---|
| Heading | Heading text, intro text, size, alignment |
| Layout | Page width or full width, columns on desktop and mobile, spacing |
| Look cards | Image shape (tall, portrait, square, landscape, or original), rounded corners, hover effect, look titles, "Shop the look" hover label |
| Popup | Image on left or right, width, height, arrows, colors, background dimming |
| Products in popup | Quick add or link to product page, image size and shape, vendor, price, all button labels |

The popup matches your page's background and text color by default. Set **Popup background** and **Popup text** only if you want something different.

## Quick add and your cart icon

Adding to cart works in every theme. Updating the cart icon in your header depends on the theme:

| Theme | Cart count updates? | Cart drawer |
|---|---|---|
| Horizon and other themes using Shopify's standard cart events | Yes (tested on Horizon) | Opens after the shopper closes the lookbook |
| Dawn, and themes built on Dawn (Sense, Craft, Refresh, Studio, and others) | Should update (not yet tested) | No |
| Other themes | After the next page load | No |

If you prefer shoppers go to the product page instead, set **When a shopper picks a product** to **Go to product page**.

**For developers:** after every add, the section fires `lookbook:cart:added` on `document` with `{ variantId, cart }` in `event.detail`. Listen for it to refresh your theme's cart UI.

```js
document.addEventListener('lookbook:cart:added', (event) => {
  // event.detail.cart is the full /cart.js response
});
```

## Troubleshooting

**"Lookbook gallery" isn't in the Add section list.**
Check the file is in the **Sections** folder and named exactly `lookbook-gallery.liquid`. If your theme is older than 2021, it may not support sections on pages.

**The `lookbook` template isn't in the page's Theme template dropdown.**
The dropdown only shows templates from your **published** theme. If you built the template on a theme copy, publish that copy first, or add the section to your live theme too.

**My cart icon doesn't update after adding.**
See [Quick add and your cart icon](#quick-add-and-your-cart-icon). The item is in the cart, and the icon catches up on the next page load.

**A look shows a product photo instead of my look photo.**
The look has no photo set, so it falls back to its first product's image. Pick a **Look photo** for that look.

## Try the demo

The `demo` folder has everything used to build the demo store: 27 clothing products and 9 filled-in looks. It's handy for testing on a development store.

1. **Products:** in **Products > Import**, upload [`demo/products.csv`](demo/products.csv). The product photos load from Shopify's free [Burst](https://burst.shopify.com) library.
2. **Look photos:** in **Content > Files**, upload the 9 images from [`demo/look-images`](demo/look-images). Keep the filenames.
3. **Template:** in **Edit code**, create a page template named `lookbook` (choose JSON) and paste in [`demo/page.lookbook.json`](demo/page.lookbook.json). Then create a page that uses it, as in step 2 above.

To change the demo catalog, edit `demo/build_products_csv.py` and run `python3 demo/build_products_csv.py`.

Demo photos are from [Burst](https://burst.shopify.com), free for commercial use.

## Install with Shopify CLI

If you use the CLI, copy `sections/lookbook-gallery.liquid` into your theme's `sections` folder and push:

```bash
shopify theme push --only sections/lookbook-gallery.liquid
```

## License

MIT. Use it, change it, sell stores with it. See [LICENSE](LICENSE).
