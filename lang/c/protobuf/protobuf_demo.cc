/*
   Protocol buffers are a flexible, efficient, automated mechanism
   for serializing structured data

   @reference https://developers.google.com/protocol-buffers/docs/overview
   @reference https://developers.google.com/protocol-buffers/docs/proto
   @reference https://developers.google.com/protocol-buffers/docs/cpptutorial
 */

#include "person.pb.h"
#include <fstream>
#include <iostream>

using namespace std;

int
main (void)
{
  cout << "create and save protobuf" << endl;
  {
    Person person;
    person.set_name("John Doe");
    person.set_id(1234);
    person.set_email("jdoe@example.com");
    cout << "Name: " << person.name() << endl;
    cout << "E-mail: " << person.email() << endl;
    fstream output("myfile", ios::out | ios::binary);
    person.SerializeToOstream(&output);
  }

  cout << "read file and restore protobuf" << endl;
  {
    fstream input("myfile", ios::in | ios::binary);
    Person person;
    person.ParseFromIstream(&input);
    cout << "Name: " << person.name() << endl;
    cout << "E-mail: " << person.email() << endl;
  }

  return 0;
}
