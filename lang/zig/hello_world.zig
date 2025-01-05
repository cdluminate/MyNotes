const std = @import("std");

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    try stdout.print("Hello, {s} World! {d}\n", .{"Zig", 100});

    std.debug.print("debug print\n", .{});
}
