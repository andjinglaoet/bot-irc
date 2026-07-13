import socket
import time

# ==========================================
# SETTINGAN BOT KAMU (Bebas Ubah)
# ==========================================
SERVER = "irc.austnet.org"
PORT = 6667
NICK = "GatorZ"  # Nama/Nick bot kamu di IRC (bebas diganti)
CHANNEL = "#AndjingLaoet"  # Channel milik kamu
OWNER = "AndjingLaoet"  # Nick mIRC kamu pas online
# ==========================================


def run_bot():
  while True:
    try:
      print(f"[+] Menghubungkan ke {SERVER}...")
      irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      irc.connect((SERVER, PORT))

      # Kirim data identitas bot
      irc.send(f"NICK {NICK}\r\n".encode())
      irc.send(f"USER {NICK} 0 * :Satpam Resmi #AndjingLaoet\r\n".encode())

      time.sleep(3)

      # Join ke channel kamu
      irc.send(f"JOIN {CHANNEL}\r\n".encode())
      print(f"[+] BERHASIL PARKIR DI {CHANNEL}!")

      # Loop penjaga koneksi
      while True:
        data = irc.recv(2048).decode("utf-8", errors="ignore")
        if not data:
          break

        # Tampilkan aktivitas di terminal
        print(data.strip())

        # Auto PONG biar gak disconnect/ping timeout dari server
        if data.startswith("PING"):
          ping_code = data.split()[1]
          irc.send(f"PONG {ping_code}\r\n".encode())

        # Kalau kamu (AndjingLaoet) masuk room, bot otomatis kasih Op (@)
        if "JOIN" in data and OWNER in data:
          irc.send(f"MODE {CHANNEL} +o {OWNER}\r\n".encode())

    except Exception as e:
      print(
          f"[-] Koneksi terputus ({e}). Mencoba Reconnect dalam 10 detik..."
      )
      time.sleep(10)


if __name__ == "__main__":
  run_bot()