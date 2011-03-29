from sys import stdin;
from sys import stdout;
import random;

colors = {
  'red' : 'red',
  'green': 'green',
  'include': 'green',
  'yellow' : 'yellow',
  'dark' : 'black',
  'function' : 'yellow',
  'type' : 'green',
  'black' : 'black',
  'keyword' : 'blue',
  'operator' : 'green',
  'biela' : 'white',
  'biela2' : 'star',
}

word_colors = {
  'bloody': {
    'color': colors['red'],
  },
  'demonic': {
    'color': colors['red'],
  },
  'questionable' : {
    'color' : colors['type'],
  },
  'lie' : {
    'color' : colors['red'],
  },
  'sacred' : {
    'color' : colors['red'],
  },
  'dark' : {
    'color' : colors['black'],
  },
  'syllable' : {
    'color' : colors['type'],
  },
  'sinned' : {
    'color' : colors['type'],
  },
  'shit' : {
    'color' : colors['type'],
  },
  'unnatural' : {
    'color' : colors['type'],
  },
  'holy' : {
    'color' : colors['type'],
  },
  'chainlen' : {
    'color' : colors['function'],
  },
  'chaincmp' : {
    'color' : colors['function'],
  },
  'chain' : {
    'color' : colors['type'],
  },
  'listenToChain' : {
    'color' : colors['function'],
  },
  'live' : {
    'color' : colors['keyword'],
  },
  'fear' : {
    'color' : colors['keyword'],
  },
  'whine' : {
    'color' : colors['keyword'],
  },
  'escape' : {
    'color' : colors['keyword'],
  },

  'moan' : {
    'color' : colors['function'],
  },
  'listenToScreams' : {
    'color' : colors['function'],
  },
  'ears' : {
    'color' : colors['yellow'],
  },
  'listenToWholeSentence' : {
    'color' : colors['function'],
  },
  'nothingToHear' : {
    'color' : colors['function'],
  },

  '#brains': {
    'color' : colors['include'],
  },
  'stdsounds.h': {
    'color' : colors['include'],
  },
  'soundstream': {
    'color' : colors['include'],
  },
  'explore': {
    'color' : colors['keyword'],
  },
  'dungeon': {
    'color' : colors['keyword'],
  },
  'shriek' : {
    'color' : colors['function'],
  },
  'lastShriek' : {
    'color' : colors['function'],
  },
  'hearWhispers' : {
    'color' : colors['function'],
  },
  'mine' : {
    'color' : colors['keyword'],
  },
  'cage' : {
    'color' : colors['keyword'],
  },
  'spawn' : {
    'color' : colors['red'],
  },
  'kill' : {
    'color' : colors['red'],
  },
  'so' : {
    'color' : colors['keyword'],
  },
  'birth' : {
    'color' : colors['keyword'],
  },
  'death' : {
    'color' : colors['keyword'],
  },
  'tooSoon' : {
    'color' : colors['keyword'],
  },
  'doom' : {
    'color' : colors['keyword'],
  },
  'summon' : {
    'color' : colors['keyword'],
  },
  'invocation' : {
    'color' : colors['keyword'],
  },
  'ritual' : {
    'color' : colors['keyword'],
  },
  'andAgainAndAgainAndAgain' : {
    'color' : colors['keyword'],
  },
  'tillSpoonBreaks' : {
    'color' : colors['keyword'],
  },
  'moanSentence' : {
    'color' : colors['function'],
  },
  'listenToSentence' : {
    'color' : colors['function'],
  },
  'together' : {
    'color' : colors['operator'],
  },
  'split' : {
    'color' : colors['operator'],
  },
  'slash' : {
    'color' : colors['operator'],
  },
  'remnants' : {
    'color' : colors['operator'],
  },
  'biela' : {
    'color' : colors['biela'],
  },
  'white' : {
    'color' : colors['biela'],
  },
  'blanco' : {
    'color' : colors['biela'],
  },
  'weiss' : {
    'color' : colors['biela'],
  },
  '*' : {
    'color' : colors['biela2'],
  },
  '+' : {
    'color' : colors['biela2'],
  },
  '/' : {
    'color' : colors['biela2'],
  },
  '-' : {
    'color' : colors['biela2'],
  },
}

def try_concat(words, length):
  out = ''
  while (len(out) < length):
    out = out + ' ' + random.choice(words)
  return out

def vypis(farba, pocet):
  pouzitelne = [];
  for x in word_colors.keys():
    if word_colors[x]['color'] == farba:
      pouzitelne.append(x)

  best = 'x' * 1000;

  sequence = {
    'blue' : "\x1b[0;34m",
    'green' : "\x1b[0;32m",
    'yellow' : "\x1b[1;33m",
    'white' : "\x1b[1;37m",
    'star' : "\x1b[1;37m",
  }

  for i in range(1, 1000):
    t = try_concat(pouzitelne, pocet + 1)
    if len(t) < len(best):
      best = t

  stdout.write(sequence[farba])
  stdout.write(best)

for line in stdin:
  line = line.rstrip();
  tokens = line.split(' ');
  while tokens:
    col = tokens[0]
    pocet = int(tokens[1])
    tokens = tokens[2:]
    vypis(col, pocet)
  print

