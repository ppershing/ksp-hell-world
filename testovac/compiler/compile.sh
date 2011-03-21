if [ $# -ne 1 ]; then
    echo "Usage: compile.sh filename"
    exit 1
fi

filename="$1"
if [ "${filename: -6}" == ".hellc" ]; then
    cat "$filename" | bash ./preprocess_cpp.sh > __.cpp;
    g++ -static -W -Wall __.cpp -o hell 2> __.err ||
      (cat __.err | bash ./recover_errormsg.sh && exit 1)
elif [ "${filename: -6}" == ".hellp" ]; then
    cat "$filename" | bash ./preprocess_pas.sh > __.pas;
    fpc -ve -viwn __.pas -ohell 2> __.err ||
      (cat __.err | bash ./recover_errormsg.sh && exit 1)
else
    echo "Unknown extension";
    exit 1;
fi
