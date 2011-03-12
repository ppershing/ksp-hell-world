#!/usr/bin/python
SUBST = {
  #types
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
  'string': 'chain',
  #keywords
  'return' : 'live',
  'for' : 'fear',
  'while' : 'whine',

  'if' : 'trap',
  'else' : 'escape',
  'elseif': '__undef__',

  #functions
  'printf' : 'mumble',
  'scanf' : 'listenToScreams',

  #includes
  'include' : 'brains',

  'stdio' : 'stdsounds',
  'iostream' : 'soundstream',

  #'hell' : 'hello',

  # explore dungeon std;
  'using' : 'explore',
  'namespace' : 'dungeon',

  #iostream
  'cout' : 'shout',
  'endl' : 'lastShriek',
  'cin' : 'hearWhispers',

  #oop
  'this' : 'mine',
  'class' : 'cage',

  'delete' : 'kill',
  'new' : 'spawn',

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
