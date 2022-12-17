// Old City Transforming Issue
// Mixed Integer Programming

Max
  obj: 0.5 x1 + 0.95 x2 + 1.35 x3 + 1.7 x4
St
  c1: 720 x1 + 1120 x2 + 1600 x3 + 2000 x4 - 850 x5 <= 0
  c2: x5 <= 300
  c3: -0.8 x1 + 0.2 x2 + 0.2 x3 + 0.2 x4 <= 0
  c4: 0.1 x1 - 0.9 x2 + 0.1 x3 + 0.1 x4 <= 0
  c5: 0.25 x1 + 0.25 x2 - 0.75 x3 - 0.75 x4 <= 0
  c6: 25 x1 + 35 x2 + 65 x3 + 80 x4 + x5 <= 7500
Bounds
  x1 >= 0
  x2 >= 0
  x3 >= 0
  x4 >= 0
  x5 >= 0
Integers
  x1 x2 x3 x4 x5 
End

// the LP solution is correct.
// Why is the MIP solution wrong?
//   After adding Integer: x1 x2 x3 x4 x5
