---
title: "Table Comparison Across Databases "
date: "2024-10-29"
---

### Comparing Tables Across SQL Server Databases with PowerShell

When managing databases across environments, such as development and production, it’s essential to ensure data consistency. 
This PowerShell script compares specific columns in a table across two SQL Server databases. 
Let’s walk through each section to understand how it works and how you can customize it to your needs.

### Prerequisites

- **PowerShell** installed on your machine.
- **Permissions** to connect to both SQL Server instances and query the databases.
- **Database setup** with the table structure and primary keys in place.

### Script Overview

This script:
1. Connects to two SQL Server databases.
2. Retrieves data from a specified table in each database.
3. Compares specific columns for each primary key.
4. Outputs any differences between the two datasets.

### Parameter Definitions

At the beginning, we use the `param` block to define the script’s parameters. 
These include the server instance names, database names, table name, primary key, and the columns to compare.

```powershell
param(
    [string]$ServerInstance1 = "",    
    [string]$ServerInstance2 = "",    
    [string]$Database1 = "",          
    [string]$Database2 = "",          
    [string]$TableName,               
    [string]$PrimaryKeyColumn,        
    [string[]]$ColumnsToCompare       
)
```

Each parameter serves a specific purpose:
- `$ServerInstance1` and `$ServerInstance2` are the server names or IPs of the SQL Server instances.
- `$Database1` and `$Database2` represent the database names on each server.
- `$TableName` is the name of the table we want to compare.
- `$PrimaryKeyColumn` is the primary key column used to identify rows uniquely.
- `$ColumnsToCompare` is an array of column names in the table that we want to compare.

### Connection String Setup

Next, we define connection strings to connect to each database. 
Here, the `TrustServerCertificate=True` option helps connect securely even if the SSL certificate is not trusted by the machine:

```powershell
$ConnectionString1 = "Server=$ServerInstance1;Database=$Database1;Integrated Security=True;TrustServerCertificate=True"
$ConnectionString2 = "Server=$ServerInstance2;Database=$Database2;Integrated Security=True;TrustServerCertificate=True"
```

These connection strings use **Windows Integrated Security**, which requires the user to have permissions on both SQL Server instances.

### Creating a Column List

The `ColumnsToCompare` parameter is used to create a comma-separated list of columns, including the primary key column. 
This will help build the SQL `SELECT` query dynamically:

```powershell
$columnList = $PrimaryKeyColumn + "," + ($ColumnsToCompare -join ", ")
```

### Retrieving Table Data Function

This `Get-TableData` function handles data retrieval by:
1. Building a SQL `SELECT` query.
2. Establishing a connection to the SQL Server.
3. Executing the query and loading the results into a DataTable object.
4. Converting the DataTable into a hashtable, keyed by the primary key value for easy comparison.

```powershell
function Get-TableData {
    param (
        [string]$ConnectionString,
        [string]$Table,
        [string]$Columns
    )

    $query = "SELECT $Columns FROM $Table"
    $connection = New-Object System.Data.SqlClient.SqlConnection
    $connection.ConnectionString = $ConnectionString
    $command = $connection.CreateCommand()
    $command.CommandText = $query

    $dataTable = New-Object System.Data.DataTable

    try {
        $connection.Open()
        $reader = $command.ExecuteReader()
        $dataTable.Load($reader)
        $reader.Close()
    } catch {
        Write-Error "Failed to execute query: $($_.Exception.Message)"
    } finally {
        $connection.Close()
    }

    return $dataTable | Group-Object -Property $PrimaryKeyColumn -AsHashTable -AsString
}
```

### Loading and Comparing Data

After data retrieval, we have two hashtables: `$tableData1` and `$tableData2`. 
Each key represents a primary key from the table, with values holding the row data.

The following block collects all unique keys from both tables into `$allKeys`, which will be used to compare rows across both datasets:

```powershell
$tableData1 = Get-TableData -ConnectionString $ConnectionString1 -Table $TableName -Columns $columnList
$tableData2 = Get-TableData -ConnectionString $ConnectionString2 -Table $TableName -Columns $columnList

$allKeys = [System.Collections.Generic.HashSet[string]]::new()
$tableData1.Keys | ForEach-Object { $allKeys.Add($_) }
$tableData2.Keys | ForEach-Object { $allKeys.Add($_) }
```

### Data Comparison and Output

For each key in `$allKeys`, the script checks if the row exists in both datasets:
1. **Row exists in both**: Each column in `$ColumnsToCompare` is compared. If a difference is found, the column name and differing values are output.
2. **Row missing in one database**: If a row is only in one database, it is identified as missing in the other.

Here’s the comparison and output code:

```powershell
if ($allKeys.Count -eq 0) {
    Write-Output "No differences found between the tables in the specified databases."
} else {
    Write-Output "Differences found:"
    foreach ($key in $allKeys) {
        $row1 = $tableData1[$key]
        $row2 = $tableData2[$key]

        if ($row1 -and $row2) {
            $hasDifference = $false
            foreach ($column in $ColumnsToCompare) {
                if ($row1.$column -ne $row2.$column) {
                    Write-Output "Row ID ($PrimaryKeyColumn): $key - Column '$column' differs"
                    Write-Output "  Database1: $($row1.$column)"
                    Write-Output "  Database2: $($row2.$column)"
                    $hasDifference = $true
                }
            }
            if (-not $hasDifference) {
                Write-Output "Row ID ($PrimaryKeyColumn): $key - No differences found in specified columns."
            }
        } elseif ($row1 -and -not $row2) {
            Write-Output "Row ID ($PrimaryKeyColumn): $key exists only in Database1"
        } elseif ($row2 -and -not $row1) {
            Write-Output "Row ID ($PrimaryKeyColumn): $key exists only in Database2"
        }
    }
}
```

### Customization Options

You can further customize this script by:
- **Adding parameters** for connection authentication (username and password).
- **Expanding error handling** for scenarios such as connection issues, or missing columns.
- **Adjusting output formatting** to suit logging requirements or output to a file for record-keeping.

