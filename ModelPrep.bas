Attribute VB_Name = "ModelPrep"
Public outRow As Integer


'Get the used range from worksheet excluding first column and row
Private Sub HighlightValues(inSheetName As String)
    Dim totalRange As Range
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets(inSheetName)
    ws.Activate
    Set totalRange = ws.usedRange
    totalRange.Offset(1, 2).Resize(totalRange.Rows.Count - 1, totalRange.Columns.Count - 2).Select
End Sub

Private Sub CreateSheets(inSheetName As String)
    Dim ws As Worksheet
    Dim ws2 As Worksheet
    With ThisWorkbook
        Set ws = ThisWorkbook.Worksheets(inSheetName)
        ws.Copy after:=Sheets(.Sheets.Count)
        activeSheet.Name = "tmp"
        Set ws2 = .Sheets.Add(after:=.Sheets(.Sheets.Count))
        ws2.Name = "Output"
    End With
End Sub

Private Sub MakeHeaders()
    'Set starting destination cell
    Dim Destination As Range
    Set Destination = Worksheets("Output").Range("A1")
    'Write column headers to "Output" sheet
    colHeaders = Array("Name", "X", "Y", "Bottom Layer", "Top Layer", "NumTrans", "ScreenRadius", "CasingRadius", "Reach")
    Destination.Resize(1, UBound(colHeaders)) = colHeaders
    'For Each cel In colHeaders
        'Debug.Print cel
    'Next cel
End Sub

Private Sub getCol(inSheetName As String, colNum As Integer)
    Dim totalRange As Range
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets(inSheetName)
    ws.Activate
    Set totalRange = ws.usedRange.Columns(colNum)
    totalRange.Select
End Sub

Private Sub addStartStop(inRange As Range)
    Dim i As Integer
    Dim zeroStart As Integer
    Dim zeroEnd As Integer
    Dim lastValue As Integer
    Dim ws_out As Worksheet
    Dim rowCursor As Integer
     
    Set ws_out = Worksheets("Output")
     
    zeroStart = 0
    zeroEnd = 0
    lastValue = -50
    rowCursor = outRow
    For i = 1 To inRange.Rows.Count
        'If the row is station name, print it
        If IsNumeric(inRange(i).Value) = False Then
            ws_out.Range("A2").Offset(rowCursor, 0).Value = inRange(i).Value
            rowCursor = rowCursor + 1
            Debug.Print inRange(i).Value
        'If the row is a zero
        ElseIf inRange(i).Value = 0 Then
            'And it's not preceded immediately by a zero, set the zeroStart
            If lastValue <> 0 Then
                zeroStart = i - 1
            End If
            'Update the zero end
            zeroEnd = i - 1
            lastValue = 0
        'If you've gone through all the zeros and are now to a non-zero
        ElseIf inRange(i).Value <> 0 And lastValue = 0 Then
            'Print the coalesced zero periods
            ws_out.Range("A2").Offset(rowCursor, 0) = zeroStart
            ws_out.Range("A2").Offset(rowCursor, 1) = zeroEnd
            ws_out.Range("A2").Offset(rowCursor, 2) = lastValue
            Debug.Print zeroStart, zeroEnd, lastValue
            'Print the current non-zero period
            rowCursor = rowCursor + 1
            ws_out.Range("A2").Offset(rowCursor, 0) = i - 1
            ws_out.Range("A2").Offset(rowCursor, 1) = i - 1
            ws_out.Range("A2").Offset(rowCursor, 2) = inRange(i).Value
            Debug.Print i - 1, i - 1, inRange(i).Value
            lastValue = -50
            rowCursor = rowCursor + 1
        Else
            ws_out.Range("A2").Offset(rowCursor, 0) = i - 1
            ws_out.Range("A2").Offset(rowCursor, 1) = i - 1
            ws_out.Range("A2").Offset(rowCursor, 2) = inRange(i).Value
            Debug.Print i - 1, i - 1, inRange(i).Value
            rowCursor = rowCursor + 1
        End If
    Next i
    If lastValue = 0 Then
        ws_out.Range("A2").Offset(rowCursor, 0) = zeroStart
        ws_out.Range("A2").Offset(rowCursor, 1) = zeroEnd
        ws_out.Range("A2").Offset(rowCursor, 2) = lastValue
    End If
    'rowLen = ws_out.Cells(Rows.Count, 1).End(xlUp).
    outRow = ws_out.Range("A2", ws_out.Cells(Rows.Count, 1).End(xlUp)).Rows.Count
End Sub

Private Sub MakeStations()
    'Set starting destination cell
    Dim Destination As Range
    Set Destination = Worksheets("Output").Range("A3")
    'Write stations to "Output" sheet
    
End Sub

Sub LoopSelection()
    
    Dim inSheetName As String
    Dim threshold As Double
    Dim cel As Range
    Dim selectedRange As Range
    Dim SPRange As Range
    Dim colCount As Integer
    Dim i As Integer
    
    inSheetName = Worksheets("Dashboard").Range("F8").Text
    threshold = Worksheets("Dashboard").Range("F14").Text
    'Create intermediate sheet and output sheet
    Call CreateSheets(inSheetName)
    'Add required headers to output sheet
    Call MakeHeaders
    Call HighlightValues("tmp")
    
    Set selectedRange = Application.Selection
    'If cell values less than threshold, zero them
    For Each cel In selectedRange.Cells
        If cel.Value < threshold Then
            cel.Value = 0
        End If
    Next cel
    
    'Get number of columns
    colCount = selectedRange.Columns.Count
    
    'Iterate through columns until number hit, printing address
    outRow = 0
    For i = 3 To colCount + 2
        Call getCol("tmp", i)
        Set SPRange = Application.Selection
        
        Call addStartStop(SPRange)
    Next i

End Sub




