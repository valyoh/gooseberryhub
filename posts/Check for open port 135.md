---
title: "Check for open port 135"
date: "2024-10-22"
---

To check if **port 135** (used by **RPC Endpoint Mapper**, essential for WMI and DCOM communication) is open on a remote machine, you can use several methods. Here's a guide to check the status of port 135, both locally and remotely.

### 1. **Using `Telnet`**
You can use **Telnet** to check if port 135 is open on a remote machine.

#### Steps:
1. **Enable Telnet (if it's not already installed)**:
   - On Windows: Open **Command Prompt** with administrator privileges and run:
     ```cmd
     dism /online /Enable-Feature /FeatureName:TelnetClient
     ```
   - On Linux/macOS: Telnet is often pre-installed, or you can install it via your package manager.
     ```bash
     sudo apt-get install telnet    # On Ubuntu/Debian
     sudo yum install telnet        # On CentOS/RHEL
     ```

2. **Use Telnet to Check Port 135**:
   ```cmd
   telnet <RemoteComputerName or IP> 135
   ```
   - If the connection is successful, you’ll get a blank screen, which indicates that port 135 is open.
   - If the connection fails, you’ll see an error like `Could not open connection to the host`, meaning the port is closed or blocked.

### 2. **Using `PowerShell` and `Test-NetConnection`**
In **PowerShell**, you can use the `Test-NetConnection` cmdlet to check if a specific port is open.

#### Command:
```powershell
Test-NetConnection -ComputerName <RemoteComputerName or IP> -Port 135
```

#### Output:
- If the port is open, you’ll see:
  ```plaintext
  TcpTestSucceeded : True
  ```
- If the port is closed, you’ll see:
  ```plaintext
  TcpTestSucceeded : False
  ```

### 3. **Using `Nmap`**
You can use **Nmap** to scan for open ports, including port 135.

#### Steps:
1. **Install Nmap**:
   - On Windows, you can download Nmap from the [Nmap website](https://nmap.org/download.html).
   - On Linux/macOS, you can install it via package managers:
     ```bash
     sudo apt-get install nmap    # On Ubuntu/Debian
     sudo yum install nmap        # On CentOS/RHEL
     ```

2. **Run Nmap to Check Port 135**:
   ```bash
   nmap -p 135 <RemoteComputerName or IP>
   ```
   - If port 135 is open, Nmap will show it as **open** in the scan results.
   - If it's closed or filtered, Nmap will indicate that as well.

### 4. **Using `Netstat` Locally**
To check if port 135 is **listening locally** on the machine, you can use the `netstat` command.

#### Command:
- **On Windows**:
  ```cmd
  netstat -an | find "135"
  ```
- **On Linux (for RPC services)**:
  ```bash
  sudo netstat -tuln | grep 135
  ```

#### Output:
- If port 135 is open, you’ll see an entry like this:
  ```plaintext
  TCP    0.0.0.0:135      LISTENING
  ```

### 5. **Using `Firewall Rules`**
You can check firewall rules to see if port 135 is allowed.

#### On Windows (via Command Prompt or PowerShell):
- **Command Prompt**:
  ```cmd
  netsh advfirewall firewall show rule name=all | findstr 135
  ```
- **PowerShell**:
  ```powershell
  Get-NetFirewallRule | Where-Object { $_.LocalPort -eq "135" }
  ```

#### On Linux (via `iptables`):
```bash
sudo iptables -L -n | grep 135
```

### 6. **Using Online Tools**
If you want to check if port 135 is open on an external machine from the internet (outside the local network), you can use online port scanning services such as:
- [Canyouseeme.org](http://canyouseeme.org/) – Enter port 135 and the target IP to check if it’s accessible.

### Summary of Methods:
- **Telnet**: Simple test for connectivity.
- **PowerShell**: Use `Test-NetConnection` for a quick test on Windows.
- **Nmap**: A more comprehensive network scan tool for checking open ports.
- **Netstat**: Check locally if port 135 is listening.
- **Firewall Rules**: Ensure firewall rules allow traffic on port 135.

These methods help ensure that **port 135 is open**, which is necessary for WMI, DCOM, and RPC-based communications.