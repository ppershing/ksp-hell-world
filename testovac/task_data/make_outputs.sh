echo "generating outputs for all inputs"
echo "compiling program"

if [ -f solution.cpp ]; then
    g++ solution.cpp -W -Wall -o solution
elif [ -f solution.hs ]; then
    ghc solution.hs -W -O2 -o solution
fi;

if [ "$?" -ne 0 ]; then
    echo "problem compiling solution"
    exit 1
fi;

echo "removing all outputs"
rm *.out

for infile in *.in; do
    echo ""
    echo "generating out for $infile"
    base=`basename $infile .in`
    outfile=$base.out
    time ./solution <$infile >$base.tst
    if [ "$?" -ne 0 ]; then
        echo -n "Problem generating output"
        echo "at input $base"
        exit 1
    fi;
done

echo "removing compiled solution"
rm solution
if [ -f solution.hs ]; then
    rm solution.hi
    rm solution.o
fi;

echo "all done"
exit 0;
