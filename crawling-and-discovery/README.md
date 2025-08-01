# Domain Crawling Automation Script

A comprehensive Python script that automates crawling for given domains using multiple popular security tools.

## Features

- **Multi-tool Integration**: Runs waymore, waybackurls, gau, and katana
- **Threading Support**: Katana runs in parallel across 3 different modes
- **Colored Output**: Beautiful terminal output with status indicators
- **Error Handling**: Robust error handling and timeout management
- **Flexible Input**: Accepts single domain or file with multiple domains
- **Organized Output**: Creates timestamped directories for each crawl session

## Required Tools

Before running the script, ensure you have the following tools installed:

1. **waymore** - Wayback Machine URL discovery
2. **waybackurls** - Wayback Machine URL extraction
3. **gau** - Get All URLs from various sources
4. **katana** - Web crawling framework

### Installation Links

- **waymore**: https://github.com/xnl-h4ck3r/waymore
- **waybackurls**: https://github.com/tomnomnom/waybackurls
- **gau**: https://github.com/lc/gau
- **katana**: https://github.com/projectdiscovery/katana

## Usage

### Basic Usage

```bash
# Crawl a single domain
python crawler.py example.com

# Crawl multiple domains from a file
python crawler.py -f domains.txt

# Check if required tools are available
python crawler.py --check-tools
```

### Command Line Options

- `domain`: Single domain to crawl
- `-f, --file`: File containing list of domains (one per line)
- `--check-tools`: Check if all required tools are available

### Examples

```bash
# Crawl a single domain
python crawler.py google.com

# Crawl multiple domains
python crawler.py -f target_domains.txt

# Check tool availability first
python crawler.py --check-tools
```

## Output Structure

The script creates a timestamped directory for each crawl session:

```
crawl_results_example.com_20231201_143022/
├── waymore_output.txt
├── waybackurls_output.txt
├── gau_output.txt
├── katana_depth-first.txt
├── katana_breadth-first.txt
└── katana_headless.txt
```

## Tools Executed

### 1. waymore
```bash
waymore -i $domain -mode U -oU
```
Discovers URLs from Wayback Machine with unique mode.

### 2. waybackurls
```bash
cat subdomains.txt | waybackurls
```
Extracts URLs from Wayback Machine for discovered subdomains.

### 3. gau
```bash
cat subdomains.txt | gau
```
Gets all URLs from various sources for discovered subdomains.

### 4. katana (3 modes)
```bash
# Depth-first mode
katana -d 5 -jc -ct 1h -aff -fx -s depth-first -o katana-df.txt

# Breadth-first mode
katana -d 5 -jc -ct 1h -aff -fx -s breadth-first -o katana-bf.txt

# Headless mode
katana -d 5 -jc -ct 1h -aff -fx -headless -o katana-headless.txt
```

## Features

### Threading
- Katana runs in all three modes simultaneously using threading
- Improves performance and reduces total execution time

### Error Handling
- Timeout protection (1 hour default)
- Tool availability checking
- Graceful failure handling
- Detailed error reporting

### Colored Output
- Green: Success messages
- Red: Error messages
- Yellow: Warning messages
- Blue: Information messages
- Cyan: Progress indicators

### Input Validation
- Checks for required tools before execution
- Validates input parameters
- Handles missing files gracefully

## Sample domains.txt

Create a file with domains (one per line):

```
example.com
google.com
github.com
```

## Requirements

- Python 3.6+
- All required tools installed and available in PATH
- Internet connection for tool execution

## Troubleshooting

### Common Issues

1. **"Command not found" errors**
   - Ensure all tools are installed and in your PATH
   - Use `--check-tools` to verify installation

2. **Permission errors**
   - Ensure you have write permissions in the current directory

3. **Timeout errors**
   - Large domains may take longer to crawl
   - Consider running on smaller subdomains first

4. **Missing subdomains.txt**
   - The script will create an empty file if not found
   - Consider running subdomain enumeration tools first

### Performance Tips

- Run on smaller domains first to test
- Use SSD storage for better I/O performance
- Ensure sufficient RAM for concurrent katana instances
- Consider running during off-peak hours for better network performance

## License

This script is provided for educational and authorized security testing purposes only. Always ensure you have proper authorization before crawling any domain. 