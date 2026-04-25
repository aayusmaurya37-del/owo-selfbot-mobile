# bot_core.py
import requests
import time
import asyncio
from random import randrange

class BotCore:
    """Discord bot using REST API instead of discord.py"""
    
    def __init__(self, config, status_callback=None):
        self.config = config
        self.status_callback = status_callback
        self.is_running = False
        self.total_cmds = 0
        self.base_url = "https://discord.com/api/v10"
        self.headers = {
            "Authorization": config['token'],
            "Content-Type": "application/json"
        }
        self.channel_id = str(config['channel'])
        
    def log(self, message, level="INFO"):
        """Send log to UI"""
        if self.status_callback:
            self.status_callback(f"[{level}] {message}")
    
    def send_message(self, content):
        """Send message via REST API"""
        try:
            url = f"{self.base_url}/channels/{self.channel_id}/messages"
            data = {"content": content}
            response = requests.post(url, headers=self.headers, json=data, timeout=10)
            return response.status_code == 200
        except Exception as e:
            self.log(f"Send error: {str(e)}", "ERROR")
            return False
    
    def get_messages(self, limit=10):
        """Get recent messages"""
        try:
            url = f"{self.base_url}/channels/{self.channel_id}/messages?limit={limit}"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            return []
        except:
            return []
    
    async def hunt_battle_loop(self):
        """Main hunt/battle loop"""
        while self.is_running:
            try:
                if self.send_message("owo hunt"):
                    self.log("Sent: owo hunt")
                    self.total_cmds += 1
                
                await asyncio.sleep(3)
                
                if self.send_message("owo battle"):
                    self.log("Sent: owo battle")
                    self.total_cmds += 1
                
                await asyncio.sleep(randrange(15, 20))
            except Exception as e:
                self.log(f"Hunt/Battle error: {str(e)}", "ERROR")
                await asyncio.sleep(10)
    
    async def pray_loop(self):
        """Pray loop"""
        while self.is_running:
            try:
                if self.config.get("pm", False):
                    if self.send_message("owo pray"):
                        self.log("Sent: owo pray")
                await asyncio.sleep(300)
            except Exception as e:
                self.log(f"Pray error: {str(e)}", "ERROR")
                await asyncio.sleep(10)
    
    async def daily_loop(self):
        """Daily loop"""
        while self.is_running:
            try:
                if self.config.get("daily", False):
                    if self.send_message("owo daily"):
                        self.log("Claimed daily")
                await asyncio.sleep(86400)  # 24 hours
            except Exception as e:
                self.log(f"Daily error: {str(e)}", "ERROR")
                await asyncio.sleep(60)
    
    async def sell_loop(self):
        """Sell loop"""
        while self.is_running:
            try:
                if self.config.get("sell", {}).get("enable", False):
                    types = self.config["sell"].get("types", "c")
                    if self.send_message(f"owo sell {types}"):
                        self.log(f"Sold: {types}")
                await asyncio.sleep(180)
            except Exception as e:
                self.log(f"Sell error: {str(e)}", "ERROR")
                await asyncio.sleep(60)
    
    async def start_bot(self):
        """Start the bot"""
        self.is_running = True
        self.log("Bot started!", "SUCCESS")
        
        # Test connection
        messages = self.get_messages(1)
        if messages:
            self.log("Connected to Discord!", "SUCCESS")
        else:
            self.log("Connection test failed", "WARNING")
        
        # Start all loops
        await asyncio.gather(
            self.hunt_battle_loop(),
            self.pray_loop(),
            self.daily_loop(),
            self.sell_loop()
        )
    
    async def stop_bot(self):
        """Stop the bot"""
        self.is_running = False
        self.log("Bot stopped!", "WARNING")
    
    async def close(self):
        """Cleanup"""
        await self.stop_bot()

    async def start(self, token):
        """Start with token (compatibility method)"""
        await self.start_bot()
