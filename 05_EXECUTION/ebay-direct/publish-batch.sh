#!/usr/bin/env bash
# eBay Direct — batch publish (20 SKU, top by net profit)
#
# Ogni write e' gated da --expected-sha256 (hash del pack, gia' commitato).
# Le 3 fasi sono idempotenti: apply-inventory ("unchanged" se gia' presente),
# create-offer ("reused" se esiste), publish-offer ("already_published" se live).
# Eseguire SOLO dall'owner: e' il suo keystroke = GO per le 20 pubblicazioni.
set -uo pipefail

cd "$(dirname "$0")" || { echo "cd fallito"; exit 1; }

# SKU|packSha256
SKUS=(
"AE-1005006695661987|bee652399026bc10ee46354ca5a784c7dba996d822e768a3015f14602933ea75"
"AE-3256806985368273|8d72ec90b52577bf95c0eabbc7108d61e04d9fb17a4164ee9bb204457e891179"
"AE-3256807891363426|15473577f4eab02bcf9e6c1323610a3e4a515f00c3a264570a12b01269dd1e2b"
"AE-1005007635138561|c279d8aaad5a6fcd06eb72115a1fd5ceb87f29078453cdb9248c396730363f4e"
"AE-1005006727725208|4df34b851a8dad3cbc68a7be3fbf596675eee42185591d3c0fcad29731b6ef14"
"AE-1005010002169658|1c70ccaae3af2c9a56806ddf115ed8e39a5bac67bd9895714ff53eeb9abe8886"
"AE-1005009366884119|06d376ff80d5104c8fabbdab7a13f5c7ea585b3e95ba789af73ae2e74a9ee714"
"AE-3256806518016932|8f33ba7d998f84991e859f0765673a8fb991a197d6c5514dcc7aa0b41920c29a"
"AE-1005005638658052|181bb01d56101c070165482ee79cd04361ae9c74d883c3fcbb968333f9393418"
"AE-1005007856972957|31b15e3f971e5fd74e2eec7a97df5007d1fb2fd43ae17d4dc79daebe65b5b147"
"AE-3256806675414853|2464e0d8150a5ff2074c61fb466a1cf13bd39c660785ff70910adb8bd5cf9061"
"AE-1005007583827147|af18ae38f7e73cca570f6bd4c177c7fb49199ccb86b7d2be2582c949f8d0702c"
"AE-1005006381299125|1eee090d8c4d7d1cdd6ed660df993ec9efa5d119c885f4d293bfe87b881f2ea1"
"AE-1005007857231190|4a11ffb843ac9ba313424d93c417cfbf8f68ce96c15cd92ec72c3e852fd1def8"
"AE-3256806852591311|b5791bd8959909dfc490b955ff9d7733b868771a7614e17933df660abcc1aab2"
"AE-3256810466984003|dfb16eea640305275f0863f69124c39dc79cf62d586e36fb8aeb330524c1b8b7"
"AE-1005007010007533|77261b79142888a58e6e19ca3141ff6e4e71985786495cac88d49ab197c098c8"
"AE-1005009472550839|1473084ed3be757b6f00d787f129db442ff7331bb3d64b8822399bc9bf48872b"
"AE-3256807032522577|fa706d96b90dba0fd4dca13d8cc1811bc0b90235fb78dd6f1da1fd7ab0130ad6"
"AE-1005009383964875|491767235c37f2fbc6223c17913957415bedcf031edbdf5440e68ac2a13148ca"
)

LOG="audit/batch-publish-$(date +%Y%m%d-%H%M%S).log"
mkdir -p audit
: > "$LOG"

echo "Batch publish — avvio $(date '+%F %T')" | tee -a "$LOG"

for entry in "${SKUS[@]}"; do
  sku="${entry%%|*}"
  sha="${entry##*|}"
  echo "" | tee -a "$LOG"
  echo "===== $sku =====" | tee -a "$LOG"

  echo "--- apply-inventory ---" | tee -a "$LOG"
  deno task cli apply-inventory --action-pack "action-packs/$sku.json" --expected-sha256 "$sha" --manifest "manifests/$sku.json" 2>&1 | tee -a "$LOG"

  echo "--- create-offer ---" | tee -a "$LOG"
  offer_out=$(deno task cli create-offer --action-pack "action-packs/$sku.json" --expected-sha256 "$sha" --manifest "manifests/$sku.json" 2>&1)
  echo "$offer_out" | tee -a "$LOG"
  offer_id=$(echo "$offer_out" | sed -n 's/.*"offerId": *"\([^"]*\)".*/\1/p')

  if [ -z "$offer_id" ]; then
    echo "!! nessun offerId per $sku — salto publish" | tee -a "$LOG"
    continue
  fi

  echo "--- publish-offer ($offer_id) ---" | tee -a "$LOG"
  deno task cli publish-offer --action-pack "action-packs/$sku.json" --expected-sha256 "$sha" --offer-id "$offer_id" 2>&1 | tee -a "$LOG"
done

echo "" | tee -a "$LOG"
echo "FATTO — log: $LOG" | tee -a "$LOG"
