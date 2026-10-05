import Foundation
let data = FileHandle.standardInput.readDataToEndOfFile()
let s = String(data: data, encoding: .utf8)?.trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
print(s + " -> Swift", terminator: "")
