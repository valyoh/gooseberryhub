---
title: "Table Comparison Across Databases "
date: "2024-10-29"
---

## PowerShell Script for Table Comparison Across Databases on Different Servers

When working in a multi-database environment, especially across different servers, ensuring data consistency is often critical. Whether it's validating data replication, migration, or identifying discrepancies across environments, comparing tables is a common but challenging task. This blog post will walk through a PowerShell script that compares tables from two different databases on separate servers. It’s customizable, easy to use, and provides insights into row-level and column-level differences.

### Script Overview

The script compares specific columns within tables in two databases, displaying any differences found for easy review. By leveraging PowerShell’s ability to connect to SQL databases, execute queries, and manage data, this script efficiently automates a task that would otherwise be labor-intensive.

### Parameters

The script accepts the following parameters:

- **ConnectionString1**: The connection string for the first database.
- **ConnectionString2**: The connection string for the second database.
- **TableName**: The name of the table to compare.
- **PrimaryKeyColumn**: The column used as the primary key, which uniquely identifies rows in the table.
- **ColumnsToCompare**: An array of column names to be compared between the two databases.

### Detailed Script Walkthrough

#### Step 1: Defining the Column List

The first step of the script is to prepare the list of columns to retrieve from each database. This list includes the primary key column to uniquely identify rows and the columns specified for comparison.

```powershell
$columnList = $PrimaryKeyColumn + ", " + ($ColumnsToCompare -join ", ")
```

#### Step 2: Function to Retrieve Table Data

The `Get-TableData` function takes three parameters:

- **ConnectionString**: The database connection string.
- **Table**: The table name.
- **Columns**: The columns to query.

The function constructs an SQL `SELECT` statement to retrieve data from the specified columns and uses the connection string to connect to the database.

```powershell
function Get-TableData {
    param (
        [string]$ConnectionString,
        [string]$Table,
        [string]$Columns
    )

    # SQL query
    $query = "SELECT $Columns FROM $Table"
```

1. **Setting up the SQL Connection and Command**:
   The function creates an SQL connection and command object using the connection string. Then, it executes the query and stores the results in a `DataTable`.

2. **Error Handling**:
   If an error occurs, it’s logged using `Write-Error`, helping to troubleshoot issues with query execution.

3. **Data Storage**:
   After loading the query result into a `DataTable`, the script converts it into a hashtable keyed by the primary key column. This allows efficient lookup and comparison.

```powershell
    # Convert DataTable to a hashtable keyed by Primary Key Column
    return $dataTable | Group-Object -Property $PrimaryKeyColumn -AsHashTable -AsString
}
```

#### Step 3: Retrieving Data from Both Databases

The main script calls `Get-TableData` twice, once for each database, and stores the results in two hashtables, `tableData1` and `tableData2`.

```powershell
$tableData1 = Get-TableData -ConnectionString $ConnectionString1 -Table $TableName -Columns $columnList
$tableData2 = Get-TableData -ConnectionString $ConnectionString2 -Table $TableName -Columns $columnList
```

#### Step 4: Comparing the Two Data Sets

1. **Combining Keys**:
   The script collects all unique keys (primary keys) from both tables into a set, `allKeys`. This ensures that all rows, even those missing in one of the tables, are accounted for.

```powershell
$allKeys = [System.Collections.Generic.HashSet[string]]::new()
$tableData1.Keys + $tableData2.Keys | ForEach-Object { $allKeys.Add($_) }
```

2. **Iterating Through Keys**:
   For each key, the script:
   
   - Checks if the key exists in both tables.
   - Compares each column specified in `$ColumnsToCompare`.
   - Reports any differences, including the values from both databases.

```powershell
foreach ($key in $allKeys) {
    $row1 = $tableData1[$key]
    $row2 = $tableData2[$key]

    if ($row1 -and $row2) {
        # Row exists in both tables, compare specified columns
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
            Write-Output "Row ID ($PrimaryKeyColumn): $key - No differences found across specified columns."
        }
    }
    ...
}
```

3. **Handling Missing Rows**:
   If a row is missing in one of the tables, the script logs this information, helping to identify discrepancies in data structure or availability.

```powershell
elseif ($row1 -and -not $row2) {
    Write-Output "Row ID ($PrimaryKeyColumn): $key exists in Database1 but not in Database2."
} 
elseif (-not $row1 -and $row2) {
    Write-Output "Row ID ($PrimaryKeyColumn): $key exists in Database2 but not in Database1."
}
```

### Example Usage

To run the script, provide the required parameters:

```powershell
.\Compare-Tables.ps1 -ConnectionString1 "Server=Server1;Database=DB1;User Id=User;Password=Pass;" `
-ConnectionString2 "Server=Server2;Database=DB2;User Id=User;Password=Pass;" `
-TableName "Employee" -PrimaryKeyColumn "EmployeeID" `
-ColumnsToCompare @("FirstName", "LastName", "Email")
```

