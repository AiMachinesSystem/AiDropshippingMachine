declare -a JOBS=(
"6a3c8d8df6ecf06db16066e4|slide out cabinet"
"6a3c8fb319b87e38e4738af2|64 drawer"
"6a3c8eea4bb9aa14ed4d1706|stackable food storage"
"6a3c8e0619b87e38e4738ae5|airtight food storage containers 32"
"6a3c8f3f4c6cec162e5647e4|stackable storage bins"
"6a3c8968dded5c227c643610|fire pit cover"
"6a3c889f4c6cec162e5647b4|adirondack"
"6a3d089724cbed43294c99dd|under sink organizer"
"6a3d084b2478c0a6dbe0a7e7|pool cover pump"
"6a3d090d2478c0a6dbe0a7f1|rice dispenser"
"6a3cf579dd3641e3b9015563|hair catcher"
"6a3c88a319b87e38e4738ac1|water soakers"
"6a3c887aa62e5d76174d11dd|inflatable drink holders"
)
N=0
for j in "${JOBS[@]}"; do
  ID="${j%%|*}"; G="${j##*|}"; N=$((N+1))
  echo "===== [$N] $ID :: $G ====="
  OUT=$(PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe publish_one_draft.py "$ID" "$G" 2>&1)
  echo "$OUT" | grep -E "RESULT:|draft title:|MESSAGES:"
  if echo "$OUT" | grep -q "BLOCKED-EBAY-RESTRICTION"; then
    echo "!!! STOP: eBay restriction hit at [$N]. Halting to protect account."; break
  fi
done
echo "DRIVER DONE"
