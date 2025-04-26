name: Test | MetaTrader5 Integration Test

on: [push]

jobs:
  build:
    strategy:
      matrix:
        os: [windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Download MetaTrader5 Installer
      run: |
        $url = "https://download.mql5.com/cdn/web/metaquotes.software.corp/mt5/mt5setup.exe"
        $output = "$env:GITHUB_WORKSPACE\mt5setup.exe"
        Invoke-WebRequest -Uri $url -OutFile $output
      shell: pwsh

    - name: Install MetaTrader5
      run: |
        $installArgs = @(
          "/S",
          "/portable=$env:GITHUB_WORKSPACE\MT5Portable",
          "/skipupdate"
        )
        Start-Process "$env:GITHUB_WORKSPACE\mt5setup.exe" -ArgumentList $installArgs -Wait -NoNewWindow
        if (-not (Test-Path "$env:GITHUB_WORKSPACE\MT5Portable\terminal64.exe")) {
          Write-Error "Installation failed - terminal.exe not found"
          exit 1
        }
      shell: pwsh

    - name: Launch MetaTrader5
      run: |
        $mt5Path = "$env:GITHUB_WORKSPACE\MT5Portable\terminal64.exe"
        $configPath = "$env:GITHUB_WORKSPACE\MT5Portable\config"
        
        # Create basic configuration
        New-Item -Path $configPath -ItemType Directory -Force
        Set-Content -Path "$configPath\servers.dat" -Value "YourServerHere,Demo,ServerAddressHere,443"

        # Launch with headless options
        $process = Start-Process $mt5Path -ArgumentList @(
          "/portable", 
          "/headless",
          "/config:$configPath",
          "/login:12345 /password:demo /server:ServerAddressHere"
        ) -PassThru
        
        # Wait and verify process
        Start-Sleep -Seconds 60
        if ($process.HasExited -or -not (Get-Process terminal64 -ErrorAction SilentlyContinue)) {
          Write-Error "Failed to launch MT5"
          Get-Content "$env:GITHUB_WORKSPACE\MT5Portable\logs\*.log" | Write-Host
          exit 1
        }
      shell: pwsh

    - name: Run MT5 Test
      run: |
        python -c "import os, MetaTrader5 as mt5
        print('Python version:', os.sys.version)
        for i in range(10):
            try:
                if mt5.initialize():
                    print('MT5 initialized successfully')
                    print(mt5.terminal_info())
                    mt5.shutdown()
                    exit(0)
                print(f'Attempt {i+1} failed')
            except Exception as e:
                print(f'Error: {str(e)}')
            import time; time.sleep(10)
        print('All attempts failed')
        exit(1)"