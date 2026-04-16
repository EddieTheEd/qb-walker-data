for i in $(seq 1000 3999); do
  for f in science/science-$i-*; do
    [ -e "$f" ] || continue
    if (( i % 2 == 0 )); then
      git mv "$f" science1/
    else
      git mv "$f" science2/
    fi
  done
done

git commit -m "Move files batch 0-999"
