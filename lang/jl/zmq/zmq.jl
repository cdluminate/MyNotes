using ZMQ

server = Socket(REP)
client = Socket(REQ)
addr = "tcp://127.0.0.1:5555"

bind(server, addr)
connect(client, addr)

send(client, "request")
println("<-", "request")
msg = recv(server, String)
println("->", msg)
send(server, "response")
println("<-", "response")
close(server)
close(client)
