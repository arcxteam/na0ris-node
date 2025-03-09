from curl_cffi import requests
from fake_useragent import FakeUserAgent
from datetime import datetime
import asyncio, time, json, os, pytz, random
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

wib = pytz.timezone('Asia/Jakarta')

class NaorisProtocol:
    def __init__(self) -> None:
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "chrome-extension://cpikalnagknmlfhnilhfelifgbollmmp",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "none",
            "User-Agent": FakeUserAgent().random
        }
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.last_earnings_time = {}
        self.wallet_indices = {}  # To store wallet index mapping
        self.ping_interval = 300  # 5 minutes in seconds
        self.ping_frequency = (2, 4)  # Random number of pings per interval (min, max)
        self.earnings_report_interval = 3600  # 1 hour in seconds

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def print_welcome_message(self):
        welcome_banner = f"""
{Fore.YELLOW}
 ██████╗██╗   ██╗ █████╗ ███╗   ██╗███╗   ██╗ ██████╗ ██████╗ ███████╗
██╔════╝██║   ██║██╔══██╗████╗  ██║████╗  ██║██╔═══██╗██╔══██╗██╔════╝
██║     ██║   ██║███████║██╔██╗ ██║██╔██╗ ██║██║   ██║██║  ██║█████╗  
██║     ██║   ██║██╔══██║██║╚██╗██║██║╚██╗██║██║   ██║██║  ██║██╔══╝  
╚██████╗╚██████╔╝██║  ██║██║ ╚████║██║ ╚████║╚██████╔╝██████╔╝███████╗
 ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚══════╝
{Fore.RESET}
{Fore.GREEN}========================================================================={Fore.RESET}
{Fore.CYAN}      Welcome to CUANNODE the ONCHAIN FOOTPRINT Testnet & Mainnet {Fore.RESET}
{Fore.YELLOW}          - CUANNODE By Greyscope&Co, Credit By 0xgr3y -        {Fore.RESET}
{Fore.GREEN}========================================================================={Fore.RESET}
{Fore.MAGENTA}                  🚀 Naoris Protocol Automated Bot 🚀{Fore.RESET}
"""
        print(welcome_banner)
        print(f"{Fore.GREEN}============================ WELCOME TO ONCHAIN ============================{Fore.RESET}")

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    async def load_proxies(self):
        filename = "proxy.txt"
        try:
            if not os.path.exists(filename):
                self.log(f"{Fore.YELLOW + Style.BRIGHT}⚠️ File {filename} not found. Running without proxies.{Style.RESET_ALL}")
                return False
                
            with open(filename, 'r') as f:
                self.proxies = f.read().splitlines()
            
            if not self.proxies:
                self.log(f"{Fore.YELLOW + Style.BRIGHT}⚠️ No proxies found in file. Running without proxies.{Style.RESET_ALL}")
                return False

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}🔄 Proxies loaded successfully: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(self.proxies)} proxies available{Style.RESET_ALL}"
            )
            return True
        
        except Exception as e:
            self.log(f"{Fore.YELLOW + Style.BRIGHT}⚠️ Failed to load proxies: {e}. Running without proxies.{Style.RESET_ALL}")
            self.proxies = []
            return False

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}"

    def get_next_proxy_for_account(self, account):
        if account not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[account] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[account]

    def rotate_proxy_for_account(self, account):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[account] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
    
    def load_accounts(self):
        try:
            with open('accounts.json', 'r') as file:
                accounts = json.load(file)
                if accounts:
                    # Initialize wallet indices
                    for i, account in enumerate(accounts, 1):
                        self.wallet_indices[account['Address'].lower()] = i
                        
                    self.log(f"{Fore.GREEN + Style.BRIGHT}✅ Successfully loaded {len(accounts)} accounts from accounts.json{Style.RESET_ALL}")
                    return accounts
                else:
                    self.log(f"{Fore.RED + Style.BRIGHT}❌ No accounts found in accounts.json{Style.RESET_ALL}")
                    return []
        except FileNotFoundError:
            self.log(f"{Fore.RED + Style.BRIGHT}❌ File accounts.json not found{Style.RESET_ALL}")
            return []
        except json.JSONDecodeError:
            self.log(f"{Fore.RED + Style.BRIGHT}❌ Invalid JSON format in accounts.json{Style.RESET_ALL}")
            return []
    
    def mask_account(self, account):
        mask_account = account[:6] + '*' * 6 + account[-6:]
        return mask_account
    
    def print_message(self, address, wallet_index, proxy_status, color, message):
        proxy_info = f"[{Fore.MAGENTA + Style.BRIGHT}Proxy{Style.RESET_ALL}]" if proxy_status else f"[{Fore.MAGENTA + Style.BRIGHT}Local{Style.RESET_ALL}]"
        
        self.log(
            f"{Fore.CYAN + Style.BRIGHT}[ Wallet-{wallet_index}:{Style.RESET_ALL}"
            f"{Fore.YELLOW + Style.BRIGHT} {self.mask_account(address)} {Style.RESET_ALL}"
            f"{proxy_info}"
            f"{Fore.CYAN + Style.BRIGHT} Status:{Style.RESET_ALL}"
            f"{Fore.GREEN + Style.BRIGHT} {message} {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}"
        )

    async def user_login(self, address: str, wallet_index, proxy=None, retries=5):
        url = "https://naorisprotocol.network/sec-api/auth/generateToken"
        data = json.dumps({"wallet_address":address})
        headers = {
            **self.headers,
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxy=proxy, timeout=60, impersonate="safari15_5")
                if response.status_code == 404:
                    return self.print_message(address, wallet_index, proxy is not None, Fore.RED, f"❌ Authentication Failed: Join Testnet & Complete Required Tasks First")
                    
                response.raise_for_status()
                result = response.json()
                return result['token']
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                
                return self.print_message(address, wallet_index, proxy is not None, Fore.RED, f"❌ Authentication Failed: {str(e)}")

    async def wallet_details(self, address: str, wallet_index, token: str, use_proxy: bool, proxy=None, retries=5):
        url = "https://naorisprotocol.network/testnet-api/api/testnet/walletDetails"
        data = json.dumps({"walletAddress":address})
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
            "Token": token
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxy=proxy, timeout=60, impersonate="safari15_5")
                if response.status_code == 401:
                    token = await self.process_get_access_token(address, wallet_index, use_proxy)
                    headers["Authorization"] = f"Bearer {token}"
                    headers["Token"] = token
                    continue

                response.raise_for_status()
                result = response.json()
                return result['details']
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                
                return self.print_message(address, wallet_index, proxy is not None, Fore.RED, f"❌ Wallet Details Failed: {str(e)}")
    
    async def add_whitelisted(self, address: str, wallet_index, token: str, use_proxy: bool, proxy=None, retries=5):
        url = "https://naorisprotocol.network/sec-api/api/addWhitelist"
        data = json.dumps({"walletAddress":address, "url":"naorisprotocol.network"})
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
            "Token": token
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxy=proxy, timeout=60, impersonate="safari15_5")
                if response.status_code == 401:
                    token = await self.process_get_access_token(address, wallet_index, use_proxy)
                    headers["Authorization"] = f"Bearer {token}"
                    headers["Token"] = token
                    continue
                elif response.status_code == 403:
                    return self.print_message(address, wallet_index, proxy is not None, Fore.YELLOW, f"⚠️ Whitelist Status: Already In Whitelist")

                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                
                return self.print_message(address, wallet_index, proxy is not None, Fore.RED, f"❌ Whitelist Failed: {str(e)}")
    
    async def toggle_activated(self, address: str, wallet_index, state: str, device_hash: int, proxy=None, retries=5):
        url = "https://naorisprotocol.network/sec-api/api/toggle"
        data = json.dumps({"walletAddress":address, "state":state, "deviceHash":device_hash})
        headers = {
            **self.headers,
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxy=proxy, timeout=60, impersonate="safari15_5")
                response.raise_for_status()
                return response.text
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
        
                return self.print_message(address, wallet_index, proxy is not None, Fore.RED, f"❌ Protection Toggle Failed: {str(e)}")
            
    async def send_heartbeats(self, address: str, wallet_index, token: str, use_proxy: bool, proxy=None, retries=5):
        url = "https://beat.naorisprotocol.network/api/ping"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Length": "2",
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, json={}, proxy=proxy, timeout=60, impersonate="safari15_5")
                if response.status_code == 401:
                    token = await self.process_get_access_token(address, wallet_index, use_proxy)
                    headers["Authorization"] = f"Bearer {token}"
                    continue
                elif response.status_code == 410:
                    return self.print_message(address, wallet_index, proxy is not None, Fore.GREEN, f"✅ {response.text}")

                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                
                if "502" in str(e):
                    return self.print_message(address, wallet_index, proxy is not None, Fore.RED, f"❌ PING Failed: Server Down")
                
                self.rotate_proxy_for_account(address) if use_proxy else None
                return self.print_message(address, wallet_index, proxy is not None, Fore.RED, f"❌ PING Failed: {str(e)}")
            
    async def process_get_access_token(self, address: str, wallet_index, use_proxy: bool):
        proxy = self.get_next_proxy_for_account(address) if use_proxy else None
        token = None
        while token is None:
            token = await self.user_login(address, wallet_index, proxy)
            if not token:
                proxy = self.rotate_proxy_for_account(address) if use_proxy else None
                await asyncio.sleep(5)
                continue

            self.print_message(address, wallet_index, proxy is not None, Fore.GREEN, "✅ Authentication Successful")
            return token
            
    async def process_user_earnings(self, address: str, wallet_index, token, use_proxy: bool):
        self.last_earnings_time[address] = datetime.now()
        
        while True:
            current_time = datetime.now()
            time_diff = (current_time - self.last_earnings_time[address]).total_seconds()
            
            if time_diff >= self.earnings_report_interval:
                proxy = self.get_next_proxy_for_account(address) if use_proxy else None

                wallet = await self.wallet_details(address, wallet_index, token, use_proxy, proxy)
                if wallet:
                    today_earning = wallet.get("todayEarnings", "N/A")
                    total_earning = wallet.get("totalEarnings", "N/A")
                    total_uptime = wallet.get("totalUptimeMinutes", "N/A")

                    self.print_message(address, wallet_index, proxy is not None, Fore.BLUE, 
                        f"💰 Earnings Report - Today: {today_earning} PTS | "
                        f"Total: {total_earning} PTS | "
                        f"Uptime: {total_uptime} Minutes"
                    )
                    
                    self.last_earnings_time[address] = current_time
            
            await asyncio.sleep(60)  # Check every minute

    async def process_activate_toggle(self, address, wallet_index, device_hash, token, use_proxy):
        proxy = self.get_next_proxy_for_account(address) if use_proxy else None

        whitelist = await self.add_whitelisted(address, wallet_index, token, use_proxy, proxy)
        if whitelist and whitelist.get("message") == "url saved successfully":
            self.print_message(address, wallet_index, proxy is not None, Fore.GREEN, "✅ Added to Whitelist Successfully")

        while True:
            deactivate = await self.toggle_activated(address, wallet_index, "OFF", device_hash, proxy)
            if deactivate and deactivate.strip() == "No action needed":
                activate = await self.toggle_activated(address, wallet_index, "ON", device_hash, proxy)
                if activate and activate.strip() == "Session started":
                    self.print_message(address, wallet_index, proxy is not None, Fore.GREEN, "✅ Protection Activated Successfully")
                    return True
                else:
                    continue
            else:
                continue

    async def process_send_heatbeats(self, address, wallet_index, token, use_proxy):
        last_ping_time = datetime.now()
        ping_counter = 0
        
        while True:
            current_time = datetime.now()
            time_diff = (current_time - last_ping_time).total_seconds()
            
            if time_diff >= self.ping_interval:
                # Determine random number of pings to send in this interval
                num_pings = random.randint(self.ping_frequency[0], self.ping_frequency[1])
                
                for i in range(num_pings):
                    proxy = self.get_next_proxy_for_account(address) if use_proxy else None
                    ping_counter += 1

                    heartbeat = await self.send_heartbeats(address, wallet_index, token, use_proxy, proxy)
                    if heartbeat:
                        self.print_message(address, wallet_index, proxy is not None, Fore.GREEN, f"✅ PING #{ping_counter} Successful")
                    
                    # Add small delay between multiple pings in the same interval
                    if i < num_pings - 1:
                        await asyncio.sleep(random.randint(15, 45))
                
                last_ping_time = current_time
                
                # Add some randomness to the main interval to avoid looking like a bot
                jitter = random.randint(-30, 60)  # -30 to +60 seconds
                await asyncio.sleep(self.ping_interval + jitter)
            else:
                await asyncio.sleep(10)  # Check every 10 seconds

    async def process_accounts(self, address: str, device_hash: int, use_proxy: bool):
        wallet_index = self.wallet_indices.get(address, 0)  # Get the wallet index, default to 0 if not found
        token = await self.process_get_access_token(address, wallet_index, use_proxy)
        
        if token:
            tasks = []
            tasks.append(asyncio.create_task(self.process_user_earnings(address, wallet_index, token, use_proxy)))

            activate = await self.process_activate_toggle(address, wallet_index, device_hash, token, use_proxy)
            if activate:
                tasks.append(asyncio.create_task(self.process_send_heatbeats(address, wallet_index, token, use_proxy)))

            await asyncio.gather(*tasks)

    async def main(self):
        try:
            self.clear_terminal()
            self.print_welcome_message()
            
            accounts = self.load_accounts()
            if not accounts:
                self.log(f"{Fore.RED}❌ No accounts loaded. Please check your accounts.json file.{Style.RESET_ALL}")
                return

            # Check if proxy.txt exists and load proxies
            use_proxy = await self.load_proxies()
            
            self.log(f"{Fore.GREEN}🚀 Starting Naoris Protocol Node Bot with {len(accounts)} accounts{Style.RESET_ALL}")
            self.log(f"{Fore.CYAN}ℹ️ Using {'proxies' if use_proxy else 'local connection'}{Style.RESET_ALL}")
            self.log(f"{Fore.GREEN}🕐 PING interval set to {self.ping_interval} seconds with {self.ping_frequency[0]}-{self.ping_frequency[1]} pings per interval{Style.RESET_ALL}")
            self.log(f"{Fore.GREEN}📊 Earnings report interval set to {self.earnings_report_interval} seconds{Style.RESET_ALL}")
            self.log(f"{Fore.CYAN + Style.BRIGHT}={'='*65}{Style.RESET_ALL}")

            while True:
                tasks = []
                for account in accounts:
                    address = account['Address'].lower()
                    device_hash = int(account['deviceHash'])

                    if address and device_hash:
                        tasks.append(asyncio.create_task(self.process_accounts(address, device_hash, use_proxy)))

                await asyncio.gather(*tasks)
                await asyncio.sleep(10)

        except FileNotFoundError:
            self.log(f"{Fore.RED}❌ Required file not found.{Style.RESET_ALL}")
            return
        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}❌ Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        bot = NaorisProtocol()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.YELLOW + Style.BRIGHT}👋 Shutting down Naoris Protocol Node - BOT{Style.RESET_ALL}"                             
        )
