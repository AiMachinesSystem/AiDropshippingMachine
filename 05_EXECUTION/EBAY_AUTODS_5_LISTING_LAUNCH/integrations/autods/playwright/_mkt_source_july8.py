#!/usr/bin/env python3
"""
_mkt_source_july8.py — pull 2026-07-08: 36 fresh clusters not used before —
pet grooming, automotive organizers, pickleball/outdoor games, air fryer & IP accessories,
early Halloween decor, shoe organization, indoor sports & gaming, fishing accessories,
tea/craft specialty, window care, yarn/knitting, aquarium deco, senior care, baby feeding,
plant specialty, dental organizer, sewing, STEM toys, jewelry storage, bedroom drawers,
book accessories, tool organize, home brewing, party, camping specialty, board game.
"""
import marketplace_source as ms

ms.CLUSTERS = [
    # Pet grooming (non-consumable)
    ("Pet — search 'dog grooming brush slicker'",   "search", "dog grooming brush slicker self cleaning deshedding"),
    ("Pet — search 'pet nail grinder dog'",         "search", "pet nail grinder quiet electric dog cat trimmer"),
    ("Pet — search 'deshedding glove pet'",         "search", "deshedding glove pet grooming massage rubber mitt"),
    # Automotive organizers
    ("Auto — search 'car seat back organizer'",     "search", "car seat back organizer kickproof pocket storage travel"),
    ("Auto — search 'car trunk organizer'",         "search", "car trunk organizer collapsible foldable storage tote"),
    ("Auto — search 'car sun shade windshield'",    "search", "car sun shade windshield foldable accordion reflective"),
    # Pickleball & outdoor racket
    ("Pickleball — search 'pickleball paddle set'", "search", "pickleball paddle set 4 player outdoor carbon fiber"),
    ("Pickleball — search 'pickleball ball outdoor'","search","pickleball balls outdoor 12 pack USA USAPA approved"),
    # Air fryer accessories
    ("Kitchen — search 'air fryer liners silicone'","search", "air fryer silicone liner reusable basket mat set"),
    ("Kitchen — search 'air fryer rack accessories'","search","air fryer rack accessories double layer grill skewer"),
    # Instant pot / pressure cooker
    ("Kitchen — search 'instant pot sealing ring'", "search", "instant pot sealing ring silicone replacement 6 quart"),
    ("Kitchen — search 'pressure cooker steamer rack'","search","pressure cooker steamer rack insert trivet stainless"),
    # Early Halloween / fall decor
    ("Halloween — search 'halloween banner garland'","search","halloween banner garland spider web outdoor decoration"),
    ("Halloween — search 'pumpkin string lights'",  "search", "pumpkin string lights outdoor halloween decoration"),
    # Shoe organization
    ("Storage — search 'shoe rack multi tier'",     "search", "shoe rack multi tier stackable entryway organizer metal"),
    ("Storage — search 'clear shoe storage box'",   "search", "clear shoe storage box stackable display sneaker"),
    # Indoor sports / gaming room
    ("Sports — search 'dart board set cabinet'",    "search", "dart board set cabinet steel tip electronic wall"),
    ("Sports — search 'cornhole set outdoor'",      "search", "cornhole set outdoor bags boards tailgate game regulation"),
    # Fishing accessories
    ("Outdoors — search 'tackle box organizer'",    "search", "tackle box organizer fishing gear storage waterproof"),
    ("Outdoors — search 'fishing rod holder rack'", "search", "fishing rod holder rack wall mount storage freestanding"),
    # Tea & coffee specialty
    ("Kitchen — search 'tea chest storage box'",    "search", "tea chest storage box wooden compartment organizer"),
    ("Kitchen — search 'tea infuser strainer set'", "search", "tea infuser loose leaf strainer set stainless steel"),
    # Window care & curtains
    ("Decor — search 'curtain rod set adjustable'", "search", "curtain rod set adjustable no drill tension spring"),
    ("Decor — search 'blackout curtain liner'",     "search", "blackout curtain liner thermal insulated window panel"),
    # Yarn & knitting
    ("Craft — search 'circular knitting needle set'","search","circular knitting needle set interchangeable bamboo"),
    ("Craft — search 'crochet hook set ergonomic'", "search", "crochet hook set ergonomic soft grip case bag"),
    # Jewelry storage
    ("Storage — search 'earring organizer stand'",  "search", "earring organizer stand holder jewelry display rack"),
    ("Storage — search 'ring dish holder set'",     "search", "ring dish holder set ceramic jewelry tray bedside"),
    # STEM & science kits kids
    ("Kids — search 'crystal growing kit kids'",    "search", "crystal growing kit kids science experiment STEM"),
    ("Kids — search 'slime kit making set'",        "search", "slime kit making set kids activity science non-toxic"),
    # Tool organization
    ("Garage — search 'socket organizer tray set'", "search", "socket organizer tray set rail holder 1/4 3/8 1/2"),
    ("Garage — search 'wrench roll canvas pouch'",  "search", "wrench roll canvas pouch tool kit organizer storage"),
    # Senior care helpers
    ("Health — search 'reacher grabber tool long'", "search", "reacher grabber tool long 32 inch foldable ergonomic"),
    ("Health — search 'pill organizer travel daily'","search","pill organizer travel daily weekly monthly case"),
    # Board game accessories
    ("Games — search 'card game organizer box'",    "search", "card game organizer box storage deck holder case"),
    ("Games — search 'dice tower set wooden'",      "search", "dice tower set wooden rolling dungeon tabletop game"),
]

if __name__ == "__main__":
    ms.main()
