#!/bin/bash

echo "script running"
if [ -n "$1" ]; then
  echo -n "Printing arg: "
  echo $1
else
  echo "Default print"
fi
