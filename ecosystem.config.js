module.exports = {
  apps: [{
    name: "naoris-bot",
    script: "naoris.py",
    interpreter: "python3",
    autorestart: true,
    watch: false,
    max_memory_restart: "300M",
    env: {
      NODE_ENV: "production"
    }
  }]
}
