package hello_world;

import java.net.*;
import java.io.*;

public class HelloWorld {
    public static void main(String[] args) throws IOException {
        
        if (args.length != 1) {
            System.err.println("Usage: java EchoServer <port number>");
            System.exit(1);
        }
        
        int portNumber = Integer.parseInt(args[0]);
        EchoServer echo = new EchoServer(portNumber);
        echo.run();
    }
}