# This function will set the version of python executed

function Pick-Python
{
    $version = Read-Host -Prompt 'Which version of Python would you like, [2] or [3]?'
    if ($version -eq "3")
    {
      $env:path += ";C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3"
    }
    else
    {
      $env:path += ";C:\Python27\ArcGIS10.3"
    }
}

Pick-Python
