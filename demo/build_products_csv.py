"""Generate a Shopify product import CSV of demo clothing products.

Images come from Burst (burst.shopify.com), Shopify's free stock photo library.
Run: python3 demo/build_products_csv.py  ->  demo/products.csv
"""
import csv
from pathlib import Path

VENDOR = "Common Thread"
IMG = "https://burst.shopifycdn.com/photos/{}.jpg?width=1600"

APPAREL = ["XS", "S", "M", "L", "XL"]
DENIM = ["28", "30", "32", "34", "36"]
SHOES = ["6", "7", "8", "9", "10", "11"]
ONE = None  # single-variant product

# handle, title, type, price, compare_at, sizes, image, tags, description
PRODUCTS = [
    ("leather-moto-jacket", "Leather Moto Jacket", "Outerwear", 245, 295, APPAREL,
     "close-up-leather-jacket-over-shoulders", "women, outerwear, fall, new",
     "Buttery lambskin with an asymmetric zip and quilted shoulders. Broken in from day one."),
    ("light-overcoat", "Stone Overcoat", "Outerwear", 280, None, APPAREL,
     "man-poses-in-light-colored-overcoat", "men, outerwear, fall",
     "A lightweight wool-blend overcoat in stone. Notch lapel, clean single-breasted front."),
    ("camel-wool-coat", "Camel Wool Coat", "Outerwear", 260, None, APPAREL,
     "womens-fall-fashion-in-autumn-landscape", "women, outerwear, fall, bestseller",
     "Relaxed, longline coat in brushed camel wool. Made for layering over knits."),
    ("denim-trucker-jacket", "Denim Trucker Jacket", "Outerwear", 128, None, APPAREL,
     "hotdog-pin-man-jean-jacket", "men, outerwear, denim",
     "Classic mid-wash trucker in rigid 13oz denim. Pin not included."),
    ("faux-fur-coat", "Faux Fur Statement Coat", "Outerwear", 310, 360, APPAREL,
     "fashion-model-in-fur", "women, outerwear, evening",
     "Plush faux fur with a hidden hook closure. The coat that does all the talking."),
    ("green-tailored-blazer", "Forest Tailored Blazer", "Tailoring", 195, None, APPAREL,
     "green-blazer-shoes-step-in-style", "women, tailoring, new",
     "Sharp shoulders, nipped waist, deep forest green. Pairs with denim or its matching trouser."),
    ("three-piece-suit", "Three-Piece Suit", "Tailoring", 495, None, APPAREL,
     "three-piece-suit", "men, tailoring, evening",
     "Jacket, waistcoat and trouser in Italian wool. Half-canvassed construction."),
    ("silk-tie", "Silk Tie", "Accessories", 45, None, ONE,
     "suit-and-tie", "men, accessories, tailoring",
     "Hand-rolled silk tie in a subtle micro pattern."),
    ("oxford-button-down", "Oxford Button-Down", "Shirts", 78, None, APPAREL,
     "mens-fashion-close-up-shirt-tucked-in-leaning", "men, shirts, bestseller",
     "Garment-washed oxford cloth with a soft button-down collar. Tucks in clean."),
    ("chambray-work-shirt", "Chambray Work Shirt", "Shirts", 72, None, APPAREL,
     "mens-fashion-man-in-shirt-and-jeans-leaning-on-bicycle", "men, shirts, denim",
     "Lightweight chambray with twin chest pockets. Wear it open over a tee."),
    ("linen-camp-shirt", "Linen Camp Shirt", "Shirts", 84, None, APPAREL,
     "man-in-white-and-light-tan-outfit", "men, shirts, summer, new",
     "Breezy European linen with a camp collar and boxy fit."),
    ("essential-tee-cobalt", "Essential Tee - Cobalt", "T-Shirts", 32, None, APPAREL,
     "cobalt-blue-t-shirt", "unisex, t-shirts, summer",
     "Heavyweight 240gsm cotton tee in cobalt. Holds its shape wash after wash."),
    ("essential-tee-3-pack", "Essential Tee 3-Pack", "T-Shirts", 85, 96, APPAREL,
     "stack-of-t-shirts", "unisex, t-shirts, bestseller",
     "Three essential tees in white, grey and black."),
    ("stonewash-slim-jeans", "Stonewash Slim Jean", "Denim", 98, None, DENIM,
     "mens-fashion-stonewash-jeans-and-boots", "men, denim, bestseller",
     "Slim through the leg with a light stonewash and a touch of stretch."),
    ("denim-cutoff-shorts", "High-Rise Cutoff Short", "Denim", 64, None, DENIM,
     "womens-fashion-woman-denim-shorts-holding-pockets", "women, denim, summer",
     "Vintage-wash denim with a high rise and raw hem."),
    ("denim-overalls", "Denim Overalls", "Denim", 120, None, APPAREL,
     "model-in-heels-and-overalls-with-blue", "women, denim, new",
     "Relaxed overalls in a clean indigo wash with adjustable straps."),
    ("floral-sundress", "Floral Sundress", "Dresses", 118, None, APPAREL,
     "woman-in-summer-floral-fashion", "women, dresses, summer, bestseller",
     "Airy floral print with a smocked back and flutter sleeves."),
    ("white-midi-dress", "White Cotton Midi Dress", "Dresses", 135, None, APPAREL,
     "woman-in-white-dress-outside", "women, dresses, summer",
     "Crisp cotton poplin midi with a tiered skirt."),
    ("red-maxi-dress", "Poppy Maxi Dress", "Dresses", 145, 175, APPAREL,
     "woman-in-red-in-yellow-field", "women, dresses, evening",
     "Floor-length maxi in poppy red with a wrap bodice."),
    ("pink-summer-set", "Blush Two-Piece Set", "Sets", 110, None, APPAREL,
     "pink-summer-outfit", "women, sets, summer, new",
     "Matching top and short in soft blush. Wear together or apart."),
    ("leather-lace-up-boots", "Leather Lace-Up Boot", "Shoes", 210, None, SHOES,
     "boots-on-blue", "unisex, shoes, fall",
     "Full-grain leather boot on a Goodyear-welted lug sole."),
    ("studded-flats", "Studded Pointed Flat", "Shoes", 125, None, SHOES,
     "studded-flats", "women, shoes",
     "Pointed-toe leather flat with gold stud detailing."),
    ("aviator-sunglasses", "Gold Aviator Sunglasses", "Accessories", 95, None, ONE,
     "woman-wearing-aviator-glasses", "unisex, accessories, summer",
     "Thin gold frames with gradient lenses and full UV protection."),
    ("felt-fedora", "Felt Fedora", "Accessories", 68, None, ONE,
     "the-man-in-the-hat", "men, accessories, fall",
     "Wool felt fedora with a grosgrain band."),
    ("leather-messenger-bag", "Leather Messenger Bag", "Bags", 240, None, ONE,
     "man-holding-a-leather-bag-on-a-set-of-stairs", "men, bags, bestseller",
     "Vegetable-tanned leather messenger that fits a 15\" laptop."),
    ("wood-leather-watch", "Walnut & Leather Watch", "Accessories", 180, None, ONE,
     "wood-leather-watches", "unisex, accessories",
     "Walnut case with a Japanese quartz movement and leather strap."),
    ("gold-pendant-necklace", "Gold Pendant Necklace", "Jewelry", 58, None, ONE,
     "stylish-summer-necklace", "women, jewelry, summer",
     "Delicate 14k gold-plated chain with a disc pendant."),
]

