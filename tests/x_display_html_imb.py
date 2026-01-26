html_content = """
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<html>
  <head><title></title></head>
  <body>
    <p style="font-family:USPSIMBStandard;font-size:16pt">
      AADTFFDFTDADTAADAATFDTDDAAADDTDTTDAFADADDDTFFFDDTTTADFAAADFTDAADA
    </p>
  </body>
</html>
"""

with open("tests/data/display_imb.html", "w", encoding="utf-8") as f:
    f.write(html_content)
