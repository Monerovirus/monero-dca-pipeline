# Monero Dollar-cost Averaging Pipeline
This repo is a collection of scripts that help with automatically buying Monero from an exchange that doesn't offer it (Like Coinbase) using fiat currency.

I am a resident of a state that has regulations against exchanges that have Monero, so I had to use Coinbase. My method for buying Monero is to buy Stellar Lumens (XLM) on Coinbase Pro, transfer to ChangeNow, and swap there for Monero. The fees are minimal.

## Setup
After cloning the repo, copy 'template auth.json' to a new file named 'auth.json'.
Enter your API connection details there. Feel free to use the existing ChangeNow api key (I will get a tiny commission, thanks!)

Then, also edit the settings.json with the settings you want.
- The "transfer crypto" is the one that will be bought on the first exchange (Coinbase Pro in this case) and transferred to ChangeNow. I recommend leaving this as Stellar Lumens (XLM) because the transfer fee is so low, that it doesn't need to be accounted for in the script. Coins with higher transaction fees have not been tested and it will probably cause a failure.
- The "final crypto" is obviously Monero. But it can be something else if you want. (But why would you? lol).
- The "final crypto address" is the address that ChangeNow will send your final crypto to after the exchange finishes.
- The "fiat" is the fiat currency used to buy the transfer crypto.
- "Topup threshold" -- At the end of the script, it will check your fiat balance, and if it is lower than this amount, it will initiate a withdrawal from your bank automatically.
- "Topup amount" -- The amount of fiat the script will request from your bank when initiating a withdrawal.
- "Bank Identifier" -- Check on Coinbase or Coinbase Pro what it has named your bank. It will probably need be all caps. For example: If the name is "Meme Financial Credit Union", you can just enter "MEME" here and it should work.

Once your settings are how you want them, make sure you have the latest python installed and pip. Get the dependencies by running ```pip install -r requirements.txt``` in the script's directory.

## Running the Script
```python dca_pipeline.py <fiat amount here>```

If you get a syntax error, make sure you are running the latest python. You may need to run ```python3``` instead of ```python```

## Automating
I put the script on a web server running debian, but any linux distro should be fine. In debian, run ```crontab -e``` to edit the crontab. Add a line at the bottom that looks like this for example: ```0 0 * * * python /home/monerovirus/monero-dca-pipeline/dca_pipeline.py 40``` This will buy $40 worth of Monero every day at midnight. To change the frequency, refer to crontab documentation.

I have not tried running the script on Windows but I imagine you can set up something similar using the Task Scheduler.

##
I hope this script is useful. Don't hesitate to create an issue if you have problems.
