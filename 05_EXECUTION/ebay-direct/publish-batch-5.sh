#!/usr/bin/env bash
# eBay Direct — batch publish 5 (SKU list generated from LIVE-verified Amazon prices, 2026-09-04)
# Dry-run dinamico (sha dal pack generato) + 3 fasi idempotenti.
# Routine batch: GO implicito owner (memoria feedback-routine-go).
set -uo pipefail
cd "$(dirname "$0")" || { echo "cd fallito"; exit 1; }

# filled by build step
SKUS=(
US-B00K0157UW
US-B00VNECWSA
US-B016R4B0MY
US-B01H7935D0
US-B06X9X6VYY
US-B0749WPC6V
US-B0753CRLJM
US-B07CRS4FWW
US-B07DBLHZ2L
US-B07M6Y9PMJ
US-B07MLJMMNF
US-B07P4MD2C2
US-B07PDR8CGG
US-B07PSFP38T
US-B07PWN2CW7
US-B07SVQ3RQF
US-B0832PDJG9
US-B0888SRMHS
US-B08FFB9C7P
US-B08FRF12YC
US-B08G53L8B5
US-B08KFXV74T
US-B08S2PG1TK
US-B08SHLNMKR
US-B08ZSMTSVP
US-B092VL9RB1
US-B094JQ9KG9
US-B09JNK5CXF
US-B09XVHV8M1
US-B0CCVQNC7F
US-B0F2F6DT63
US-B0FGPY7D6V
US-B0H1YSN4N6
)

LOG="audit/batch-publish-5-$(date +%Y%m%d-%H%M%S).log"
mkdir -p audit
: > "$LOG"

published=0; blocked=0; error=0
declare -a RESULT_LINES=()

for sku in "${SKUS[@]}"; do
  echo "" | tee -a "$LOG"
  echo "===== $sku =====" | tee -a "$LOG"

  dry=$(deno task cli dry-run --manifest "manifests/$sku.json" --bootstrap audit/bootstrap-production.json 2>&1)
  sha=$(echo "$dry" | grep -oE '"packSha256":"[0-9a-f]{64}"' | head -1 | sed 's/.*:"\([0-9a-f]*\)"/\1/')
  if [ -z "$sha" ]; then
    echo "!! dry-run fallito per $sku" | tee -a "$LOG"
    RESULT_LINES+=("$sku|DRYRUN_FAIL")
    error=$((error+1)); continue
  fi

  inv=$(deno task cli apply-inventory --action-pack "action-packs/$sku.json" --expected-sha256 "$sha" --manifest "manifests/$sku.json" 2>&1)
  echo "$inv" | grep -Eo '\{.*\}' | tee -a "$LOG"

  offer_out=$(deno task cli create-offer --action-pack "action-packs/$sku.json" --expected-sha256 "$sha" --manifest "manifests/$sku.json" 2>&1)
  echo "$offer_out" | grep -Eo '\{.*\}' | tee -a "$LOG"
  offer_id=$(echo "$offer_out" | grep -oE '"offerId":"[0-9]+"' | head -1 | sed 's/.*:"\([0-9]*\)"/\1/')
  if [ -z "$offer_id" ]; then
    echo "!! nessun offerId per $sku (item-specific o errore) — vedi sopra" | tee -a "$LOG"
    RESULT_LINES+=("$sku|NO_OFFER")
    blocked=$((blocked+1)); continue
  fi

  pub=$(deno task cli publish-offer --action-pack "action-packs/$sku.json" --expected-sha256 "$sha" --offer-id "$offer_id" 2>&1)
  echo "$pub" | grep -Eo '\{.*\}' | tee -a "$LOG"
  if echo "$pub" | grep -qE '"outcome":"published"|"listingId"'; then
    lid=$(echo "$pub" | grep -oE '"listingId":"[0-9]+"' | head -1 | sed 's/.*:"\([0-9]*\)"/\1/')
    RESULT_LINES+=("$sku|PUBLISHED|$lid")
    published=$((published+1))
  elif echo "$pub" | grep -qiE 'item specific|aspect|required|missing|error'; then
    RESULT_LINES+=("$sku|BLOCKED_ITEMSPECIFIC")
    blocked=$((blocked+1))
  else
    RESULT_LINES+=("$sku|PUBLISH_ERROR")
    error=$((error+1))
  fi
done

echo "" | tee -a "$LOG"
echo "===== RIEPILOGO =====" | tee -a "$LOG"
for l in "${RESULT_LINES[@]}"; do echo "$l" | tee -a "$LOG"; done
echo "published=$published blocked=$blocked error=$error" | tee -a "$LOG"
echo "FATTO — log: $LOG" | tee -a "$LOG"
