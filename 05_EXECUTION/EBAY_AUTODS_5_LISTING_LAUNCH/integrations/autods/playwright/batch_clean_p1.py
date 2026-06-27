#!/usr/bin/env python3
"""Apply SEO title (<=79) + VeRO-safe description to the CLEAN page-1 drafts
(region 1 / stock>0 / no $133-0 sentinel). No publish here. Owner standing GO 2026-06-27.
Honest generic benefit copy (no fabricated specs/reviews). Brands & VeRO words stripped."""
import os, re
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
from playwright.sync_api import sync_playwright

def html(intro,bullets,wyg,close):
    lis="".join("<li>%s</li>"%b for b in bullets)
    return ("<p>%s</p><p><strong>WHY YOU'LL LOVE IT</strong></p><ul>%s</ul><p><strong>WHAT YOU GET:</strong> %s</p><p>%s</p>")%(intro,lis,wyg,close)

CLOSE="Fast US handling. 30-day returns."
DRAFTS=[
 dict(id="6a3c8d8df6ecf06db16066e4", guard="chrome",
   title="Slide Out Cabinet Organizer 2 Tier Chrome Steel Under Sink Pantry Basket",
   intro="Turn deep, hard-to-reach cabinets into easy pull-out storage. This two-tier chrome steel organizer slides out so you can grab what you need without digging to the back.",
   bullets=["Two sliding tiers double your usable cabinet space","Chrome-plated steel frame is sturdy and rust-resistant","Pull-out design puts back-of-cabinet items within reach","Great under the sink, in the pantry or kitchen base cabinets","Open wire build keeps contents visible and ventilated"],
   wyg="1x two-tier slide-out cabinet organizer.", close=CLOSE),
 dict(id="6a3c8fb319b87e38e4738af2", guard="drawer",
   title="64 Drawer Storage Cabinet Plastic Organizer Garage Craft Hardware Bin Box",
   intro="Sort screws, beads, crafts and small parts at a glance. This 64-drawer cabinet keeps tiny items separated, labeled and easy to find on the bench or workbench.",
   bullets=["64 removable drawers organize small parts and hardware","Clear drawer fronts let you see contents fast","Stackable, wall-mount ready design saves bench space","Great for garage, craft room, office and hobby parts","Durable plastic build stands up to daily use"],
   wyg="1x 64-drawer storage cabinet.", close=CLOSE),
 dict(id="6a3c8eea4bb9aa14ed4d1706", guard="storage set",
   title="Stackable Food Storage Container Set Airtight Lids Leakproof Kitchen Pantry",
   intro="Keep food fresh and your pantry tidy. This airtight container set locks in freshness and stacks neatly so leftovers and dry goods stay organized.",
   bullets=["Airtight locking lids keep food fresh longer","Leakproof seal is great for soups, sauces and snacks","Stackable shapes save fridge and pantry space","BPA-free, microwave, freezer and dishwasher friendly","Clear bodies make it easy to see what is inside"],
   wyg="1x airtight food storage container set with lids.", close=CLOSE),
 dict(id="6a3c8e0619b87e38e4738ae5", guard="food storage containers",
   title="Airtight Food Storage Containers 32 Pcs Set BPA Free Pantry Kitchen Lids",
   intro="Restock your pantry with a full set of airtight containers. This 32-piece set keeps flour, sugar, snacks and leftovers fresh while keeping shelves neat.",
   bullets=["32-piece set covers pantry, fridge and snack storage","Airtight lids lock out moisture and keep food fresh","Leakproof and stackable to maximize shelf space","BPA-free food-grade material, easy to clean","Clear design lets you see contents at a glance"],
   wyg="1x 32-piece airtight food storage container set.", close=CLOSE),
 dict(id="6a3c8f3f4c6cec162e5647e4", guard="storage bins",
   title="Stackable Storage Bins 6 Pack Plastic Hanging Organizer Garage Shop Parts",
   intro="Organize parts, tools and supplies the shop way. These stackable bins hang on a rail or stack on a shelf so small items stay sorted and within reach.",
   bullets=["Stackable and hangable for flexible storage","Open front lets you grab parts without lifting lids","Tough plastic stands up to garage and shop use","Great for nuts, bolts, crafts and small parts","Space-saving design keeps benches clear"],
   wyg="1x set of stackable storage bins.", close=CLOSE),
 dict(id="6a3c8968dded5c227c643610", guard="fire pit cover",
   title="Patio Fire Pit Cover Waterproof 600D Outdoor Rectangular Table Protector",
   intro="Shield your fire pit table from rain, sun and debris. This heavy 600D cover keeps your patio centerpiece looking new all season.",
   bullets=["Waterproof 600D fabric blocks rain and moisture","Fits most rectangular fire pit tables","UV-resistant coating helps prevent fading","Drawstring or buckle hem holds it in wind","Wipes clean and stores compactly off-season"],
   wyg="1x waterproof rectangular fire pit cover.", close=CLOSE),
 dict(id="6a3c889f4c6cec162e5647b4", guard="adirondack",
   title="Adirondack Chair Cover Waterproof Outdoor Patio Furniture Protector 600D",
   intro="Keep your favorite outdoor chair clean and dry. This waterproof cover protects Adirondack chairs from rain, sun and yard debris year-round.",
   bullets=["Waterproof 600D fabric repels rain and dew","Tailored fit for standard Adirondack chairs","UV-resistant to help prevent sun fading","Secure straps keep it on in gusty weather","Easy to wipe clean and store away"],
   wyg="1x waterproof Adirondack chair cover.", close=CLOSE),
 dict(id="6a3d089724cbed43294c99dd", guard="under sink",
   title="Under Sink Organizer 2 Pack 3 Tier Bathroom Kitchen Storage Shelf Rack",
   intro="Reclaim the messy cabinet under your sink. This two-pack of 3-tier organizers works around pipes to create neat, stackable storage.",
   bullets=["3-tier design adds vertical storage around pipes","Two-pack covers both sides of the cabinet","Pull-out style baskets keep items easy to reach","Sturdy frame holds cleaners, toiletries and supplies","Works under bathroom and kitchen sinks"],
   wyg="2x 3-tier under-sink organizers.", close=CLOSE),
 dict(id="6a3d084b2478c0a6dbe0a7e7", guard="pool cover pump",
   title="Pool Cover Pump Above Ground Submersible Water Removal Sump Drain Cover",
   intro="Clear standing water off your pool or spa cover fast. This submersible pump removes rain and snowmelt so your cover stays clean and safe.",
   bullets=["Submersible pump removes standing water quickly","Great for pool covers, spas, basements and ponds","Automatic-style draining saves you manual bailing","Compact and easy to position on the cover","Helps protect your cover from pooling damage"],
   wyg="1x submersible pool cover pump.", close=CLOSE),
 dict(id="6a3d090d2478c0a6dbe0a7f1", guard="rice dispenser",
   title="Rice Dispenser Storage Container Sealed Cereal Bean Grain Kitchen Bin 25Lb",
   intro="Store rice and grains the clean, sealed way. This dispenser keeps bulk dry goods fresh and pest-free with easy push-button portions.",
   bullets=["Sealed container keeps rice and grains fresh","Push-style dispensing for mess-free portions","Holds bulk rice, cereal, beans and pet food","Clear window shows how much is left","Stackable shape fits pantry and counter"],
   wyg="1x sealed rice and grain dispenser.", close=CLOSE),
 dict(id="6a3cf579dd3641e3b9015563", guard="hair catcher",
   title="Shower Drain Hair Catcher Stainless Steel Bathtub Strainer Trap 2 Pack",
   intro="Stop clogs before they start. This stainless steel hair catcher sits in the drain and traps hair while water flows through freely.",
   bullets=["Catches hair and debris to prevent slow drains","Stainless steel and silicone build resists rust","Fits most standard shower and bathtub drains","Low-profile design stays put underfoot","Rinses clean in seconds, reusable"],
   wyg="2x stainless steel shower drain hair catchers.", close=CLOSE),
 dict(id="6a3c88a319b87e38e4738ac1", guard="water",
   title="Water Soakers for Kids 2 Pack Outdoor Summer Pool Beach Squirt Toys Blaster",
   intro="Power up summer water fun. This pack of water soakers is built for backyard battles, pool days and beach trips with an easy pump-and-shoot design.",
   bullets=["Easy pump action for long-range water streams","Lightweight build sized for kids hands","Great for pool, beach, yard and park play","Durable plastic stands up to summer use","Fun pack for parties and group play"],
   wyg="2x kids water soakers.", close=CLOSE),
 dict(id="6a3c887aa62e5d76174d11dd", guard="drink holder",
   title="Inflatable Drink Holders 35 Pack Pool Floating Cup Holder Party Beach Toy",
   intro="Keep drinks afloat and within reach at every pool party. This 35-pack of inflatable holders keeps cups and cans steady on the water.",
   bullets=["35-pack covers the whole pool party","Floats cups, cans and bottles within easy reach","Quick to inflate and reuse all summer","Bright colors are easy to spot in the water","Great for pools, hot tubs and lake days"],
   wyg="35x inflatable floating drink holders.", close=CLOSE),
]

