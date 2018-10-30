#! /bin/bash
# This script relies on being executed from ${GIT_ROOT}/7
# USAGE:
#       ./testme.sh
#       bash testme.sh


for test in ./rules-tests/*in*.json
    do
        DIFF=$(cat "$test" | python3 xrules | diff --strip-trailing-cr "${test/in/out}" -)
        echo "$test"
        echo "------------------------"
        if [ "$DIFF" != "" ]; then
            echo "Test Failed!"
            echo "$DIFF"
        else
            echo "Test Passed!"
        fi
        echo "------------------------"
    done
