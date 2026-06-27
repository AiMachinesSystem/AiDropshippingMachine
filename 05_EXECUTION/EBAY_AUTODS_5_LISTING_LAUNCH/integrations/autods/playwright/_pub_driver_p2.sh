declare -a JOBS=(
"6a3c8968dded5c227c643610|fire pit cover"
"6a3c818b9c27405eae643247|string lights 96 ft commercial"
"6a3be15e1883684e077f92fa|cast iron skillet set"
"6a3c7a04d2d8ac63b0564650|pool vacuum hose"
"6a3c8776f6ecf06db16066b5|solar pathway lights 8 pack"
"6a3c7eb7dded5c227c6435a0|sectional sofa cover l shape"
"6a3c7e7bdded5c227c64359d|string lights 200 ft led bistro"
"6a3c804a4bb9aa14ed4d168a|solar flame lights"
"6a3c8742dded5c227c6435fe|led outdoor string lights 200 ft"
"6a3c82444bb9aa14ed4d1694|patio chair covers waterproof outdoor lounge"
"6a3c798e4c6cec162e56472e|string lights 96 ft waterproof edison"
"6a3c80e29c27405eae643245|round patio furniture cover"
"6a3c84b6dded5c227c6435e0|patio sofa cover 3 seater"
"6a3c82e74bb9aa14ed4d1699|solar pathway lights 4 pack"
"6a3c80a2f6ecf06db1606673|patio table cover rectangular oval"
"6a3c801219b87e38e4738a8a|solar watering can lantern"
"6a3c87b6f6ecf06db16066b9|patio chair cover waterproof uv"
"6a3c7fdefed157c6ed6065ad|hanging egg chair cover"
"6a3c79c9f6ecf06db1606623|swimming pool brush head 18"
"6a3c8654fed157c6ed6065b7|solar lanterns outdoor 2 pack"
"6a3bc614dbfbc1aaa00c69bd|dog snuffle mat"
"6a3bc3bde005d7fdf315927a|slow feeder dog bowl maze"
"6944529981093377fd673cff|mini flat iron hair straightener"
"6a3c7ce14c6cec162e56474f|inflatable baseball 12 pack"
"6a3c7a3ff6ecf06db160662e|pool float adult inflatable lounger"
"6a377b894ee7478cd887fe30|flameless led tea lights 24 pack"
"6a3c7b2e4bb9aa14ed4d1659|floating drink holder 6 pack"
"6a3bd5a01883684e077f927c|dog nail clippers stainless steel"
)
N=0; PUB=0
for j in "${JOBS[@]}"; do
  ID="${j%%|*}"; G="${j##*|}"; N=$((N+1))
  echo "===== [$N] $ID :: $G ====="
  OUT=$(PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe publish_one_draft.py "$ID" "$G" 2>&1)
  echo "$OUT" | grep -E "RESULT:|draft title:"
  if echo "$OUT" | grep -q "RESULT: PUBLISHED"; then PUB=$((PUB+1)); fi
  if echo "$OUT" | grep -q "BLOCKED-EBAY-RESTRICTION"; then
    echo "!!! STOP: eBay restriction at [$N]. Halting."; break
  fi
done
echo "DRIVER DONE | PUBLISHED_THIS_RUN=$PUB"
