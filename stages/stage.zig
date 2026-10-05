const std = @import("std");

pub fn main() !void {
    const stdin = std.io.getStdIn().reader();
    var buf: [8192]u8 = undefined;
    const n = try stdin.readAll(&buf);
    const trimmed = std.mem.trim(u8, buf[0..n], " \t\r\n");
    const stdout = std.io.getStdOut().writer();
    try stdout.print("{s} -> Zig", .{trimmed});
}
