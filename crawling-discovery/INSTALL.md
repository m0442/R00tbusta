# Tool Installation Guide

This guide will help you install all the required tools for the domain crawling automation script.

## Prerequisites

- Python 3.6 or higher
- Git
- Go (for some tools)

## Tool Installation

### 1. waymore

```bash
# Clone the repository
git clone https://github.com/xnl-h4ck3r/waymore.git
cd waymore

# Install Python dependencies
pip install -r requirements.txt

# Make it executable (Linux/Mac)
chmod +x waymore.py

# Add to PATH or create alias
alias waymore="python3 /path/to/waymore/waymore.py"
```

### 2. waybackurls

```bash
# Install using Go
go install github.com/tomnomnom/waybackurls@latest

# Or download pre-built binary
# Visit: https://github.com/tomnomnom/waybackurls/releases
```

### 3. gau

```bash
# Install using Go
go install github.com/lc/gau/v2/cmd/gau@latest

# Or download pre-built binary
# Visit: https://github.com/lc/gau/releases
```

### 4. katana

```bash
# Install using Go
go install github.com/projectdiscovery/katana/cmd/katana@latest

# Or download pre-built binary
# Visit: https://github.com/projectdiscovery/katana/releases
```

## Windows Installation

### Using Chocolatey (Recommended)

```powershell
# Install Chocolatey first if not installed
# Then install tools:
choco install go
choco install git

# Install tools using Go
go install github.com/tomnomnom/waybackurls@latest
go install github.com/lc/gau/v2/cmd/gau@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
```

### Manual Installation

1. Download pre-built binaries from respective GitHub releases
2. Extract to a directory (e.g., `C:\Tools\`)
3. Add the directory to your PATH environment variable

## Linux Installation

### Ubuntu/Debian

```bash
# Install Go
sudo apt update
sudo apt install golang-go

# Install tools
go install github.com/tomnomnom/waybackurls@latest
go install github.com/lc/gau/v2/cmd/gau@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest

# Add Go bin to PATH
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.bashrc
source ~/.bashrc
```

### CentOS/RHEL

```bash
# Install Go
sudo yum install golang

# Follow same steps as Ubuntu
```

## macOS Installation

### Using Homebrew

```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Go
brew install go

# Install tools
go install github.com/tomnomnom/waybackurls@latest
go install github.com/lc/gau/v2/cmd/gau@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
```

## Verification

After installation, verify all tools are working:

```bash
# Check if tools are in PATH
which waymore
which waybackurls
which gau
which katana

# Or use the script's built-in checker
python crawler.py --check-tools
```

## Troubleshooting

### Common Issues

1. **"command not found" errors**
   - Ensure tools are in your PATH
   - Restart your terminal after adding to PATH

2. **Permission denied errors**
   - Make sure tools are executable
   - Check file permissions

3. **Go installation issues**
   - Verify Go is properly installed: `go version`
   - Check GOPATH and GOROOT environment variables

4. **Python dependency issues**
   - Use virtual environment: `python -m venv venv`
   - Activate and install: `source venv/bin/activate && pip install -r requirements.txt`

### PATH Configuration

#### Windows
1. Open System Properties → Advanced → Environment Variables
2. Edit PATH variable
3. Add directory containing tool executables
4. Restart terminal

#### Linux/macOS
```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH=$PATH:/path/to/tools
export PATH=$PATH:$(go env GOPATH)/bin
```

## Quick Test

After installation, test with a simple domain:

```bash
python crawler.py example.com
```

This should create a crawl results directory with output files from all tools. 