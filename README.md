<br />    
<p align="center">
<a href="https://github.com/danielepelleg/PercentageTrainingBot">
    <img src="https://cdn-icons-png.flaticon.com/512/2738/2738580.png" alt="Logo" width="130" height="130">
</a>
<h1 align="center">Percentage Training Bot</h1>
<p align="center">
    Telegram Bot to spare time during your Percentage Based Training program. It keeps track of your weights in relation of your maximum capacity.
</p>
  
<!-- TABLE OF CONTENTS -->
## 📚 Table of Contents
  
- [📚 Table of Contents](#-table-of-contents)
- [🤖 About The Project](#-about-the-project)
- [🔨 Getting Started](#-getting-started)
  - [Updates](#updates)
- [⚙️ Commands](#️-commands)
- [🔑 LICENSE](#-license)
- [Contributors](#contributors)

## 🤖 About The Project
**Percentage Training Bot** is a Telegram bot running on Python3 which can be used during a training session. The bot is useful for the Percentage Training Programs to improve phisical strength, such as the ones used in sports such as Powerlifting, Weightlifting or Crossfit.

The bot registers the user's true or estimated 1-rep max for a certain exercise (also known as PRs or RMs). Once registered, the user can access to the table showing all the percentages of that exercise by just typing */tables* and selecting the exercise name. 

## 🔨 Getting Started
1. Insert your *API_KEY* and your *PostgreSQL Database credentials* in a *.env* file placed in the root directory. 
2. Install the dependencies by running:
    ```bash
    $> pip install -r requirements.txt
    ```
3. Run the *bot/main.py* file to run your bot on Telegram.

### Updates
Pull this repository for updates.

## ⚙️ Commands
This is the list of commands available within the bot:
- `/start` Starts the bot. It allows the bot to store user's first informations, such as chat ID and it's first name.
- `/help` Show the list of available commands to the user.
- `/set` Set the user's training type.
- `/exercise` Allow the user to set his PRs for the exercise chosen. 
- `/tables` Display a keyboard that allows the user to see his PR's tables.

## 🔑 LICENSE

Distributed under the GPL License. See `LICENSE` for more information.

## Contributors

[Daniele Pellegrini](https://github.com/danielepelleg)


