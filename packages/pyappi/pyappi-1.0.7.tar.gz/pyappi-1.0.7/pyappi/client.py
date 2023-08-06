import pyappi
from colorama import Fore, Style
import httpx
import click

from pyappi.util.login import SessionChallenge

@click.command()
@click.argument('cmd')
@click.option("--id", default="", help="Id of resource to read")
@click.option("--host", default="127.0.0.1:8099", help="Host name or ip address with optional port after a :")
@click.option("--user", default="", help="User name of account you are logging into.")
@click.option("--password", default="", help="Password of your account.")
def read(cmd, id, host, user, password):
    result = httpx.get(f"http://{host}/document/{id}?{SessionChallenge(user,password)}")
    print(cmd, id, result,result.status_code)
    pass

@click.command()
@click.option("--user", default="", help="User name of account you are logging into.")
@click.option("--password", default="", help="Password of your account.")
def login():
    pass

@click.command()
def logout():
    pass

@click.command()
@click.argument('cmd')
@click.option("--id", default="", help="Id of resource to read")
@click.option("--host", default="", help="Host name or ip address with optional port after a :")
@click.option("--user", default="", help="User name of account you are logging into.")
@click.option("--password", default="", help="Password of your account.")
def main(cmd, id, host, user, password):
    match cmd:
        case "read":
            return read()
        case "login":
            return login()
        case "logout":
            return logout()
        case "about":
            print(f"{Fore.GREEN}PYAPPI-CLIENT {pyappi.__version__}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()