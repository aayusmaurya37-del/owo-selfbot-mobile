# bot_core.py
import discord
import aiohttp
import asyncio
from json import load, dump
from random import randrange
from re import findall
from time import time
from base64 import b64encode
from datetime import timedelta

class BotCore(discord.Client):
    """Modified Discord Client for mobile"""
    
    def __init__(self, config, status_callback=None):
        super().__init__(guild_subscription_options=discord.GuildSubscriptionOptions.off())
        self.config = config
        self.status_callback = status_callback
        self.is_running = False
        self.total_cmds = 0
        self.start_balance = 0
        self.next_daily = 0
        self.owo = 408785106942164992
        self.channel = None
        self.tasks_list = []
        
    def log(self, message, level="INFO"):
        """Send log to UI"""
        if self.status_callback:
            self.status_callback(f"[{level}] {message}")
    
    async def get_balance(self):
        """Fetch current balance"""
        try:
            await self.channel.send("owo cash")
            await asyncio.sleep(3)
            async for message in self.channel.history(limit=15):
                if message.author.id == self.owo and self.user.name in message.content:
                    content = message.content
                    return int("".join(findall("[0-9]+", content[content.find("have"):])))
        except:
            return self.start_balance
        return self.start_balance
    
    async def use_gems(self):
        """Use gems automatically"""
        try:
            await self.channel.send("owo inv")
            self.log("Checking gems...")
            await asyncio.sleep(3)
            
            async for message in self.channel.history(limit=15):
                if message.author.id == self.owo and self.user.name in message.content:
                    inv = findall(r"`(.*?)`", message.content)
                    if "050" in inv:
                        await self.channel.send("owo lootbox all")
                        self.log("Opened lootboxes")
                        await asyncio.sleep(3)
                    
                    gems = [item for item in inv if item.isdigit() and 50 < int(item) < 100]
                    if gems:
                        await self.channel.send(f"owo use {' '.join(gems[:3])}")
                        self.log(f"Used gems: {', '.join(gems[:3])}")
                    break
        except Exception as e:
            self.log(f"Gem error: {str(e)}", "ERROR")
    
    async def hunt_battle_loop(self):
        """Main hunt/battle loop"""
        while self.is_running:
            try:
                await self.channel.send("owo hunt")
                self.log("Sent: owo hunt")
                self.total_cmds += 1
                await asyncio.sleep(3)
                
                await self.channel.send("owo battle")
                self.log("Sent: owo battle")
                self.total_cmds += 1
                
                await asyncio.sleep(randrange(14, 19))
            except Exception as e:
                self.log(f"Hunt/Battle error: {str(e)}", "ERROR")
                await asyncio.sleep(10)
    
    async def pray_loop(self):
        """Pray loop"""
        while self.is_running:
            try:
                if self.config.get("pm", False):
                    await self.channel.send("owo pray")
                    self.log("Sent: owo pray")
                await asyncio.sleep(240)  # 4 minutes
            except Exception as e:
                self.log(f"Pray error: {str(e)}", "ERROR")
                await asyncio.sleep(10)
    
    async def daily_loop(self):
        """Daily claim loop"""
        while self.is_running:
            try:
                if self.config.get("daily", False) and time() >= self.next_daily:
                    await self.channel.send("owo daily")
                    self.log("Claiming daily...")
                    await asyncio.sleep(3)
                    
                    async for message in self.channel.history(limit=15):
                        if message.author.id == self.owo:
                            if "Nu" in message.content:
                                next_time = findall("[0-9]+", message.content)
                                if len(next_time) >= 3:
                                    seconds = int(next_time[0])*3600 + int(next_time[1])*60 + int(next_time[2])
                                    self.next_daily = time() + seconds
                                    self.log(f"Next daily in {seconds//3600}h")
                            elif "daily" in message.content.lower():
                                self.log("Daily claimed!")
                            break
                
                await asyncio.sleep(30)
            except Exception as e:
                self.log(f"Daily error: {str(e)}", "ERROR")
                await asyncio.sleep(10)
    
    async def sell_loop(self):
        """Auto sell loop"""
        while self.is_running:
            try:
                if self.config.get("sell", {}).get("enable", False):
                    types = self.config["sell"].get("types", "c")
                    await self.channel.send(f"owo sell {types}")
                    self.log(f"Sold animals: {types}")
                await asyncio.sleep(120)  # 2 minutes
            except Exception as e:
                self.log(f"Sell error: {str(e)}", "ERROR")
                await asyncio.sleep(10)
    
    async def on_ready(self):
        """On bot ready"""
        self.log(f"Logged in as {self.user.name}")
        self.channel = self.get_channel(self.config["channel"])
        
        if not self.channel:
            self.log("Invalid channel ID!", "ERROR")
            return
        
        self.start_balance = await self.get_balance()
        self.log(f"Starting balance: {self.start_balance:,}")
        
        # Start tasks
        if self.is_running:
            self.tasks_list = [
                asyncio.create_task(self.hunt_battle_loop()),
                asyncio.create_task(self.pray_loop()),
                asyncio.create_task(self.daily_loop()),
                asyncio.create_task(self.sell_loop()),
            ]
    
    async def on_message(self, message):
        """Check for verification"""
        if message.author.id == self.owo and self.user.name in message.content:
            if "⚠" in message.content or "captcha" in message.content.lower():
                self.log("⚠️ VERIFICATION DETECTED!", "CRITICAL")
                await self.stop_bot()
    
    async def start_bot(self):
        """Start the bot"""
        self.is_running = True
        self.log("Bot started!")
    
    async def stop_bot(self):
        """Stop the bot"""
        self.is_running = False
        for task in self.tasks_list:
            task.cancel()
        self.tasks_list = []
        self.log("Bot stopped!")