import rich
import readFile
import json

console = rich.console.Console()

def load_config() -> dict:#load config.json
    try:
        config = readFile.LoadJson("config.json")
    except FileNotFoundError:
        console.print("[bold yellow][WARNING][/bold yellow]: config.json not found or corrupted.")
        readFile.fix_config()
        config = readFile.LoadJson("config.json")
    return config

def start():#settings menu
    while True:
        config = load_config()
        console.print("[bold]Function                               options[/bold]")
        console.print("[bold]==============================================[/bold]")
        console.print("[0] Save Config and exit")
        console.print("[1] Change Language                      [ {} ]".format(config["language"]))
        console.print("[2] Change API Domain                    [ {} ]".format(config["APIdomain"]))
        console.print("[3] Toggle Auto Refresh Page            [{}]".format(config["autoFreshPage"]))
        console.print("[4] Toggle Encrypted User Token         [{}]".format(config["EncryptedUserToken"]))
        command = console.input("[bold green]> [/bold green]")
        console.clear()
        if command.lower() in ["exit", "q"]:
            console.print("[bold yellow]Exiting...[/bold yellow]")
            break
        elif command.lower() == "0":
            with open("config.json", "w") as f:
                json.dump(config, f, indent=4)
            console.print("[bold green]Config saved![/bold green]")
            break
        elif command.lower() == "1":
            config["language"] = console.input("[bold green]Enter language (en/zh): [/bold green]")
        elif command.lower() == "2":
            config["APIdomain"] = console.input("[bold green]Enter API domain (https://api.solian.app): [/bold green]")
        elif command.lower() == "3":
            config["autoFreshPage"] = not config["autoFreshPage"]
        elif command.lower() == "4":
            config["EncryptedUserToken"] = not config["EncryptedUserToken"]
        elif command.lower() == "clear":
            console.clear()
