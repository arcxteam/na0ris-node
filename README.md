# A Completed Guides - Naoris Protocol Run Node DePIN

![image](https://github.com/user-attachments/assets/4594fa32-8c9e-4e51-9782-319404d2acbd)

## Here We Go...GAS 

**`Is there incentivized?` ![Confirm](https://img.shields.io/badge/confirm-yes-brightgreen)**

> [!IMPORTANT]
> **Disclaimer:**: This rewards structure is subject to change at any time. The entire point system and associated benefits may be revamped depending on testnet developments. Naoris reserves all rights to modify or update these terms as necessary to ensure optimal network growth and functionality. [Detail](https://www.naorisprotocol.com/blog/user-guide-to-points-referrals)

---

## **Fitur**

- **Pengiriman heartbeat otomatis**  
  Mengirimkan sinyal heartbeat secara berkala ke server

- **Dukungan penggunaan proxy (HTTP/s, SOCKS4, SOCKS5)**  
  Bekerja dengan berbagai jenis proxy untuk menjaga anonimitas

- **Tampilan status akun dan log aktivitas**  
  Menampilkan status terkini dan riwayat aktivitas akun

- **Dukungan multi-wallet dengan warna berbeda**  
  Mengelola beberapa wallet sekaligus dengan identifikasi warna unik

---

## **Persyaratan**

- **Python 3.7 atau lebih baru**
- **Modul Python yang diperlukan (lihat di bawah)**
- **Pm2 - Proses Manager (biar lebih tertata/termonitor)**
- **Proxy (opsional)**

---

## A. Setup Install
**1. Proxies Akun (residentials)**

- Saya menghargai Anda, `GUE GAK PROMOSI, TAPI KARENA GUE PAKAI GUNAKAN` Jika membutuhkan proxy, 2captcha adalah yang terbaik, aman aja. Ada promo diskon 50% mulai 1GB/$3, bayar pakai kripto tanpa biaya, low-bandwitch + pengaturan lokasi IP yang rotasi tergantung generate kamu. [COBA DAFTAR AJA](https://2captcha.com/?from=24919769)

![image](https://github.com/user-attachments/assets/ac433d24-f082-4ade-9269-a1dea2a71695)

**2. Naoris Menu Utama**

- Cek menu register https://naorisprotocol.network/testnet
- Ikuti aja perintahnya download wallet + node extention (kalo udah run hapus extensi aja)
- Kode refferal gue ini `sVaFdrRX6zV8AsZO`

**B. Install Bang**

1. **Kloning Repositori & Instal Modul:**

  - Kloning repo
  ```bash
  git clone https://github.com/arcxteam/na0ris-node.git
  cd na0ris-node
  ```
  - Install PM2 
  ```
  npm install -g pm2
  ```
  - Instal Modul
   ```bash
   pip3 install -r requirements.txt
   ```

---

2. **Cara Menjalankan**

- Dapatkan token dengan membuka DevTools `CTRL+SHIFT+i` atau `F12` atau `inspection` di ekstensi Naoris Protocol Node contoh token dimulai dengan devicehash `36252513`

![image](https://github.com/user-attachments/assets/315221bb-1cfc-4d91-884d-70197f7597a2)

- Tempel wallet & hash device yang ente punya ke dalam file `accounts.json` lalu CTRL+X dan Y
  ```
  nano accounts.json
  ```

- Jika menggunakan proxy (opsional), tambahkan ke file `proxy.txt` dengan format lalu CTRL+X dan Y
  
  `http://username:password@host:port | socks4://username:password@host:port | socks5://username:password@host:port | http://host:port | socks4://host:port | socks5://host:port`
  
  ```
  nano proxy.txt
  ```
- Jalankan dengan python
  ```
  python3 naoris.py
  ```
- Lalu Jalankan dengan Pm2
  ```
  pm2 start naoris.py --name naoris-bot
  ```

---

## **Catatan**
- `accounts.json`: Berisi token devicehash dan alamat dompet
- `proxy.txt`: Berisi daftar proxy 
- `naoris.py`: Skrip utama bot

## C. Cek Command logs

- status logs info `pm2 logs naoris-bot`
- status manejemen PM2 `pm2 status` atau `pm2 monit`
- Untuk stop&delete `pm2 stop naoris-bot` | `pm2 delete naoris-bot`
