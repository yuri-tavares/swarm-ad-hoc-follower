hol=holo
for arg in `seq 20 20 300 | shuf`; do
  for j in `seq 1 9 | shuf`; do
    bash experiment.sh scripts/NoCoordAlt/$hol/confTRVF\_prob$arg\_$j.sh
  done
done
