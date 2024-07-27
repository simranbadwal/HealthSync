/**
 * -------------------------------------------------------
 * Updates the class name of all child elements of a specified parent element.
 * The class name is set to the value provided in elementCSS.
 * Use: updateSiblings('parentID', 'newCSSClass')
 * -------------------------------------------------------
 * Parameters:
 *     ParentID  - The ID of the parent element whose child elements' class names will be updated (String).
 *     elementCSS - The new CSS class name to assign to each child element (String).
 * -------------------------------------------------------
 */
function updateSiblings(ParentID, elementCSS) {
  let siblings = document.getElementById(ParentID).childNodes;
  console.log(siblings);
  siblings.forEach((item) => {
    item.className = elementCSS;
  });
}



/**
 * -------------------------------------------------------
 * Sets a cookie with a specified name, value, and expiration date.
 * Use: setCookie('cookieName', 'cookieValue', 7)
 * -------------------------------------------------------
 * Parameters:
 *     cname  - The name of the cookie to set (String).
 *     cvalue - The value to assign to the cookie (String).
 *     exdays - The number of days until the cookie expires (Number).
 * -------------------------------------------------------
 * Returns:
 *     None
 * -------------------------------------------------------
 */
function setCookie(cname, cvalue, exdays) {
  const d = new Date();
  d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1000);
  let expires = "expires=" + d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}


/**
 * -------------------------------------------------------
 * Retrieves the value of a specified cookie.
 * Use: let cookieValue = getCookie('cookieName')
 * -------------------------------------------------------
 * Parameters:
 *     cname - The name of the cookie whose value is to be retrieved (String).
 * -------------------------------------------------------
 * Returns:
 *     The value of the specified cookie if it exists (String).
 *     An empty string if the cookie does not exist.
 * -------------------------------------------------------
 */
function getCookie(cname) {
  let name = cname + "=";
  let ca = document.cookie.split(";");
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}


/**
 * -------------------------------------------------------
 * Sets a cookie to indicate that the user has consented to cookies.
 * Calls removeCookieMessageBox() to remove the cookie consent message box.
 * Use: acceptCookies()
 * -------------------------------------------------------
 * Parameters:
 *     None
 * -------------------------------------------------------
 * Returns:
 *     None
 * -------------------------------------------------------
 */
function acceptCookies() {
  setCookie("userConsent", "userConsent", 10);
  removeCookieMessageBox();
}



/**
 * -------------------------------------------------------
 * Removes the cookie consent message box from the DOM.
 * Use: removeCookieMessageBox()
 * -------------------------------------------------------
 * Parameters:
 *     None
 * -------------------------------------------------------
 * Returns:
 *     None
 * -------------------------------------------------------
 */
function removeCookieMessageBox() {
  document.getElementById("cookieMessageBox").remove();
}

function displayLoader(){
  document.getElementById('menu-r').innerHTML='<div class="w-full text-center"><div class="loader mx-auto"></div></div>'
}




