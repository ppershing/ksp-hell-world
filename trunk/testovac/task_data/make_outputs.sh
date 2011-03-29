#!/bin/bash
echo "generating outputs for all inputs"
echo "compiling program"


COMPILER="../../compiler"
if [ -f solution.hellc ]; then
    rm tmp -rf tmp
    mkdir tmp
    cp solution.hellc tmp
    cp -r "$COMPILER"/* "tmp"
    (cd tmp && python ./make_preprocess.py && ./compile.sh solution.hellc)
else
    echo "No solution found!"
    exit 1
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
    time tmp/hell <$infile >$base.tst
    if [ "$?" -ne 0 ]; then
        echo -n "Problem generating output"
        echo "at input $base"
        exit 1
    fi;
done

echo "removing compiled solution"
rm -rf tmp

echo "all done"
exit 0;
