# Installation: pip3 install python-telegram-bot
# Usage:        /cmd COMMAND
# Examples:     /cmd whoami, /cmd ls -la, /cmd echo "a" > a.txt 

import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Fill with your token after creating a bot using @BotFather
TOKEN = "8637155031:AAFyWKES1RanFGEiwotzobhJE3gJhJyBuwY"

def exec_cmd(command: str) -> str:
    """Executes a shell command safely and returns the output."""
    try:
        sub_ = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        subprocess_return, _ = sub_.communicate()
        return subprocess_return.decode("utf-8", errors="ignore")
    except Exception:
        return "There was an error executing the command."

async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Async command handler for executing CLI instructions via Telegram."""
    if not update.message:
        return
        
    chat_id = update.message.chat_id
    command = " ".join(context.args) if context.args else ""
    
    if not command:
        await context.bot.send_message(chat_id=chat_id, text="Please provide a command to execute. Example: /cmd whoami")
        return

    # Execute the command (consider running in an executor if blocking is heavy)
    subprocess_return = exec_cmd(command)
    
    # Truncate output if it exceeds Telegram's message character limit (4096 chars)
    if len(subprocess_return) > 4000:
        subprocess_return = subprocess_return[:4000] + "\n[Output truncated...]"

    await context.bot.send_message(chat_id=chat_id, text=subprocess_return or "Command executed with no output.")

def main() -> None:
    """Start the bot."""
    # Build application using the modern v20+ pattern
    application = Application.builder().token(TOKEN).build()

    # Register command handler
    application.add_handler(CommandHandler("cmd", cmd))

    # Start the Bot polling loop
    application.run_polling()

if __name__ == "__main__":
    main()