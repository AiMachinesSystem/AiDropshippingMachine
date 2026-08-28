#!/usr/bin/env bash
# eBay Direct — batch publish 4 (20 SKU, up-ticket, top by net profit)
# Dry-run dinamico (sha dal pack generato) + 3 fasi idempotenti.
# Routine batch: GO implicito owner (memoria feedback-routine-go).
set -uo pipefail
cd "$(dirname "$0")" || { echo "cd fallito"; exit 1; }

SKUS=(
US-B0D59WHNGP
US-B08HCMKN8P
US-B002WP1R1W
US-B07MBFMG5W
US-B0063879QQ
US-B07SQH3FCT
US-B07JYW65Y5
US-B07WD9YQZG
US-B074W2DT3N
US-B071X64XQX
US-B072N2BSGD
US-B09VX9MGX7
US-B0DBYLD9WY
US-B0GHNFQGN1
US-B08HCMQ1H6
US-B07YF74Z4T
US-B07YF53FFD
US-B07ZTFVZXJ
US-B00K027D0S
US-B001ESO9KO
)

LOG="audit/batch-publish-4-$(date +%Y%m%d-%H%M%S).log"
mkdir -p audit
: > "$LOG"

published=0; blocked=0; error=0
declare -a RESULT_LINES=()

for sku in "${SKUS[@]}"; do
  echo "" | tee -a "$LOG"
  echo "===== $sku =====" | tee -a "$LOG"

  # dry-run -> packSha256
  dry=$(deno task cli dry-run --manifest "manifests/$sku.json" --bootstrap audit/bootstrap-production.json 2>&1)
  sha=$(echo "$dry" | grep -oE '"packSha256":"[0-9a-f]{64}"' | head -1 | sed 's/.*:"\([0-9a-f]*\)"/\1/')
  if [ -z "$sha" ]; then
    echo "!! dry-run fallito per $sku" | tee -a "$LOG"
    RESULT_LINES+=("$sku|DRYRUN_FAIL")
    error=$((error+1)); continue
  fi

  # apply-inventory
  inv=$(deno task cli apply-inventory --action-pack "action-packs/$sku.json" --expected-sha256 "$sha" --manifest "manifests/$sku.json" 2>&1)
  echo "$inv" | grep -Eo '\{.*\}' | tee -a "$LOG"

  # create-offer
  offer_out=$(deno task cli create-offer --action-pack "action-packs/$sku.json" --expected-sha256 "$sha" --manifest "manifests/$sku.json" 2>&1)
  echo "$offer_out" | grep -Eo '\{.*\}' | tee -a "$LOG"
  offer_id=$(echo "$offer_out" | grep -oE '"offerId":"[0-9]+"' | head -1 | sed 's/.*:"\([0-9]*\)"/\1/')
  if [ -z "$offer_id" ]; then
    echo "!! nessun offerId per $sku (item-specific o errore) — vedi sopra" | tee -a "$LOG"
    RESULT_LINES+=("$sku|NO_OFFER")
    blocked=$((blocked+1)); continue
  fi

  # publish-offer
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
