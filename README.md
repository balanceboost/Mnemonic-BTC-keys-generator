Эта программа выполняет проверку BTC-адресов, сгенерированных из мнемонических фраз, на наличие транзакций и баланса. Программа выводит системные метрики (использование ЦП, оперативной памяти и жесткого диска) в реальном времени, и сохраняет результаты в файлы:

	Found_BTC.txt — адреса, у которых есть транзакции.
	BAD_BTC.txt — адреса без транзакций.

Инструкция по использованию:
Сначала установите все необходимые зависимости. 
Создайте файл requirements.txt с таким содержимым:

    requests
    blessed
    psutil
    rich
    mnemonic
    bip32utils

Далее выполните команду:

	pip install -r requirements.txt

Запустите скрипт в консоли командой:

	python Mnemonic BTC.py
--------------------------------------------------------------------------------------
This program performs a check of BTC addresses generated from mnemonic phrases for transactions and balances. It also displays real-time system metrics (CPU, RAM, and disk usage), and saves the results to files:

	Found_BTC.txt — contains addresses with transactions.
	BAD_BTC.txt — contains addresses without transactions.
 
Usage Instructions:
First, install all necessary dependencies. Create a requirements.txt file with the following content:

    requests
    blessed
    psutil
    rich
    mnemonic
    bip32utils
 
Then, run the command:

	pip install -r requirements.txt
 
Start the script by running the following command in the console:

	python Mnemonic BTC.py
