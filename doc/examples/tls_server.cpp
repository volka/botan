/*
* (C) 2008 Jack Lloyd
*
* Distributed under the terms of the Botan license
*/

#include <botan/botan.h>
#include <botan/tls_server.h>
#include <botan/unx_sock.h>

#include <botan/rsa.h>
#include <botan/dsa.h>
#include <botan/x509self.h>

using namespace Botan;

#include <stdio.h>
#include <string>
#include <iostream>
#include <memory>

int main(int argc, char* argv[])
   {

   int port = 4433;

   if(argc == 2)
      port = to_u32bit(argv[1]);

   try
      {
      LibraryInitializer init;

      AutoSeeded_RNG rng;

      //RSA_PrivateKey key(rng, 1024);
      DSA_PrivateKey key(rng, DL_Group("dsa/jce/1024"));

      X509_Cert_Options options(
         "localhost/US/Syn Ack Labs/Mathematical Munitions Dept");

      X509_Certificate cert =
         X509::create_self_signed_cert(options, key, "SHA-1", rng);

      Unix_Server_Socket listener(port);

      TLS_Policy policy;

      while(true)
         {
         try {
            printf("Listening for new connection on port %d\n", port);

            Socket* sock = listener.accept();

            printf("Got new connection\n");

            TLS_Server tls(policy, rng, *sock, cert, key);

            std::string hostname = tls.requested_hostname();

            if(hostname != "")
               printf("Client requested host '%s'\n", hostname.c_str());

            printf("Writing some text\n");

            char msg[] = "Foo\nBar\nBaz\nQuux\n";
            tls.write((const byte*)msg, strlen(msg));

            printf("Now trying a read...\n");

            char buf[1024] = { 0 };
            u32bit got = tls.read((byte*)buf, sizeof(buf)-1);
            printf("%d: '%s'\n", got, buf);

            tls.close();
            }
         catch(std::exception& e) { printf("%s\n", e.what()); }
         }
   }
   catch(std::exception& e)
      {
      printf("%s\n", e.what());
      return 1;
      }
   return 0;
   }