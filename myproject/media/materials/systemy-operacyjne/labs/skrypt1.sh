#!/bin/bash
grep "OK D" cdlinux.ftp.log | cut -d '"' -f 2,4 | sort -u | grep -o "cdlinux-.*iso" | sort | uniq -c | sort > wynik1.txt
grep " 20" cdlinux.www.log | cut -d '"' -f 1,2,3 | cut -d ' ' -f 1,7 | cut -d ":" -f 2 | sort -u | grep -o "cdlinux-.*iso" | sort | uniq -c | sort > wynik2.txt

awk '{arr[$2] += $1} END {for (key in arr) print arr[key], key}' wynik1.txt wynik2.txt
