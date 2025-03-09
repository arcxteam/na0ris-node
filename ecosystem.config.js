module.exports = {
  apps: [{
    name: "naoris-bot",
    script: "naoris.py",
    interpreter: "python3",
    autorestart: true,
    watch: true,
    max_memory_restart: "150M",
    restart_delay: 10000,
    log_date_format: "YYYY-MM-DD HH:mm:ss Z",
    error_file: "logs/naoris-error.log",
    out_file: "logs/naoris-out.log",
    merge_logs: true,
    max_size: "10M",
    rotate_logs: true,
    env: {
      PYTHON_ENV: "production",
      TZ: "Asia/Jakarta"
    }
  }]
}