echo "<font color='yellow'> <h2> Welcome to testing session </h2> </font>"

SHOW_DIFF=0
if [ "$1" == "--fulllog" ]; then
    SHOW_DIFF=1
    shift
fi
echo "<p><font color='yellow'> Test parameters I'm using now are: '$*', "
echo "full_log_enabled: $SHOW_DIFF </font></p>"

for infile in *.in; do
    echo "<p><font color='yellow'> ********* "
    echo "Testing $infile ******** </font><br>"

    base=`basename $infile .in`
    outfile=$base.out
    tstfile=$base.tst
    difffile=$base.diff
    echo -n "<font color='yellow'> running... </font> <pre>"
    ./wrapper $* ./program -i$infile -o$outfile &>tmp
    RETVAL=$?
    cat tmp
    echo "</pre>"

    if grep EXC tmp; then
        echo "<font color='red'> Your program received a signal. This means that"
        echo "probably you have index out of bounds or other memory"
        echo "corruption.<br>"
        echo "But note, that this could mean your program did not fit"
        echo "into alloted memory (buy more memory) </font><br>"
    fi

    if grep TLE tmp; then
        echo "<font color='red'>Your program did not finish "
        echo "in specified time (buy more time)</font><br>"
    fi

    if grep SEC tmp; then
        echo "<font color='red'>Security violation! You tried to access some files "
        echo "or use some nasty functions</font><br>"
    fi

    if [ "$RETVAL" -ne 0 ]; then
        echo -n "<font color='red'> ****** Program ended unexpectedly "
        echo "at input $base </font>"
        exit 1
    fi;
    echo "<font color='yellow'> program exitted normally"
    echo "checking output for validity...</font><br>"

    diff $outfile $tstfile > $difffile;
    DIFFRES=$?

    if [ $SHOW_DIFF -ne 0 ]; then
        echo "<font color='yellow'> Diff: </font><pre> "
        cat $difffile | sed 's/</≪/' \
                | sed 's/>/≫/' \
                | sed 's/&/∝/';
        echo "</pre>";
    fi

    if [ "$DIFFRES" -ne 0 ]; then
        echo -n "<font color='red'> **** The output of testcase "
        echo " $base is not correct </font>"
        exit 1
    fi;
    echo "<font color='green'> OK, empty diff </font>"
    echo "</p>"
done
echo "<font color='green'> Everything seems to be OK, accepting </font>"
exit 0;
