import uuid
import jwt
import time
import requests
from datetime import datetime
from typing import List, Optional
from colorama import init, Fore, Style
import os

# Inisialisasi colorama
init(autoreset=True)

def tampilkan_banner():
    """Menampilkan banner saat program dijalankan."""
    banner = """
    ██████╗██╗   ██╗ █████╗ ███╗   ██╗███╗   ██╗ ██████╗ ██████╗ ███████╗
    ██╔════╝██║   ██║██╔══██╗████╗  ██║████╗  ██║██╔═══██╗██╔══██╗██╔════╝
    ██║     ██║   ██║███████║██╔██╗ ██║██╔██╗ ██║██║   ██║██║  ██║█████╗  
    ██║     ██║   ██║██╔══██║██║╚██╗██║██║╚██╗██║██║   ██║██║  ██║██╔══╝ 
    ╚██████╗╚██████╔╝██║  ██║██║ ╚████║██║ ╚████║╚██████╔╝██████╔╝███████╗
     ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚══════╝
    =========================================================================
                Welcome To Validator Extensions Build on Docker
                - CUANNODE By Greyscope&Co, Credit By 0xgr3y -
    =========================================================================
    """
    print(Fore.GREEN + banner)

# Utilitas
def generate_hash_perangkat() -> str:
    """Menghasilkan hash perangkat unik."""
    return str(int(uuid.uuid4().hex.replace("-", "")[:8], 16))

def dekode_token(token: str) -> Optional[dict]:
    """Mendekode token JWT dan mengekstrak data yang relevan."""
    try:
        decoded = jwt.decode(token, options={"verify_signature": False})
        if not decoded:
            raise ValueError("Format token tidak valid")
        return {
            "wallet_address": decoded.get("wallet_address"),
            "id": decoded.get("id"),
            "exp": decoded.get("exp"),
        }
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Gagal mendekode token: {e}")
        return None

def cek_kadaluarsa_token(akun: dict) -> bool:
    """Memeriksa apakah token akun telah kedaluwarsa."""
    if not akun.get("decoded") or not akun["decoded"].get("exp"):
        return True
    return time.time() >= akun["decoded"]["exp"]

def muat_proxy(file_proxy: str) -> List[str]:
    """Memuat daftar proxy dari file teks."""
    try:
        with open(file_proxy, "r") as file:
            proxies = [line.strip() for line in file if line.strip()]
        return proxies
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Gagal memuat proxy: {e}")
        return []

def tanya_penggunaan_proxy():
    """Menanyakan apakah pengguna ingin menggunakan proxy."""
    while True:
        pilihan = input(f"{Fore.CYAN}[?] Ingin menggunakan proxy? (y/n): ").strip().lower()
        if pilihan in ["y", "n"]:
            return pilihan == "y"
        else:
            print(f"{Fore.RED}[ERROR] Masukkan 'y' untuk Ya atau 'n' untuk Tidak.")

# Konfigurasi
API_CONFIG = {
    "base_url": "https://naorisprotocol.network",
    "endpoints": {
        "heartbeat": "/sec-api/api/produce-to-kafka",
    },
    "headers": {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "chrome-extension://cpikainghpmifinihfeigiboilmmp",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    },
}

APP_CONFIG = {
    "heartbeat_interval": 10000,  # 10 detik ubah aja
    "data_file": "data.txt",
    "proxy_file": "proxy.txt",
}

