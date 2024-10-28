---
title: "Automating Change Label Exports"
date: "2024-10-25"
---

### Automating One Identity Change Label Exports with PowerShell: A Step-by-Step Guide

When managing databases and IAM (Identity and Access Management) tools, there are times when you need to export specific tags or objects 
for use in other systems or environments. Here’s a breakdown of a PowerShell script that streamlines this process by automating data export
from a SQL Server database for transporting other systems using One Identity Manager’s `DBTransporterCmd.exe` command-line tool.

This script leverages PowerShell, SQL queries, and XML handling to create an export file while ensuring compatibility with secure connections.

This guide provides a breakdown of the PowerShell script, which:
1. Connects to a specified SQL Server instance and database.
2. Retrieves a unique identifier (`UID_DialogTag`) based on a provided tag name (`Ident_DialogTag`).
3. Structures the data into an XML template.
4. Saves the XML output to a specified location.
5. Uses `DBTransporterCmd.exe` to export the change labels for further usage.

### Script Walkthrough

---

#### **Parameters Setup**

The script starts by defining six parameters:

```powershell
param (
    [string]$DatabaseName = "",         
    [string]$ServerInstance = "",   
    [string]$username = '',
    [string]$password = '',
    [string]$identValue = '',
	[string]$userId = ''
)
```

- **DatabaseName**: The name of the database to connect to.
- **ServerInstance**: The SQL Server instance name.
- **username** and **password**: Used for authenticating the `DBTransporterCmd.exe` transport step, representing a system user who has the necessary permissions for data export. These credentials are not used for the initial database query (which relies on integrated security) but specifically for transport authentication.
- **identValue**: A unique tag identifier (`Ident_DialogTag`), used to locate the specific tag in the database.
- **userId**: An identifier that is used to create the export filename, differentiating it by user and date.

#### **Current Directory & Tool Paths**

```powershell
$currentDir = Get-Location
Write-Host $currentDir.Path
$oim_tools_location="C:\IAMTools\" # The location of the One Identity Manager tools
$outputPath = "C:\Temp\" # The path where the transport file will be outputed
$outputFile = "TransportTemplate.xml" # Name of the template xml, later used as parameter
```

The script stores the initial directory to return to it later. It then defines:
- **oim_tools_location**: Path to the One Identity Manager tools directory containing `DBTransporterCmd.exe`.
- **outputPath** and **outputFile**: Directory and filename where the XML template will be saved.

#### **Enforcing Secure TLS Connection**

```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
```

TLS 1.2 is enforced to ensure secure connections when the script interacts with SQL Server or other services over HTTPS, 
providing strong encryption by default.

#### **Database Connection & Query Execution**

```powershell
$connectionString = "Server=$ServerInstance;Database=$DatabaseName;Integrated Security=True;TrustServerCertificate=True"
$sqlQuery = "SELECT UID_DialogTag FROM DialogTag WHERE Ident_DialogTag = '$identValue'"
```

A connection string using **Integrated Security** connects to SQL Server. For systems using untrusted SSL, `TrustServerCertificate=True` is added to ensure the connection proceeds without certificate verification issues.

The **SQL query** retrieves `UID_DialogTag` based on the specified `identValue`, which is necessary for structuring the XML export.

#### **Error Handling**

```powershell
try {
    $result = Invoke-Sqlcmd -ConnectionString $connectionString -Query $sqlQuery -MaxCharLength 2147483647
    $pkValue = $result[0]
    Write-Host "UID_DialogTag: $pkValue"
} catch {
    Write-Host "Error querying the database: $_"
    exit
}
```

A `try-catch` block handles errors gracefully. If any issue arises during the query execution, a message is displayed, and the script halts.

#### **Building the XML Export Template**

```powershell
$xmlTemplate = @"
<TransportTemplate Version="1.0">
  <Header>
    <Parameter Name="Description">$identValue</Parameter>
  </Header>
  <Tasks>
    <Task Class="VI.Transport.TagTransport, VI.Transport" Display="TagTransport">
      <Parameter Name="Tags">
        <Parameter Name="PK">$pkValue</Parameter>
      </Parameter>
      <Parameter Name="Options">
        <Parameter Name="LockTags">1</Parameter>
        <Parameter Name="UseRelations">0</Parameter>
      </Parameter>
    </Task>
  </Tasks>
</TransportTemplate>
"@
```

