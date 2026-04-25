# main.py
import asyncio
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.switch import Switch
from kivy.clock import Clock
from kivy.core.window import Window
from json import load, dump
import os

from bot_core import BotCore

Window.clearcolor = (0.1, 0.1, 0.1, 1)

class ConfigScreen(BoxLayout):
    """Configuration screen"""
    
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Title
        title = Label(
            text='OwO Selfbot Configuration',
            size_hint_y=0.1,
            font_size='20sp',
            bold=True
        )
        self.add_widget(title)
        
        # Scroll view for inputs
        scroll = ScrollView(size_hint=(1, 0.7))
        grid = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=10)
        grid.bind(minimum_height=grid.setter('height'))
        
        # Token input
        grid.add_widget(Label(text='Discord Token:', size_hint_y=None, height=30))
        self.token_input = TextInput(
            hint_text='Enter your token',
            multiline=False,
            size_hint_y=None,
            height=40,
            password=True
        )
        grid.add_widget(self.token_input)
        
        # Channel ID
        grid.add_widget(Label(text='Channel ID:', size_hint_y=None, height=30))
        self.channel_input = TextInput(
            hint_text='Enter channel ID',
            multiline=False,
            size_hint_y=None,
            height=40,
            input_filter='int'
        )
        grid.add_widget(self.channel_input)
        
        # Auto Pray
        pray_box = BoxLayout(size_hint_y=None, height=40)
        pray_box.add_widget(Label(text='Auto Pray:'))
        self.pray_switch = Switch(active=True)
        pray_box.add_widget(self.pray_switch)
        grid.add_widget(pray_box)
        
        # Auto Gems
        gems_box = BoxLayout(size_hint_y=None, height=40)
        gems_box.add_widget(Label(text='Auto Gems:'))
        self.gems_switch = Switch(active=True)
        gems_box.add_widget(self.gems_switch)
        grid.add_widget(gems_box)
        
        # Auto Daily
        daily_box = BoxLayout(size_hint_y=None, height=40)
        daily_box.add_widget(Label(text='Auto Daily:'))
        self.daily_switch = Switch(active=True)
        daily_box.add_widget(self.daily_switch)
        grid.add_widget(daily_box)
        
        # Auto Sell
        sell_box = BoxLayout(size_hint_y=None, height=40)
        sell_box.add_widget(Label(text='Auto Sell:'))
        self.sell_switch = Switch(active=True)
        sell_box.add_widget(self.sell_switch)
        grid.add_widget(sell_box)
        
        # Sell types
        grid.add_widget(Label(text='Sell Types:', size_hint_y=None, height=30))
        self.sell_types = TextInput(
            hint_text='e.g., c (common)',
            text='c',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        grid.add_widget(self.sell_types)
        
        scroll.add_widget(grid)
        self.add_widget(scroll)
        
        # Buttons
        btn_box = BoxLayout(size_hint_y=0.2, spacing=10)
        
        save_btn = Button(
            text='Save & Start',
            background_color=(0.2, 0.8, 0.2, 1)
        )
        save_btn.bind(on_press=self.save_and_start)
        btn_box.add_widget(save_btn)
        
        load_btn = Button(
            text='Load Config',
            background_color=(0.2, 0.5, 0.8, 1)
        )
        load_btn.bind(on_press=self.load_config)
        btn_box.add_widget(load_btn)
        
        self.add_widget(btn_box)
        
        # Auto-load config
        self.load_config()
    
    def save_and_start(self, instance):
        """Save configuration and start bot"""
        if not self.token_input.text or not self.channel_input.text:
            self.app.show_message("Please fill in token and channel ID!")
            return
        
        config = {
            'token': self.token_input.text,
            'channel': int(self.channel_input.text),
            'pm': self.pray_switch.active,
            'gm': self.gems_switch.active,
            'daily': self.daily_switch.active,
            'sell': {
                'enable': self.sell_switch.active,
                'types': self.sell_types.text
            },
            'em': {'text': False, 'owo': False},
            'sm': False,
            'sbcommands': {'enable': False},
            'webhook': {'link': ''},
            'solve': False
        }
        
        # Save to file
        with open('config.json', 'w') as f:
            dump(config, f, indent=4)
        
        self.app.start_bot(config)
    
    def load_config(self, instance=None):
        """Load existing configuration"""
        if os.path.exists('config.json'):
            try:
                with open('config.json', 'r') as f:
                    config = load(f)
                    self.token_input.text = config.get('token', '')
                    self.channel_input.text = str(config.get('channel', ''))
                    self.pray_switch.active = config.get('pm', True)
                    self.gems_switch.active = config.get('gm', True)
                    self.daily_switch.active = config.get('daily', True)
                    self.sell_switch.active = config.get('sell', {}).get('enable', True)
                    self.sell_types.text = config.get('sell', {}).get('types', 'c')
            except:
                pass

class BotScreen(BoxLayout):
    """Bot running screen"""
    
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Title
        title = Label(
            text='OwO Selfbot Running',
            size_hint_y=0.08,
            font_size='20sp',
            bold=True
        )
        self.add_widget(title)
        
        # Stats
        stats_grid = GridLayout(cols=2, size_hint_y=0.15, spacing=5)
        stats_grid.add_widget(Label(text='Commands Sent:'))
        self.cmds_label = Label(text='0', bold=True)
        stats_grid.add_widget(self.cmds_label)
        
        stats_grid.add_widget(Label(text='Balance Gained:'))
        self.balance_label = Label(text='0', bold=True)
        stats_grid.add_widget(self.balance_label)
        
        self.add_widget(stats_grid)
        
        # Log area
        log_label = Label(text='Activity Log:', size_hint_y=0.05, font_size='16sp')
        self.add_widget(log_label)
        
        scroll = ScrollView(size_hint=(1, 0.52))
        self.log_grid = GridLayout(cols=1, spacing=2, size_hint_y=None, padding=5)
        self.log_grid.bind(minimum_height=self.log_grid.setter('height'))
        scroll.add_widget(self.log_grid)
        self.add_widget(scroll)
        
        # Control buttons
        btn_box = BoxLayout(size_hint_y=0.2, spacing=10)
        
        self.pause_btn = Button(
            text='Pause',
            background_color=(0.8, 0.5, 0.2, 1)
        )
        self.pause_btn.bind(on_press=self.toggle_pause)
        btn_box.add_widget(self.pause_btn)
        
        stop_btn = Button(
            text='Stop',
            background_color=(0.8, 0.2, 0.2, 1)
        )
        stop_btn.bind(on_press=self.stop_bot)
        btn_box.add_widget(stop_btn)
        
        self.add_widget(btn_box)
        
        # Update stats periodically
        Clock.schedule_interval(self.update_stats, 1)
    
    def add_log(self, message):
        """Add log message"""
        log_label = Label(
            text=message,
            size_hint_y=None,
            height=30,
            halign='left',
            valign='middle',
            text_size=(Window.width - 30, None)
        )
        self.log_grid.add_widget(log_label)
        
        # Keep only last 100 logs
        if len(self.log_grid.children) > 100:
            self.log_grid.remove_widget(self.log_grid.children[-1])
    
    def update_stats(self, dt):
        """Update statistics"""
        if self.app.bot:
            self.cmds_label.text = str(self.app.bot.total_cmds)
            balance_gain = self.app.bot.start_balance  # Will be updated with actual balance
            self.balance_label.text = f"{balance_gain:,}"
    
    def toggle_pause(self, instance):
        """Pause/resume bot"""
        if self.app.bot:
            if self.app.bot.is_running:
                asyncio.run_coroutine_threadsafe(
                    self.app.bot.stop_bot(),
                    self.app.loop
                )
                self.pause_btn.text = 'Resume'
                self.pause_btn.background_color = (0.2, 0.8, 0.2, 1)
            else:
                asyncio.run_coroutine_threadsafe(
                    self.app.bot.start_bot(),
                    self.app.loop
                )
                self.pause_btn.text = 'Pause'
                self.pause_btn.background_color = (0.8, 0.5, 0.2, 1)
    
    def stop_bot(self, instance):
        """Stop bot and return to config"""
        self.app.stop_bot()

class OwOBotApp(App):
    """Main application"""
    
    def build(self):
        self.bot = None
        self.loop = None
        self.bot_thread = None
        self.config_screen = ConfigScreen(self)
        return self.config_screen
    
    def show_message(self, message):
        """Show temporary message"""
        from kivy.uix.popup import Popup
        popup = Popup(
            title='Message',
            content=Label(text=message),
            size_hint=(0.8, 0.3)
        )
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)
    
    def status_callback(self, message):
        """Receive status from bot"""
        if hasattr(self, 'bot_screen'):
            Clock.schedule_once(lambda dt: self.bot_screen.add_log(message))
    
    def start_bot(self, config):
        """Start the bot"""
        self.bot_screen = BotScreen(self)
        self.root.clear_widgets()
        self.root.add_widget(self.bot_screen)
        
        # Start bot in separate thread
        self.bot_thread = threading.Thread(target=self.run_bot, args=(config,))
        self.bot_thread.daemon = True
        self.bot_thread.start()
    
    def run_bot(self, config):
        """Run bot in asyncio loop"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        self.bot = BotCore(config, self.status_callback)
        
        async def start():
            await self.bot.start_bot()
            await self.bot.start(config['token'])
        
        try:
            self.loop.run_until_complete(start())
        except Exception as e:
            self.status_callback(f"Error: {str(e)}")
    
    def stop_bot(self):
        """Stop bot and return to config"""
        if self.bot:
            asyncio.run_coroutine_threadsafe(self.bot.close(), self.loop)
            self.bot = None
        
        self.root.clear_widgets()
        self.config_screen = ConfigScreen(self)
        self.root.add_widget(self.config_screen)
    
    def on_stop(self):
        """Cleanup on app close"""
        if self.bot:
            asyncio.run_coroutine_threadsafe(self.bot.close(), self.loop)

if __name__ == '__main__':
    OwOBotApp().run()