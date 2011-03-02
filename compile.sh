cat $@ | ./preprocess.sh > __.cpp;
g++ __.cpp -o hell 2> __.err ||
  (cat __.err | ./recover_errormsg.sh && exit 1)
