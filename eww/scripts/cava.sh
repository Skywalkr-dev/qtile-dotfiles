#!/bin/bash

cava -p /dev/stdin <<'EOF' |
[general]
bars = 24
framerate = 30
autosens = 1

[input]
method = pulse
source = auto

[output]
method = raw
raw_target = /dev/stdout
data_format = ascii
ascii_max_range = 8

[smoothing]
monstercat = 1
waves = 0
gravity = 100
ignore = 0
noise_reduction = 77
EOF

while IFS= read -r line; do
    printf '%s\n' "$line" | awk '
    {
        out=""
        for (i=1; i<=length($0); i++) {
            c=substr($0,i,1)

            if      (c == "0") out = out " "
            else if (c == "1") out = out "▁"
            else if (c == "2") out = out "▂"
            else if (c == "3") out = out "▃"
            else if (c == "4") out = out "▄"
            else if (c == "5") out = out "▅"
            else if (c == "6") out = out "▆"
            else if (c == "7") out = out "▇"
            else if (c == "8") out = out "█"
        }
        print out
    }'
done
