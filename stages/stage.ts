const buf = new Uint8Array(65536);
let s = "";
while (true) {
  const n = await Deno.stdin.read(buf);
  if (n === null) break;
  s += new TextDecoder().decode(buf.subarray(0, n));
}
console.log(s.trim() + " -> TypeScript");
