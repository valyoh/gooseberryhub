---
title: "WMI Connection requirements "
date: "2024-10-22"
---
To establish a **Windows Management Instrumentation (WMI)** connection to a remote PC, several requirements need to be fulfilled. WMI provides a standardized way to interact with and manage remote Windows systems, but for it to work over the network, certain services, ports, permissions, and firewall settings must be correctly configured.

Here’s a breakdown of what is needed:

### 1. **WMI Service**
The **WMI service** must be running on both the local and remote machines to facilitate WMI queries and operations.

- **Service Name**: `Winmgmt`
- **Start Type**: Ensure that the service is set to **Automatic** or **Manual** if it needs to be manually started.
  - Check the status of the service using the following in PowerShell:
    ```powershell
    Get-Service winmgmt
    ```

### 2. **User Permissions**
The user account making the connection must have appropriate permissions on the remote machine.

- **Local Administrator Rights**: By default, only members of the **Administrators group** can make WMI connections to a remote machine.
- **WMI Namespace Permissions**: The user must have access to the appropriate WMI namespaces (typically `root\cimv2`). You can grant a user permission using the **wmimgmt.msc** snap-in:
  1. Open `wmimgmt.msc` on the target machine.
  2. Right-click **WMI Control (Local)** and select **Properties**.
  3. Under the **Security** tab, select the namespace (`root\cimv2`).
  4. Click **Security**, add the user, and grant the necessary permissions (e.g., **Remote Enable**).

### 3. **Windows Firewall Configuration**
The firewall on the remote machine must allow traffic on the necessary ports for WMI to work.

- **WMI-related Ports**:
  - **RPC Endpoint Mapper**: Port 135 (TCP) must be open to allow initial RPC communication.
  - **Dynamic RPC Ports**: WMI uses dynamic ports assigned by the system in the range of 1024 to 65535. To limit this to a specific range, you can configure the dynamic port range used by WMI.
    - **Limiting Ports**: To define a specific range for RPC traffic (e.g., 5000-5100):
      ```cmd
      netsh int ipv4 set dynamicport tcp start=5000 num=100
      ```
  - **Firewall Rule**: Ensure the following rule is enabled:
    - **Allow Remote Administration (RPC)** or manually create a rule to allow TCP on port 135 and the dynamic range.
  
  **Example to open necessary ports in Windows Firewall**:
  ```powershell
  netsh advfirewall firewall set rule group="Windows Management Instrumentation (WMI)" new enable=yes
  ```

### 4. **DCOM Configuration**
**DCOM (Distributed Component Object Model)** is required for WMI to work over a network, as WMI uses DCOM for remote communication.

- **Ensure DCOM is Enabled**:
  1. Open **Component Services** (`dcomcnfg`).
  2. Expand **Component Services** > **Computers** > **My Computer**.
  3. Right-click **My Computer** and select **Properties**.
  4. Under the **Default Properties** tab, ensure the following:
     - **Enable Distributed COM on this computer** is checked.
     - **Default Authentication Level** is set to **Connect**.
     - **Default Impersonation Level** is set to **Identify** or higher.

### 5. **Remote UAC Consideration**
In non-domain environments or when using local accounts, **User Account Control (UAC)** might prevent remote connections, even for administrators. Remote UAC can block remote execution privileges unless the user is accessing the machine via a domain account or UAC is configured to allow it.

To disable Remote UAC for WMI, modify the registry on the target machine:

- **Registry Key**:
  - Path: `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System`
  - Key: `LocalAccountTokenFilterPolicy`
  - Value: `1` (This disables UAC filtering for local accounts, allowing them to connect via WMI remotely).
  
  **Command to disable Remote UAC**:
  ```cmd
  reg add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v LocalAccountTokenFilterPolicy /t REG_DWORD /d 1 /f
  ```

### 6. **Network Connectivity**
- **DNS Resolution**: Ensure that you can resolve the remote machine’s name via DNS or provide its IP address.
- **Ping**: Test the network connectivity to ensure the machines can communicate:
  ```cmd
  ping <RemoteComputerName>
  ```

### 7. **WMI Query Execution**
Once all of the above are in place, you can use WMI to connect to the remote machine. The most common tool for this is **PowerShell**.

- **PowerShell Command Example**:
  ```powershell
  Get-WmiObject -Class Win32_OperatingSystem -ComputerName <RemoteComputerName> -Credential <AdminUsername>
  ```

Alternatively, you can also use the WMI Command-Line (WMIC) tool:

```cmd
wmic /node:<RemoteComputerName> /user:<AdminUsername> /password:<AdminPassword> computersystem get name
```

### Summary of Requirements:
1. **WMI Service (`Winmgmt`)** must be running.
2. **User Permissions**: The user needs to be a member of the **Administrators group** and have WMI namespace access.
3. **Firewall Ports**: Open port 135 (RPC) and configure dynamic ports for RPC communication.
4. **DCOM Configuration**: DCOM must be enabled on the remote machine.
5. **Remote UAC**: Disable Remote UAC (optional, but required for local accounts).
6. **Network**: Ensure network connectivity and DNS resolution between the local and remote machines.

By ensuring all of these elements are configured correctly, you'll be able to successfully establish a WMI connection to a remote PC.