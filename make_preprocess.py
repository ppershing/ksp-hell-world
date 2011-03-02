#!/usr/bin/python
SUBST = {
  'int' : 'bloody',
  'double' : 'demonic',
  'bool' : 'questionable',
  'false' : 'lie',
  'true' : 'sacred',
  'void' : 'dark',
  'char' : 'syllable',
  'signed' : 'sinned',
  'short' : 'shit',
  'long' : '____',
  'long long' : 'struggling', 
  'unsigned' : 'holy',
  'include' : 'brains',
  'printf' : 'whisper',
  'scanf' : 'listenToScreams',
  'stdio' : 'stdsounds',
  #'hell' : 'hello',
  'for' : 'fear',
  'string': 'chain',
  'namespace' : 'room',

  'cout' : 'shout',
  'endl' : 'shriek',
  'cin' : 'hearWhispers',

  'this' : 'mine',

  'delete' : 'kill',
  'new' : 'spawn',

  'return' : 'live',
  'while' : 'whine',

  'class' : 'cage',

  'if' : 'trap',
  'else' : 'escape',
  'elseif': '__undef__',
}
#shout, knife, stab, saw, candle, fire, howl


NON_ALPHA = '[^a-zA-Z0-9]'
f = open("preprocess.sh", "w")
print >>f, "#!/bin/bash"
print >>f, "sed 's/\\(.*\\)/ \\1 /' | \\"
for k in SUBST.keys():
  # undefine original
  print >>f, "  sed 's/\\(" + NON_ALPHA +"\\)" + \
    k + "\\(" + NON_ALPHA + "\\)/\\1__UNDEFINED__\\2/g' | \\"
  # replace alias
  print >>f, "  sed 's/\\(" + NON_ALPHA +"\\)" + \
    SUBST[k] + "\\(" + NON_ALPHA + "\\)/\\1"+ k +"\\2/g' | \\"

print >>f, "  cat"

f = open("recover_errormsg.sh", "w");
print >>f, "sed 's/\\(.*\\)/ \\1 /' | \\"
for k in SUBST.keys():
  # replace alias
  print >>f, "  sed 's/\\(" + NON_ALPHA +"\\)" + \
    k + "\\(" + NON_ALPHA + "\\)/\\1"+ SUBST[k] +"\\2/g' | \\"

print >>f, "  cat"
