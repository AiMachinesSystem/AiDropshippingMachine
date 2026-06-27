#!/usr/bin/env python3
"""Apply SEO title (<=79) + VeRO-safe desc to CLEAN inventory drafts (batch p2).
Owner standing GO 2026-06-27. Honest generic benefit copy; brands/VeRO words stripped.
Per-item skip if title>79 or guard miss (no hard abort)."""
import os, re
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
from playwright.sync_api import sync_playwright
def html(intro,bullets,wyg,close):
    lis="".join("<li>%s</li>"%b for b in bullets)
    return ("<p>%s</p><p><strong>WHY YOU'LL LOVE IT</strong></p><ul>%s</ul><p><strong>WHAT YOU GET:</strong> %s</p><p>%s</p>")%(intro,lis,wyg,close)
C="Fast US handling. 30-day returns."
def lights(intro): return dict(intro=intro,bullets=["Bright, even outdoor lighting for patios and yards","Weather-resistant build for year-round outdoor use","Easy to hang and connect end to end","Warm ambiance for parties, dining and backyard nights","Energy-efficient LED design"],wyg="1x outdoor light set.",close=C)
def cover(intro,what): return dict(intro=intro,bullets=["Waterproof fabric blocks rain, dew and moisture","UV-resistant to help prevent sun fading","Secure straps or hem hold it in windy weather","Durable heavy-duty build for all seasons","Wipes clean and stores compactly off-season"],wyg=what,close=C)
def solar(intro): return dict(intro=intro,bullets=["Solar powered - no wiring or outlets needed","Charges by day, glows automatically at night","Weatherproof for year-round garden use","Easy stake-and-go or hang installation","Soft accent light for paths, beds and patios"],wyg="1x solar light set.",close=C)
def pet(intro,what,b): return dict(intro=intro,bullets=b,wyg=what,close=C)
def pool(intro,what,b): return dict(intro=intro,bullets=b,wyg=what,close=C)

