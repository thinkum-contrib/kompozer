<script type="text/javascript">
var isDisplayed = true;

function togglePanel() {
  isDisplayed = !isDisplayed;
  var displayValue = isDisplayed ? "display: block" : "display: none";
  var bodyValue = isDisplayed ? "margin-left: 175px" : "margin-left:5px";

  document.getElementById("contentsBox").setAttribute("style", displayValue);
  document.getElementsByTagName("body").item(0).setAttribute("style", bodyValue);
}
</script>

<table width="100%" id="navTable">
<tr>
<td valign="bottom" width="20"><small><a href="#" onclick="togglePanel();" style="margin-top:10px;">Megjelen�t�s/Elrejt�s</a></small></td>
<td width="72"><img src="chrome://editor/skin/icons/throbber.png" width="32" height="32" alt="&brandShortName;" align="center"/></td><td align="left"><span id="topText">S�g�k�zpont</span></td>
</tr>
</table>
