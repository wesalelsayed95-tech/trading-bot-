name: Run C++ Bot Automatically

on:
  workflow_dispatch:
  schedule:
    - cron: '0 */6 * * *'

jobs:
  build-and-run:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Set up GCC compiler
      run: sudo apt-get update && sudo apt-get install -y build-essential libcurl4-openssl-dev nlohmann-json3-dev

    - name: Compile C++ code
      run: g++ -O3 run_bot.cpp -o run_bot_executable -lcurl -lpthread

    - name: Run compiled bot
      env:
        GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
      run: ./run_bot_executable
