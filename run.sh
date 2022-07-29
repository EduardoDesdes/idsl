echo "Presion Ctrl + c para cancelar el proceso..."
rm shells
touch shells

time=`date -d "2000-01-01 GMT" '+%s'`

while true;do
  LISTBASH=$(ps axo user:20,pid,comm | grep -v root | grep bash | awk '{print $2","$1}')
  for i in $LISTBASH;do
    if ! (cat shells | grep $i 2>&1 >/dev/null);then
      echo $i >> shells
      #Command
      # (strace -e write=1 -e trace=write -p PID 2>&1) | stdbuf -o0 grep -oP 'write\(.*?\)' > /tmp/sniffx
      uPID=`echo $i | cut -d ',' -f 1`
      uUSR=`echo $i | cut -d ',' -f 2`
      ((strace -e write=1 -e trace=write -p $uPID 2>&1) | stdbuf -o0 grep -oP 'write\(.*?\)' >> /root/idsl/commands/$uPID.$uUSR)&
      PROCCESO=`echo $!`
      echo "[*] Se detecta una shell en el proceso $uPID, relacionada al usuario $uUSR."
      echo "[*] Se realiza el snif en el proceso $PROCCESO"
    fi
  done
  python3 /root/idsl/main.py >> /root/idsl/log/$time.log
done
