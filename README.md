# Telegram-Automation-VPN-Sell-Bot


This is a clean and professional README.md for your VPN Sales Bot. You can copy this directly to your project repository.

🚀 Telegram VPN Sales Bot
A professional, automated VPN sales assistant built with aiogram 3.x. This bot allows users to browse VPN plans, make payments, and receive their subscription keys automatically through an admin-approved workflow.

🌟 Key Features
Automated Sales Flow: Users can choose plans and submit payment screenshots directly in the chat.

Admin Dashboard: Admin receives instant notifications with user details and payment proof.

Key Delivery: Admins can send VPN keys directly to users with one click.

Built-in Guides: Users can access step-by-step visual tutorials on how to set up their VPN.

FSM (Finite State Machine): Handles complex user interactions (state management) like ordering and key delivery efficiently.

Commands: Easy-to-use menu commands (/start, /buy, /help).

🛠 Technologies Used
Language: Python 3.10+

Framework: aiogram 3.x (Asynchronous Telegram Bot API)

States Management: FSMContext (Finite State Machine)

API: Telegram Bot API

📋 How to Set Up
1. Requirements
Ensure you have Python installed. Install the necessary library:

Bash
pip install aiogram
2. Configuration
Open main.py and update the constants:

TOKEN: Your Bot Token from @BotFather.

ADMIN_ID: Your personal Telegram User ID (use @userinfobot to get it).

3. Running the Bot
Run the bot script:

Bash
python main.py
💡 How It Works
User: Clicks /start or /buy -> Selects a VPN plan.

User: Sends a payment screenshot -> Bot forwards the photo + user details to the Admin.

Admin: Clicks "Key ပေးမည် 🔑" -> Types the VPN key in the chat.

User: Receives the key instantly from the bot.

🛡 Security Notes
Token Safety: Never share your TOKEN publicly. If you push this code to GitHub, ensure you use environment variables (.env file) to hide your credentials.

Admin Verification: The logic ensures that only the ADMIN_ID can trigger the key delivery process, preventing unauthorized users from sending keys.

🚀 Future Enhancements
Adding a database (SQLite) to track user subscriptions and expiry dates automatically.

Integrating payment gateways for automated verification.

Pro-Tips:
README Badge: If you'd like, you can add a "Build Status" or "Python Version" badge to the top of this README to make it look even more professional.

BotFather: Don't forget to set the bot's description and commands in @BotFather using the /setcommands command to match the ones in your code.