The XML structure is built using the retrieved `UID_DialogTag` value, with:
- **Description**: Set to `identValue`, providing context for the exported data.
- **PK**: Primary key (`UID_DialogTag`) used to identify the specific tag.
- **Options**: Configured to lock tags (`LockTags=1`) and not use relations (`UseRelations=0`).

#### **Saving the XML File**

```powershell
$location = "${outputPath}${outputFile}"
$xmlTemplate | Out-File -FilePath $location -Encoding UTF8
Write-Host "XML file generated successfully at $location"
```

The XML template is saved with UTF-8 encoding, ensuring compatibility across systems and avoiding encoding-related issues.

#### **Generating the Transport Filename**

```powershell
$dateStr = Get-Date -Format "yyyyMMdd"
$transportFilename="${outputPath}Transport_${identValue}_${userId}_${dateStr}.zip"
```

The `transportFilename` is dynamically generated using:
- `identValue` and `userId` (to identify the developer of the change label).
- The current date in **yyyyMMdd** format.
  
This unique filename structure prevents overwriting and helps identify when each export was created and by whom.

#### **Launching the DBTransporterCmd Tool**

The **DBTransporterCmd.exe** tool is a command-line utility for One Identity Manager, designed for exporting and transporting data from one OIM system to other. 
The `DBTransporterCmd.exe` tool is configured with specific command-line arguments for this process:

```powershell
$trasporterParams = " /File=""${transportFilename}"" /Conn=""Server=${ServerInstance}; Database=${DatabaseName}; Integrated Security=SSPI;"" /Auth=""Module=DialogUser;User=${username};Password=${password}"" /template=""c:\temp\${outputFile}"""
```

Key points for each parameter:
- **/File**: Specifies the name and path of the export file.
- **/Conn**: Defines the database connection, using integrated security to ensure a secure connection.
- **/Auth**: Specifies the use of a system user (dialog user) as defined by `username` and `password`. 
These are system-level credentials specifically required for One Identity Manager.

- **/template**: Points to the XML file generated by the script.

Finally, the script changes to the directory containing `DBTransporterCmd.exe`, launches it with the specified parameters, and then returns to the original working directory:

```powershell
Set-Location -Path $oim_tools_location
Start-Process ".\DBTransporterCmd.exe" -ArgumentList $trasporterParams
Set-Location -Path $currentDir
```

With these modules and configurations in place, the PowerShell script will be able to execute SQL queries, handle XML, and run the secure transport process with `DBTransporterCmd.exe`.

### Prerequisites: PowerShell Modules Required

To run this script successfully, certain PowerShell modules are required, specifically:

1. **SQL Server Module**: The script relies on `Invoke-Sqlcmd` to execute SQL queries against the database, which is available in the **SQLServer** PowerShell module. This module must be installed and imported into your PowerShell environment. You can install it from the PowerShell Gallery with the following command:

   ```powershell
   Install-Module -Name SqlServer
   ```

   After installation, import the module at the start of your session with:

   ```powershell
   Import-Module SqlServer
   ```

   This ensures that `Invoke-Sqlcmd` is available for querying SQL Server.

2. **PowerShell Execution Policy**: Make sure the PowerShell execution policy on your system allows running scripts. You can check and set this by using:

   ```powershell
   Get-ExecutionPolicy
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **.NET Framework**: Since the script manipulates XML and uses the `[Net.ServicePointManager]` to enforce TLS 1.2, it requires a compatible .NET Framework version (4.5 or newer). 

### **Conclusion**

This PowerShell script is a streamlined solution for exporting specific tags from a SQL Server database and preparing them 
for transport in One Identity Manager. By structuring the data in XML format and using the secure `DBTransporterCmd.exe` tool, 
the script enables database administrators to perform exports efficiently and securely. 
Parameters such as `userId`, `identValue`, and system user credentials ensure traceability and security, and 
the flexible file naming structure makes it easy to track exports. This approach can be adapted or 
extended for other export or automation needs within IAM or similar systems.

### **Access the Script on GitHub**

The full PowerShell script, along with any future updates, is available on GitHub. 
You can find it [here on GitHub](https://github.com/valyoh/powershellscripts). 
Feel free to clone the repository, submit issues, or contribute improvements.


