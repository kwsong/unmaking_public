Scripts developed and tested in Rhino 6 for Mac. Create a custom Command by going to Rhino -> Preferences -> Aliases.
<br><br>Example:
<br>Alias = UnMakingBulge
<br>Command macro = <code>! _-RunPythonScript  "~/UnmakingBulge.py"</code>

<br><br>Both examples require that you create (or import) a "normal" printable model mesh and create a second mesh surface that defines the splitting or bulging plane. The bulge macro will also prompt you to enter a real number (> 1.0) that defines the height of the bulging chamber.
  
