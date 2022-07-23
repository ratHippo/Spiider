games = {}
games["srcdir"] = "src/games/"
games["indexdir"] = "games/"
games["indexlinkdir"] = ""
games["builddir"] = "games/"
games["articletemplate"] = """
<!DOCTYPE html>
<html lang="en" dir="ltr">
    <head>
        <meta charset="utf-8">
        <title>{title}</title>
        <link rel="stylesheet" href="../../index.css">
    </head>
    <body class="font1">
        <div class="main-content">
            <div class="grid">
                <h1>{title}</h1>
                <card>
                    {article}
                </card>
                <card>
                    <img src = "play/preview.png"></img>
                </card>
                <card>
                    <a href = "play/">click here to play</a>
                </card>
                <h3><a href="../">Back</a></h3>
                </div>
            </div>
    </body>
 </html>
"""
games["indextemplate"] = """
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="../index.css">
    <title> Games </title>
  </head>
  <body class = "font1">
    <div class = "main-content">
      <div class="grid">
        <h1>Games</h1>
        <card>
            <p>
                These are the games I've made, and I've put them here for you to play. Try them out, but they might be a bit laggy.
            </p>
        </card>
        {previews}
        <h3><a href = "/">back</a></h3>
    </div>
    </div>
  </body>
</html>
"""
games["previewtemplate"] = """
<a class ="nocolor" href = {indexlinkdir}{path}>
    <card>
        <h3>{title}</h3>
        <p>{description}</p>
        <h5>{date}</h5>
      </card>
</a>"""
games["dorss"] = False