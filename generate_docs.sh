#!/usr/bin/env bash
###
 # Utility script to auto-generate/auto-update sphinx docs for project.
 # Because I'm not sure I'll remember the exact commands in the future.
 #
 # Note that some manual updating might be required, after initial generation.
 # But this is at least a start, for any instance after the project is updated and docs need to be remade.
 ##


# Stop on error.
set -e


# Ensure bash is executing from project root, regardless of where it was invoked from.
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"


# Auto-generate docs source files, from actual Python code in project.
sphinx-apidoc -o ./docs/source/ ./django_expanded_test_cases/

# Generate sphinx docs from source files.
sphinx-build ./docs/source/ ./docs/build/


# Remove modules .rst file, because we don't actually care about it.
if [[ -f "./docs/source/modules.rst" ]]
then
    rm ./docs/source/modules.rst
fi