package hello_world;
import java.net.*;
import java.io.*;

public class EchoServer {
    private int _portNumber;

    public EchoServer(int portNumber){
        _portNumber = portNumber;
    }
    public void run() {
        try (ServerSocket serverSocket = new ServerSocket(_portNumber);
            Socket clientSocket = serverSocket.accept();     
            PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);                   
            BufferedReader in = new BufferedReader( new InputStreamReader(clientSocket.getInputStream()));
        ) {
            String inputLine;
            while ((inputLine = in.readLine()) != null) {
                out.println(inputLine);
            }
        } catch (IOException e) {
            System.out.println("Exception caught when trying to listen on port "
                + _portNumber + " or listening for a connection");
            System.out.println(e.getMessage());
        }
    }
}