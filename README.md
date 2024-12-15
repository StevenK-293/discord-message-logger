# Discord Message Logger

A Python bot for logging messages from public Discord servers. This bot logs both really old message and live messages, and it saves the messages in `.txt` and `.json` formats for easy access and analysis.

---

## Usage

1. **Old Message Fetching**:
   - When the bot starts, it fetches all Old messages from all accessible text channels in the servers where the bot is present.
   - Progress bars will display the status of the fetching process.

2. **Live Logging**:
   - New messages are logged in real-time as they are sent in the server.

3. **Log Storage**:
   - Logs are stored in `message_storage_log/<server-name>/`.
   - Each server has its own `.txt` and `.json` files containing the messages.

---

## Example Logs

- **TXT Format**:
  ```plaintext
  [2024-12-14 10:00:00] Channel: general, Author: User#1234, Message: Hello, world!
  ```

- **JSON Format**:
  ```json
  [
    {
      "timestamp": "2024-12-14 10:00:00",
      "channel": "general",
      "author": "User#1234",
      "message": "Hello, world!"
    }
  ]
  ```

---

## License

Free to use

