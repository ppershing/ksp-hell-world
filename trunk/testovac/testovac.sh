#!/bin/bash
# @param $1 path_to_source_code
# @param $2 task_name

function die {
    echo $@
    exit 1
}

if [ $# -ne 2 ]; then
    die "Usage: testovac.sh path_to_source_code task_name"
fi
TASKNAME="$2"
SOURCE="$1"
TESTDIR=`dirname $0`
TESTDIR=`readlink -f "$TESTDIR"`

# default constants
BACKUPDIR="$TESTDIR/backup";
SANDBOXDIR="$TESTDIR/sandbox";
TASKDIR="$TESTDIR/tasks";
BINARY="$SANDBOXDIR/hell.bin";
WRAPPERDIR="$TESTDIR"
COMPILESCRIPTDIR="$TESTDIR/compiler"


function backup_sandbox {
    tmpdir=$BACKUPDIR/`date "+%F-%T"`
    mkdir "$tmpdir" || die "Can't backup"
    cp -r "$SANDBOXDIR" "$tmpdir" || die "Can't backup"
    return 0
}

function clean_sandbox {
    rm -rf "$SANDBOXDIR"/* || die "Can't clean sandbox"
}

function copy_wrapper_to_sandbox {
    cp "$WRAPPERDIR/wrapper" "$SANDBOXDIR/wrapper" || die "Can't copy wrapper"
}

# @param task_name
function copy_test_data {
    cp "$TASKDIR/$1"/* "$SANDBOXDIR" || die "Can't copy test data"
}

function copy_compile_script {
    cp "$COMPILESCRIPTDIR"/* "$SANDBOXDIR" || die "Can't copy compilation scripts"
}

# @param $1 path_to_source_code
function compile {
    src=`readlink -f "$1"`
    cd $SANDBOXDIR || die
    ./make_preprocess.py || die "Can't setup compilation"
    chmod +x *.sh
    ./compile.sh "$src" || die "Can't compile file."
}

function run_tests {
    cd $SANDBOXDIR || die
    MEMORY=25600
    TIME=2000
    FULLLOG="" # "--fulllog" to enable full diff
    wrapper_args=" -a0 -f -m$MEMORY -t$TIME"
    ./test.sh $FULLLOG $wrapper_args || die

}

backup_sandbox
clean_sandbox
copy_wrapper_to_sandbox
copy_compile_script
copy_test_data "$TASKNAME"
compile "$SOURCE"
run_tests
exit 0
