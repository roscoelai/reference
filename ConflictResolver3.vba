' Quickstart (from source code):
' - Open Excel
' - Press Alt + F11 to open VBA Editor
' - Select Insert > Module
' - Paste source code into new module
' - Select/Open target Workbook
' - Press Alt + F8 to list macros
' - Select the appropriate macro and press Run

Sub ConflictResolver3()
' Conflict resolution macro
'
' Preconditions:
' - The 2 spreadsheets to be compared are the 1st and 2nd in a Workbook
' - The 1st will be referred to as "Entry 1", the 2nd as "Entry 2"
' - Entry 1 and 2 must have the same number of rows and columns
' - Entry 1 and 2 must have the same arrangement of rows and columns
' - Entry 1 and 2 preferably have the same row and column names
'
' Assumption:
' - User is comparing 2 very similar spreadsheets with few differences
'
' Approach:
' - Entry 1 and 2 are copied, and Entry 1 is pasted into a new Sheet
' - Entry 1 and 2 are scanned for mismatches
' - Corresponding cells in the new sheet will be overwritten with "#N/A"
' - These cells will be given unconditional green background and font
' - These cells will be given conditional red background and font
' - So, when changes are made, red would change to green
' - Entry 1 and 2 are not modified; Comparison Sheet can be regenerated anytime
'
    Dim entry1()
    Dim entry2()
    Dim i As Long
    Dim j As Long
    Dim nrows As Long
    Dim ncols As Long
    
    ' Read 1st and 2nd entry sheets into memory
    entry1 = Sheets(1).UsedRange.Value
    entry2 = Sheets(2).UsedRange.Value
    
    nrows = UBound(entry1, 1)
    ncols = UBound(entry1, 2)
    
    ' Add a new sheet in the 3rd position
    Sheets.Add , Sheets(2)
    
    With Sheets(3)
        ' Paste the values of the 1st entry into the new sheet
        .Cells(1, 1).Resize(nrows, ncols).Value = entry1
        
        ' Compare 1st and 2nd entries to find cells with mismatches
        For i = 1 To nrows
            For j = 1 To ncols
                ' If there are mismatches, overwrite the cell value with "#N/A"
                ' Add a comment with the 1st and 2nd entry values
                ' Give the cell an unconditional green color
                If entry1(i, j) <> entry2(i, j) Then
                    With .Cells(i, j)
                        .Value = "#N/A"
                        .AddComment "Entry 1: '" & entry1(i, j) & "'" & Chr(10) & _
                                    "Entry 2: '" & entry2(i, j) & "'"
                        .Font.Color = RGB(0, 97, 0)  ' Dark green
                        .Interior.Color = RGB(198, 239, 206)  ' Light green
                    End With
                End If
            Next j
        Next i
        
        ' Conditional formatting to highlight all cells with errors
        With .UsedRange.FormatConditions.Add(xlErrorsCondition)
            .Font.Color = RGB(156, 0, 6)  ' Dark red
            .Interior.Color = RGB(255, 199, 206)  ' Light red
        End With
    End With
End Sub
