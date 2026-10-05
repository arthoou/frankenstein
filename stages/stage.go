package main
import("bufio";"fmt";"os";"strings")
func main(){b:=bufio.NewReader(os.Stdin);s,_:=b.ReadString(0);fmt.Print(strings.TrimSpace(s)+" -> Go")}
