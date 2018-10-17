#! /bin/bash

for test in ./board-tests/*in*.json
    do
        DIFF=$(cat "$test" | python3 xboard | diff --strip-trailing-cr "${test/in/out}" -)
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
