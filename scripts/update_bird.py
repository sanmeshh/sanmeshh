
import os
import json
import urllib.request
from datetime import datetime, timedelta, timezone
from html import escape

USERNAME = "sanmeshh"
TOKEN = os.environ["GITHUB_TOKEN"]

# Get GitHub contributions from the last 365 days
end = datetime.now(timezone.utc)
start = end - timedelta(days=365)

query = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        totalContributions
      }
    }
  }
}
"""

payload = {
    "query": query,
    "variables": {
        "login": USERNAME,
        "from": start.isoformat(),
        "to": end.isoformat()
    }
}

request = urllib.request.Request(
    "https://api.github.com/graphql",
    data=json.dumps(payload).encode(),
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
)

with urllib.request.urlopen(request) as response:
    data = json.loads(response.read())

if "errors" in data:
    raise RuntimeError(data["errors"])

contributions = data["data"]["user"]["contributionsCollection"][
    "contributionCalendar"
]["totalContributions"]

if contributions <= 5:
    stage = "egg"
elif contributions <= 20:
    stage = "hatch"
elif contributions <= 50:
    stage = "growing"
else:
    stage = "grown"

# Bird artwork
if stage == "egg":
    bird = """
    <ellipse cx="400" cy="145" rx="29" ry="39"
             fill="#FFF4D2" stroke="#D9B77A" stroke-width="3"/>
    <path d="M380 142 Q400 130 420 142"
          fill="none" stroke="#D9B77A" stroke-width="3"/>
    <text x="400" y="155" text-anchor="middle"
          font-size="17">✨</text>
    """

elif stage == "hatch":
    bird = """
    <path d="M374 142 L388 157 L398 142"
          fill="#F5D66D" stroke="#C99A37" stroke-width="3"/>
    <ellipse cx="400" cy="127" rx="27" ry="29" fill="#FFD84D"/>
    <circle cx="410" cy="121" r="3" fill="#49351D"/>
    <path d="M425 130 L441 136 L425 140 Z" fill="#F28C28"/>
    <path d="M384 105 L379 88 L394 99"
          fill="#FFD84D" stroke="#D6A72D" stroke-width="2"/>
    """

elif stage == "growing":
    bird = """
    <ellipse cx="400" cy="132" rx="40" ry="31" fill="#FFD84D"/>
    <circle cx="427" cy="103" r="24" fill="#FFE36B"/>
    <path d="M391 127 Q361 119 371 153 Q389 151 399 139"
          fill="#F4B82E"/>
    <circle cx="435" cy="99" r="3.5" fill="#49351D"/>
    <path d="M449 108 L467 114 L449 120 Z" fill="#F28C28"/>
    <path d="M414 81 L407 65 L424 77"
          fill="#FFD84D" stroke="#D6A72D" stroke-width="2"/>
    <path d="M388 159 L383 174 M412 159 L417 174"
          stroke="#D58C27" stroke-width="4"/>
    """

else:
    bird = """
    <ellipse cx="394" cy="132" rx="45" ry="32" fill="#FFD84D"/>
    <circle cx="428" cy="99" r="27" fill="#FFE36B"/>
    <path d="M380 123 Q347 103 350 151 Q378 155 399 139"
          fill="#F2B82E" stroke="#D6A72D" stroke-width="2"/>
    <path d="M389 127 Q410 105 418 137 Q406 150 389 127"
          fill="#F6C53B"/>
    <circle cx="438" cy="95" r="3.5" fill="#49351D"/>
    <path d="M453 105 L473 112 L453 119 Z" fill="#F28C28"/>
    <path d="M415 77 L406 59 L424 73 L438 57 L434 82"
          fill="#FFD84D" stroke="#D6A72D" stroke-width="2"/>
    <path d="M380 160 L374 177 M405 160 L411 177"
          stroke="#D58C27" stroke-width="4"/>
    <path d="M472 93 Q486 83 490 94"
          fill="none" stroke="#FFF2B0" stroke-width="3"/>
    """

# Extra forest decoration after 100 contributions
extra_forest = """
<circle cx="80" cy="70" r="23" fill="#478C51"/>
<circle cx="105" cy="53" r="29" fill="#559D5C"/>
<circle cx="710" cy="66" r="29" fill="#478C51"/>
<circle cx="745" cy="79" r="22" fill="#559D5C"/>
""" if contributions >= 100 else ""

svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
width="800" height="240" viewBox="0 0 800 240">

<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#173F39"/>
    <stop offset="100%" stop-color="#285C43"/>
  </linearGradient>
</defs>

<rect width="800" height="240" rx="18" fill="url(#sky)"/>

{extra_forest}

<!-- Forest trees -->
<path d="M45 240 L65 100 L85 240 Z" fill="#17452F"/>
<path d="M690 240 L720 105 L750 240 Z" fill="#17452F"/>
<path d="M130 240 L145 160 L160 240 Z" fill="#205337"/>
<path d="M630 240 L650 155 L670 240 Z" fill="#205337"/>

<!-- Leaves -->
<g fill="#72B76C">
  <ellipse cx="110" cy="180" rx="25" ry="11" transform="rotate(-25 110 180)"/>
  <ellipse cx="690" cy="178" rx="24" ry="11" transform="rotate(25 690 178)"/>
  <ellipse cx="170" cy="200" rx="21" ry="9" transform="rotate(-20 170 200)"/>
  <ellipse cx="625" cy="198" rx="22" ry="10" transform="rotate(20 625 198)"/>
</g>

<!-- Stars -->
<g fill="#F6E8A7">
  <circle cx="180" cy="48" r="2"/>
  <circle cx="590" cy="39" r="2"/>
  <circle cx="640" cy="90" r="2"/>
  <circle cx="240" cy="85" r="2"/>
</g>

<!-- Branch -->
<path d="M285 183 Q400 160 520 185"
      fill="none" stroke="#9B7043" stroke-width="10"
      stroke-linecap="round"/>

<!-- Nest -->
<path d="M347 176 Q400 218 453 176"
      fill="none" stroke="#B9824C" stroke-width="8"
      stroke-linecap="round"/>
<path d="M354 184 Q400 212 446 184"
      fill="none" stroke="#D39A5C" stroke-width="4"/>

<!-- Bird -->
{bird}

<!-- Decorative flowers -->
<g fill="#F4D6E6">
  <circle cx="300" cy="187" r="5"/>
  <circle cx="510" cy="186" r="5"/>
</g>

<text x="400" y="28" text-anchor="middle"
      fill="#E8F5D7" font-size="17"
      font-family="Verdana" font-weight="bold">
  SANMESHH'S LITTLE FOREST
</text>

<text x="400" y="225" text-anchor="middle"
      fill="#E8F5D7" font-size="12"
      font-family="Verdana">
  {escape(stage.upper())} BIRD • {contributions} CONTRIBUTIONS THIS YEAR
</text>

</svg>
"""

os.makedirs("assets", exist_ok=True)

with open("assets/bird.svg", "w", encoding="utf-8") as file:
    file.write(svg)

print(f"Bird updated! Stage: {stage}, Contributions: {contributions}")
