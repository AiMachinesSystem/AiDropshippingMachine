# EBAY + AMAZON AUTODS PRODUCT RESEARCH TRAINING OS

## 0. CHAT COMPACT

The user wants to build an eBay dropshipping system using Amazon.com as the product/data source and AutoDS as the automation/import layer.

Core idea:
- Do not blindly import Amazon products into eBay.
- Use Amazon data as supply/source intelligence.
- Use eBay data as demand/profit validation.
- AutoDS is only the execution layer, not the decision-maker.
- The machine must become a filter, not an importer.

Main objective:
Build a repeatable system that can find, validate, score, draft, test, improve, and scale profitable eBay listings while protecting seller account health.

Important operating constraints:
- Marketplace: eBay.com
- Source/data: Amazon.com
- Automation: AutoDS
- Mode: research + draft first
- No mass publishing
- No risky products
- No live publishing without OWNER_GO
- Protect eBay account health before chasing revenue

Policy-aware note:
eBay dropshipping policy risk must always be evaluated. The machine should distinguish between:
1. Amazon used only as a research/data source.
2. Amazon used as a fulfillment source.
3. Wholesale/authorized supplier relationship.
If fulfillment creates marketplace-policy or seller-of-record risk, the machine must flag it clearly.

The machine must track:
- eBay demand
- sold listings
- active competition
- sell-through rate
- Amazon source price
- tax/shipping buffer
- eBay fees
- promoted listing cost
- AutoDS allocation
- return reserve
- net profit
- margin %
- account-health risk
- stock risk
- shipping risk
- IP/brand/VERO risk

Final operating model:
Amazon data → eBay demand proof → margin proof → risk proof → optimized draft → controlled test → kill/fix/scale decision.

---

# 1. MACHINE TRAINING OBJECTIVE

## Skill Name
`ebay-amazon-autods-profit-research`

## Mission
Train the machine to become a profitable eBay product research and validation operator using Amazon.com data, eBay marketplace demand signals, and AutoDS execution tools.

The machine must learn to:
- find candidate products
- compare Amazon supply against eBay demand
- calculate realistic profit
- reject weak/risky products
- create optimized eBay listing drafts
- define AutoDS rules
- test listings safely
- learn from results
- improve future product selection

The goal is not volume.
The goal is profitable, low-risk, repeatable product selection.

---

# 2. CORE PRINCIPLE

Bad system:

```text
Find Amazon product
→ import with AutoDS
→ publish to eBay
→ hope it sells
```

Correct system:

```text
Find Amazon product
→ verify eBay demand
→ simulate profit
→ check risks
→ rewrite listing for eBay SEO
→ create draft
→ test with rules
→ measure
→ improve or kill
```

The machine must never recommend a product only because it is cheap, trending, or available on Amazon.

A product is valid only if it passes:

```text
Demand proof
+ margin proof
+ competition gap
+ shipping safety
+ low return risk
+ low policy risk
+ strong SEO opportunity
+ clear buyer reason
```

---

# 3. DAILY TRAINING LOOP

## STEP 1 — Product Discovery Practice

### Definition
The machine trains by finding Amazon product candidates that may have eBay demand.

### Execution
Search Amazon.com for 20 candidate products using these filters:
- price between $15 and $80 preferred
- rating 4.2+
- review count 300+
- not dominated by major brands
- clear utility or emotional buying reason
- small/medium size
- not fragile
- not medical
- not supplements
- not cosmetics
- not weapons
- not adult
- not copyrighted/IP-based
- not high-risk electronics
- not seasonal-only unless intentionally testing seasonality

### Output
For each product:
- product name
- ASIN
- Amazon price
- rating
- review count
- category
- main use case
- buyer problem solved
- possible eBay keyword
- initial risk note

### Training Goal
The machine learns to identify products worth investigating, not products worth publishing yet.

---

## STEP 2 — eBay Demand Validation Practice

### Definition
The machine checks if each Amazon candidate has real demand on eBay.

### Execution
For each Amazon candidate, search eBay for:
- active listings
- sold listings
- average sold price
- lowest competitor price
- highest realistic price
- sell-through estimate
- number of competitors
- common title keywords
- common category
- common item specifics
- promoted listing density if visible
- seller feedback level of competitors

### Output
For each product:
- active listing count
- sold listing count
- sell-through estimate
- average sold price
- competition level
- demand score 1–10
- reason demand is strong/weak

### Training Goal
The machine learns that Amazon availability is not enough. eBay demand must be proven.

---

## STEP 3 — Profit Simulation Practice

### Definition
The machine calculates whether the product can be profitable after realistic costs.

### Required Formula

```text
Net Profit =
eBay selling price
- Amazon source cost
- estimated tax/shipping buffer
- eBay final value fee
- payment fee
- promoted listing cost
- AutoDS cost allocation
- refund/return reserve
```

