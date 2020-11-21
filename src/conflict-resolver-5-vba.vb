' conflict-resolver-5-vba.vb

' Quickstart (from source code):
' - Open Excel
' - Press Alt + F11 to open VBA Editor
' - Select Insert > Module
' - Paste source code into new module
' - Select/Open target Workbook
' - Press Alt + F8 to list macros
' - Select the appropriate macro and press Run

Sub ConflictResolver5()
' Conflict resolution macro (version 5)
'
' This macro is designed to facilitate the entry 1 vs. entry 2 conflict 
' resolution workflow. Entries 1 and 2 have to be prepared beforehand 
' (requirements below). The macro will produce a view of the comparison 
' result.
'
' Features:
' - Conflicts will be made obvious and editable
' - Cell comments will provide details of mismatch
' - Non-conflicts will be read-only
'
' Preconditions:
' - Entries 1 and 2 are sheets 1 and 2
'   - Same number of rows and columns
'   - Same order of rows and columns
'   - Same row and column names
'
' Limitations:
' - Small datasets
' - Not too many conflicts
'
    Dim entry1()
    Dim entry2()
    Dim i As Long
    Dim j As Long
    Dim nrows As Long
    Dim ncols As Long
    Dim refrow As Long
    Dim line1 As String
    Dim line2 As String
    
    ' Read 1st and 2nd entry sheets into memory
    entry1 = Sheets(1).UsedRange.Value
    entry2 = Sheets(2).UsedRange.Value
    
    ' Basic checks -----------------------------------------------------------
    
    If Not same_shape(entry1, entry2) Then
        Debug.Print "Shapes of entries do not match."
        Debug.Print "Entry 1 shape: " & _
                    UBound(entry1) & ", " & UBound(entry1, 2)
        Debug.Print "Entry 2 shape: " & _
                    UBound(entry2) & ", " & UBound(entry2, 2)
        Debug.Assert same_shape(entry1, entry2)
    End If
    
    If Not same_columns(entry1, entry2) Then
        Debug.Print "Columns of entries do not match. Please check."
        Debug.Assert same_columns(entry1, entry2)
    End If
    
    If Not same_index(entry1, entry2) Then
        Debug.Print "Indexes of entries do not match. Please check."
        Debug.Assert same_index(entry1, entry2)
    End If
    
    ' We might need more checks in the future... -----------------------------
    
    nrows = UBound(entry1, 1)
    ncols = UBound(entry1, 2)
    
    ' Standard procedure for speed up; Re-set to True at the end
    Application.ScreenUpdating = False
    
    ' Add 2 new sheets that will take the 3rd and 4th positions
    Sheets.Add , Sheets(2)
    Sheets.Add , Sheets(2)
    
    With Sheets(3)
        ' Paste the values of the 1st entry into the new sheet
        .Cells(1, 1).Resize(nrows, ncols).Value = entry1
        
        With .UsedRange
            .Locked = True
'            .ClearComments
'            .Validation.Delete
            
            ' Conditional formatting to highlight all cells with errors
            With .FormatConditions.Add(xlErrorsCondition)
                .Font.Color = RGB(156, 0, 6)  ' Dark red
                .Interior.Color = RGB(255, 199, 206)  ' Light red
            End With
        End With
        
        ' Compare 1st and 2nd entries to find cells with mismatches
        For i = 1 To nrows
            For j = 1 To ncols
                ' If there are mismatches...
                If entry1(i, j) <> entry2(i, j) Then
                    line1 = "1: '" & entry1(i, j) & "'"
                    line2 = "2: '" & entry2(i, j) & "'"
                    
                    ' Record both entries in 4th sheet
                    refrow = i + i - 1
                    Sheets(4).Cells(refrow, j) = entry1(i, j)
                    Sheets(4).Cells(refrow + 1, j) = entry2(i, j)
                    
                    With .Cells(i, j)
                        .Value = "#N/A"
                        .Locked = False
                        .Font.Color = RGB(0, 97, 0)  ' Dark green
                        .Interior.Color = RGB(198, 239, 206)  ' Light green
                        
                        ' Add a comment with the 1st and 2nd entry values
                        .AddComment line1 & Chr(10) & line2
                        .comment.Shape.TextFrame.AutoSize = True
                        
                        With .Validation
                            ' Create drop-down list; Reference from 4th sheet
                            .Add Type:=xlValidateList, _
                                 Formula1:="=" & Sheets(4).Name & "!" & _
                                           Cells(refrow, j).Resize(2).Address
                            .InCellDropdown = True
                            
                            ' InputTitle has a 32 character limit
                            .InputTitle = "--------------------------------"
                            
                            ' InputMessage has a 255 character limit
                            .InputMessage = Left(line1, 126) & Chr(10) & _
                                            Left(line2, 126)
                            .ShowInput = True
                            
                            ' Allow other values (manual entry)
                            .ShowError = False
                        End With
                    End With
                End If
            Next j
        Next i
    End With
    
    ' Formatting to prettify the resultant sheet
    Rows(1).Font.Bold = True
    Columns("A:C").AutoFit
    Cells(2, 2).Select
    ActiveWindow.FreezePanes = True
    ActiveWindow.Zoom = 100
    
    Sheets(3).Name = "ConflictResolve"
    Sheets(4).Name = "DropDownOptions"
    Sheets(1).Protect
    Sheets(2).Protect
    Sheets(3).Protect
    Sheets(4).Protect
    Sheets(4).Visible = xlSheetHidden
'    Sheets(4).Visible = xlSheetVeryHidden
    
    Application.ScreenUpdating = True
End Sub

Function same_shape(entry1, entry2) As Boolean
    same_shape = (UBound(entry1, 1) = UBound(entry2, 1)) And _
                  (UBound(entry1, 2) = UBound(entry2, 2))
End Function

Function same_index(entry1, entry2) As Boolean
    Dim i As Long
    
    For i = 2 To UBound(entry1)
        If entry1(i, 1) <> entry2(i, 1) Then
            same_index = False
            Exit Function
        End If
    Next i
    
    same_index = True
End Function

Function same_columns(entry1, entry2) As Boolean
    Dim j As Long
    
    For j = 1 To UBound(entry1, 2)
        If entry1(1, j) <> entry2(1, j) Then
            same_columns = False
            Exit Function
        End If
    Next j
    
    same_columns = True
End Function