HEADERS = [
    "Handle", "Title", "Body (HTML)", "Vendor", "Type", "Tags", "Published",
    "Option1 Name", "Option1 Value", "Variant SKU", "Variant Grams",
    "Variant Inventory Tracker", "Variant Inventory Qty", "Variant Inventory Policy",
    "Variant Fulfillment Service", "Variant Price", "Variant Compare At Price",
    "Variant Requires Shipping", "Variant Taxable", "Image Src", "Image Position",
    "Image Alt Text", "Status",
]


def rows():
    for handle, title, ptype, price, compare, sizes, img, tags, desc in PRODUCTS:
        values = sizes or ["Default Title"]
        for i, size in enumerate(values):
            first = i == 0
            sku = f"CT-{handle.upper()}-{size}".replace(" ", "")
            yield {
                "Handle": handle,
                "Title": title if first else "",
                "Body (HTML)": f"<p>{desc}</p>" if first else "",
                "Vendor": VENDOR if first else "",
                "Type": ptype if first else "",
                "Tags": tags if first else "",
                "Published": "TRUE" if first else "",
                "Option1 Name": ("Size" if sizes else "Title") if first else "",
                "Option1 Value": size,
                "Variant SKU": sku,
                "Variant Grams": 500,
                "Variant Inventory Tracker": "shopify",
                "Variant Inventory Qty": 25,
                "Variant Inventory Policy": "deny",
                "Variant Fulfillment Service": "manual",
                "Variant Price": f"{price:.2f}",
                "Variant Compare At Price": f"{compare:.2f}" if compare else "",
                "Variant Requires Shipping": "TRUE",
                "Variant Taxable": "TRUE",
                "Image Src": IMG.format(img) if first else "",
                "Image Position": 1 if first else "",
                "Image Alt Text": title if first else "",
                "Status": "active" if first else "",
            }


if __name__ == "__main__":
    out = Path(__file__).parent / "products.csv"
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADERS)
        w.writeheader()
        w.writerows(rows())
    print(f"Wrote {out} ({len(PRODUCTS)} products)")
