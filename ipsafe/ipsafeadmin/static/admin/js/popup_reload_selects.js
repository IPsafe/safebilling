var $chosens = {};

 /**
 * Override default showAddAnotherPopup to work with chosen js
 */
function showAddAnotherPopup(triggeringLink) {
    var name = triggeringLink.id.replace(/^add_/, '');
    name = id_to_windowname(name);
    href = triggeringLink.href
    if (href.indexOf('?') == -1) {
        href += '?_popup=1';
    } else {
        href  += '&_popup=1';
    }
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
 
    /**
     * Also adding an interval to listen for when the window is closed
     * then we can fire an update on the chosen objects
     */
    var unloadInterval = setInterval(function() {
        if (!win || win.closed) {
            clearInterval(unloadInterval);
            $("select").select2({ width: 'resolve'});
        }
    }, 250);
 
    return false;
}
 
$(document).ready(function() {
    $selects = $("select");
    var $add_another = $('a.add-another');
    if ($selects.length < 1) return false
    $selects.select2({ width: 'resolve'});
});
