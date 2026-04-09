# Smalltalk _brain — palace index
# Run: smalltalk palace index _brain/ to regenerate

WING:   brain | type:topic | keywords:patterns+decisions+wins+errors+brain
ROOM:   patterns | wing:brain | hall:PATTERN+NOTE | file:patterns/patterns.st
LAYER:  L1 | file:_index.st | load:always
LAYER:  L2 | trigger:topic  | source:navigate
