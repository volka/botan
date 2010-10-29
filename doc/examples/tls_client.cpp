/*
* (C) 2008 Jack Lloyd
*
* Distributed under the terms of the Botan license
*/

#include <botan/init.h>
#include <botan/tls_client.h>
#include <botan/unx_sock.h>

using namespace Botan;

#include <stdio.h>
#include <string>
#include <iostream>
#include <memory>

int main(int argc, char* argv[])
   {
   if(argc != 2 && argc != 3)
      {
      printf("Usage: %s host [port]\n", argv[0]);
      return 1;
      }

   try
      {
      LibraryInitializer init;

      std::string host = argv[1];
      u32bit port = argc == 3 ? Botan::to_u32bit(argv[2]) : 443;

      printf("Connecting to %s:%d...\n", host.c_str(), port);

      Unix_Socket sock(argv[1], port);

      std::auto_ptr<Botan::RandomNumberGenerator> rng(
         Botan::RandomNumberGenerator::make_rng());

      TLS_Policy policy;

      TLS_Client tls(std::tr1::bind(&Socket::read, std::tr1::ref(sock), _1, _2),
                     std::tr1::bind(&Socket::write, std::tr1::ref(sock), _1, _2),
                     policy, *rng);

      printf("Handshake extablished...\n");

#if 0
      std::string http_command = "GET / HTTP/1.1\r\n"
                                 "Server: " + host + ':' + to_string(port) + "\r\n\r\n";
#else
      std::string http_command = "GET / HTTP/1.0\r\n\r\n";
#endif

      tls.write((const byte*)http_command.c_str(), http_command.length());

      u32bit total_got = 0;

      while(true)
         {
         if(tls.is_closed())
            break;

         byte buf[16+1] = { 0 };
         u32bit got = tls.read(buf, sizeof(buf)-1);
         printf("%s", buf);
         fflush(0);

         total_got += got;
         }

      printf("\nRetrieved %d bytes total\n", total_got);
   }
   catch(std::exception& e)
      {
      printf("%s\n", e.what());
      return 1;
      }
   return 0;
   }