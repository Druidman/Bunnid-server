from server.httpServer import run_http_server

def main():
    print("Running...")

    # run_ws_server() # run websocket RT server
    run_http_server() # run bunnid api
    print("End.")


if __name__ == "__main__":
    main()
    