D=[
 dict(id="6a3c818b9c27405eae643247",guard="string lights",title="Outdoor String Lights 96 FT Commercial Grade Waterproof Patio Cafe Bistro LED",**lights("Light up your backyard with cafe-style ambiance. These 96 ft commercial-grade string lights are built to handle the outdoors season after season.")),
 dict(id="6a3be15e1883684e077f92fa",guard="cast iron skillet",title="Cast Iron Skillet Set 8 10 12 Inch Pre Seasoned Frying Pan Dual Handle Grill",intro="Cook anything from sear to bake with this 3-piece cast iron skillet set. Pre-seasoned and ready for stovetop, oven, grill or campfire.",bullets=["Three sizes cover everyday cooking needs","Pre-seasoned and ready to use out of the box","Even heat retention for perfect searing","Works on stovetop, oven, grill and campfire","Dual handles for a safe, balanced grip"],wyg="3x cast iron skillets (8, 10, 12 inch).",close=C),
 dict(id="6a3c7a04d2d8ac63b0564650",guard="pool vacuum hose",title="Pool Vacuum Hose 1.5 in x 40 ft Heavy Duty Swimming Pool Cleaner Replacement",**pool("Keep your pool spotless with a heavy-duty 40 ft vacuum hose. Built to resist kinks and last through seasons of cleaning.","1x pool vacuum hose (1.5 in x 40 ft).",["40 ft length reaches the whole pool","Heavy-duty wall resists kinks and cracks","Swivel-friendly cuff for tangle-free cleaning","Fits most standard pool vacuum heads","Durable build for in-ground and above-ground pools"])),
 dict(id="6a3c8776f6ecf06db16066b5",guard="solar pathway lights",title="Solar Pathway Lights 8 Pack Color Changing Stainless Steel Outdoor Garden Path",**solar("Line your walkway with warm, automatic light. This 8-pack of solar pathway lights charges by day and glows all evening.")),
 dict(id="6a3c7eb7dded5c227c6435a0",guard="sectional sofa cover",title="Patio Sectional Sofa Cover L Shape Waterproof Outdoor Furniture Protector 600D",**cover("Protect your L-shaped patio sectional from rain, sun and debris with this tailored waterproof cover.","1x L-shaped sectional sofa cover.")),
 dict(id="6a3c7e7bdded5c227c64359d",guard="string lights",title="Outdoor String Lights 200 FT LED Bistro Waterproof Patio Backyard Cafe Garden",**lights("Stretch warm cafe lighting across the whole yard with 200 ft of waterproof LED bistro string lights.")),
 dict(id="6a3c804a4bb9aa14ed4d168a",guard="solar lights",title="Solar Flame Lights Outdoor 99 LED Flickering Torch Waterproof Garden 2 Pack",**solar("Add dancing flame-effect light to your garden. These 99-LED solar torches flicker like real fire, fully weatherproof.")),
 dict(id="6a3c8742dded5c227c6435fe",guard="string lights",title="LED Outdoor String Lights 200 FT Patio Waterproof Shatterproof Bistro Backyard",**lights("Bring the patio to life with 200 ft of shatterproof LED string lights, ready for any weather.")),
 dict(id="6a3c82444bb9aa14ed4d1694",guard="patio chair covers",title="Patio Chair Covers Waterproof Outdoor Lounge Deep Seat Furniture Protector 2pk",**cover("Keep your lounge and deep-seat chairs dry and clean with this waterproof 2-pack of covers.","2x patio chair covers.")),
 dict(id="6a3c798e4c6cec162e56472e",guard="string lights",title="Outdoor String Lights 96 FT Waterproof Edison Bulb Patio Backyard Cafe Bistro",**lights("Warm Edison-style glow for patios and backyards - 96 ft of waterproof outdoor string lights.")),
 dict(id="6a3c80e29c27405eae643245",guard="patio furniture cover",title="Round Patio Furniture Cover Waterproof Outdoor Table Chair Set Protector 600D",**cover("Shield your round patio table and chair set from the elements with this heavy 600D waterproof cover.","1x round patio furniture cover.")),
 dict(id="6a3c84b6dded5c227c6435e0",guard="patio sofa cover",title="Patio Sofa Cover 3 Seater Waterproof Outdoor Couch Furniture Protector 600D",**cover("Keep your 3-seater outdoor sofa looking new with this 100% waterproof heavy-duty cover.","1x 3-seater patio sofa cover.")),
 dict(id="6a3c82e74bb9aa14ed4d1699",guard="solar pathway lights",title="Solar Pathway Lights 4 Pack Outdoor 150 LM Stainless Steel Garden Walkway",**solar("Brighten your path with 150-lumen solar lights. This 4-pack installs in minutes, no wiring needed.")),
 dict(id="6a3c80a2f6ecf06db1606673",guard="patio table cover",title="Patio Table Cover Rectangular Oval Heavy Duty Waterproof Outdoor Furniture 600D",**cover("Protect your rectangular or oval patio table with this heavy-duty 600D waterproof cover.","1x rectangular/oval patio table cover.")),
 dict(id="6a3c801219b87e38e4738a8a",guard="watering can",title="Solar Watering Can Lantern Light Outdoor Retro Metal Hanging Garden Decor Light",**solar("A charming retro watering-can lantern that pours warm solar light into your garden after dark.")),
 dict(id="6a3c87b6f6ecf06db16066b9",guard="patio chair cover",title="Patio Chair Cover Waterproof UV Resistant Outdoor Garden Furniture 600D",**cover("Keep your garden chair clean and dry year-round with this waterproof, UV-resistant cover.","1x patio chair cover.")),
 dict(id="6a3c7fdefed157c6ed6065ad",guard="egg chair cover",title="Hanging Egg Chair Cover 600D Waterproof Outdoor Patio Swing Furniture Protector",**cover("Protect your hanging egg chair from rain, sun and dust with this tailored 600D waterproof cover.","1x hanging egg chair cover.")),
 dict(id="6a3c79c9f6ecf06db1606623",guard="pool brush",title="Swimming Pool Brush Head 18 Inch Heavy Duty Wall Floor Algae Cleaning Bristle",**pool("Scrub away algae and grime fast with this 18-inch heavy-duty pool brush head.","1x 18-inch pool brush head.",["18 inch wide head cleans faster","Stiff bristles lift algae from walls and floors","Heavy-duty build resists bending","Fits most standard pool poles","Great for in-ground and above-ground pools"])),
 dict(id="6a3c8654fed157c6ed6065b7",guard="solar lanterns",title="Solar Lanterns Outdoor 2 Pack Waterproof Hanging Garden Table Patio Decor Light",**solar("Set a cozy mood with this 2-pack of waterproof solar lanterns - hang them or set them on the table.")),
 dict(id="6a3bc614dbfbc1aaa00c69bd",guard="snuffle mat",title="Dog Snuffle Mat Slow Feeder Foraging Enrichment Training Pad Stress Relief Pet",**pet("Turn mealtime into enrichment. This snuffle mat hides kibble in soft folds so your dog forages, slows down and de-stresses.","1x dog snuffle mat.",["Encourages natural foraging instincts","Slows fast eaters to aid digestion","Relieves boredom and anxiety","Machine washable and easy to fill","Great for dogs of all sizes"])),
 dict(id="6a3bc3bde005d7fdf315927a",guard="slow feeder dog bowl",title="Slow Feeder Dog Bowl Maze Puzzle Bloat Stop Anti Gulp Pet Food Water Dish",**pet("Slow down gulping and help prevent bloat with this maze-style slow feeder bowl.","1x slow feeder dog bowl.",["Maze design slows fast eaters","Helps reduce bloat, gas and vomiting","Non-slip base stays put while eating","Food-safe, BPA-free material","Dishwasher safe and easy to clean"])),
 dict(id="6944529981093377fd673cff",guard="flat iron",title="Mini Flat Iron Hair Straightener Travel Size Ceramic Dual Voltage Portable",intro="Smooth, straight hair anywhere you go. This travel-size ceramic flat iron heats fast and runs on dual voltage worldwide.",bullets=["Compact size fits any travel bag","Ceramic plates glide for smooth results","Heats up fast and holds temperature","Dual voltage works worldwide","Great for bangs, touch-ups and short styles"],wyg="1x mini travel flat iron.",close=C),
 dict(id="6a3c7ce14c6cec162e56474f",guard="inflatable baseball",title="Inflatable Baseball 12 Pack 16 Inch Beach Ball Pool Party Sports Kids Toy",**pool("Score big at pool parties and backyard games with this 12-pack of 16-inch inflatable baseballs.","12x inflatable baseballs (16 inch).",["12-pack for group play and parties","Fun baseball print, 16 inch size","Soft and safe for kids of all ages","Great for pool, beach and yard","Deflates flat for easy storage"])),
 dict(id="6a3c7a3ff6ecf06db160662e",guard="pool floats",title="Pool Float Adult Inflatable Lounger Fabric Headrest 4 in 1 Raft Lake Beach",**pool("Relax on the water in comfort. This 4-in-1 adult pool float has a fabric headrest for all-day lounging.","1x adult pool float.",["Comfortable fabric headrest","4-in-1 versatile lounging positions","Supports adults for pool or lake","Durable inflatable build","Folds compact when deflated"])),
 dict(id="6a377b894ee7478cd887fe30",guard="tea lights",title="Flameless LED Tea Lights 24 Pack Battery Votive Flickering Candles Wedding",intro="Get candle ambiance with zero fire risk. This 24-pack of flameless LED tea lights flickers like the real thing.",bullets=["24-pack for events and whole-home decor","Realistic flickering flame effect","Battery powered - safe around kids and pets","Great for weddings, parties and centerpieces","Long-lasting and reusable"],wyg="24x flameless LED tea lights.",close=C),
 dict(id="6a3c7b2e4bb9aa14ed4d1659",guard="drink holder",title="Floating Drink Holder 6 Pack Pool Hot Tub Inflatable Cup Beverage Beach Party",**pool("Keep drinks afloat and within reach. This 6-pack of inflatable drink holders is perfect for pool and hot tub days.","6x floating drink holders.",["6-pack for the whole group","Floats cups, cans and bottles","Quick to inflate and reuse","Bright and easy to spot in water","Great for pools, hot tubs and lakes"])),
 dict(id="6a3bd5a01883684e077f927c",guard="dog nail clippers",title="Dog Nail Clippers Stainless Steel Safety Guard Pet Grooming Trimmer Cat Claw",**pet("Trim your pet's nails safely at home. These stainless steel clippers have a safety guard to prevent over-cutting.","1x pet nail clippers.",["Safety guard helps prevent over-cutting","Sharp stainless steel blades cut cleanly","Non-slip ergonomic handle","Works for dogs and cats","Built-in or included filing option"])),
]

