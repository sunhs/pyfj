fj() {
    if [ $# -eq 1 ]; then
        if [[ $1 = "-" || $1 -lt 0 ]]; then
            cd $1
            return 0
        fi
    fi

    local dir
    local code

    dir="$(pyfj_cli.py jump $@)"
    code=$?
    if [ $code -eq 0 ]; then
        cd "$dir"
    else
        echo "no match"
    fi
}