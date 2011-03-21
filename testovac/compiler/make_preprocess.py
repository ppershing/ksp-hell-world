#!/usr/bin/python
SUBST_CPP = {
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
  'long long' : 'unnatural', 
  'unsigned' : 'holy',
  'const' : 'dead',
  'string': 'chain',
  #string.h
  'strlen': 'chainlen',
  'strcmp': 'chaincmp',
  'sscanf': 'listenToChain',
  #keywords
  'return' : 'live',
  'for' : 'fear',
  'while' : 'whimper',

  'if' : 'trap',
  'else' : 'escape',
  'elseif': '__undef__',

  #functions
  'printf' : 'moan',
  'scanf' : 'listenToScreams',
  'stdin' : 'ears',
  'fgets' : 'listenWholeSentence',
  'feof' : 'nothingToHear',

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
  'struct' : 'TODO',

  'delete' : 'kill',
  'new' : 'spawn',

}
#shout, knife, stab, saw, candle, fire, howl
SUBST_PAS = {
  # types
  'longint' : 'bloody',
  'int64' : 'unnatural',
  'double' : 'demonic',
  'string' : 'chain',
  'char' : 'syllable',
  'const' : 'dead',
  #keywords
  'begin' : 'birth',
  'end' : 'death',
  'to' : 'tooSoon',
  'downto' : '_internal_',
  'for' : 'fear',
  'do' : 'doom',
  'case' : 'switch',
  'class' : '_undef_',
  'var' : 'summon', 

  'if' : 'trap',
  'else' : 'escape',
  'function' : 'invocation',
  'procedure' : 'ritual',
  'goto': 'fall',
  'nil' : '_undef_',
  'record' : 'TODO',
  'class' : 'cage',
  'object' : '_undef_',
  'repeat' : 'andAgainAndAgainAndAgain',
  'then' : 'so',
  'until' : '_undef_',
  'uses' : 'explore',

  # io
  'write' : 'moan',
  'writeln' : 'moanSentence',
  'read' : 'listenToScreams',
  'readln' : 'listenToSentence',

  # operators
  'and' : 'together',
  'or' : 'split',
  'div' : 'slash',
  'mod' : 'corpse',
  # bool
  'true' : 'sacred',
  'false' : 'lie',
}

NON_ALPHA = '[^a-zA-Z0-9_]'


def write_substitution_script(filename, SUBST):
    f = open(filename, "w")
    print >>f, "#!/bin/bash"
    print >>f, "sed 's/\\(.*\\)/ \\1 /' | \\"
    for k in SUBST.keys():
      # undefine original
      print >>f, "  sed 's/\\(" + NON_ALPHA +"\\)" + \
        k + "\\(" + NON_ALPHA + "\\)/\\1__UNDEFINED__" + k + "\\2/g' | \\"
      # replace alias
      print >>f, "  sed 's/\\(" + NON_ALPHA +"\\)" + \
        SUBST[k] + "\\(" + NON_ALPHA + "\\)/\\1"+ k +"\\2/g' | \\"
    print >>f, "  cat"


def write_reverse_substitution_script(filename, SUBST):
    f = open("recover_errormsg.sh", "w");
    print >>f, "sed 's/\\(.*\\)/ \\1 /' | \\"
    for k in SUBST.keys():
      # replace alias
      print >>f, "  sed 's/\\(" + NON_ALPHA +"\\)" + \
        k + "\\(" + NON_ALPHA + "\\)/\\1"+ SUBST[k] +"\\2/g' | \\"
    print >>f, "  cat"

write_substitution_script("preprocess_cpp.sh", SUBST_CPP)
write_substitution_script("preprocess_pas.sh", SUBST_PAS)
write_reverse_substitution_script("recover_errormsg.sh", dict(SUBST_CPP, **SUBST_PAS));
