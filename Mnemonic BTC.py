import random
import time
import concurrent.futures as cf
import requests
from blessed import Terminal
import psutil
from rich.panel import Panel
from rich.console import Console
from mnemonic import Mnemonic
import os
import sys
import bip32utils

console = Console()

def OnClear():
    if "win" in sys.platform.lower():
        os.system("cls")
    else:
        os.system("clear")

def balance(addr):
    url_n = f"https://blockchain.info/q/addressbalance/{addr}?confirmations=6"
    while True:
        try:
            req = requests.get(url_n)
            req.raise_for_status()  # Raise an error for bad status codes
            return int(req.text) / 100000000  # Сатоши в BTC
        except requests.exceptions.RequestException as e:
            if e.response and e.response.status_code == 429:  # Check for rate limit error
                console.print("[yellow]Достигнут лимит API, ожидаем 1 час...[/yellow]")
                time.sleep(3600)  # Wait for 1 hour
            else:
                console.print(f"[red]Error retrieving balance for {addr}: {e}[/red]")
                return 0

def transaction(addr):
    while True:
        try:
            req = requests.get(f"https://blockchain.info/q/getreceivedbyaddress/{addr}")
            req.raise_for_status()  # Raise an error for bad status codes
            return int(req.text) / 100000000  # Сатоши в BTC
        except requests.exceptions.RequestException as e:
            if e.response and e.response.status_code == 429:  # Check for rate limit error
                console.print("[yellow]Достигнут лимит API, ожидаем 1 час...[/yellow]")
                time.sleep(3600)  # Wait for 1 hour
            else:
                console.print(f"[red]Error retrieving transaction info for {addr}: {e}[/red]")
                return 0

def draw_system_status(term):
    cpu_percent = psutil.cpu_percent()
    ram_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    termWidth = term.width
    system_status = (
        f'\n{draw_graph("CPU", cpu_percent, termWidth)}\n'
        f'\n{draw_graph("RAM", ram_percent, termWidth)}\n'
        f'\n{draw_graph("HDD", disk_percent, termWidth)}\n'
    )
    return system_status

def draw_btc_info(z, w, addr, priv, mixWord, txs):
    btc_info_panel = (
        f'\n[gold1]Total Checked: [orange_red1]{z}[/][gold1]  Win: [white]{w}[/]'
        f'[gold1]  Transactions Received: [/][aquamarine1]{txs}\n\n[/][gold1]ADDR: [white] {addr}[/white]\n\n'
        f'PRIVATE: [grey54]{priv}[/grey54]\n\nMNEMONIC: [white]{mixWord}[/white]\n'
    )
    return btc_info_panel

def draw_graph(title, percent, width):
    bar_length = int(width - 17)
    num_blocks = int(percent * bar_length / 100)
    dash = "[grey54]–[/]"
    barFill = "[green]▬[/]"
    bar = barFill * num_blocks + dash * (bar_length - num_blocks)
    return f"[white]{title}[/]: |{bar}| {percent}%"

def generate_key_from_mnemonic(words):
    # Генерация seed на основе мнемонической фразы
    seed = Mnemonic.to_seed(words)

    # Генерация мастер-ключа и получение приватного ключа
    bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed)
    bip32_child_key_obj = bip32_root_key_obj.ChildKey(0).ChildKey(0)

    priv_key = bip32_child_key_obj.WalletImportFormat()  # Приватный ключ в формате WIF
    addr = bip32_child_key_obj.Address()  # Получаем Bitcoin-адрес

    return priv_key, addr

def main():
    term = Terminal()
    with term.fullscreen():
        with term.cbreak(), term.hidden_cursor():
            OnClear()
            z = 0
            w = 0
            while True:
                system_status = draw_system_status(term)
                draw_system_status_panel = Panel(system_status, border_style="grey66")
                
                # Генерируем мнемоническую фразу
                mne = Mnemonic("english")
                NumberList = [128, 256]
                randomSize = random.choice(NumberList)
                words = mne.generate(strength=randomSize)
                
                # Используем функцию для генерации ключей и адресов
                priv, addr = generate_key_from_mnemonic(words)
                mixWord = words[:64]
                txs = transaction(addr)

                if txs > 0:
                    w += 1
                    # Сохраняем адреса с транзакциями
                    with open("Found_BTC.txt", "a") as fr:
                        fr.write(f"{addr} TXS: {txs} BAL: {balance(addr)}\n")
                        fr.write(f"{priv}\n")
                        fr.write(f"{words}\n")
                        fr.write(f"{'-' * 50}\n")
                else:
                    # Сохраняем адреса без транзакций
                    with open("BAD_BTC.txt", "a") as fr:
                        fr.write(f"ADDR: {addr}\n")
                        fr.write(f"PRIVATE: {priv}\n")
                        fr.write(f"MNEMONIC: {words}\n")
                        fr.write(f"{'-' * 50}\n")

                btc_info_panel = draw_btc_info(z, w, addr, priv, mixWord, txs)
                with term.location(0, 1):
                    console.print(draw_system_status_panel, justify="full", soft_wrap=True)
                    console.print(Panel(btc_info_panel, title="[white]Bitcoin Mnemonic Checker V1[/]", style="green"),
                                  justify="full", soft_wrap=True)
                z += 1

if __name__ == "__main__":
    with cf.ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        for _ in range(os.cpu_count()):
            executor.submit(main).result()