### Execution
For each candidate calculate:
- estimated eBay selling price
- Amazon source cost
- tax/shipping buffer
- estimated eBay/payment fee
- promoted listing cost
- AutoDS cost allocation
- return/refund reserve
- net profit
- net margin %
- break-even promoted cost
- minimum profitable eBay price
- maximum safe Amazon source cost

### Minimum Acceptance Rules
Reject if:
- estimated net profit is under $5
- net margin is under 12–15%
- eBay price must be unrealistically high
- Amazon price changes would immediately destroy margin
- competition is already cheaper than our minimum profitable price

### Output
Product table:
- product
- Amazon cost
- eBay price
- fees
- reserve
- estimated net profit
- margin %
- pass/fail

### Training Goal
The machine learns to protect profit before creating drafts.

---

## STEP 4 — Risk Scoring Practice

### Definition
The machine evaluates account-health and compliance risks before listing.

### Execution
Score each product 1–10 for:
- eBay policy risk
- Amazon fulfillment/seller-of-record risk
- IP/brand/VERO risk
- counterfeit risk
- fragile/damage risk
- high-return risk
- late shipment risk
- stock-out risk
- cancellation risk
- negative feedback risk
- misleading image/title risk

### Automatic Reject Conditions
Reject immediately if:
- famous brand dependency
- unclear authenticity
- IP/copyright character or logo
- high defect complaints
- fragile glass/electronics with weak packaging
- product requires medical/health claims
- supplement/cosmetic/regulated item
- shipping estimate unstable
- out-of-stock risk high
- return complaints are common
- packaging or fulfillment creates unacceptable marketplace risk

### Output
For each product:
- risk score
- exact risk reason
- classification:
  - LOW RISK
  - MEDIUM RISK
  - HIGH RISK
  - REJECT

### Training Goal
The machine learns that account health is more important than short-term revenue.

---

## STEP 5 — Competitor Gap Practice

### Definition
The machine finds how to beat existing eBay listings.

### Execution
For each product that passed margin and risk:
Analyze top eBay competitors:
- weak titles
- missing keywords
- bad photos
- poor descriptions
- unclear item specifics
- weak shipping copy
- bad pricing
- no bundle
- poor trust signals
- poor seller feedback
- slow handling time
- no clear use-case positioning

### Output
For each product:
- top competitor weakness
- our advantage angle
- SEO improvement opportunity
- pricing opportunity
- bundle opportunity
- trust/description improvement

### Training Goal
The machine learns to list only when there is a real advantage.

---

## STEP 6 — eBay SEO Rewrite Practice

### Definition
The machine rewrites Amazon-style product info into eBay-native SEO listings.

### Execution
For approved products generate:
- optimized eBay title
- category suggestion
- item specifics checklist
- 5 bullet benefits
- clean description
- buyer objections + answers
- image selection notes
- return policy recommendation
- handling time recommendation
- promoted listing recommendation

### Title Rules
The title must:
- target eBay buyer search intent
- avoid keyword stuffing
- avoid unsupported claims
- avoid copying Amazon title directly
- avoid brand names unless safe and accurate
- include product type, use case, key feature, size/material when useful

### Output Example

```text
Product:
Amazon Title:
eBay Optimized Title:
Main Keywords:
Category:
Item Specifics Needed:
Description:
Pricing:
Reason This Title Is Better:
```

### Training Goal
The machine learns to transform product data into marketplace-native selling assets.

---

## STEP 7 — AutoDS Draft Strategy Practice

### Definition
The machine prepares products for AutoDS without blindly publishing.

### Execution
For each TEST NOW product define:
- import priority
- draft-only or publish-ready status
- stock monitoring rule
- price-change rule
- minimum profit rule
- out-of-stock action
- supplier change alert
- repricing rule
- manual review checklist
- OWNER_GO requirement

### Output
For each product:
- AutoDS action:
  - DO NOT IMPORT
  - IMPORT AS DRAFT
  - READY FOR OWNER REVIEW
  - PUBLISH ONLY AFTER OWNER_GO
- monitoring settings
- profit protection settings

### Training Goal
The machine learns that AutoDS is an execution layer controlled by validation logic.

---

## STEP 8 — 7-Day Listing Test Practice

### Definition
The machine trains on small controlled tests and learns from marketplace response.

### Execution
For each approved listing after OWNER_GO:
Track for 7 days:
- impressions
- views
- watchers
- clicks
- sales
- price changes
- competitor changes
- stock changes
- margin changes
- buyer questions
- shipping issues
- returns/cancellations

### Output
Daily status:
- listing health
- visibility
- buyer interest
- profit status
- risk status
- recommended action