# Layanan Heartbeat dengan dukungan proxy
class LayananHeartbeat:
    def __init__(self, gunakan_proxy: bool):
        self.akun: List[dict] = []
        self.waktu_mulai = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.warna_wallet = [Fore.GREEN, Fore.CYAN]  # Warna untuk setiap wallet
        self.proxies = muat_proxy(APP_CONFIG["proxy_file"]) if gunakan_proxy else []
        self.gunakan_proxy = gunakan_proxy

    def muat_akun(self):
        """Memuat akun dari file data."""
        try:
            with open(APP_CONFIG["data_file"], "r") as file:
                tokens = file.read().splitlines()

            self.akun = []
            for idx, token in enumerate(tokens):
                decoded = dekode_token(token.strip())
                if not decoded or not decoded.get("wallet_address"):
                    print(f"{Fore.RED}[ERROR] Gagal mendekode token: {token[:20]}...")
                    continue

                # Menetapkan proxy untuk akun (jika menggunakan proxy)
                proxy = self.proxies[idx % len(self.proxies)] if self.gunakan_proxy and self.proxies else None

                self.akun.append({
                    "token": token.strip(),
                    "decoded": decoded,
                    "device_hash": generate_hash_perangkat(),
                    "status": "diinisialisasi",
                    "nomor_wallet": idx + 1,  # Nomor wallet (Wallet 1, Wallet 2)
                    "proxy": proxy,
                })

            if not self.akun:
                raise ValueError("Tidak ada akun valid yang dimuat")

            print(f"{Fore.CYAN}[INFO] Berhasil memuat {len(self.akun)} akun.")
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Gagal memuat akun: {e}")
            raise

    def buat_sesi(self, proxy: Optional[str] = None):
        """Membuat sesi requests dengan dukungan proxy."""
        sesi = requests.Session()
        if proxy:
            sesi.proxies = {
                "http": proxy,
                "https": proxy,
            }
        return sesi

    def kirim_heartbeat(self, akun: dict):
        """Mengirimkan permintaan heartbeat untuk akun tertentu."""
        try:
            sesi = self.buat_sesi(akun["proxy"])
            headers = API_CONFIG["headers"].copy()
            headers["Authorization"] = f"Bearer {akun['token']}"
            payload = {
                "topic": "device-heartbeat",
                "deviceHash": akun["device_hash"],
                "walletAddress": akun["decoded"]["wallet_address"],
            }
            response = sesi.post(
                f"{API_CONFIG['base_url']}{API_CONFIG['endpoints']['heartbeat']}",
                headers=headers,
                json=payload,
            )
            akun["last_heartbeat"] = datetime.now().strftime("%H:%M:%S")
            akun["status"] = "aktif"

            warna_wallet = self.warna_wallet[(akun["nomor_wallet"] - 1) % len(self.warna_wallet)]

            # Menampilkan pesan sukses dengan atau tanpa proxy
            if akun["proxy"]:
                print(f"{warna_wallet}[SUKSES] Wallet {akun['nomor_wallet']}: Heartbeat terkirim untuk {akun['decoded']['wallet_address']} (dengan proxy)")
            else:
                print(f"{warna_wallet}[SUKSES] Wallet {akun['nomor_wallet']}: Heartbeat terkirim untuk {akun['decoded']['wallet_address']} (tanpa proxy)")

            return response.json()
        except Exception as e:
            akun["status"] = "error"
            print(f"{Fore.RED}[ERROR] Wallet {akun['nomor_wallet']}: Gagal mengirim heartbeat untuk {akun['decoded']['wallet_address']}: {e}")
            return None

    def mulai(self):
        """Memulai layanan heartbeat."""
        self.muat_akun()
        print(f"{Fore.CYAN}[INFO] Layanan heartbeat dimulai pada {self.waktu_mulai}.")

        # Menampilkan akun aktif
        print(f"\n[AKUN] Akun aktif:")
        for akun in self.akun:
            last_heartbeat = akun.get("last_heartbeat", "Belum pernah")
            exp_date = datetime.fromtimestamp(akun["decoded"]["exp"]).strftime("%Y-%m-%d %H:%M:%S")
            print(
                f"  - Wallet {akun['nomor_wallet']}: {akun['decoded']['wallet_address'][:10]}... | "
                f"Terakhir heartbeat: {last_heartbeat} | "
                f"Kadaluarsa: {exp_date} | "
                f"Status: {akun.get('status', 'menunggu')}"
            )

        # Spasi sebelum mulai mengirim heartbeat
        print()

        # Loop pengiriman heartbeat
        while True:
            for akun in self.akun:
                if cek_kadaluarsa_token(akun):
                    print(f"{Fore.YELLOW}[PERINGATAN] Wallet {akun['nomor_wallet']}: Token kedaluwarsa untuk {akun['decoded']['wallet_address']}")
                    akun["status"] = "kedaluwarsa"
                    continue

                self.kirim_heartbeat(akun)
                time.sleep(1)  # Jeda 1 detik antar akun

            time.sleep(APP_CONFIG["heartbeat_interval"] / 1000)  # Jeda sesuai interval

# Fungsi utama untuk menjalankan bot
def main():
    """Fungsi utama untuk menjalankan bot."""
    tampilkan_banner()  # Menampilkan banner

    # Konfirmasi penggunaan proxy
    gunakan_proxy = tanya_penggunaan_proxy()

    # Memulai layanan heartbeat
    layanan = LayananHeartbeat(gunakan_proxy)
    try:
        layanan.mulai()
    except KeyboardInterrupt:
        print(f"\n{Fore.CYAN}[INFO] Layanan heartbeat dihentikan.")

if __name__ == "__main__":
    main()
