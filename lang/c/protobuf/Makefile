main:
	protoc -I=. --cpp_out=. person.proto
	g++ -Wall person.pb.cc -c -o person.pb.o
	g++ -Wall protobuf_demo.cc person.pb.o -lprotobuf -o demo
clean:
	-rm person.pb.cc person.pb.h person.pb.o myfile a.out demo
