#!/bin/bash

changetime="$1"

[[ -z "${changetime}" ]] && { echo "time is null" ;exit 0; }

date -s "$changetime"
