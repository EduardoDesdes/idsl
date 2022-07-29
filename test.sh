((strace -e write=1 -e trace=write -p 711601 2>&1) | stdbuf -o0 grep -oP 'write\(.*?\)' > commands/123.test123)&