### Training Goal
The machine learns from real eBay behavior instead of guessing.

---

# 4. KILL / FIX / SCALE RULES

## Kill Rules
Kill or pause if:
- no impressions after test window
- impressions but no views
- views but no watchers/clicks after enough traffic
- price is not competitive
- margin falls below minimum
- Amazon source price increases
- source stock becomes unstable
- eBay competitor undercuts below our profitable price
- risk increases
- buyer complaints appear
- shipping estimate becomes unsafe

## Fix Rules
Fix the listing if:
- impressions are low → improve title/category/item specifics
- views are low → improve main image/title
- watchers exist but no sales → improve price/offer
- clicks exist but no sales → improve description/trust/shipping/returns
- questions repeat → add FAQ
- competitor is stronger → adjust offer or reject

## Scale Rules
Scale only if:
- net profit is positive
- margin remains stable
- source stock is stable
- no account-health risks appear
- no late shipment risk
- no return/defect signals
- listing gets watchers/sales
- competitor pressure is manageable

Never scale only because a product sold once.

---

# 5. WEEKLY TRAINING LOOP

Every week the machine must produce:

## A. Research Summary
- products scanned
- products rejected
- products approved
- best opportunity
- worst risk
- top category
- strongest eBay demand pattern

## B. Product Learning
- which products had demand
- which products failed margin
- which failed due to competition
- which failed due to policy risk
- which failed due to supplier/source risk

## C. Listing Learning
- title patterns that got impressions
- image patterns that got views
- price ranges that got watchers
- categories that performed
- weak description patterns

## D. Profit Learning
- average estimated net profit
- average margin
- products with margin compression
- source price volatility
- promoted listing cost tolerance

## E. Next Week Rules
The machine must update its rules:
- categories to focus on
- categories to avoid
- price bands to focus on
- keywords that performed
- competitor types to avoid
- risk patterns to reject faster

---

# 6. PRODUCT SCORECARD

Use this scoring table for every product.

| Factor | Score 1–10 | Notes |
|---|---:|---|
| eBay demand |  |  |
| sell-through |  |  |
| Amazon source stability |  |  |
| net profit |  |  |
| net margin % |  |  |
| competition gap |  |  |
| SEO opportunity |  |  |
| image/creative strength |  |  |
| return risk |  |  |
| shipping risk |  |  |
| IP/brand risk |  |  |
| policy/account risk |  |  |
| bundle opportunity |  |  |
| scaling potential |  |  |

## Final Classification

```text
Score 85–100: TEST NOW
Score 70–84: WATCHLIST
Score 50–69: RESEARCH MORE
Below 50: REJECT
Any high policy/account risk: REJECT
Any no-margin result: REJECT
```

---

# 7. PRODUCT RESEARCH OUTPUT TEMPLATE

For every research run, produce this file:

```text
REPORTS/EBAY_AUTODS/PRODUCT_RESEARCH_RUN_YYYY_MM_DD.md
```

## Required Structure

```markdown
# Product Research Run — YYYY-MM-DD

## Executive Summary
- Products scanned:
- Products rejected:
- Products approved:
- Best opportunity:
- Highest risk:
- Recommended action:

## Product Comparison Table
| Product | Amazon Cost | eBay Price | Net Profit | Margin % | Demand | Risk | Decision |
|---|---:|---:|---:|---:|---:|---:|---|

## Top 3 TEST NOW

### 1. Product Name
- Amazon source:
- eBay demand evidence:
- Average sold price:
- Estimated net profit:
- Main competitor weakness:
- Main risk:
- Optimized eBay title:
- Recommended price:
- Recommended AutoDS action:
- OWNER_GO required: Yes

### 2. Product Name
...

### 3. Product Name
...

## Rejected Products
| Product | Reason Rejected | Lesson |
|---|---|---|

## Machine Learning Notes
- What worked:
- What failed:
- New rejection rule:
- New opportunity pattern:
- Next run focus:
```

---

# 8. MASTER PROMPT FOR TEST RUN

Use this prompt to make the machine practice.