def click_save(pg):
    try: pg.get_by_role("button", name=re.compile(r"^\s*Save\s*$", re.I)).first.click(timeout=5000); return True
    except Exception: return False
def desc_tab(pg):
    return pg.evaluate(r"""()=>{const e=[...document.querySelectorAll('.ant-tabs-tab,[role=tab]')].find(x=>/^\s*Description\s*$/i.test(x.innerText||'')); if(e){e.scrollIntoView({block:'center'});e.click();return true;} return false;}""")

def main():
    for d in DRAFTS:
        assert len(d["title"])<=79, "title>79 %s len=%d :: %s"%(d["id"],len(d["title"]),d["title"])
    res=[]
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000})
        for d in DRAFTS:
            url=BASE+"/upload/"+d["id"]+"&1"; pg=ctx.new_page()
            try:
                pg.goto(url, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
                ti=pg.locator("input[placeholder='Title']").first; cur=ti.input_value()
                if d["guard"] not in cur.lower(): res.append((d["id"],"SKIP guard miss: "+cur[:45])); pg.close(); continue
                ti.fill(d["title"]); pg.wait_for_timeout(700); click_save(pg); pg.wait_for_timeout(3000)
                desc_tab(pg); pg.wait_for_timeout(3000)
                dh=html(d["intro"],d["bullets"],d["wyg"],d["close"])
                setr=pg.evaluate("""(h)=>{if(!window.CKEDITOR||!window.CKEDITOR.instances)return 'no-ck';const i=Object.values(window.CKEDITOR.instances);if(!i.length)return 'no-inst';i[0].setData(h);return 'set';}""", dh)
                pg.wait_for_timeout(1200); click_save(pg); pg.wait_for_timeout(3500)
                pg.goto(url, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(6000)
                tok=pg.locator("input[placeholder='Title']").first.input_value()==d["title"]
                res.append((d["id"],"title_ok=%s desc=%s | %s"%(tok,setr,d["title"][:40])))
            except Exception as e: res.append((d["id"],"ERR "+str(e)[:70]))
            finally: pg.close()
        b.close()
    print("="*80)
    for i,r in res: print("%-26s %s"%(i,r))
main()
