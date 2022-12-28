use NativeCall;
sub sin(num64) returns num64 is native("m", v6) { * }
say sin(0.1.Num);