```text
STEP 1 — EBAY + AMAZON AUTODS PRODUCT RESEARCH TRAINING RUN

Definizione Skill:
Act as an eBay product research and profitability machine. Use Amazon.com as the product/data source and eBay.com as the demand marketplace. Use AutoDS only as the automation/draft execution layer. Your job is not to import products blindly. Your job is to train, validate, reject weak products, and identify only profitable low-risk listing opportunities.

Operating Context:
- Marketplace: eBay.com
- Source/Data: Amazon.com
- Automation: AutoDS
- Mode: Training Run
- Output: Research report + draft recommendations
- No live publishing unless OWNER_GO is explicitly given
- No mass upload
- No risky policy products
- No copyrighted/IP products
- No fake claims
- No fragile/high-return/high-defect products

Objective:
Find 10 Amazon product candidates and validate them against eBay demand, profit potential, competition, risk, SEO opportunity, and AutoDS execution readiness.

Esecuzione:

1. Amazon Product Discovery
Find 10 products with:
- price preferably $15–$80
- rating 4.2+
- review count 300+
- not dominated by major brands
- clear utility/problem-solving/gift/hobby/home value
- low fragility
- low return risk
- no medical/supplement/cosmetic/weapon/adult/IP/copyright risk

Extract:
- product name
- ASIN
- Amazon price
- rating
- review count
- category
- positive review patterns
- negative review patterns
- return/defect risks
- source stability notes

2. eBay Demand Validation
For each product, research eBay:
- active listings
- sold listings
- average sold price
- lowest competitor price
- highest realistic selling price
- sell-through estimate
- number of competitors
- common title keywords
- common item specifics
- competitor listing weaknesses

3. Profit Simulation
Calculate:
- estimated eBay selling price
- Amazon source cost
- tax/shipping buffer
- eBay/payment fees
- promoted listing estimate
- AutoDS allocation
- return/refund reserve
- estimated net profit
- net margin %
- break-even promoted cost
- minimum profitable eBay price

Reject if:
- net profit under $5
- margin under 12–15%
- competition price is below our minimum profitable price
- source price volatility is too dangerous
- product requires unrealistic eBay price

4. Risk Scoring
Score:
- eBay policy risk
- Amazon fulfillment/seller-of-record risk
- IP/brand/VERO risk
- counterfeit risk
- fragile/damage risk
- return risk
- late shipment risk
- stock-out risk
- cancellation risk
- negative feedback risk

Classify:
- LOW RISK
- MEDIUM RISK
- HIGH RISK
- REJECT

5. eBay Listing Optimization
For approved products generate:
- optimized eBay title
- category suggestion
- item specifics checklist
- 5 bullet benefits
- clean description
- buyer objections + answers
- image notes
- price recommendation
- promoted listing recommendation
- handling time recommendation
- return policy recommendation

6. AutoDS Draft Strategy
For each approved product define:
- AutoDS action
- draft/import priority
- minimum profit rule
- stock monitoring rule
- price-change rule
- out-of-stock action
- repricing rule
- manual review checklist
- OWNER_GO requirement

7. Final Decision
Classify each product:
- TEST NOW
- WATCHLIST
- RESEARCH MORE
- REJECT

Output del Risultato:
Create a report called:
PRODUCT_RESEARCH_RUN_001.md

Include:
A. Executive Summary
B. Product Comparison Table
C. Top 3 TEST NOW Deep Dive
D. Rejected Products + reasons
E. AutoDS Draft Recommendations
F. 7-Day Test Plan
G. Kill/Fix/Scale Rules
H. Machine Learning Notes

Archiviazione:
Save the report in:
REPORTS/EBAY_AUTODS/PRODUCT_RESEARCH_RUN_001.md

Sincronizzazione Index:
Update the machine index with:
- date
- products scanned
- products rejected
- products approved
- best opportunity
- highest risk
- new rejection rule
- next run focus

Conferma Visibile:
Show only:
1. Top 3 TEST NOW products
2. Estimated net profit
3. Main eBay demand signal
4. Main risk
5. Recommended AutoDS action
6. OWNER_GO required or not
```

---

# 9. HOW THE MACHINE IMPROVES OVER TIME

The machine improves by storing every result as evidence.

## After Every Run
Save:
- products scanned
- products rejected
- reason rejected
- margin assumptions
- risk findings
- competitor patterns
- titles generated
- actual test results
- kill/fix/scale decision

## After Every Failed Product
Create a lesson:

```text
Product failed because:
- no demand
- weak margin
- too much competition
- risky supplier
- high return risk
- bad SEO
- bad price
- account-health risk
```

Then create a new rule:

```text
Future Rule:
Reject products with [specific pattern] before draft creation.
```

## After Every Winning Product
Create a pattern:

```text
Winning Pattern:
- category:
- price band:
- buyer problem:
- eBay keyword pattern:
- competitor weakness:
- margin structure:
- source characteristics:
- listing angle:
```

Then use the pattern to find similar products.

---

# 10. FINAL OWNER RULE

The machine is authorized to:
- research
- analyze
- compare
- score
- reject
- draft
- recommend
- update internal reports

The machine is not authorized to:
- publish live listings
- change live prices
- scale promoted listings
- mass upload
- message customers
- change store policies
- make external commitments

unless OWNER_GO is explicitly provided.

Final principle:

```text
Research unlimited.
Draft controlled.
Publish with OWNER_GO.
Scale only after profit proof.
Protect account health always.
```