def click_save(pg):
    try: pg.get_by_role("button", name=re.compile(r"^\s*Save\s*$", re.I)).first.click(timeout=5000); return True
    except Exception: return False
def desc_tab(pg):
    return pg.evaluate(r"""()=>{const e=[...document.querySelectorAll('.ant-tabs-tab,[role=tab]')].find(x=>/^\s*Description\s*$/i.test(x.innerText||'')); if(e){e.scrollIntoView({block:'center'});e.click();return true;} return false;}""")
def main():
    res=[]
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000})
        for d in D:
            if len(d["title"])>79: res.append((d["id"],"SKIP title>79 len=%d :: %s"%(len(d["title"]),d["title"]))); continue
            url=BASE+"/upload/"+d["id"]+"&1"; pg=ctx.new_page()
            try:
                pg.goto(url, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
                ti=pg.locator("input[placeholder='Title']").first; cur=ti.input_value()
                if d["guard"] not in cur.lower(): res.append((d["id"],"SKIP guard '%s' miss: %s"%(d["guard"],cur[:40]))); pg.close(); continue
                ti.fill(d["title"]); pg.wait_for_timeout(700); click_save(pg); pg.wait_for_timeout(3000)
                desc_tab(pg); pg.wait_for_timeout(3000)
                dh=html(d["intro"],d["bullets"],d["wyg"],d["close"])
                setr=pg.evaluate("""(h)=>{if(!window.CKEDITOR||!window.CKEDITOR.instances)return 'no-ck';const i=Object.values(window.CKEDITOR.instances);if(!i.length)return 'no-inst';i[0].setData(h);return 'set';}""", dh)
                pg.wait_for_timeout(1200); click_save(pg); pg.wait_for_timeout(3500)
                pg.goto(url, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(6000)
                tok=pg.locator("input[placeholder='Title']").first.input_value()==d["title"]
                res.append((d["id"],"OK title=%s desc=%s | %s"%(tok,setr,d["title"][:38])))
            except Exception as e: res.append((d["id"],"ERR "+str(e)[:70]))
            finally: pg.close()
        b.close()
    print("="*80)
    for i,r in res: print("%-26s %s"%(i,r))
main()
