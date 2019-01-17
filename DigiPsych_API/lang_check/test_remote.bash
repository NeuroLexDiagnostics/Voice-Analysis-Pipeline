#!/bin/bash

set -eux

readonly port=8081

# TODO: Find this more portably.
readonly jar='./build/lib/language_check/LanguageTool-3.1/languagetool-server.jar'

java -cp "$jar" org.languagetool.server.HTTPServer --port "$port" &
java_pid=$!

clean ()
{
    kill "$java_pid"
}
trap clean EXIT

echo 'This is okay.' | \
    language-check --remote-host localhost --remote-port "$port" -

! echo 'This is noot okay.' | \
    language-check --remote-host localhost --remote-port "$port" -
